from flask import Flask, request, render_template
import global_vars
import json
from reconocimientoTexto import traducirImagenPortaPapeles, convertirATextoImagenDePortapapeles
from modelo import config_sonidos
from modelo import configuracion
from mixer import audioController
import sounddevice
from pygame import mixer, time 
import arduino as ino
import keyboard 
import pythoncom
from pycaw.pycaw import AudioUtilities
import requests
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

app = Flask("app")


@app.route("/")
def index():

    return render_template("index.html", modales = leerModales())

@app.route("/sonido")
def sonido():

    return render_template("sonido.html", modales = leerModales())


@app.route("/juego")
def juego():

    return render_template("juego.html", modales = leerModales())


@app.route("/video")
def video():

    return render_template("video.html", modales = leerModales())


@app.route("/rgb")
def rgb():
    return render_template("rgb.html", modales = leerModales(), conectado = ino.conectado)

@app.route("/botones")
def botones():
    return render_template("botones.html", modales = leerModales())








@app.route("/pegarCapturaYTraducir")
def pegarCapturaYTraducir():
    idiomaOrigen = request.args.get("idiomaOrigen")
    idiomaDestino = request.args.get("idiomaDestino")
    codigoResultado, resultado = traducirImagenPortaPapeles(idiomaOrigen, idiomaDestino)
    return json.dumps({'code':codigoResultado, 'result':resultado})

@app.route("/pegarCapturaYReconocerTexto")
def pegarCapturaYReconocerTexto():
    idiomaOrigen = request.args.get("idiomaOrigen")
    codigoResultado, resultado = convertirATextoImagenDePortapapeles(idiomaOrigen)
    return json.dumps({'code':codigoResultado, 'result':resultado})

@app.route("/getConfiguracionesSonidos")
def getConfiguracionesSonidos():
    configuraciones = []
    for c in config_sonidos.getConfiguracionesSonidos():
        configuraciones.append({'id': c.id, 'identificador': c.identificador, 'rutaFichero': c.rutaFichero})
    return json.dumps({'code': 200, 'configuraciones': configuraciones})

@app.route("/getMensajesDestacados")
def getMensajesDestacados():
    mensajes = requests.get("http://192.168.1.188:5000/getMensajesDestacados")
    return json.dumps({'code': 200, 'mensajesDestacados': json.loads(mensajes.text)})

@app.route("/repetirMensajeDestacado")
def repetirMensajeDestacado():
    usuario = request.args.get("usuario")
    mensaje = request.args.get("mensaje")
    requests.get("http://192.168.1.188:5000/destacarMensaje?user="+usuario+"&mensaje="+mensaje+"&noInsertInDB=false")
    return ""

@app.route("/eliminarMensajeDestacado")
def eliminarMensajeDestacado():
    id = request.args.get("id")
    requests.get("http://192.168.1.188:5000/eliminarMensajeDestacado?id="+id)
    return ""



@app.route("/guardarConfiguracionSonido",  methods = ['POST'])
def guardarConfiguracionSonido():
    status = "ok"
    response = ""
    id = request.form.get("id")
    identificador = request.form.get("identificador")
    ruta = request.form.get("ruta")
    ruta = ruta.replace("\\", "/")
    if id == "creando":
        nuevoId = config_sonidos.nuevaConfiguracionSonido(identificador, ruta)
        response = json.dumps({'status': status, 'id': nuevoId})
    else:
        if not config_sonidos.actualizarConfiguracionSonido(id, identificador, ruta):
            status = "failed"
        response = json.dumps({'status': status})
    return response


@app.route("/eliminarConfiguracionSonido",  methods = ['POST'])
def eliminarConfiguracionSonido():
    status = "ok"
    id = request.form.get("id")
    if not config_sonidos.eliminarConfiguracionSonido(id):
        status = "failed"
    return json.dumps({'status': status})




# RGB

@app.route("/rgb_establecerAnimacion", methods= ["POST"])
def rgb_establecerAnimacion():
    animacion = request.form.get("animacion")
    ino.escribirMensaje("setAnimacion|"+animacion)
    return ""

@app.route("/rgb_establecerColor", methods= ["POST"])
def rgb_establecerColor():
    color = request.form.get("color")
    ino.escribirMensaje("setRGB|"+color)
    return ""


# RGB





#REST
@app.route("/getDispositivosAudio")
def getDispositivosAudio():
    pythoncom.CoInitialize()
    tipo = request.args.get("tipo")
    if tipo == "altavoces":
        devs = sounddevice.query_devices()
        devs2 = []
        for dev in devs:
            if dev['max_input_channels'] == 0 and dev["name"] not in devs2:
                devs2.append(dev['name'])
        devs2.sort()
        dispositivoSeleccionado = configuracion.getConfiguracion().salida_audio
    else:
        devs2 = []
        for dev in audioController.AudioUtilities.GetAllDevices():
            if dev.FriendlyName:
                devs2.append(dev.FriendlyName)
        devs2.sort()
        dispositivoSeleccionado = configuracion.getConfiguracion().microfono_default

    

    return json.dumps({'code': 200, 'dispositivos': devs2, 'seleccionado': dispositivoSeleccionado})


@app.route("/setSalidaAudio", methods = ["POST"])
def setSalidaAudio():
    dispositivoSeleccionado = request.form.get("dispositivoSeleccionado")
    actualizado = configuracion.actualizarConfiguracionSonido(dispositivoSeleccionado, None)
    if actualizado:
        print(f"Se establece la salida a {dispositivoSeleccionado}")
    return json.dumps({'code': 200, 'status': actualizado})


@app.route("/setMicrofonoPorDefecto", methods = ["POST"])
def setMicrofonoPorDefecto():
    microfono_default = request.form.get("microfono_default")
    actualizado = configuracion.actualizarConfiguracionSonido(None, microfono_default)
    if actualizado:
        print(f"Se el micrófono por defecto a {microfono_default}")
        setMicrofonoPorDefecto(microfono_default)
    return json.dumps({'code': 200, 'status': actualizado})



@app.route("/reproducirSonido")
def reproducirSonido():
    identificador = request.args.get("identificador")   
    try:
        print(f"Reproduciendo {global_vars.sonidos[identificador]}")
        mixer.music.load(global_vars.sonidos[identificador])
        mixer.music.play()
        # while mixer.music.get_busy(): 
        #     time.Clock().tick(10)
    except Exception as e:
        print(e)
    return json.dumps({'code': 200})


@app.route("/pararReproduccionSonido")
def pararReproduccionSonido():
    try:
        mixer.music.stop()
    except Exception as e:
        print(e)
    return json.dumps({'code': 200})


@app.route("/ensordecerDiscord")
def ensordecerDiscord():
    keyboard.press_and_release('Ctrl + shift + plus') 
    return json.dumps({'code': 200})


@app.route("/mutearDesmutearMicro")
def mutearDesmutearMicro():
    audioController.mutearDesmutearMicro()
    return json.dumps({'code': 200})




def leerModales():
    modales = ""
    with open(global_vars.currentPath+"templates/modales.html", encoding="utf-8") as file:
        modales = file.read()
        file.close()
    return modales


def setMicrofonoPorDefecto(microfono):
    pythoncom.CoInitialize()
    devices = AudioUtilities.GetAllDevices()
    for device in devices:
        if device.FriendlyName == microfono:
            global_vars.microfonoPorDefecto = device
            break



if __name__ == '__main__':

    
    microfono = configuracion.getConfiguracion().microfono_default
    setMicrofonoPorDefecto(microfono)
    
    app.run(debug=False, host="192.168.1.189")