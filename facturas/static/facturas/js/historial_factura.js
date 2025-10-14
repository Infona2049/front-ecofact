// --- Espera a que el DOM esté listo --- 20/09/2025
document.addEventListener("DOMContentLoaded", function () {
  console.log("✅ JS cargado y DOM listo");

  // --- Botón BUSCAR ---
  const botonBuscar = document.querySelector(".boton-buscar");
  const botonLimpiar = document.querySelector(".boton-limpiar");
  const fechaInicialInput = document.getElementById("fecha-inicial");
  const fechaFinalInput = document.getElementById("fecha-final");

  if (botonBuscar) {
    botonBuscar.addEventListener("click", function () {
      console.log("🔍 Botón BUSCAR presionado");

      const fechaInicial = fechaInicialInput.value;
      const fechaFinal = fechaFinalInput.value;

      if (fechaInicial && fechaFinal) {
        // Redirige con parámetros GET (recarga la página mostrando las facturas filtradas)
        window.location.href = `/facturas/historial_factura/?fecha_inicial=${fechaInicial}&fecha_final=${fechaFinal}`;
      } else {
        alert("Selecciona las dos fechas antes de buscar.");
      }
    });
  } else {
    console.log(" No encontré el botón .boton-buscar en el DOM");
  }

  // --- Botón LIMPIAR ---
  if (botonLimpiar) {
    botonLimpiar.addEventListener("click", function () {
      console.log("🧹 Botón LIMPIAR presionado");

      // Limpia los campos de fecha
      fechaInicialInput.value = "";
      fechaFinalInput.value = "";

      // Redirige al historial sin filtros (vuelve a mostrar todas las facturas)
      window.location.href = `/facturas/historial_factura/`;
    });
  } else {
    console.log("No encontré el botón .boton-limpiar en el DOM");
  }
});
