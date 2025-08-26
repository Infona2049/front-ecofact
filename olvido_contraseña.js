document.addEventListener("DOMContentLoaded", () => {
    
    // Botón cancelar → redirige al login
    const btnCancelar = document.querySelector(".cancelar");
    if (btnCancelar) {
        btnCancelar.addEventListener("click", () => {
            window.location.href = "login.html"; // 👈 cambia si tu login tiene otro nombre
        });
    }

    // Botón aceptar → muestra mensaje de éxito
    const form = document.querySelector("form");
    if (form) {
        form.addEventListener("submit", (e) => {
            e.preventDefault(); // evita que recargue la página
            alert("✅ Código de seguridad enviado con éxito a su correo.");
        });
    }
});
