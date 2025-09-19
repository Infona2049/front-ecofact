from django.shortcuts import render, redirect
from .models import Inventario
from .forms import ProductoForm
from django.urls import reverse

def registro_producto_view(request):
    exito = request.GET.get('exito')
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            Inventario.objects.create(
                producto=producto,
                stock_actual_inventario=0,
                stock_minimo_inventario=1,
                codigo_barras_inventario=producto.codigo_barras_producto
            )
            return redirect(f"{reverse('registro_producto')}?exito=1")
    else:
        form = ProductoForm()
    return render(request, 'productos/registro_producto.html', {'form': form, 'exito': exito})


def inventario_view(request):
    inventarios = Inventario.objects.select_related('producto').order_by('fecha_actualizacion_inventario')
    return render(request, 'productos/inventario.html', {'inventarios': inventarios}) 