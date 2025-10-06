import dbcon
from pygame import mixer, time
tabla = "configuracion"
class Configuracion:
    def __init__(self, salida_audio, microfono_default):
        self.salida_audio = salida_audio
        self.microfono_default = microfono_default


def getConfiguracion():
    configuracion = None
    db = dbcon.getDB()
    cursor = db.cursor()
    results = cursor.execute(f"select salida_audio, microfono_default from {tabla} where id =1")
    r = results.fetchone()
    configuracion = Configuracion(r[0], r[1])
    cursor.close()
    db.close()
    return configuracion

def actualizarConfiguracionSonido(salida_audio, microfono_default):
    db = dbcon.getDB()
    cursor = db.cursor()
    if salida_audio:
        cursor.execute(f"update {tabla} set salida_audio = ? where id = 1", (salida_audio,))
    if microfono_default:
        cursor.execute(f"update {tabla} set microfono_default = ? where id = 1", (microfono_default,))
    db.commit()
    cursor.close()
    db.close()
    return True


try:
    mixer.init(devicename=getConfiguracion().salida_audio)
except Exception as e:
    print("No se puede inicializar el panel de sonidos")
    print(e)