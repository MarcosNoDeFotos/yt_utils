
var completadoIcon = '<i class="fa fa-check tick" aria-hidden="true"></i>'
var cargandoIcon = '<i class="fa fa-spinner" aria-hidden="true"></i>'


$("#pegarCapturaYTraducir").on("click", pegarCapturaYTraducir)
$("#pegarCapturaYReconocerTexto").on("click", pegarCapturaYReconocerTexto)
function pegarCapturaYTraducir() {
    $("#resultadoTraducción").val("Traduciendo...");
    var idiomaOrigen = $("#idiomaOrigen").val();
    var idiomaDestino = $("#idiomaDestino").val();
    $.ajax({
        type: "GET",
        url: "/pegarCapturaYTraducir?idiomaOrigen=" + idiomaOrigen + "&idiomaDestino=" + idiomaDestino,
        success: (response) => {
            var response = JSON.parse(response)
            $("#resultadoTraducción").val(response.result);
        },
        error: () => {
            $("#resultadoTraducción").val("Error al traducir. Consulta la consola");
        }
    });
}


function pegarCapturaYReconocerTexto() {
    $("#resultadoReconocimientoTexto").val("Obteniendo texto...");
    var idiomaOrigen = $("#idiomaOrigenReconocimientoTexto").val();
    $.ajax({
        type: "GET",
        url: "/pegarCapturaYReconocerTexto?idiomaOrigen=" + idiomaOrigen,
        success: (response) => {
            var response = JSON.parse(response)
            $("#resultadoReconocimientoTexto").val(response.result);
        },
        error: () => {
            $("#resultadoReconocimientoTexto").val("Error al reconocer el texto. Consulta la consola");
        }
    });
}

function abrirConfiguracionesSonidos() {
    $("#contenidoConfigSonidos").text("");
    $("#modalConfiguracionPanelSonidos").modal("show")
    $.ajax({
        type: "GET",
        url: "/getConfiguracionesSonidos",
        success: function (response) {
            var response = JSON.parse(response)
            response.configuraciones.forEach(config => {
                var tr = document.createElement("tr")
                tr.setAttribute("data-id", config.id)
                tr.innerHTML = '<td><input type="text" value="' + config.identificador + '" class="form-control" data-type="conf-sonido-id"></td>' +
                    '<td><input type="text" value="' + config.rutaFichero + '" class="form-control" data-type="conf-sonido-ruta"></td>' +
                    '<td class="acciones-lista">' +
                    '    <a href="#" onclick="guardarConfSonido(this)"><i class="fa fa-floppy-o" aria-hidden="true"></i></a>' +
                    '    <a href="#" onclick="eliminarConfSonido(this)"><i class="fa fa-trash-o btn-trash" aria-hidden="true"></i></a>' +
                    '</td>'
                document.querySelector("#contenidoConfigSonidos").appendChild(tr)
            });

        }
    });
    $("#salidaAudio").text("");
    $.ajax({
        type: "GET",
        url: "/getDispositivosAudio?tipo=altavoces",
        success: function (response) {
            var response = JSON.parse(response)
            response.dispositivos.forEach(dev => {
                var option = document.createElement("option")
                option.setAttribute("value", dev)
                if (dev == response.seleccionado) {
                    option.setAttribute("selected", "")
                }
                option.innerHTML = dev

                document.querySelector("#salidaAudio").appendChild(option)
            });

        }
    });


}

function abrirMensajesDestacados() {
    $("#contenidoMensajesDestacados").text("");
    $("#modalMensajesDestacados").modal("show")
    $.ajax({
        type: "GET",
        url: "/getMensajesDestacados",
        success: function (response) {
            var response = JSON.parse(response)
            response.mensajesDestacados.forEach(mensajeDestacado => {
                var tr = document.createElement("tr")
                tr.innerHTML = '<td>' + mensajeDestacado.usuario + '</td>' +
                    '<td>' + mensajeDestacado.mensaje + '</td>' +
                    '<td>' +
                    '    <a href="#" onclick="repetirMensajeDestacado(\''+mensajeDestacado.usuario+'\', \''+mensajeDestacado.mensaje+'\')"><i class="fa fa-play" aria-hidden="true"></i></a>' +
                    '</td>' +
                    '<td>' +
                    '    <a href="#" onclick="eliminarMensajeDestacado('+mensajeDestacado.id+')"><i class="fa fa-trash" style="color:red;" aria-hidden="true"></i></a>' +
                    '</td>'
                document.querySelector("#contenidoMensajesDestacados").appendChild(tr)
            });

        }
    });
}

function repetirMensajeDestacado(usuario, mensaje) {
    $.ajax({
        type: "GET",
        url: "/repetirMensajeDestacado?usuario="+usuario+"&mensaje="+mensaje,
        success: function (response) {}
    });
}
function eliminarMensajeDestacado(id) {
    $.ajax({
        type: "GET",
        url: "/eliminarMensajeDestacado?id="+id,
        success: function (response) {
            abrirMensajesDestacados()
        }
    });
}

function abrirConfiguracionMicroDef() {
    $("#modalConfiguracionMicroDefecto").modal("show")
    $("#microDefecto").text("");
    $.ajax({
        type: "GET",
        url: "/getDispositivosAudio?tipo=microfonos",
        success: function (response) {
            var response = JSON.parse(response)
            response.dispositivos.forEach(dev => {
                var option = document.createElement("option")
                option.setAttribute("value", dev)
                if (dev == response.seleccionado) {
                    option.setAttribute("selected", "")
                }
                option.innerHTML = dev

                document.querySelector("#microDefecto").appendChild(option)
            });

        }
    });


}


