// --- Configuración inicial ---
let consecutivoFactura = 1000;
let subtotalGeneral = 0;
let ivaGeneral = 0;
let totalGeneral = 0;

// --- Datos de productos ---
const PRODUCTOS = {
  moviles: [
    "iPhone 13", "iPhone 13 Pro", "iPhone 13 Pro Max",
    "iPhone 14", "iPhone 14 Pro", "iPhone 14 Pro Max",
    "iPhone 15", "iPhone 15 Pro", "iPhone 15 Pro Max",
    "iPhone 16", "iPhone 16 Pro", "iPhone 16 Pro Max"
  ],
  cargadores: [
    "Cargador USB-C 20W",
    "Cargador MagSafe Duo",
    "Cargador USB-C 35W doble"
  ],
  auriculares: [
    "AirPods 2.ª gen",
    "AirPods 3.ª gen",
    "AirPods 4",
    "AirPods Pro 2.ª gen",
    "AirPods Max",
    "EarPods con USB-C",
    "EarPods con Lightning"
  ]
};

// --- Utilidades ---
function formatearMoneda(valor) {
  return valor.toLocaleString("es-CO", { minimumFractionDigits: 2 });
}

function actualizarTotales() {
  document.getElementById("subtotal").textContent = formatearMoneda(subtotalGeneral);
  document.getElementById("ivaTotal").textContent = formatearMoneda(ivaGeneral);
  document.getElementById("granTotal").textContent = formatearMoneda(totalGeneral);
}

function limpiarFormulario() {
  document.getElementById("cantidad").value = "";
  document.getElementById("precio").value = "";
}

function mostrarOcultarContenedores(categoria) {
  const contenedores = {
    producto: document.getElementById("producto-container"),
    almacenamiento: document.getElementById("almacenamiento-container"),
    color: document.getElementById("color-container")
  };

  // Ocultar todos por defecto
  Object.values(contenedores).forEach(container => {
    if (container) container.style.display = "none";
  });

  // Mostrar según categoría
  if (categoria && PRODUCTOS[categoria]) {
    if (contenedores.producto) contenedores.producto.style.display = "block";
    
    if (categoria === "moviles") {
      if (contenedores.almacenamiento) contenedores.almacenamiento.style.display = "block";
      if (contenedores.color) contenedores.color.style.display = "block";
    }
  }
}

// --- Dropdown usuario ---
function inicializarDropdown() {
  const dropdownToggle = document.querySelector(".usuario");
  const dropdownMenu = document.querySelector(".dropdown-usuario");

  if (!dropdownToggle || !dropdownMenu) return;

  dropdownToggle.addEventListener("click", (e) => {
    e.stopPropagation();
    dropdownMenu.classList.toggle("visible");
  });

  document.addEventListener("click", (e) => {
    if (!dropdownToggle.contains(e.target) && !dropdownMenu.contains(e.target)) {
      dropdownMenu.classList.remove("visible");
    }
  });
}

// --- Lógica de productos ---
function mostrarOpciones() {
  const categoriaSelect = document.getElementById("categoria");
  const productoSelect = document.getElementById("producto");
  
  if (!categoriaSelect || !productoSelect) return;

  const categoria = categoriaSelect.value;
  
  // Limpiar opciones anteriores
  productoSelect.innerHTML = '<option value="">Seleccione un producto</option>';
  
  mostrarOcultarContenedores(categoria);

  if (categoria && PRODUCTOS[categoria]) {
    const fragment = document.createDocumentFragment();
    
    PRODUCTOS[categoria].forEach(item => {
      const option = document.createElement("option");
      option.value = item;
      option.textContent = item;
      fragment.appendChild(option);
    });
    
    productoSelect.appendChild(fragment);
  }
}

// --- Manejo de tabla de productos ---
function eliminarProducto(fila, subtotal, iva, total) {
  subtotalGeneral -= subtotal;
  ivaGeneral -= iva;
  totalGeneral -= total;

  actualizarTotales();
  fila.remove();

  const tablaProductos = document.querySelector("#tablaProductos tbody");
  const tablaProductosContainer = document.getElementById("tablaProductosContainer");
  
  if (tablaProductos && tablaProductos.rows.length === 0 && tablaProductosContainer) {
    tablaProductosContainer.style.display = "none";
  }
}

