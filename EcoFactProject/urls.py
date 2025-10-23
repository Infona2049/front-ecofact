from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect
from core import views  # importar vistas principales

def redirect_to_login(request):
    return redirect('login')

urlpatterns = [
    path('', redirect_to_login, name='home'),
    path('admin/', admin.site.urls),

    # Auth
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Dashboards
    path('visualizacion_admin/', views.visualizacion_admin_view, name='visualizacion_admin'),
    path('visualizacion_vendedor/', views.visualizacion_vendedor_view, name='visualizacion_vendedor'),
    path('visualizacion_cliente/', views.visualizacion_cliente_view, name='visualizacion_cliente'),

    # Perfil y otras vistas
    path('actualizar_perfil/', views.actualizar_perfil_view, name='actualizar_perfil'),
    path('cambiocontraseña/', views.cambiocontraseña_view, name='cambiocontraseña'),
    path('olvido_contraseña/', views.olvido_contraseña_view, name='olvido_contraseña'),
    path('registro/', views.registro_view, name='registro'),

    path('acerca_nosotros/', views.acerca_nosotros_view, name='acerca_nosotros'),
    path('historial_factura/', views.historial_factura_view, name='historial_factura'),
    path('documentos/', views.documentos_view, name='documentos'),

    # Apps
    path('productos/', include('productos.urls')),
    path('facturas/', include('facturas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else settings.STATIC_ROOT)