function guardarSalidaAudio(src) {
    var formData = new FormData()
    formData.append("dispositivoSeleccionado", src.value)

    $.ajax({
        type: "POST",
        url: "/setSalidaAudio",
        data: formData,
        crossDomain: 'true',
        contentType: false,
        processData: false,
        success: function (response) {
        }
    });
}

function guardarMicrofonoPorDefecto(src) {
    var formData = new FormData()
    formData.append("microfono_default", src.value)

    $.ajax({
        type: "POST",
        url: "/setMicrofonoPorDefecto",
        data: formData,
        crossDomain: 'true',
        contentType: false,
        processData: false,
        success: function (response) {
        }
    });
}


function guardarConfSonido(src) {
    var row = src.parentNode.parentNode;
    var id = row.getAttribute("data-id")
    var initialBTNInner = src.innerHTML;
    src.innerHTML = cargandoIcon
    var identificadorInput = row.querySelector("td input[data-type='conf-sonido-id']")
    var rutaInput = row.querySelector("td input[data-type='conf-sonido-ruta']")
    var formData = new FormData()
    formData.append("id", id)
    formData.append("identificador", identificadorInput.value)
    formData.append("ruta", rutaInput.value)

    $.ajax({
        type: "POST",
        url: "/guardarConfiguracionSonido",
        data: formData,
        crossDomain: 'true',
        contentType: false,
        processData: false,
        success: function (response) {
            response = JSON.parse(response)
            if (response.status == "ok") {
                if (response.id != null) {
                    row.setAttribute("data-id", response.id)
                }
                src.innerHTML = completadoIcon
                setTimeout(() => {
                    src.innerHTML = initialBTNInner
                }, 2000);
            }

        }
    });
}

function eliminarConfSonido(src) {
    var row = src.parentNode.parentNode;
    var id = row.getAttribute("data-id")
    src.innerHTML = cargandoIcon
    var formData = new FormData()
    formData.append("id", id)

    $.ajax({
        type: "POST",
        url: "/eliminarConfiguracionSonido",
        data: formData,
        crossDomain: 'true',
        contentType: false,
        processData: false,
        success: function (response) {
            response = JSON.parse(response)
            if (response.status == "ok") {
                src.innerHTML = completadoIcon
                setTimeout(() => {
                    row.parentNode.removeChild(row)
                }, 2000);
            }

        }
    });
}


function nuevoConfSonido() {
    if (document.querySelector("tr[data-id='creando']") == null) {
        var tr = document.createElement("tr")
        tr.setAttribute("data-id", "creando")
        tr.innerHTML = '<td><input type="text" value="" class="form-control" data-type="conf-sonido-id" data-id="creando"></td>' +
            '<td><input type="text" value="" class="form-control" data-type="conf-sonido-ruta" data-id="creando"></td>' +
            '<td class="acciones-lista">' +
            '    <a href="#" onclick="guardarConfSonido(this, \'creando\')"><i class="fa fa-floppy-o" aria-hidden="true"></i></a>' +
            '    <a href="#" onclick="eliminarConfSonido(this, \'creando\')"><i class="fa fa-trash-o btn-trash" aria-hidden="true"></i></a>' +
            '</td>'
        document.querySelector("#contenidoConfigSonidos").appendChild(tr)
        tr.querySelector("td input[data-type='conf-sonido-id']").focus()
    }


}





// RGB

function rgb_establecerAnimacion(animacion) {

    var formData = new FormData()
    formData.append("animacion", animacion)

    $.ajax({
        type: "POST",
        url: "/rgb_establecerAnimacion",
        data: formData,
        crossDomain: 'true',
        contentType: false,
        processData: false,
        success: function (response) {
        }
    });
}
function rgb_establecerColor() {

    var formData = new FormData()
    formData.append("color", hexToRgb(document.querySelector("#rgb_color").value))

    $.ajax({
        type: "POST",
        url: "/rgb_establecerColor",
        data: formData,
        crossDomain: 'true',
        contentType: false,
        processData: false,
        success: function (response) {
        }
    });
}

function setColorConPredefinido(src) {
    var rgb = src.style.backgroundColor
    rgb = rgb.replace("rgb(", "").replace(")", "")
    var r_g_b = rgb.split(",")

    document.querySelector("#rgb_color").value = rgbToHex(r_g_b[0], r_g_b[1], r_g_b[2])
}

function componentToHex(c) {
    c = parseInt(c)
    var hex = c.toString(16);
    return hex.length == 1 ? "0" + hex : hex;
}
function rgbToHex(r, g, b) {
    r = r.trim()
    g = g.trim()
    b = b.trim()
    return "#" + componentToHex(r) + componentToHex(g) + componentToHex(b);
}



function hexToRgb(hex) {
    // Expand shorthand form (e.g. "03F") to full form (e.g. "0033FF")
    var shorthandRegex = /^#?([a-f\d])([a-f\d])([a-f\d])$/i;
    hex = hex.replace(shorthandRegex, function (m, r, g, b) {
        return r + r + g + g + b + b;
    });

    var result = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
    return result ? parseInt(result[1], 16)+","+parseInt(result[2], 16)+","+parseInt(result[3], 16) : null;
}

// RGB