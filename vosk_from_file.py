import wave
from vosk import Model, KaldiRecognizer
import speech_recognition as sr
import pyaudio
import json


currentPath = __file__.replace("vosk_from_file.py", "").replace("\\", "/")

file = currentPath+"payday3.wav"


model = Model(currentPath+"vosk-model-es-0.42")
wf = wave.open(file, "rb")

recognizer = KaldiRecognizer(model, wf.getframerate())

print("Listo!")
with open(currentPath+"out.txt", "a", encoding="utf-8") as out:
    try:
        while True:
            data = wf.readframes(4000)
            if len(data) == 0:
                break
            if recognizer.AcceptWaveform(data):
                text = json.loads(recognizer.Result())
                text = str(text["text"]).strip();
                if text:
                    print(text);
                    out.write(text+"\n");
    except Exception as e:
        print(e);
    out.close();
