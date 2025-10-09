from django.http import HttpResponseRedirect
def eliminar_inventario_view(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    producto = inventario.producto
    if request.method == 'POST':
        inventario.delete()
        producto.delete()
        return redirect('inventario')
    # Si es GET, eliminar directamente y redirigir (sin confirmación extra)
    inventario.delete()
    producto.delete()
    return redirect('inventario')
from django.shortcuts import render, redirect
from .models import Inventario
from .forms import ProductoForm
from django.shortcuts import get_object_or_404
def editar_inventario_view(request, pk):
    inventario = get_object_or_404(Inventario, pk=pk)
    if request.method == 'POST':
        producto = inventario.producto
        producto.nombre_producto = request.POST.get('nombre_producto', producto.nombre_producto)
        producto.modelo_producto = request.POST.get('modelo_producto', producto.modelo_producto)
        producto.color_producto = request.POST.get('color_producto', producto.color_producto)
        producto.capacidad_producto = request.POST.get('capacidad_producto', producto.capacidad_producto)
        # Nuevo: actualizar precio
        precio = request.POST.get('precio_producto')
        if precio is not None and precio != '':
            try:
                producto.precio_producto = float(precio)
            except ValueError:
                pass
        producto.save()
        inventario.stock_actual_inventario = request.POST.get('stock_actual_inventario', inventario.stock_actual_inventario)
        inventario.stock_minimo_inventario = request.POST.get('stock_minimo_inventario', inventario.stock_minimo_inventario)
        inventario.save()
        return redirect('inventario')
    return redirect('inventario')
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
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            stock_actual = form.cleaned_data.get('stock_actual_inventario', 0)
            Inventario.objects.create(
                producto=producto,
                stock_actual_inventario=stock_actual,
                stock_minimo_inventario=1,
                codigo_barras_inventario=producto.codigo_barras_producto
            )
            return redirect(f"{reverse('registro_producto')}?exito=1")
    else:
        form = ProductoForm()
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