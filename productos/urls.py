from django.urls import path
from . import views

urlpatterns = [
    path('inventario/', views.inventario_view, name='inventario'),
    path('registro_producto/', views.registro_producto_view, name='registro_producto'),
    # ...otras vistas de productos...
]