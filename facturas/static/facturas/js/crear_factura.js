// --- Configuración inicial ---
let consecutivoFactura = 1000;
let subtotalGeneral = 0;
let ivaGeneral = 0;
let totalGeneral = 0;

// --- Datos de productos  ---
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

  Object.values(contenedores).forEach(container => {
    if (container) container.style.display = "none";
  });

  if (categoria && PRODUCTOS[categoria]) {
    if (contenedores.producto) contenedores.producto.style.display = "block";
    if (categoria === "moviles") {
      if (contenedores.almacenamiento) contenedores.almacenamiento.style.display = "block";
      if (contenedores.color) contenedores.color.style.display = "block";
    }
  }
}

// --- Dropdown usuario  ---
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

// --- Manejo de productos ---
function mostrarOpciones() {
  const categoriaSelect = document.getElementById("categoria");
  const productoSelect = document.getElementById("producto");
  if (!categoriaSelect || !productoSelect) return;

  const categoria = categoriaSelect.value;
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

  if (!datos.categoria || !datos.producto || datos.cantidad <= 0 || datos.precio <= 0) {
    alert("Por favor complete correctamente todos los datos del producto.");
    return;
  }

  let nombreProducto = datos.producto;
  if (datos.categoria === "moviles" && datos.almacenamiento && datos.color) {
    nombreProducto += ` - ${datos.almacenamiento} GB - ${datos.color}`;
  }

  const subtotal = datos.cantidad * datos.precio;
  const iva = subtotal * 0.19;
  const total = subtotal + iva;

  const tablaProductosContainer = document.getElementById("tablaProductosContainer");
  const tablaProductos = document.querySelector("#tablaProductos tbody");
  if (!tablaProductosContainer || !tablaProductos) {
    console.error("No se encontró la tabla de productos");
    return;
  }

  tablaProductosContainer.style.display = "block";

  const fila = document.createElement("tr");

  fila.dataset.precio = datos.precio;
  fila.dataset.iva = iva;
  fila.dataset.total = total;
  fila.dataset.subtotal = subtotal;

  fila.innerHTML = `
    <td style="text-align:left;">${nombreProducto}</td>
    <td>${datos.cantidad}</td>
    <td>$${formatearMoneda(datos.precio)} COP</td>
    <td>$${formatearMoneda(iva)} COP</td>
    <td>$${formatearMoneda(total)} COP</td>
    <td>
      <button type="button" class="btn-eliminar" aria-label="Eliminar producto">
        <img src="/static/facturas/img/eliminar.png" alt="Eliminar" class="iconoEliminar">
      </button>
    </td>
  `;

  const btnEliminar = fila.querySelector(".btn-eliminar");
  btnEliminar.addEventListener("click", () => {
    eliminarProducto(fila, subtotal, iva, total);
  });

  tablaProductos.appendChild(fila);

  subtotalGeneral += subtotal;
  ivaGeneral += iva;
  totalGeneral += total;
  actualizarTotales();

  limpiarFormulario();
}

// --- CSRF helper ---
function getCSRFToken() {
  const cookie = document.cookie.split("; ").find(row => row.startsWith("csrftoken="));
  if (cookie) return cookie.split("=")[1];
  const el = document.querySelector('[name=csrfmiddlewaretoken]');
  if (el) return el.value;
  return "";
}

// --- Construir items desde la tabla ---
function construirItemsDesdeTabla() {
  const tablaBody = document.querySelector("#tablaProductos tbody");
  const items = [];
  if (!tablaBody) return items;
  for (const fila of tablaBody.rows) {
    const producto = fila.cells[0].textContent.trim();
    const cantidad = parseInt(fila.cells[1].textContent.trim()) || 0;
    const precio = parseFloat(fila.dataset.precio) || 0;
    const iva = parseFloat(fila.dataset.iva) || 0;
    const total = parseFloat(fila.dataset.total) || 0;
    items.push({ producto, cantidad, precio, iva, total });
  }
  return items;
}

// --- Generar factura (envío al backend) ---
function generarFactura() {
  const emisor = document.getElementById("nombreCliente")?.value?.trim();
  const correo = document.getElementById("correoCliente")?.value?.trim();
  const tablaProductos = document.querySelector("#tablaProductos tbody");

  if (!emisor || !correo) {
    alert("Debe llenar los datos del cliente.");
    return;
  }

  if (!tablaProductos || tablaProductos.rows.length === 0) {
    alert("Debe agregar al menos un producto.");
    return;
  }

  //revisar estos campos para que no de los diferentes medios de pago e igua que los id de los clientes 
  const items = construirItemsDesdeTabla();

    const data = {
      metodo_pago_factura: "Efectivo",
      subtotal: subtotalGeneral,
      iva: ivaGeneral,
      total: totalGeneral,
      cliente_id: 1  // o el id real del cliente
    };

  fetch("/facturas/crear/", {
  method: "POST",
  headers: {
    "Content-Type": "application/json",
    "X-CSRFToken": getCSRFToken()
  },
  body: JSON.stringify(data),
})
  .then(response => response.json())
  .then(result => {
    if (result.status === "ok") {
      consecutivoFactura++;
      alert(`Factura enviada con éxito. CUFE: ${result.cufe}`);
      // opcional: redirigir a página de éxito
      window.location.href = "/facturas/exitosa/";
    } else {
      alert("Error al generar la factura");
    }
  })
  .catch(error => {
    console.error("Error al generar factura:", error);
    alert("Ocurrió un error al generar la factura.");
  });
}

// --- Inicialización ---
document.addEventListener("DOMContentLoaded", () => {
  inicializarDropdown();

  const categoriaSelect = document.getElementById("categoria");
  if (categoriaSelect) categoriaSelect.addEventListener("change", mostrarOpciones);

  const btnAgregar = document.getElementById("btnAgregar");
  if (btnAgregar) btnAgregar.addEventListener("click", agregarProductoATabla);

  const btnGenerarFactura = document.getElementById("btnGenerarFactura");
  if (btnGenerarFactura) btnGenerarFactura.addEventListener("click", generarFactura);

  mostrarOpciones();
});