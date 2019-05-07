import os
import datetime
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import json
#broken pipe issue
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)

#Biggest learning=> Pingpong of variables across html/js/application is a pain
#multi level dictionary for chat history with possibility to get extended if new channel is added
#No consistency in logic. Is it in Javascript(add channel to dictionary) or Application (Change channel)
#Appending child <a> inside <li> with javascript

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config["SESSION_TYPE"] = "filesystem"
socketio = SocketIO(app)

# set channels as a global dictionary
channels = [ 'Default Channel' ,'Existing channel' ]
currentchannel = channels[0]

messagehistory2 = {"Default Channel": {
                                  "name": "Default Channel",
                                  "messages": []
                                },
                   "Existing channel": {
                                    "name": "Existing channel",
                                    "messages": []
                                }
                   }

@app.route("/")
def index(username = "non"):
    if username == "non":
        return render_template("login.html")
    else:
        return render_template("index.html", username=username, channels=channels)

@app.route("/login", methods=["GET", "POST"])
def login():
    print("check if print works")
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
    print(channelname)
    # make sure thedata for the new channel is added
    if channelname not in channels:
        addChannel(channelname)
    global currentchannel
    currentchannel = channelname
    #load chat history of this channel
    messagehistory=messagehistory2[currentchannel]["messages"]
    return render_template("index.html", username=session['username'], channels=channels, currentchannel=currentchannel, messagehistory=messagehistory)

# Adding data for new channel
@app.route("/addchannel/<string:channelname>", methods=["GET", "POST"])
def addChannel(channelname):
    print(channelname)
    channels.append(channelname)
    newdata={channelname: {
                                  "name": channelname,
                                  "messages": []
                                }}
    messagehistory2.update(newdata)
    print(messagehistory2)
    # messagehistory2["newchannel"] = {}
    return render_template("index.html", username=session['username'], channels=channels, currentchannel=currentchannel)

@socketio.on("submit message")
def newMessage(data):
    message = data["message"]
    usernameSend = session['username']
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    print(timestamp)
    usernameSend = usernameSend + " "+ str(timestamp)
    #make sure that the saved message history is never more than 100 messages
    if len(messagehistory2[currentchannel]["messages"]) >= 10:
        del messagehistory2[currentchannel]["messages"][0]
    else:
        messagehistory2[currentchannel]["messages"].append(usernameSend + ": " + message)
        emit("announce message", {"message": message, "usernameSend": usernameSend}, broadcast=True)