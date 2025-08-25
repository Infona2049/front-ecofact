// --- Dropdown usuario (solo si existe en el HTML) ---
const dropdownToggle = document.querySelector(".usuario");
const dropdownMenu = document.querySelector(".dropdown-usuario");

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

// --- Lógica dinámica de productos ---
document.getElementById("categoria").addEventListener("change", mostrarOpciones);

function mostrarOpciones() {
  const categoria = document.getElementById("categoria").value;
  const productoSelect = document.getElementById("producto");
  const productoContainer = document.getElementById("producto-container");
  const almacenamientoContainer = document.getElementById("almacenamiento-container");
  const colorContainer = document.getElementById("color-container");

  // Limpiar y ocultar por defecto
  productoSelect.innerHTML = "";
  productoContainer.style.display = "none";
  almacenamientoContainer.style.display = "none";
  colorContainer.style.display = "none";

  if (categoria === "moviles") {
    // Mostrar producto, almacenamiento y color solo si es móvil
    productoContainer.style.display = "block";
    almacenamientoContainer.style.display = "block";
    colorContainer.style.display = "block";

    const iphones = [
      "iPhone 13","iPhone 13 Pro","iPhone 13 Pro Max",
      "iPhone 14","iPhone 14 Pro","iPhone 14 Pro Max",
      "iPhone 15","iPhone 15 Pro","iPhone 15 Pro Max",
      "iPhone 16","iPhone 16 Pro","iPhone 16 Pro Max"
    ];

    iphones.forEach(modelo => {
      let opt = document.createElement("option");
      opt.value = modelo;
      opt.textContent = modelo;
      productoSelect.appendChild(opt);
    });

  } else if (categoria === "cargadores") {
    productoContainer.style.display = "block";

    const cargadores = [
      "Cargador USB-C 20W",
      "Cargador MagSafe",
      "Cargador MagSafe Duo",
      "Cargador USB-C 35W doble"
    ];

    cargadores.forEach(item => {
      let opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      productoSelect.appendChild(opt);
    });

  } else if (categoria === "auriculares") {
    productoContainer.style.display = "block";
 
    const auriculares = [
      "AirPods (2ª generación)",
      "AirPods (3ª generación)",
      "AirPods Pro (2ª generación)",
      "AirPods Max"
    ];

    auriculares.forEach(item => {
      let opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      productoSelect.appendChild(opt);
    });
  }
}
