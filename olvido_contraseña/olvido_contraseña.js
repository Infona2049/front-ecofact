document.addEventListener("DOMContentLoaded", () => {
    const btnCancelar = document.querySelector(".cancelar");
    btnCancelar.addEventListener("click", () => {
        window.location.href = "login.html"; // Ajusta si tu archivo de login tiene otro nombre
    });
});


document.addEventListener("DOMContentLoaded", () => {
    const btnCancelar = document.querySelector(".cancelar");
    const btnSiguiente = document.querySelector(".siguiente");

    // Botón Cancelar → volver al login
    btnCancelar.addEventListener("click", () => {
        window.location.href = "login.html"; 
    });

    // Botón Siguiente → ir a pantalla de código de recuperación
    btnSiguiente.addEventListener("click", () => {
        window.location.href = "codigo_recuperacion.html"; 
    });
});
