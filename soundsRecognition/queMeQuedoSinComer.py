import winsound
from utils import *

sonido = "que_me_quedo_sin_comer.wav"
playing = False


def canPlay(textDetected:str):
    return textDetected.split("si").__len__()>3



def playSound(textDetected:str):
    global playing
    if textDetected.split("si").__len__()>3:
        playing = True
        winsound.PlaySound(currentPath+"soundsRecognition/sonidos/"+sonido, winsound.SND_APPLICATION)
        playing = False