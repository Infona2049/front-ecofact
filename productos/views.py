from django.shortcuts import render, redirect
from .models import Inventario
from .forms import ProductoForm
from django.urls import reverse

def registro_producto_view(request):
    """
    Vista para registrar un nuevo producto.

    - Si la petición es POST, procesa el formulario enviado.
    - Si el formulario es válido, guarda el producto y crea un registro inicial en Inventario con stock 0 y stock mínimo 1.
    - Luego redirige a la misma página con un parámetro GET 'exito=1' para mostrar mensaje de éxito.
    - Si la petición no es POST, muestra un formulario vacío para registrar un producto.
    """
    exito = request.GET.get('exito')  # Captura el parámetro para mostrar mensaje de éxito
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)  # Crea el formulario con datos enviados y archivos
        if form.is_valid():
            producto = form.save()  # Guarda el nuevo producto en la base de datos
            # Crea un registro en Inventario asociado al producto recién creado
            Inventario.objects.create(
                producto=producto,
                stock_actual_inventario=0,  # Stock inicial en 0
                stock_minimo_inventario=1,  # Stock mínimo por defecto en 1
                codigo_barras_inventario=producto.codigo_barras_producto  # Código de barras igual al del producto
            )
            # Redirige a la misma vista con parámetro para mostrar alerta de éxito
            return redirect(f"{reverse('registro_producto')}?exito=1")
    else:
        form = ProductoForm()  # Formulario vacío para GET
    # Renderiza la plantilla con el formulario y la variable 'exito' para mostrar alertas
    return render(request, 'productos/registro_producto.html', {'form': form, 'exito': exito})


def inventario_view(request):
    """
    Vista para mostrar el inventario de productos.

    - Obtiene todos los registros de Inventario ordenados por fecha de actualización.
    - Usa select_related para optimizar la consulta y traer los datos relacionados del producto.
    - Renderiza la plantilla con la lista de inventarios.
    """
    inventarios = Inventario.objects.select_related('producto').order_by('fecha_actualizacion_inventario')
    return render(request, 'productos/inventario.html', {'inventarios': inventarios})