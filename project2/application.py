import os

from flask import Flask, render_template
from flask_socketio import SocketIO, emit
#broken pipe issue
#from signal import signal, SIGPIPE, SIG_DFL
#signal(SIGPIPE,SIG_DFL)

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)


@app.route("/")
def index():
    return render_template("index.html")

@socketio.on("submit message")
def newMessage(data):
    message = data["message"]
    emit("announce message", {"message": message}, broadcast=True)
