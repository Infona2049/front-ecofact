"""
URL configuration for App_registroUsuario app.

Aquí defines las rutas específicas de la app de usuarios.
"""

from django.urls import path
from . import views  # 👈 Importa tus vistas de la app

urlpatterns = [
    # 👇 Ejemplos de rutas para usuarios
    path('login/', views.login_usuario, name='login_usuario'),
    path('registrar/', views.registrar_usuario, name='registrar_usuario'),
    path('perfil/<int:id>/', views.ver_perfil, name='ver_perfil'),
]
