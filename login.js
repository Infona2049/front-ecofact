/* =========================================================
   LÓGICA DE INICIO DE SESIÓN
   - Si el correo contiene "@ecofact_sadmin"  -> super admin
   - Si el correo contiene "@ecofact_admin"   -> admin
   - En cualquier otro caso                   -> mostrar modal
========================================================= */

function mostrarModal(event) {
  event.preventDefault();                               // Cancela el submit real

  const email = event.target                             // <form> → input email
                 .querySelector('input[type="email"]')
                 .value
                 .trim()
                 .toLowerCase();

  // 1) Super Admin
  if (email.includes('@ecofactsadmin')) {
    window.location.href =
      'visualizacion_superAdmin/visualizacion_superAdmin.html';
    return;
  }

  // 2) Admin
  if (email.includes('@ecofactadmin')) {
    window.location.href =
      'visualizacion_admin/visualizacion_admin.html';
    return;
  }

  // 3) Usuario normal → elegir vendedor / cliente
  document.getElementById('modalRol').style.display = 'flex';
}



/* =========================================================
   SELECCIÓN DE ROL EN EL MODAL
========================================================= */
function seleccionarRol(rol) {
  const rutas = {
    vendedor: 'visualizacion_vendedor/visualizacion_vendedor.html',
    cliente : 'visualizacion_cliente/visualizacion_cliente.html'
  };

  const destino = rutas[rol];
  if (destino) {
    window.location.href = destino;
  } else {
    alert('Rol no reconocido');
  }
}
