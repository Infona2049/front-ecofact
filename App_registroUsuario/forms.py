from django import forms
from django.contrib.auth.forms import UserCreationForm
from core.models import Usuario

class UsuarioForm(UserCreationForm):
    class Meta:
        model = Usuario
        fields = [
            'nombre_usuario', 'segundo_nombre_usuario', 'apellido_usuario',
            'segundo_apellido_usuario', 'tipo_documento_usuario',
            'numero_documento_usuario', 'correo_electronico_usuario',
            'direccion_usuario', 'telefono_usuario', 'rol_usuario',
            'password1', 'password2'
        ]
        widgets = {
            'nombre_usuario': forms.TextInput(attrs={'placeholder': 'Primer nombre'}),
            'segundo_nombre_usuario': forms.TextInput(attrs={'placeholder': 'Segundo nombre'}),
            'apellido_usuario': forms.TextInput(attrs={'placeholder': 'Primer apellido'}),
            'segundo_apellido_usuario': forms.TextInput(attrs={'placeholder': 'Segundo apellido'}),
            'tipo_documento_usuario': forms.Select(attrs={'placeholder': 'Tipo de documento'}),
            'numero_documento_usuario': forms.TextInput(attrs={'placeholder': 'Número de documento'}),
            'correo_electronico_usuario': forms.EmailInput(attrs={'placeholder': 'Correo electrónico'}),
            'direccion_usuario': forms.TextInput(attrs={'placeholder': 'Dirección'}),
            'telefono_usuario': forms.TextInput(attrs={'placeholder': 'Teléfono'}),
            'rol_usuario': forms.Select(),  # Placeholder se agrega en __init__
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  # 👈 Esto inicializa el formulario padre
        # Placeholders para password
        self.fields['password1'].widget.attrs.update({'placeholder': 'Contraseña'})#self.fields['password1']: Selecciona el campo password1 del formulario.
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirmar contraseña'})#.widget.attrs.update({...}): Añade atributos HTML extra al widget ya existente.
        # Placeholder para select de rol
       # self.fields['rol_usuario'].empty_label = 'Selecciona tu rol'
