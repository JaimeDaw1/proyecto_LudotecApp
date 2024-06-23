// Configuración para el campo "duracion"
flatpickr("#id_duracion", {
    enableTime: true,
    noCalendar: true,
    dateFormat: "H:i",
    time_24hr: true,
    maxTime: "08:00"
});

document.addEventListener("DOMContentLoaded", function() {
    const camposObligatorios = document.querySelectorAll('[required]');
    //Se añade un asterisco en los campos que son obligatorios.
    //Cuando el usuario escribe algo en uno de esos campos, desaparece el asterisco, y si lo vuelve a dejar vacío vuelve a aparecer
    if (camposObligatorios) {
        camposObligatorios.forEach(function(campo) {
            if (campo.previousElementSibling) {
                campo.previousElementSibling.innerHTML = campo.previousElementSibling.textContent.replace('*', '');
                if (!campo.value.trim()) {
                    campo.previousElementSibling.innerHTML = campo.previousElementSibling.textContent.replace('*', '') + ' *';
                }
                campo.addEventListener('input', function() {
                    if (campo.value.trim()) {
                        campo.previousElementSibling.innerHTML = campo.previousElementSibling.textContent.replace('*', '');
                    } else {
                        campo.previousElementSibling.innerHTML = campo.previousElementSibling.textContent.replace('*', '') + ' *';
                    }
                });
            }
        });
    }

    // Se ordenan alfabéticamente el listado de mecánicas y temáticas que ya hay
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

    // Se agrega la nueva mecánica si el usuario introdujo una manualmente
    document.getElementById("agregar_mecanica").addEventListener("click", function(event) {
        event.preventDefault();
        const mecanicaInput = document.getElementById("id_nueva_mecanica");
        const nuevaMecanica = mecanicaInput.value.trim();
        if (nuevaMecanica !== "") {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "nuevas_mecanicas";
            input.value = nuevaMecanica;
            document.querySelector("form").appendChild(input);
            mecanicaInput.value = '';
        }
    });

    // Se agrega nueva temática si el usuario introdujo una manualmente
    document.getElementById("agregar_tematica").addEventListener("click", function(event) {
        event.preventDefault();
        const tematicaInput = document.getElementById("id_nueva_tematica");
        const nuevaTematica = tematicaInput.value.trim();
        if (nuevaTematica !== "") {
            const input = document.createElement("input");
            input.type = "hidden";
            input.name = "nuevas_tematicas";
            input.value = nuevaTematica;
            document.querySelector("form").appendChild(input);
            tematicaInput.value = '';
        }
    });
});