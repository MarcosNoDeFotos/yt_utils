import easyocr
import cv2
import matplotlib.pyplot as plot
import numpy as np
from PIL import ImageGrab
from utils import * 
from deep_translator import GoogleTranslator
import os

def guardarImagen():
    nombreImagen = currentPath+"tempImage"+getFechaHora()+".png"
    im = ImageGrab.grabclipboard()
    im.save(nombreImagen,'PNG')
    return nombreImagen

def traducirTexto(texto):
    return GoogleTranslator(source="auto", target="es").translate(texto)



def traducirImagenPortaPapeles():
    status = 1
    try:
        imagen = guardarImagen()

        reader = easyocr.Reader(["en"])
        readed = reader.readtext(imagen)
        os.remove(imagen)
        texto = ""
        for linea in readed:
            texto += linea[1]+" "
        result = traducirTexto(texto)
    except:
        result = "No se ha podido obtener el texto de la imagen"
        status = 0

    return status, result;
