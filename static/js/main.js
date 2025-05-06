// Función para mostrar la estructura del archivo según la opción seleccionada
function mostrarEstructura() {
    var formato = document.getElementById("id_file_format");
    
    // Verificar si el campo de selección existe antes de acceder a su valor
    if (formato) {
        var formatoValue = formato.value;
        
        // Si no se selecciona un formato válido, ocultamos el modal
        if (formatoValue == '0') {
            console.error("No se seleccionó ningún formato válido");
            $('#estructuraDialog').modal('hide'); // Ocultar el modal
            return;
        } else {
            // Mostrar el modal solo cuando se selecciona un formato válido
            $('#estructuraDialog').modal('show'); // Mostrar el modal
        }

        // Obtener las tablas thead y tbody
        var theadTabla = document.getElementById("estructura_tabla").querySelector("thead");
        var tbodyTabla = document.getElementById("estructura_tabla").querySelector("tbody");

        // Limpiar el contenido de la tabla antes de agregar nuevos encabezados y datos
        theadTabla.innerHTML = '';
        tbodyTabla.innerHTML = '';

        // Determinar los encabezados dependiendo del formato
        var encabezados;
        if (formatoValue === '1005') { // Formato 1005
            encabezados = [
                "Tipo de Documento", "Numero de identificación del informado", "DV",
                "Primer apellido del informado", "Segundo apellido del informado", 
                "Otros nombres del informado", "Razón social informado", 
                "Impuesto descontable", "IVA resultante por devoluciones en ventas anuladas, rescindidas o resueltas"
            ];
        } else if (formatoValue === '1006') { // Formato 1006
            encabezados = [
                "Tipo de Documento", "Numero de identificación", "DV",
                "Primer apellido del informado", "Segundo apellido del informado", 
                "Otros nombres del informado", "Razón social informado", 
                "Impuesto generado", "IVA recuperado en devoluciones en compras anuladas. rescindidas o resueltas",
                "Impuesto al consumo"
            ];
        } else if (formatoValue === '1007') { // Formato 1007
            encabezados = [
                "Concepto", "Tipo de documento", "Número identificación del informado",
                "Primer apellido del informado", "Segundo apellido del informado", 
                "Primer nombre del informado", "Otros nombres del informado", 
                "País de residencia o domicilio", "Ingresos brutos recibidos ",
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
        $('#estructuraDialog').modal('hide'); // Ocultar el modal si no existe
    }
}

// Función para cerrar el modal
function cerrarModal() {
    $('#estructuraDialog').modal('hide'); // Ocultar el modal
}

// Usamos 'DOMContentLoaded' para asegurar que el DOM esté completamente cargado antes de ejecutar el script
document.addEventListener('DOMContentLoaded', function() {
    var formatoElement = document.getElementById("id_file_format");

    const estructuraDialog = document.getElementById("estructuraDialog");
    if (estructuraDialog) {
        estructuraDialog.classList.add("hidden");
    }

    if (formatoElement) {
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
            alert.style.display = 'none'; // Ocultar las alertas
        });
    }, 5000); // Las alertas desaparecen después de 5 segundos
};

let tareaArrastrada = null;

// Iniciar el arrastre de tarea
function iniciarArrastre(event) {
    tareaArrastrada = event.target; // Guardar la tarea que se está arrastrando
}

// Función para mover una tarea a una nueva columna
function moverTarea(event, targetColumn) {
    event.preventDefault(); // Prevenir el comportamiento predeterminado del navegador

    if (tareaArrastrada) {
        const tareaId = tareaArrastrada.dataset.id; // Obtener el ID de la tarea
        const nuevoEstado = targetColumn.getAttribute('data-estado'); // Obtener el nuevo estado de la columna destino

        // Mover la tarjeta visualmente a la nueva columna
        targetColumn.appendChild(tareaArrastrada);

        // Obtener la URL de actualización de estado
        const urlActualizarEstado = document.getElementById('url-actualizar-estado').dataset.url;

        // Enviar la actualización al servidor usando la URL obtenida
        fetch(urlActualizarEstado, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() // Obtener el token CSRF
            },
            body: JSON.stringify({
                tarea_id: tareaId,
                estado: nuevoEstado
            })
        })
        .then(response => response.json())
        .then(data => {
            console.log('tarea id: '+tareaId);
            console.log('nuevo estado: '+nuevoEstado)
            if (data.success) {
                // Recargar la página para ver los cambios reflejados
                location.reload();
            } else {
                alert("Error al actualizar la tarea.");
            }
        })
        .catch(error => {
            console.error("Error:", error);
        });
    }
}

// Función para obtener el token CSRF
function getCSRFToken() {
    const name = 'csrftoken';
    const cookieValue = document.cookie
        .split('; ')
        .find(row => row.startsWith(name + '='))?.split('=')[1];
    return cookieValue;
}

// Función para cambiar el mes desde los botones en el tablero Kanban
function cambiarMes(direccion) {
    const currentUrl = new URL(window.location.href);
    let mes = parseInt(currentUrl.searchParams.get("mes")) || new Date().getMonth() + 1;
    let anio = parseInt(currentUrl.searchParams.get("anio")) || new Date().getFullYear();

    mes += direccion;
    if (mes > 12) {
        mes = 1;
        anio++;
    } else if (mes < 1) {
        mes = 12;
        anio--;
    }

    currentUrl.searchParams.set("mes", mes);
    currentUrl.searchParams.set("anio", anio);

    window.location.href = currentUrl.toString();
}

