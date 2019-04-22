import os
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
#broken pipe issue
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

@app.route("/")
def index(username = "non"):
    if username == "non":
        return render_template("login.html")
    else:
        return render_template("index.html", username=username)

@app.route("/login", methods=["GET", "POST"])
def login():
    # Make sure you always have to put a username
    if request.method == "GET":
        return index()
    #  Request the username
    else:
        username = request.form.get("username")
        return index(username=username)

@socketio.on("submit message")
def newMessage(data):
    message = data["message"]
    usernameSend = data["usernameSend"]
    emit("announce message", {"message": message, "usernameSend": usernameSend}, broadcast=True)
