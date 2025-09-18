from django.urls import path
from . import views  # 👈 Importa las vistas definidas en tu app

urlpatterns = [
    # 👇 Path vacío '' significa que responderá a la URL base de la app,
    # en este caso http://127.0.0.1:8000/productos/
    path('', views.lista_productos, name='lista_productos'),

    # 👇 URL para crear un producto
    # Esto responde a http://127.0.0.1:8000/productos/crear/
    path('crear/', views.crear_producto, name='crear_producto'),

    # 👇 URL para ver detalle de un producto específico
    # '<int:id>/' captura un número entero como parámetro id
    # Ejemplo: http://127.0.0.1:8000/productos/1/ mostrará el producto con ID 1
    path('<int:id>/', views.detalle_producto, name='detalle_producto'),
]