function agregarProductoATabla() {
  const elementos = {
    categoria: document.getElementById("categoria"),
    producto: document.getElementById("producto"),
    almacenamiento: document.getElementById("almacenamiento"),
    color: document.getElementById("color"),
    cantidad: document.getElementById("cantidad"),
    precio: document.getElementById("precio")
  };

  // Verificar que los elementos existan
  if (!elementos.categoria || !elementos.producto || !elementos.cantidad || !elementos.precio) {
    console.error("Faltan elementos del formulario");
    return;
  }

  const datos = {
    categoria: elementos.categoria.value,
    producto: elementos.producto.value,
    almacenamiento: elementos.almacenamiento?.value || "",
    color: elementos.color?.value || "",
    cantidad: parseInt(elementos.cantidad.value) || 0,
    precio: parseFloat(elementos.precio.value) || 0
  };

  // Validaciones
  if (!datos.categoria || !datos.producto || datos.cantidad <= 0 || datos.precio <= 0) {
    alert("Por favor complete correctamente todos los datos del producto.");
    return;
  }

  // Construir nombre del producto
  let nombreProducto = datos.producto;
  if (datos.categoria === "moviles" && datos.almacenamiento && datos.color) {
    nombreProducto += ` - ${datos.almacenamiento} GB - ${datos.color}`;
  }

  // Cálculos
  const subtotal = datos.cantidad * datos.precio;
  const iva = subtotal * 0.19;
  const total = subtotal + iva;

  // Mostrar tabla y agregar fila
  const tablaProductosContainer = document.getElementById("tablaProductosContainer");
  const tablaProductos = document.querySelector("#tablaProductos tbody");
  
  if (!tablaProductosContainer || !tablaProductos) {
    console.error("No se encontró la tabla de productos");
    return;
  }

  tablaProductosContainer.style.display = "block";

  const fila = document.createElement("tr");
  fila.innerHTML = `
    <td>${nombreProducto}</td>
    <td>${datos.cantidad}</td>
    <td>$${formatearMoneda(datos.precio)} COP</td>
    <td>$${formatearMoneda(iva)} COP</td>
    <td>$${formatearMoneda(total)} COP</td>
    <td>
      <button type="button" class="btn-eliminar" aria-label="Eliminar producto">
        <img src="/img/eliminar.png" alt="Eliminar" class="iconoEliminar">
      </button>
    </td>
  `;

  // Agregar evento de eliminación
  const btnEliminar = fila.querySelector(".btn-eliminar");
  btnEliminar.addEventListener("click", () => {
    eliminarProducto(fila, subtotal, iva, total);
  });

  tablaProductos.appendChild(fila);

  // Actualizar totales
  subtotalGeneral += subtotal;
  ivaGeneral += iva;
  totalGeneral += total;
  actualizarTotales();

  // Limpiar formulario
  limpiarFormulario();
}

// --- Generar factura ---
function generarFactura() {
  const emisor = document.getElementById("emisor")?.value?.trim();
  const receptor = document.getElementById("receptor")?.value?.trim();
  const tablaProductos = document.querySelector("#tablaProductos tbody");

  if (!emisor || !receptor) {
    alert("Debe llenar los datos del emisor y receptor de la factura.");
    return;
  }

  if (!tablaProductos || tablaProductos.rows.length === 0) {
    alert("Debe agregar al menos un producto.");
    return;
  }

  consecutivoFactura++;
  const fecha = new Date().toLocaleString("es-CO", {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  });

  const mensaje = `Factura generada exitosamente

Número: FAC-${consecutivoFactura}
Fecha: ${fecha}
Emisor: ${emisor}
Receptor: ${receptor}
Total: $${formatearMoneda(totalGeneral)} COP`;

  alert(mensaje);
}

// --- Inicialización ---
document.addEventListener("DOMContentLoaded", () => {
  // Inicializar dropdown
  inicializarDropdown();

  // Event listeners
  const categoriaSelect = document.getElementById("categoria");
  if (categoriaSelect) {
    categoriaSelect.addEventListener("change", mostrarOpciones);
  }

  const btnAgregar = document.getElementById("btnAgregar");
  if (btnAgregar) {
    btnAgregar.addEventListener("click", agregarProductoATabla);
  }

  const btnGenerarFactura = document.getElementById("btnGenerarFactura");
  if (btnGenerarFactura) {
    btnGenerarFactura.addEventListener("click", generarFactura);
  }

  // Inicializar estado
  mostrarOpciones();
});
