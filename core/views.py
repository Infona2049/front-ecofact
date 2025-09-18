from django.shortcuts import render
from .models import Inventario

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
    return render(request, 'core/registro_producto.html')

def inventario_view(request):
    return render(request, 'core/inventario.html')

def inventario_view(request):
    inventarios = Inventario.objects.select_related('producto').all()
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