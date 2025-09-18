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
      "AirPods 2.ª gen",
      "AirPods 3.ª gen",
      "AirPods 4",
      "AirPods Pro 2.ª gen",
      "AirPods Max",
      "EarPods con USB-C",
      "EarPods con Lightning"
    ];

    auriculares.forEach(item => {
      let opt = document.createElement("option");
      opt.value = item;
      opt.textContent = item;
      productoSelect.appendChild(opt);
    });
  }
}

// --- AGREGAR PRODUCTO A LA TABLA ---
const btnAgregar = document.getElementById("btnAgregar");
const tablaProductosContainer = document.getElementById("tablaProductosContainer");
const tablaProductos = document.querySelector("#tablaProductos tbody");

let subtotalGeneral = 0;
let ivaGeneral = 0;
let totalGeneral = 0;

btnAgregar.addEventListener("click", () => {
  const categoria = document.getElementById("categoria").value;
  const producto = document.getElementById("producto").value;
  const almacenamiento = document.getElementById("almacenamiento").value;
  const color = document.getElementById("color").value;
  const cantidad = parseInt(document.getElementById("cantidad").value);
  const precio = parseFloat(document.getElementById("precio").value);

  if (!categoria || !producto || !cantidad || !precio) {
    alert("Por favor complete los datos del producto.");
    return;
  }

  // Nombre completo del producto
  let nombreProducto = producto;
  if (categoria === "moviles") {
    nombreProducto += ` - ${almacenamiento} GB - ${color}`;
  }

  // Calcular valores
  const subtotal = cantidad * precio;
  const iva = subtotal * 0.19;
  const total = subtotal + iva;

  // Mostrar contenedor de tabla
  tablaProductosContainer.style.display = "block";

  // Crear fila con icono eliminar
  const fila = document.createElement("tr");
  fila.innerHTML = `
    <td>${nombreProducto}</td>
    <td>${cantidad}</td>
    <td>$${precio.toFixed(2)}</td>
    <td>$${iva.toFixed(2)}</td>
    <td>$${total.toFixed(2)}</td>
    <td>
      <img src="img/eliminar.png" alt="Eliminar" class="iconoEliminar">
    </td>
  `;
  tablaProductos.appendChild(fila);

  // Actualizar totales generales
  subtotalGeneral += subtotal;
  ivaGeneral += iva;
  totalGeneral += total;

  document.getElementById("subtotal").textContent = subtotalGeneral.toFixed(2);
  document.getElementById("ivaTotal").textContent = ivaGeneral.toFixed(2);
  document.getElementById("granTotal").textContent = totalGeneral.toFixed(2);

  // Resetear campos de cantidad y precio
  document.getElementById("cantidad").value = "";
  document.getElementById("precio").value = "";

  // --- Eliminar producto ---
  fila.querySelector(".iconoEliminar").addEventListener("click", () => {
    subtotalGeneral -= subtotal;
    ivaGeneral -= iva;
    totalGeneral -= total;

    document.getElementById("subtotal").textContent = subtotalGeneral.toFixed(2);
    document.getElementById("ivaTotal").textContent = ivaGeneral.toFixed(2);
    document.getElementById("granTotal").textContent = totalGeneral.toFixed(2);

    fila.remove();

    if (tablaProductos.rows.length === 0) {
      tablaProductosContainer.style.display = "none";
    }
  });
});
