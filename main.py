from flask import Flask, request, render_template
import global_vars
import json
from reconocimientoTexto import traducirImagenPortaPapeles, convertirATextoImagenDePortapapeles
from modelo import config_sonidos
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






def leerModales():
    modales = ""
    with open(global_vars.currentPath+"templates/modales.html", encoding="utf-8") as file:
        modales = file.read()
        file.close()
    return modales


if __name__ == '__main__':
    app.run(debug=True)