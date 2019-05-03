import os
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
#broken pipe issue
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)

# set channels as a global dictionary
channels = [ 'Default Channel' ,'Channel2' ]


@app.route("/")
def index(username = "non"):
    if username == "non":
        return render_template("login.html")
    else:
        return render_template("index.html", username=username, channels=channels)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Make sure you always have to put a username
    if request.method == "GET":
        return index()
    #  Request the username
    else:
        session['username'] = request.form.get("username")
        #Add login the user will join default channel
        currentchannel = channels[0]
        return render_template("index.html", username=session['username'], channels=channels, currentchannel=currentchannel)

@app.route("/changechannel/<string:channelname>", methods=["GET", "POST"])
def changeChannel(channelname):
    currentchannel = channelname
    return render_template("index.html", username=session['username'], channels=channels, currentchannel=currentchannel)

@socketio.on("submit message")
def newMessage(data):
    message = data["message"]
    usernameSend = session['username']
    emit("announce message", {"message": message, "usernameSend": usernameSend}, broadcast=True)
