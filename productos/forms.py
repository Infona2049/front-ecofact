from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    """
    Formulario basado en el modelo Producto para crear o editar productos.

    Incluye los campos principales del modelo que se desean mostrar en el formulario.
    """

    class Meta:
        model = Producto  # Modelo asociado al formulario
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
        ]  # Campos que se mostrarán en el formulario

        widgets = {
            # Personaliza el widget para la descripción para que sea un textarea con 3 filas
            'descripcion_producto': forms.Textarea(attrs={'rows': 3}),
            # Hace que el campo IVA sea de solo lectura (aunque no está incluido en fields, queda preparado)
            'iva_producto': forms.NumberInput(attrs={'readonly': 'readonly'}),
        }