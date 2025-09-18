from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

# 👇 Vistas básicas para que no marque error
def lista_productos(request):
    return HttpResponse("Lista de productos")

def detalle_producto(request, id):
    return HttpResponse(f"Detalle del producto con ID: {id}")

def crear_producto(request):
    return HttpResponse("Formulario para crear producto")
