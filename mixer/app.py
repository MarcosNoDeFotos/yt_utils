import json
from flask import Flask, request, render_template
from datetime import datetime

from mixer.audioController import changeControllerVolume, getAudioControllers, muteUnmute
app = Flask(__name__);

logpath = __file__.replace("app.py", "").replace("\\","/")+"log.log"
def log(txt):
    
    with open(logpath, "a", encoding="UTF-8") as out:
        now = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        out.write("["+now+"] "+txt+"\n");
        out.close();



@app.route("/")
def index():
   return render_template("index.html", controllers=getAudioControllers());



@app.route("/changeVolume", methods=['POST'])
def changeVolume():
    try:
        controller = request.form.get("controller");
        volume = request.form.get("volume");
        changeControllerVolume(controller, volume);
    except Exception as e:
        print(e);
    return "";


@app.route("/mute", methods=['POST'])
def mute():
    try:
        controller = request.form.get("controller");
        status = muteUnmute(controller);
        return json.dumps({"status":status});
    except Exception as e:
        print(e);
        return "";



def runApp(debug=False):
    app.run(debug=debug, host="192.168.1.189")
    