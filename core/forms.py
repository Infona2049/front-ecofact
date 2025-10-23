from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, TIPO_DOCUMENTO_CHOICES, ROL_USUARIO_CHOICES


class RegistroUsuarioForm(UserCreationForm):
    nombre_usuario = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Primer nombre'
    }))
    segundo_nombre_usuario = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Segundo nombre (opcional)'
    }))
    apellido_usuario = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Primer apellido'
    }))
    segundo_apellido_usuario = forms.CharField(max_length=30, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Segundo apellido (opcional)'
    }))
    tipo_documento_usuario = forms.ChoiceField(choices=TIPO_DOCUMENTO_CHOICES, widget=forms.Select(attrs={
        'class': 'form-control'
    }))
    numero_documento_usuario = forms.CharField(max_length=15, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Número de documento'
    }))
    correo_electronico_usuario = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control', 'placeholder': 'correo@ejemplo.com'
    }))
    direccion_usuario = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Dirección (opcional)'
    }))
    telefono_usuario = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'Teléfono (opcional)'
    }))
    rol_usuario = forms.ChoiceField(choices=[('cliente', 'Cliente')], initial='cliente', widget=forms.HiddenInput())
    username = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Usuario
        fields = [
            'username', 'nombre_usuario', 'segundo_nombre_usuario', 'apellido_usuario',
            'segundo_apellido_usuario', 'tipo_documento_usuario', 'numero_documento_usuario',
            'correo_electronico_usuario', 'direccion_usuario', 'telefono_usuario',
            'rol_usuario', 'password1', 'password2'
        ]

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        # Personalizar inputs de contraseña
        if 'password1' in self.fields:
            self.fields['password1'].widget.attrs.update({
                'class': 'form-control', 'placeholder': 'Contraseña'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'class': 'form-control', 'placeholder': 'Confirmar contraseña'
            })

    def clean_correo_electronico_usuario(self):
        email = self.cleaned_data.get('correo_electronico_usuario')
        if email and Usuario.objects.filter(correo_electronico_usuario=email).exists():
            raise forms.ValidationError('Este correo electrónico ya está registrado.')
        return email

    def clean_numero_documento_usuario(self):
        documento = self.cleaned_data.get('numero_documento_usuario')
        if documento and Usuario.objects.filter(numero_documento_usuario=documento).exists():
            raise forms.ValidationError('Este número de documento ya está registrado.')
        return documento

    def save(self, commit=True):
        user = super().save(commit=False)
        # usar el email como username
        user.username = self.cleaned_data.get('correo_electronico_usuario') or user.username
        user.rol_usuario = 'cliente'
        if commit:
            user.save()
        return user


# Formulario para actualizar perfil (solo los editables)
class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = [
            'correo_electronico_usuario', 'direccion_usuario', 'telefono_usuario'
        ]
        widgets = {
            'correo_electronico_usuario': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'correo@ejemplo.com'}),
            'direccion_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Dirección (opcional)'}),
            'telefono_usuario': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Teléfono (opcional)'}),
        }