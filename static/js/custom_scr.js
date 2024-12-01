
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
                tr.innerHTML = '<td><input type="text" value="'+config.identificador+'" class="form-control" data-type="conf-sonido-id"></td>' +
                            '<td><input type="text" value="'+config.rutaFichero+'" class="form-control" data-type="conf-sonido-ruta"></td>' +
                            '<td class="acciones-lista">' +
                            '    <a href="#" onclick="guardarConfSonido(this)"><i class="fa fa-floppy-o" aria-hidden="true"></i></a>' +
                            '    <a href="#" onclick="eliminarConfSonido(this)"><i class="fa fa-trash-o btn-trash" aria-hidden="true"></i></a>' +
                            '</td>'
                document.querySelector("#contenidoConfigSonidos").appendChild(tr)
            });

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





