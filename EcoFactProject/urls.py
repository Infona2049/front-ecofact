from django.contrib import admin
from django.urls import path
from core import views 
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('documentos/', views.documentos_view, name='documentos'),
    path('actualizar_perfil/', views.actualizar_perfil_view, name='actualizar_perfil'),
    path('cambiocontraseña/', views.cambiocontraseña_view, name='cambiocontraseña'),
    path('acerca_nosotros/', views.acerca_nosotros_view, name='acerca_nosotros'),
    path('registro_producto/', views.registro_producto_view, name='registro_producto'),
    path('inventario/', views.inventario_view, name='inventario'),
    path('historial_factura/', views.historial_factura_view, name='historial_factura'),
    path('crear_factura/', views.crear_factura_view, name='crear_factura'),
    path('login/', views.login_view, name='login'),
    path('olvido_contraseña/', views.olvido_contraseña_view, name='olvido_contraseña'),
    path('registro/', views.registro_view, name='registro'),
    path('visualizacion_admin/', views.visualizacion_admin_view, name='visualizacion_admin'),
    path('visualizacion_cliente/', views.visualizacion_cliente_view, name='visualizacion_cliente'),
    path('visualizacion_vendedor/', views.visualizacion_vendedor_view, name='visualizacion_vendedor'),
    # Agrega aquí las demás rutas que necesites
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)