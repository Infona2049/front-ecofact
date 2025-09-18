"""
URL configuration for EcoFactProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""

from django.contrib import admin 
from django.urls import path, include   # 👈 Importa include para conectar las apps
from django.views.generic import TemplateView  # 👈 Importa TemplateView

# Importaciones necesarias para servir archivos media en desarrollo
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # 👇 Aquí agregas las rutas a tus vistas (HTML) directas
    path('visualizacion_admin/', TemplateView.as_view(template_name="visualizacion_admin/login.html")),
    path('visualizacion_cliente/', TemplateView.as_view(template_name="visualizacion_cliente/login.html")),
    path('visualizacion_vendedor/', TemplateView.as_view(template_name="visualizacion_vendedor/login.html")),

    # 👇 Aquí incluyes las urls de tus apps para que sean modulares
    path('usuarios/', include('App_registroUsuario.urls')),   # Rutas de la app usuarios
    path('productos/', include('App_registroProducto.urls')), # Rutas de la app productos
]

# Esta línea añade las URLs para servir archivos media (imágenes) solo en modo DEBUG (desarrollo)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
