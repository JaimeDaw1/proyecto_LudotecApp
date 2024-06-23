// Función para ordenar los checkboxes de mecánicas y temáticas
document.addEventListener("DOMContentLoaded", function() {
    const ordenarCheckboxes = (field) => {
        const container = document.querySelector(`.columnas-checkboxes[data-field="${field}"]`);
        if (container) {
            const checkboxes = Array.from(container.querySelectorAll('.form-check')).sort((a, b) => {
                const labelA = a.querySelector('label').textContent.trim();
                const labelB = b.querySelector('label').textContent.trim();
                return labelA.localeCompare(labelB);
            });
            container.innerHTML = '';
            checkboxes.forEach(checkbox => container.appendChild(checkbox));
        }
    };

    ordenarCheckboxes('mecanicas');
    ordenarCheckboxes('tematicas');
});

// Resto del código fuera de DOMContentLoaded para el ordenamiento de la tabla
function ordenarTabla(columna) {
    var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
    table = document.querySelector('.custom-table');
    switching = true;
    dir = "asc";

    while (switching) {
        switching = false;
        rows = table.rows;

        for (i = 1; i < (rows.length - 1); i++) {
            shouldSwitch = false;
            x = rows[i].getElementsByTagName("td")[columna];
            y = rows[i + 1].getElementsByTagName("td")[columna];

            let xContent = x.textContent.toLowerCase().trim();
            let yContent = y.textContent.toLowerCase().trim();

            if (columna === 6) {  // El índice de la columna de "Precio", ajustar si es necesario
                xContent = parseFloat(xContent.replace(/[^0-9,.-]/g, "").replace(",", "."));
                yContent = parseFloat(yContent.replace(/[^0-9,.-]/g, "").replace(",", "."));
            }

            if (dir === "asc") {
                if (xContent > yContent) {
                    shouldSwitch = true;
                    break;
                }
            } else if (dir === "desc") {
                if (xContent < yContent) {
                    shouldSwitch = true;
                    break;
                }
            }
        }

        if (shouldSwitch) {
            rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
            switching = true;
            switchcount++;
        } else {
            if (switchcount === 0 && dir === "asc") {
                dir = "desc";
                switching = true;
            }
        }
    }

    cambiarIconoFlecha(columna, dir);
}

function cambiarIconoFlecha(columna, dir) {
    var arrows = document.querySelectorAll('.arrow');
    arrows.forEach(function(arrow) {
        arrow.innerHTML = '&#8597;';
    });
    var arrow = document.querySelector('.arrow-' + columna);
    if (dir === 'asc') {
        arrow.innerHTML = '&#8593;';
    } else {
        arrow.innerHTML = '&#8595;';
    }
}

var mecanicaDetails = document.querySelector('[name="filtrar_por_mecanica"]');
var mecanicaFieldset = mecanicaDetails.parentNode.querySelector('fieldset');
mecanicaDetails.addEventListener('toggle', function() {
    if (mecanicaDetails.open) {
        mecanicaFieldset.style.display = 'block';
    } else {
        mecanicaFieldset.style.display = 'none';
    }
});