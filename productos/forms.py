from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):

    """
    Formulario basado en el modelo Producto para crear o editar productos.

    Incluye los campos principales del modelo que se desean mostrar en el formulario.
    """

    stock_actual_inventario = forms.IntegerField(
        label="Stock actual",
        min_value=0,
        initial=0,
        help_text="Cantidad inicial en inventario"
    )

    class Meta:
        model = Producto
        fields = [
            'nombre_producto',
            'categoria_producto',
            'modelo_producto',
            'capacidad_producto',
            'color_producto',
            'precio_producto',
            'imagen_producto',
        ]
        widgets = {
            'nombre_producto': forms.TextInput(attrs={
                'placeholder': 'Nombre del producto',
                'pattern': '[A-Za-zÁÉÍÓÚáéíóúÑñ ]+',
                'title': 'Solo letras y espacios',
                'oninput': "this.value = this.value.replace(/[^A-Za-zÁÉÍÓÚáéíóúÑñ ]/g, '')"
            }),
        }