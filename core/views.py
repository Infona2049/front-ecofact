from django.shortcuts import render, redirect
from .models import Inventario
from .forms import ProductoForm

def login_view(request):
    return render(request, 'core/login.html')

def documentos_view(request):
    return render(request, 'core/documentos.html')

def actualizar_perfil_view(request):
    return render(request, 'core/actualizar_perfil.html')

def cambiocontraseña_view(request):
    return render(request, 'core/olvido_contraseña.html')

def acerca_nosotros_view(request):
    return render(request, 'core/acerca_nosotros.html')

def registro_producto_view(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            producto = form.save()
            # Crear inventario automáticamente
            Inventario.objects.create(
                producto=producto,
                stock_actual_inventario=0,
                stock_minimo_inventario=1,
                codigo_barras_inventario=producto.codigo_barras_producto
            )
            mensaje_exito = True
            form = ProductoForm()  # Limpiar el formulario después de guardar
    else:
        form = ProductoForm()
    return render(request, 'core/registro_producto.html', {'form': form})

def inventario_view(request):
    inventarios = Inventario.objects.select_related('producto').order_by('fecha_actualizacion_inventario')
    return render(request, 'core/inventario.html', {'inventarios': inventarios})

def historial_factura_view(request):
    return render(request, 'core/historial_factura.html')

def crear_factura_view(request):
    return render(request, 'core/crear_factura.html')

def login_view(request):
    return render(request, 'core/login.html')

def olvido_contraseña_view(request):
    return render(request, 'core/olvido_contraseña.html')

def registro_view(request):
    return render(request, 'core/registro.html')

def visualizacion_admin_view(request):
    return render(request, 'core/visualizacion_Admin.html')

def visualizacion_cliente_view(request):
    return render(request, 'core/visualizacion_Cliente.html')

def visualizacion_vendedor_view(request):
    return render(request, 'core/visualizacion_Vendedor.html')