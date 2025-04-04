// Función para mostrar la estructura del archivo según la opción seleccionada
function mostrarEstructura() {
    var formato = document.getElementById("id_file_format");
    
    // Verificar si el campo de selección existe antes de acceder a su valor
    
    if (formato) {
        var formatoValue = formato.value;
        console.log()
        // Verificar si el valor de formatoValue no está vacío o es '0'
        if (formatoValue == '0') {  // Si el valor está vacío o es '0', no mostrar el diálogo
            console.error("No se seleccionó ningún formato válido");
            $('#estructuraDialog').modal('hide'); // Mostrar el modal
            return;
        }else{
            // Mostrar el modal solo cuando se selecciona un formato válido
           $('#estructuraDialog').modal('show'); // Mostrar el modal
        }

        
        

        var theadTabla = document.getElementById("estructura_tabla").querySelector("thead");
        var tbodyTabla = document.getElementById("estructura_tabla").querySelector("tbody");

        // Limpiar el contenido de la tabla antes de agregar nuevos encabezados y datos
        theadTabla.innerHTML = '';
        tbodyTabla.innerHTML = '';

        // Determinar los encabezados dependiendo del formato
        var encabezados;
        if (formatoValue === '1005') { // Formato 1005
            encabezados = [
                "Tipo de Documento",
                "Numero de identificación del informado",
                "DV",
                "Primer apellido del informado",
                "Segundo apellido del informado",
                "Otros nombres del informado",
                "Razón social informado",
                "Impuesto descontable",
                "IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas"
            ];
        } else if (formatoValue === '1006') { // Formato 1006
            encabezados = [
                "Tipo de Documento",
                "Numero de identificación",
                "DV",
                "Primer apellido del informado",
                "Segundo apellido del informado",
                "Otros nombres del informado",
                "Razón social informado",
                "Impuesto generado",
                "IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas",
                "Impuesto al consumo"
            ];
        } else if (formatoValue === '1007') { // Formato 1007
            encabezados = [
                "Concepto",
                "Tipo de documento",
                "Número identificación del informado",
                "Primer apellido del informado",
                "Segundo apellido del informado",
                "Primer nombre del informado",
                "Otros nombres del informado",
                "País de residencia o domicilio",
                "Ingresos brutos recibidos ",
                "Devoluciones, rebajas y descuentos"
            ];
        } else {
            console.error('Formato no válido');
            return; // No hacer nada si el formato no es reconocido
        }

        // Crear la fila de encabezados
        var filaEncabezados = document.createElement('tr');

        // Agregar cada encabezado a la fila
        encabezados.forEach(function(item) {
            var th = document.createElement('th'); // Crear una celda de encabezado (th)
            th.textContent = item; // Establecer el texto del encabezado
            filaEncabezados.appendChild(th); // Agregar el encabezado a la fila
        });

        // Agregar la fila de encabezados al <thead> de la tabla
        theadTabla.appendChild(filaEncabezados);

    } else {
        console.log('El campo de selección de formato no se encuentra en el DOM.');
        $('#estructuraDialog').modal('hide'); 
    }
}

// Función para cerrar el modal
function cerrarModal() {
    $('#estructuraDialog').modal('hide'); // Mostrar el modal
  }

// Usamos 'DOMContentLoaded' para asegurar que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function() {
    var formatoElement = document.getElementById("id_file_format");
    document.getElementById("estructuraDialog").classList.add("hidden");
    if (formatoElement) {
        console.log('antes de formato.');
        // Agregar el listener para detectar el cambio de selección
        formatoElement.addEventListener("change", mostrarEstructura);
    
    } else {
        console.error('El campo de selección de formato no se encuentra en el DOM.');
    }
});

// Función para ocultar las alertas después de 5 segundos
window.onload = function() {
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            alert.style.display = 'none';
        });
    }, 5000); // Las alertas desaparecen después de 5 segundos
};


