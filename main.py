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






def leerModales():
    modales = ""
    with open(global_vars.currentPath+"templates/modales.html", encoding="utf-8") as file:
        modales = file.read()
        file.close()
    return modales


if __name__ == '__main__':
    app.run(debug=True)