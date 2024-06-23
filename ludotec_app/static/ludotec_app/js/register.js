flatpickr("#id_duracion", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    maxTime: "08:00"
});

document.addEventListener('DOMContentLoaded', function() {
    // Obtener referencias a los campos de juego
    var juegoDropdown = document.getElementById('id_juego');
    var juegoExternoInput = document.getElementById('id_juego_externo');
    var ganadorDropdown = document.getElementById('id_ganador'); // Añadir referencia al campo ganador

    // Agregar un evento para detectar cambios en el campo de juego personalizado
    juegoExternoInput.addEventListener('input', function() {
        // Si el campo de juego personalizado está lleno, desactivar el campo de juego desplegable
        if (juegoExternoInput.value.trim() !== '') {
            juegoDropdown.disabled = true;
        } else {
            juegoDropdown.disabled = false;
        }
    });

    juegoDropdown.addEventListener('input', function() {
        if (juegoDropdown.value.trim() !== '') {
            juegoExternoInput.disabled = true;
        } else {
            juegoExternoInput.disabled = false;
        }
    });

    var guardarJugadorPuntuacionBtn = document.getElementById('guardar-jugador-puntuacion');

    guardarJugadorPuntuacionBtn.addEventListener('click', function() {
        var nombreJugadorInput = document.getElementById('id_nombre_jugador');
        var puntuacionInput = document.getElementById('id_puntuacion');
        var nombreJugador = nombreJugadorInput.value;
        var puntuacion = puntuacionInput.value;

        if (nombreJugador.trim() !== '' && puntuacion.trim() !== '') {
            var tableBody = document.querySelector('#puntuacion-table tbody');
            var row = tableBody.insertRow();
            var nombreCell = row.insertCell(0);
            var puntuacionCell = row.insertCell(1);
            nombreCell.textContent = nombreJugador;
            puntuacionCell.textContent = puntuacion;

            // Mostrar el encabezado de la tabla si se agrega el primer jugador
            var tableHead = document.getElementById('puntuacion-table-head');
            tableHead.style.display = 'table-header-group';

            // Ordenar las filas por puntuación
            sortTableByScore();

            // Aplicar estilos a las filas
            styleRows();

            // Actualizar los campos ocultos con los nombres de los jugadores y sus puntuaciones
            var jugadoresInput = document.getElementById('id_jugadores');
            var puntuacionesInput = document.getElementById('id_puntuaciones');
            var jugadores = jugadoresInput.value;
            var puntuaciones = puntuacionesInput.value;

            if (jugadores === '') {
                jugadoresInput.value = nombreJugador;
                puntuacionesInput.value = puntuacion;
            } else {
                jugadoresInput.value += ',' + nombreJugador;
                puntuacionesInput.value += ',' + puntuacion;
            }

            // Limpiar los campos de entrada después de guardar
            nombreJugadorInput.value = '';
            puntuacionInput.value = '';

            // Actualizar las opciones del campo ganador
            updateGanadorOptions();
        }
    });

    // Función para manejar el envío del formulario
    var form = document.querySelector('form');
    form.addEventListener('submit', function(event) {
        // Actualizar los campos ocultos antes de enviar el formulario
        var tableRows = document.querySelectorAll('#puntuacion-table tbody tr');
        var jugadoresInput = document.getElementById('id_jugadores');
        var puntuacionesInput = document.getElementById('id_puntuaciones');
        var jugadores = [];
        var puntuaciones = [];

        tableRows.forEach(function(row) {
            var nombreJugador = row.cells[0].textContent;
            var puntuacion = row.cells[1].textContent;
            jugadores.push(nombreJugador);
            puntuaciones.push(puntuacion);
        });

        jugadoresInput.value = jugadores.join(',');
        puntuacionesInput.value = puntuaciones.join(',');
    });

    function sortTableByScore() {
        var table = document.getElementById('puntuacion-table');
        var tbody = table.querySelector('tbody');
        var rows = Array.from(tbody.querySelectorAll('tr'));

        rows.sort(function(rowA, rowB) {
            var scoreA = parseInt(rowA.cells[1].textContent);
            var scoreB = parseInt(rowB.cells[1].textContent);
            return scoreB - scoreA; // Orden descendente
        });

        rows.forEach(function(row) {
            tbody.appendChild(row); // Reordenar las filas en el tbody
        });
    }

    function styleRows() {
        var table = document.getElementById('puntuacion-table');
        var tbody = table.querySelector('tbody');
        var rows = tbody.querySelectorAll('tr');

        rows.forEach(function(row, index) {
            if (index === 0) {
                row.style.backgroundColor = 'lightgreen'; // Primera fila
            } else if (index === rows.length - 1) {
                row.style.backgroundColor = 'lightcoral'; // Última fila
            } else {
                row.style.backgroundColor = 'lightyellow'; // Resto de filas
            }
        });
    }

    function updateGanadorOptions() {
        var tableBody = document.querySelector('#puntuacion-table tbody');
        var jugadores = new Set(); // Usar un Set para evitar jugadores duplicados

        tableBody.querySelectorAll('tr').forEach(function(row) {
            var nombreJugador = row.cells[0].textContent.trim();
            jugadores.add(nombreJugador);
        });

        // Limpiar las opciones actuales del campo ganador
        ganadorDropdown.innerHTML = '';

        // Crear una opción por cada jugador encontrado
        jugadores.forEach(function(jugador) {
            var option = document.createElement('option');
            option.textContent = jugador;
            ganadorDropdown.appendChild(option);
        });
    }
});