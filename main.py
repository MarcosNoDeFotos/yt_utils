from flask import Flask, request, render_template
import global_vars
import json
from reconocimientoTexto import traducirImagenPortaPapeles, convertirATextoImagenDePortapapeles
from modelo import config_sonidos
from modelo import configuracion
import sounddevice
from pygame import mixer, time 



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






#REST
@app.route("/getDispositivosAudio")
def getDispositivosAudio():
    devs = sounddevice.query_devices()
    devs2 = []
    for dev in devs:
        if dev['max_input_channels'] == 0 and dev["name"] not in devs2:
            devs2.append(dev['name'])
    devs2.sort()

    dispositivoSeleccionado = configuracion.getConfiguracion().salida_audio

    return json.dumps({'code': 200, 'dispositivos': devs2, 'seleccionado': dispositivoSeleccionado})


@app.route("/setSalidaAudio", methods = ["POST"])
def setSalidaAudio():
    dispositivoSeleccionado = request.form.get("dispositivoSeleccionado")
    actualizado = configuracion.actualizarConfiguracionSonido(dispositivoSeleccionado)
    if actualizado:
        print(f"Se establece la salida a {dispositivoSeleccionado}")
    return json.dumps({'code': 200, 'status': actualizado})



@app.route("/reproducirSonido")
def reproducirSonido():
    identificador = request.args.get("identificador")   
    try:
        print(f"Reproduciendo {global_vars.sonidos[identificador]}")
        mixer.music.load(global_vars.sonidos[identificador])
        mixer.music.play() #Play it
        while mixer.music.get_busy(): 
            time.Clock().tick(10)
    except Exception as e:
        print(e)
    return json.dumps({'code': 200})





def leerModales():
    modales = ""
    with open(global_vars.currentPath+"templates/modales.html", encoding="utf-8") as file:
        modales = file.read()
        file.close()
    return modales


if __name__ == '__main__':
    app.run(debug=True)