// --- Espera a que el DOM esté listo --- 20/09/2025
document.addEventListener("DOMContentLoaded", function () { // evita que se ejecute el js sin que el html se cargue por completo
  console.log("JS cargado y DOM listo");

  // --- Dropdown del usuario ---
  const dropdownToggle = document.querySelector(".usuario"); // Botón o icono usuario
  const dropdownMenu = document.querySelector(".dropdown-usuario"); // Menú desplegable

  if (dropdownToggle && dropdownMenu) {
    dropdownToggle.addEventListener("click", () => {
      dropdownMenu.classList.toggle("visible");
    });

    window.addEventListener("click", function (e) {
      if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
        dropdownMenu.classList.remove("visible");
      }
    });
  }

  // --- Botón BUSCAR ---
  const botonBuscar = document.querySelector(".boton-buscar");
  if (botonBuscar) {
    botonBuscar.addEventListener("click", function () {
      console.log("👉 Botón BUSCAR presionado");

      const fechaInicial = document.getElementById("fecha-inicial").value;
      const fechaFinal = document.getElementById("fecha-final").value;

      if (fechaInicial && fechaFinal) {
        // Redirige con parámetros GET
        window.location.href = `/facturas/historial_factura/?fecha_inicial=${fechaInicial}&fecha_final=${fechaFinal}`;
      } else {
        alert("Selecciona las dos fechas antes de buscar.");
      }
    });
  } else {
    console.log(" No encontré el botón .boton-buscar en el DOM");
  }
});
