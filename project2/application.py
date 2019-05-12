import os
import datetime
from flask import Flask, render_template, session, request
from flask_socketio import SocketIO, emit
import re
import string

#Biggest learning=> Pingpong of variables across html/js/application is a pain
#multi level dictionary for chat history with possibility to get extended if new channel is added
#No consistency in logic. Is it in Javascript(add channel to dictionary) or Application (Change channel)
#Appending child <a> inside <li> with javascript
# Missed a requirement where You should not see the message on screen if it was send from other channel


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
    channels.append(channelname)
    newdata = {channelname: {
                                  "name": channelname,
                                  "messages": []
                                }}
    messagehistory2.update(newdata)
    return render_template("index.html", username=session['username'], channels=channels, currentchannel=currentchannel)

@socketio.on("submit message")
def newMessage(data):
    message = data["message"]
    message = badwordsfilter(message)
    channel = data["channel"]
    usernameSend = session['username']
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    usernameSend = usernameSend + " "+ str(timestamp)
    #make sure that the saved message history is never more than 100 messages
    if len(messagehistory2[currentchannel]["messages"]) >= 100:
        del messagehistory2[currentchannel]["messages"][0]
    messagehistory2[currentchannel]["messages"].append(usernameSend + ": " + message)
    emit("announce message", {"message": message, "channel": channel,"usernameSend": usernameSend}, broadcast=True)

