import speech_recognition as sr
from datetime import datetime

r = sr.Recognizer()

currentPath = __file__.replace("main.py", "").replace("\\", "/")

inicio = datetime.now().timestamp()
audio_file = sr.AudioFile(currentPath+'payday3.wav')

with audio_file as source:

    audio = r.record(source)
    text = r.recognize_google(audio, language="es-ES")

    print(text)
    fin = datetime.now().timestamp()

print(f"Reconocido en {datetime.fromtimestamp(fin-inicio).second} segundos")