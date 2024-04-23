from datetime import datetime
import unicodedata
import winsound
currentPath = __file__.replace(__file__.split("\\")[-1], "").replace("\\", "/")

def getFechaHora():
    return datetime.now().strftime("%d-%m-%Y-%H%M%S")


def clearText(text:str):
    return ''.join(c for c in unicodedata.normalize('NFD', text) if unicodedata.category(c) != 'Mn')

