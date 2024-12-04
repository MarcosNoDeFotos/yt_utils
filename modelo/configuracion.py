import dbcon
from pygame import mixer, time
tabla = "configuracion"
class Configuracion:
    def __init__(self, salida_audio):
        self.salida_audio = salida_audio


def getConfiguracion():
    configuracion = None
    db = dbcon.getDB()
    cursor = db.cursor()
    results = cursor.execute(f"select salida_audio from {tabla} where id =1")
    r = results.fetchone()
    configuracion = Configuracion(r[0])
    cursor.close()
    db.close()
    return configuracion

def actualizarConfiguracionSonido(salida_audio):
    db = dbcon.getDB()
    cursor = db.cursor()
    result = cursor.execute(f"update {tabla} set salida_audio = ? where id = 1", (salida_audio,))
    db.commit()
    cursor.close()
    db.close()
    return result.rowcount == 1


try:
    mixer.init(devicename=getConfiguracion().salida_audio)
except Exception as e:
    print("No se puede inicializar el panel de sonidos")
    print(e)