def badwordsfilter(message):
    profanity = [
        '2g1c',
        '2 girls 1 cup',
        'acrotomophilia',
        'anal',
        'anilingus',
        'anus',
        'arsehole',
        'ass',
        'asshole',
        'assmunch',
        'auto erotic',
        'autoerotic',
        'babeland',
        'baby batter',
        'ball gag',
        'ball gravy',
        'ball kicking',
        'ball licking',
        'ball sack',
        'ball sucking',
        'bangbros',
        'bareback',
        'barely legal',
        'barenaked',
        'bastardo',
        'bastinado',
        'bbw',
        'bdsm',
        'beaver cleaver',
        'beaver lips',
        'bestiality',
        'bi curious',
        'big black',
        'big breasts',
        'big knockers',
        'big tits',
        'bimbos',
        'birdlock',
        'bitch',
        'black cock',
        'blonde action',
        'blonde on blonde action',
        'blow j',
        'blow your l',
        'blue waffle',
        'blumpkin',
        'bollocks',
        'bondage',
        'boner',
        'boob',
        'boobs',
        'booty call',
        'brown showers',
        'brunette action',
        'bukkake',
        'bulldyke',
        'bullet vibe',
        'bung hole',
        'bunghole',
        'busty',
        'butt',
        'buttcheeks',
        'butthole',
        'camel toe',
        'camgirl',
        'camslut',
        'camwhore',
        'carpet muncher',
        'carpetmuncher',
        'chocolate rosebuds',
        'circlejerk',
        'cleveland steamer',
        'clit',
        'clitoris',
        'clover clamps',
        'clusterfuck',
        'cock',
        'cocks',
        'coprolagnia',
        'coprophilia',
        'cornhole',
        'cum',
        'cumming',
        'cunnilingus',
        'cunt',
        'darkie',
        'date rape',
        'daterape',
        'deep throat',
        'deepthroat',
        'dick',
        'dildo',
        'dirty pillows',
        'dirty sanchez',
        'dog style',
        'doggie style',
        'doggiestyle',
        'doggy style',
        'doggystyle',
        'dolcett',
        'domination',
        'dominatrix',
        'dommes',
        'donkey punch',
        'double dong',
        'double penetration',
        'dp action',
        'eat my ass',
        'ecchi',
        'ejaculation',
        'erotic',
        'erotism',
        'escort',
        'ethical slut',
        'eunuch',
        'faggot',
        'fecal',
        'felch',
        'fellatio',
        'feltch',
        'female squirting',
        'femdom',
        'figging',
        'fingering',
        'fisting',
        'foot fetish',
        'footjob',
        'frotting',
        'fuck',
        'fucking',
        'fuck buttons',
        'fudge packer',
        'fudgepacker',
        'futanari',
        'g-spot',
        'gang bang',
        'gay sex',
        'genitals',
        'giant cock',
        'girl on',
        'girl on top',
        'girls gone wild',
        'goatcx',
        'goatse',
        'gokkun',
        'golden shower',
        'goo girl',
        'goodpoop',
        'goregasm',
        'grope',
        'group sex',
        'guro',
        'hand job',
        'handjob',
        'hard core',
        'hardcore',
        'hentai',
        'homoerotic',
        'honkey',
        'hooker',
        'hot chick',
        'how to kill',
        'how to murder',
        'huge fat',
        'humping',
        'incest',
        'intercourse',
        'jack off',
        'jail bait',
        'jailbait',
        'jerk off',
        'jigaboo',
        'jiggaboo',
        'jiggerboo',
        'jizz',
        'juggs',
        'kike',
        'kinbaku',
        'kinkster',
        'kinky',
        'knobbing',
        'leather restraint',
        'leather straight jacket',
        'lemon party',
        'lolita',
        'lovemaking',
        'make me come',
        'male squirting',
        'masturbate',
        'menage a trois',
        'milf',
        'missionary position',
        'motherfucker',
        'mound of venus',
        'mr hands',
        'muff diver',
        'muffdiving',
        'nambla',
        'nawashi',
        'negro',
        'neonazi',
        'nig nog',
        'nigga',
        'nigger',
        'nimphomania',
        'nipple',
        'nipples',
        'nsfw images',
        'nude',
        'nudity',
        'nympho',
        'nymphomania',
        'octopussy',
        'omorashi',
        'one cup two girls',
        'one guy one jar',
        'orgasm',
        'orgy',
        'paedophile',
        'panties',
        'panty',
        'pedobear',
        'pedophile',
        'pegging',
        'penis',
        'phone sex',
        'piece of shit',
        'piss pig',
        'pissing',
        'pisspig',
        'playboy',
        'pleasure chest',
        'pole smoker',
        'ponyplay',
        'poof',
        'poop chute',
        'poopchute',
        'porn',
        'porno',
        'pornography',
        'prince albert piercing',
        'pthc',
        'pubes',
        'pussy',
        'queaf',
        'raghead',
        'raging boner',
        'rape',
        'raping',
        'rapist',
        'rectum',
        'reverse cowgirl',
        'rimjob',
        'rimming',
        'rosy palm',
        'rosy palm and her 5 sisters',
        'rusty trombone',
        's&m',
        'sadism',
        'scat',
        'schlong',
        'scissoring',
        'semen',
        'sex',
        'sexo',
        'sexy',
        'shaved beaver',
        'shaved pussy',
        'shemale',
        'shibari',
        'shit',
        'shota',
        'shrimping',
        'slanteye',
        'slut',
        'smut',
        'snatch',
        'snowballing',
        'sodomize',
        'sodomy',
        'spic',
        'spooge',
        'spread legs',
        'strap on',
        'strapon',
        'strappado',
        'strip club',
        'style doggy',
        'suck',
        'sucks',
        'suicide girls',
        'sultry women',
        'swastika',
        'swinger',
        'tainted love',
        'taste my',
        'tea bagging',
        'threesome',
        'throating',
        'tied up',
        'tight white',
        'tit',
        'tits',
        'titties',
        'titty',
        'tongue in a',
        'topless',
        'tosser',
        'towelhead',
        'tranny',
        'tribadism',
        'tub girl',
        'tubgirl',
        'tushy',
        'twat',
        'twink',
        'twinkie',
        'two girls one cup',
        'undressing',
        'upskirt',
        'urethra play',
        'urophilia',
        'vagina',
        'venus mound',
        'vibrator',
        'violet blue',
        'violet wand',
        'vorarephilia',
        'voyeur',
        'vulva',
        'wank',
        'wet dream',
        'wetback',
        'white power',
        'women rapping',
        'wrapping men',
        'wrinkled starfish',
        'xx',
        'xxx',
        'yaoi',
        'yellow showers',
        'yiffy',
        'zoophilia']
    string1 = re.findall(r'\w+', message)
    cleanmessage = []
    for c in string1:
        if string.lower(c) in profanity:
            cleanmessage.append("$!#$%$")
        else:
            cleanmessage.append(c)
    return " ".join(cleanmessage)