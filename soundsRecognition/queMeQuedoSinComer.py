import winsound
from utils import *

sonido = "que_me_quedo_sin_comer.wav"

def playSound(textDetected:str):
    if textDetected.split("si").__len__()>4:
        winsound.PlaySound(currentPath+"soundsRecognition/sonidos/"+sonido, winsound.SND_APPLICATION)