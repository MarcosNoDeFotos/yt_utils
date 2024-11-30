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

def traducirTexto(texto, idioma):
    return GoogleTranslator(source="auto", target=idioma).translate(texto)



def traducirImagenPortaPapeles(idiomaOrigen, idiomaDestino):
    status = 1
    try:
        imagen = guardarImagen()

        reader = easyocr.Reader([idiomaOrigen])
        readed = reader.readtext(imagen)
        os.remove(imagen)
        texto = ""
        for linea in readed:
            texto += linea[1]+" "
        result = traducirTexto(texto, idiomaDestino)
    except:
        result = "No se ha podido obtener el texto de la imagen"
        status = 0

    return status, result;

def convertirATextoImagenDePortapapeles(idioma):
    status = 1
    try:
        imagen = guardarImagen()
        reader = easyocr.Reader([idioma])
        readed = reader.readtext(imagen)
        os.remove(imagen)
        texto = ""
        for linea in readed:
            texto += linea[1]+" "
        result = texto
    except:
        result = "No se ha podido obtener el texto de la imagen"
        status = 0

    return status, result;
