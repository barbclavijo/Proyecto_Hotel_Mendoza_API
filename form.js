function validar() {
    if (document.formulario.nombre.value.length <= 2) {
        alert("Completa tu nombre");
        document.formulario.nombre.focus();
        return;
    }

    if (document.formulario.apellido.value.length <= 2) {
        alert("Completa tu apellido");
        document.formulario.apellido.focus();
        return;
    }


    if (document.formulario.correo.value == "" || !(/^\w+([.-_+]?\w+)*@\w+([.-]?\w+)*(\.\w{2,10})+$/.test(document.formulario.correo.value))) {
        alert("Completa un correo electrónico válido");
        document.formulario.correo.focus();
        return;
    }


    if (document.formulario.telefono.value == "" || !(/^\d{7,10}$/.test(document.formulario.telefono.value))) {
        alert("Completa tu teléfono");
        document.formulario.telefono.focus();
        return;
    }

    if (document.formulario.dateIngreso.value < "2000-01-01" || document.formulario.dateEgreso.value < "2000-01-01") {
        alert("Completa una fecha");
        document.formulario.dateIngreso.focus();
        return;
        
    } else if (document.formulario.dateIngreso.value > document.formulario.dateEgreso.value) {
        alert("La fecha de ingreso no puede ser posterior a la de egreso.");
        document.formulario.dateEgreso.focus();
        return;
    }


    if (document.formulario.select.selectedIndex == 0) {
        alert("Completa una opción");
        document.formulario.select.focus();
        return;
    }

    if (formulario.comentario.value == '') {
        alert("Completá el campo comentarios");
        document.formulario.select.focus();
        return;

    }

    alert("Su formulario fue enviado");
    document.formulario.submit();

}



