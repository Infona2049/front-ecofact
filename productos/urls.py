from django.urls import path
from . import views

urlpatterns = [
    # Ruta para la vista que muestra el inventario de productos
    path('inventario/', views.inventario_view, name='inventario'),

    # Ruta para la vista que permite registrar un nuevo producto
    path('registro_producto/', views.registro_producto_view, name='registro_producto'),
]