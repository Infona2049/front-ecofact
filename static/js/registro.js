document.addEventListener("DOMContentLoaded", () => {
  const form = document.querySelector("form");
  const password = document.getElementById("password");
  const confirmPassword = document.getElementById("confirmPassword");
  const togglePassword = document.getElementById("togglePassword");
  const toggleConfirmPassword = document.getElementById("toggleConfirmPassword");

  // Mostrar / ocultar contraseña
  togglePassword.addEventListener("click", () => {
    const type = password.type === "password" ? "text" : "password";
    password.type = type;
  });

  toggleConfirmPassword.addEventListener("click", () => {
    const type = confirmPassword.type === "password" ? "text" : "password";
    confirmPassword.type = type;
  });

  // Validación del formulario
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    // Validar que las contraseñas coincidan
    if (password.value !== confirmPassword.value) {
      Swal.fire({
        icon: "error",
        title: "Contraseñas no coinciden",
        text: "Debes asegurarte de que ambas contraseñas sean iguales.",
      });
      return;
    }

    // Validar que el email tenga formato correcto
    const email = form.querySelector("input[type='email']").value;
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      Swal.fire({
        icon: "warning",
        title: "Correo inválido",
        text: "Por favor ingresa un correo electrónico válido.",
      });
      return;
    }

    // Validar teléfono (solo números y longitud)
    const telefono = form.querySelector("input[name='telefono_usuario']").value;
    if (!/^\d{7,15}$/.test(telefono)) {
      Swal.fire({
        icon: "warning",
        title: "Número de teléfono inválido",
        text: "El teléfono debe contener solo números (7 a 15 dígitos).",
      });
      return;
    }

    // Validar que se seleccione tipo de documento y rol
    const tipoDocumento = form.querySelector("select[name='tipo_documento_usuario']").value;
    const rol = form.querySelector("select[name='rol_usuario']").value;

    if (!tipoDocumento) {
      Swal.fire({
        icon: "info",
        title: "Selecciona un documento",
        text: "Debes elegir un tipo de documento.",
      });
      return;
    }

    if (!rol) {
      Swal.fire({
        icon: "info",
        title: "Selecciona un rol",
        text: "Debes elegir un rol antes de registrarte.",
      });
      return;
    }

    // Si todo está bien
    Swal.fire({
      icon: "success",
      title: "Registro exitoso",
      text: "Tu cuenta ha sido creada correctamente 🎉",
    }).then(() => {
      form.reset(); // limpia formulario después de éxito
    });
  });
});
