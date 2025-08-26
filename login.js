/* =========================================================
   LÓGICA DE INICIO DE SESIÓN (con SweetAlert2)
========================================================= */
function login(event) {
  event.preventDefault(); // Cancela el submit real

  const email = event.target
                 .querySelector('input[type="email"]')
                 .value
                 .trim()
                 .toLowerCase();

  // 1) Admin
  if (email.includes('@ecofactadmin')) {
    Swal.fire({
      icon: 'success',
      title: 'Bienvenido Administrador',
      text: 'Redirigiendo a tu panel...',
      showConfirmButton: false,
      timer: 2000
    }).then(() => {
      window.location.href = 'visualizacion_admin/visualizacion_admin.html';
    });
    return;
  }

  // 2) Usuario normal
  Swal.fire({
    icon: 'info',
    title: 'Usuario normal',
    text: 'Redirección aún no definida',
    confirmButtonText: 'Entendido'
  });
}

/* =========================================================
   OJITO PARA MOSTRAR / OCULTAR CONTRASEÑA (FontAwesome)
========================================================= */
document.addEventListener("DOMContentLoaded", () => {
  const togglePassword = document.getElementById("togglePassword");
  const passwordInput = document.getElementById("password");

  if (togglePassword && passwordInput) {
    togglePassword.addEventListener("click", () => {
      const type = passwordInput.getAttribute("type") === "password" ? "text" : "password";
      passwordInput.setAttribute("type", type);

      // Cambiar el ícono con FontAwesome
      const icon = togglePassword.querySelector("i");
      if (type === "password") {
        icon.classList.remove("fa-eye-slash");
        icon.classList.add("fa-eye");
      } else {
        icon.classList.remove("fa-eye");
        icon.classList.add("fa-eye-slash");
      }
    });
  }
});
