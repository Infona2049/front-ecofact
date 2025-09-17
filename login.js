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
  if (email.includes('@ecofactadmin.com')) {
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
    icon: 'warning',
    title: 'Aceptar Términos y Condiciones',
    text: 'Por favor, acepta los términos y condiciones para continuar.',
    showCancelButton: true,
    confirmButtonText: 'Aceptar',
    cancelButtonText: 'Cancelar'
  }).then((result) => {
    if (result.isConfirmed) {
      // Aquí puedes redirigir al usuario o realizar otra acción
      Swal.fire({
        icon: 'success',
        title: 'Gracias',
        text: 'Has aceptado los términos y condiciones.',
        confirmButtonText: 'Continuar'
      });
      // Redirigir o realizar otra acción aquí
    } else {
      Swal.fire({
        icon: 'info',
        title: 'Cancelado',
        text: 'No has aceptado los términos y condiciones.',
        confirmButtonText: 'Entendido'
      });
    }
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
