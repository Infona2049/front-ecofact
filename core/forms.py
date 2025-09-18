from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre_producto',
            'categoria_producto',
            'modelo_producto',
            'capacidad_producto',
            'color_producto',
            'descripcion_producto',
            'precio_producto',
            'codigo_barras_producto',
            'imagen_producto',
        ]