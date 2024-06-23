document.addEventListener("DOMContentLoaded", function () {

    function obtenerContenido(cell, columnIndex) {
        if (columnIndex === 1 || columnIndex === 3) { // Si la columna es la de "Fecha" o "Lugar"
            // Obtener el contenido de la celda como texto
            return cell.textContent.trim().toLowerCase();
        } else if (columnIndex === 2) { // Si la columna es la de "Duración"
            // Obtener el contenido de la celda y dividirlo en partes
            var durationParts = cell.textContent.split(':');
            var hours = 0;
            var minutes = 0;
            var seconds = 0;

            if (durationParts.length >= 2) {
                hours = parseInt(durationParts[0], 10);
                minutes = parseInt(durationParts[1], 10);
            }
            if (durationParts.length === 3) {
                seconds = parseInt(durationParts[2], 10);
            }

            // Calcular la duración total en segundos para la comparación
            var totalSeconds = hours * 3600 + minutes * 60 + seconds;
            return totalSeconds;
        } else { // Otra columna
            // Implementación para otras columnas numéricas o de texto
            return cell.textContent.trim().toLowerCase();
        }
    }

    function ordenarTabla(tabla, columna) {
        var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
        table = document.querySelector('.' + tabla);
        switching = true;
        dir = "asc";
        while (switching) {
            switching = false;
            rows = table.rows;
            for (i = 1; i < (rows.length - 1); i++) {
                shouldSwitch = false;
                x = rows[i].getElementsByTagName("td")[columna];
                y = rows[i + 1].getElementsByTagName("td")[columna];
                var xContent = obtenerContenido(x, columna);
                var yContent = obtenerContenido(y, columna);

                // Comparación especial para la primera letra de cada juego (solo para columna 0)
                if (columna === 0) {
                    if (dir == "asc") {
                        if (xContent > yContent) {
                            shouldSwitch = true;
                            break;
                        }
                    } else if (dir == "desc") {
                        if (xContent < yContent) {
                            shouldSwitch = true;
                            break;
                        }
                    }
                } else {
                    // Comparación estándar para otros tipos de datos
                    if (dir == "asc") {
                        if (isNaN(parseFloat(xContent))) {
                            if (xContent > yContent) {
                                shouldSwitch = true;
                                break;
                            }
                        } else {
                            if (parseFloat(xContent) > parseFloat(yContent)) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                    } else if (dir == "desc") {
                        if (isNaN(parseFloat(xContent))) {
                            if (xContent < yContent) {
                                shouldSwitch = true;
                                break;
                            }
                        } else {
                            if (parseFloat(xContent) < parseFloat(yContent)) {
                                shouldSwitch = true;
                                break;
                            }
                        }
                    }
                }
            }
            if (shouldSwitch) {
                rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
                switching = true;
                switchcount++;
            } else {
                if (switchcount == 0 && dir == "asc") {
                    dir = "desc";
                    switching = true;
                }
            }
        }
        cambiarIconoFlecha(tabla, columna, dir);
    }

    function cambiarIconoFlecha(tabla, columna, dir) {
        var arrows = document.querySelectorAll('.' + tabla + ' .arrow');
        arrows.forEach(function (arrow) {
            arrow.innerHTML = '&#8597;';
        });
        var arrow = document.querySelector('.' + tabla + ' .arrow-' + columna);
        if (dir === 'asc') {
            arrow.innerHTML = '&#8593;';
        } else {
            arrow.innerHTML = '&#8595;';
        }
    }

    function agregarListenersTabla(tabla) {
        var ths = document.querySelectorAll('.' + tabla + ' th');
        ths.forEach(function (th, index) {
            th.addEventListener('click', function () {
                ordenarTabla(tabla, index);
            });
        });
    }

    // Agregar listeners para las tablas específicas
    agregarListenersTabla('table-victorias');
    agregarListenersTabla('table-derrotas');
    agregarListenersTabla('boardgame-statistic'); // Para la tabla de estadísticas del juego

});