document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.kanban-column').forEach(columna => {
        new Sortable(columna, {
            group: 'kanban',
            animation: 150,
            onEnd: function (evt) {
                const tareaId = evt.item.dataset.id;
                const nuevoEstado = evt.to.dataset.estado;

                const urlActualizarEstado = document.getElementById('url-actualizar-estado').dataset.url;

                fetch(urlActualizarEstado, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCSRFToken()
                    },
                    body: JSON.stringify({
                        tarea_id: tareaId,
                        estado: nuevoEstado
                    })
                })
                .then(response => response.json())
                .then(data => {
                    if (!data.success) {
                        alert("Error al actualizar la tarea.");
                    }else{
                        location.reload();
                    }
                })
                .catch(error => {
                    console.error("Error:", error);
                });
            }
        });
    });
});

// Función que se activa al hacer clic en una tarea
window.editarTarea = function(id, titulo, descripcion, fecha){
   
    // Llenar los datos del modal con los datos de la tarea
    document.getElementById('tareaTitulo').value = titulo;
    document.getElementById('tareaDescripcion').value = descripcion;
    document.getElementById('tareaFecha').value = formatearFecha(fecha);

    // Agregar el ID de la tarea al formulario (para poder identificarla al guardar)
    const form = document.getElementById('formEditarTarea');
    form.setAttribute('data-id', id);

    // Mostrar el modal
    $('#editarTareaModal').modal('show');
}

// Función para guardar los cambios
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('formEditarTarea');
  
    // Verificamos si el formulario existe antes de agregar el listener
    if (form) {
      form.addEventListener('submit', function (event) {
        event.preventDefault();
  
        const tareaId = form.getAttribute('data-id');
        const titulo = document.getElementById('tareaTitulo').value.trim();
        const descripcion = document.getElementById('tareaDescripcion').value.trim();
        const fecha = document.getElementById('tareaFecha').value;
  
        if (!titulo || !descripcion || !fecha) {
          alert("Por favor completá todos los campos.");
          return;
        }
  
        
        const urlBase = document.getElementById('url-editar-tarea').dataset.url;
        const url = urlBase.replace(/0\/?$/, `${tareaId}/`);
  
        fetch(url, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCSRFToken()
          },
          body: JSON.stringify({
            titulo: titulo,
            descripcion: descripcion,
            fecha: fecha
          })
        })
        .then(response => response.json())
        .then(data => {
          if (data.success) {
            location.reload();
          } else {
            alert("Hubo un error al guardar la tarea.");
          }
        })
        .catch(error => console.error("Error:", error));
  
        // Cerrar el modal (si estás usando Bootstrap 5 sin jQuery)
        const modal = bootstrap.Modal.getInstance(document.getElementById('editarTareaModal'));
        if (modal) modal.hide();
      });
    }
  });


// Función para formatear la fecha en YYYY-MM-DD
function formatearFecha(fecha) {
    const dateObj = new Date(fecha);
    const anio = dateObj.getFullYear();
    const mes = String(dateObj.getMonth() + 1).padStart(2, '0');
    const dia = String(dateObj.getDate()).padStart(2, '0');
    return `${anio}-${mes}-${dia}`;
}
//habilidar tooltip
document.addEventListener('DOMContentLoaded', function () {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.forEach(function (tooltipTriggerEl) {
      new bootstrap.Tooltip(tooltipTriggerEl);
    });
  });
  
  window.eliminarTarea = function(tareaId){
    // Confirmación de eliminación
    if (confirm('¿Estás seguro que quieres eliminar esta tarea?')) {
        // Enviar la solicitud para eliminar la tarea

        const urlBase = document.getElementById('url-eliminar-tarea').dataset.url;
        const url = urlBase.replace(/0\/?$/, `${tareaId}/`);

        fetch(url, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken() 
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Actualizar la interfaz o eliminar la tarea del DOM
                alert('Tarea eliminada correctamente');
                location.reload();
            
            } else {
                alert('Hubo un error al eliminar la tarea');
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Error en la eliminación de la tarea');
        });
    }
}

//descargar formatos de como archivos de excel
function downloadTableAsXLSX() {
    var table = document.getElementById("estructura_tabla");
    var currentPath = window.location.pathname;
    var formatoSelect = document.getElementById("id_file_format");
    var formatoValue = formatoSelect ? formatoSelect.value : "formato";

    // Normaliza la ruta quitando barras finales
    currentPath = currentPath.replace(/\/+$/, "");

    // Define nombre base
    var nombreArchivo = formatoValue;

    if (currentPath.endsWith("procesar_excel")) {
        var wb = XLSX.utils.table_to_book(table, { sheet: "Hoja 1" });
        XLSX.writeFile(wb, nombreArchivo + ".xlsx");
        console.log("Descargando como .xls");
    } else if (currentPath.endsWith("procesar_csv")) {
        var csv = [];
        var rows = table.querySelectorAll("tr");

        rows.forEach(function(row) {
            var cols = row.querySelectorAll("th, td");
            var rowData = [];
            cols.forEach(function(col) {
                rowData.push('"' + col.innerText.replace(/"/g, '""') + '"');
            });
            csv.push(rowData.join(","));
        });

        var csvContent = csv.join("\n");
        var blob = new Blob([csvContent], { type: "text/csv;charset=utf-8;" });
        var link = document.createElement("a");
        link.href = URL.createObjectURL(blob);
        link.download = nombreArchivo + ".csv";
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        console.log("Descargando como .csv");
    } else {
        alert("Ruta no reconocida para descarga.");
    }
}