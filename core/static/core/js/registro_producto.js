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
document.addEventListener("DOMContentLoaded", () => {
  const categoriaSelect = document.getElementById("categoria");
  const modeloSelect = document.getElementById("modelo");
  const extrasMoviles = document.getElementById("extras-moviles");

  const labelModelo = document.querySelector('label[for="modelo"]');
  const labelColor = document.querySelector('label[for="color"]');
  const labelAlmacenamiento = document.querySelector('label[for="almacenamiento"]');
  const colorSelect = document.getElementById("color");
  const almacenamientoSelect = document.getElementById("almacenamiento");

  const iphones = [
    "iPhone 13","iPhone 13 Pro","iPhone 13 Pro Max",
    "iPhone 14","iPhone 14 Pro","iPhone 14 Pro Max",
    "iPhone 15","iPhone 15 Pro","iPhone 15 Pro Max",
    "iPhone 16","iPhone 16 Pro","iPhone 16 Pro Max"
  ];

  const cargadores = [
    "Cargador USB-C 20W",
    "Cargador USB-C 35W doble",
    "Cargador USB lightning"

  ];

const auriculares = [
  "AirPods 2.ª gen",
  "AirPods 3.ª gen",
  "AirPods 4",
  "AirPods Pro 2.ª gen",
  "AirPods Max",
  "EarPods con USB-C",
  "EarPods con Lightning"
];


  function limpiarModelos() {
    modeloSelect.innerHTML = '<option value="">Seleccione</option>';
  }

  function ocultarTodoExtras() {
    extrasMoviles.style.display = "none";
    if (labelModelo) labelModelo.style.display = "none";
    if (modeloSelect) modeloSelect.style.display = "none";
    if (labelColor) labelColor.style.display = "none";
    if (colorSelect) colorSelect.style.display = "none";
    if (labelAlmacenamiento) labelAlmacenamiento.style.display = "none";
    if (almacenamientoSelect) almacenamientoSelect.style.display = "none";
  }

  function mostrarSoloModelo() {
    extrasMoviles.style.display = "block";
    if (labelModelo) labelModelo.style.display = "block";
    if (modeloSelect) modeloSelect.style.display = "block";

    if (labelColor) labelColor.style.display = "none";
    if (colorSelect) colorSelect.style.display = "none";
    if (labelAlmacenamiento) labelAlmacenamiento.style.display = "none";
    if (almacenamientoSelect) almacenamientoSelect.style.display = "none";
  }

  function mostrarModeloColorAlmacenamiento() {
    extrasMoviles.style.display = "block";
    if (labelModelo) labelModelo.style.display = "block";
    if (modeloSelect) modeloSelect.style.display = "block";
    if (labelColor) labelColor.style.display = "block";
    if (colorSelect) colorSelect.style.display = "block";
    if (labelAlmacenamiento) labelAlmacenamiento.style.display = "block";
    if (almacenamientoSelect) almacenamientoSelect.style.display = "block";
  }

  function llenarOpciones(select, opciones) {
    limpiarModelos();
    opciones.forEach(txt => {
      const opt = document.createElement("option");
      opt.value = txt;
      opt.textContent = txt;
      select.appendChild(opt);
    });
  } 

  function mostrarOpciones() {
    const categoria = categoriaSelect.value;

    // Estado base
    ocultarTodoExtras();
    limpiarModelos();

    if (categoria === "moviles") {
      mostrarModeloColorAlmacenamiento();
      llenarOpciones(modeloSelect, iphones);
    } else if (categoria === "cargadores") {
      mostrarSoloModelo();
      llenarOpciones(modeloSelect, cargadores);
    } else if (categoria === "auriculares") {
      mostrarSoloModelo();
      llenarOpciones(modeloSelect, auriculares);
    }
  }

  categoriaSelect.addEventListener("change", mostrarOpciones);

  // Inicializar vista según valor actual (por si ya viene seleccionado)
  mostrarOpciones();
});
