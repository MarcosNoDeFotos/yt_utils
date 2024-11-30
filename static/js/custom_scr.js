
$("#pegarCapturaYTraducir").on("click", pegarCapturaYTraducir)
$("#pegarCapturaYReconocerTexto").on("click", pegarCapturaYReconocerTexto)
function pegarCapturaYTraducir() {
    $("#resultadoTraducción").val("Traduciendo...");
    var idiomaOrigen = $("#idiomaOrigen").val();
    var idiomaDestino = $("#idiomaDestino").val();
    $.ajax({
        type: "GET",
        url: "/pegarCapturaYTraducir?idiomaOrigen="+idiomaOrigen+"&idiomaDestino="+idiomaDestino,
        success:  (response) => {
            var response = JSON.parse(response)
            $("#resultadoTraducción").val(response.result);
        },
        error : ()=>{
            $("#resultadoTraducción").val("Error al traducir. Consulta la consola");
        }
    });
}
function pegarCapturaYReconocerTexto() {
    $("#resultadoReconocimientoTexto").val("Obteniendo texto...");
    var idiomaOrigen = $("#idiomaOrigenReconocimientoTexto").val();
    $.ajax({
        type: "GET",
        url: "/pegarCapturaYReconocerTexto?idiomaOrigen="+idiomaOrigen,
        success:  (response) => {
            var response = JSON.parse(response)
            $("#resultadoReconocimientoTexto").val(response.result);
        },
        error : ()=>{
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
                tr.innerHTML = '<td><input type="text" value="'+config.identificador+'" class="form-control" data-type="conf-sonido-id" data-id="'+config.id+'"></td>' +
                            '<td><input type="text" value="'+config.rutaFichero+'" class="form-control" data-type="conf-sonido-ruta" data-id="'+config.id+'"></td>' +
                            '<td class="acciones-lista">' +
                            '    <a href="#" onclick="guardarConfSonido('+config.id+')"><i class="fa fa-floppy-o" aria-hidden="true"></i></a>' +
                            '    <a href="#" onclick="eliminarConfSonido('+config.id+')"><i class="fa fa-trash-o btn-trash" aria-hidden="true"></i></a>' +
                            '</td>'
                document.querySelector("#contenidoConfigSonidos").appendChild(tr)
            });

        }
    });
}


function guardarConfSonido(id) {
    var identificador = document.querySelector("input[data-id='"+id+"'][data-type='conf-sonido-id']").value
    var ruta = document.querySelector("input[data-id='"+id+"'][data-type='conf-sonido-ruta']").value
    var formData = new FormData()
    formData.append("id", id)
    formData.append("identificador", identificador)
    formData.append("ruta", ruta)
    $.ajax({
        type: "POST",
        data : formData,
        url: "/guardarConfiguracionSonido",
        success: function (response) {
            alert("Bien!")
            // TODO crear la funcionalidad de guardar configuración
        }
    });
}


abrirConfiguracionesSonidos()



