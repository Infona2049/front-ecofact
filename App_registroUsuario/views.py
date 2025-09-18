from django.shortcuts import render, redirect
from core.models import Usuario
from .forms import UsuarioForm  # Importa tu formulario de usuarios
from django.http import HttpResponse

# 👇 Vista para login de usuario
def login_usuario(request):
    return HttpResponse("Página de login de usuario")

# 👇 Vista para registrar usuario
def registrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
           # usuario = form.save(commit=False) #activa la alerta
           # usuario.set_password(form.cleaned_data['password1'])
           # usuario.save()
            print("Datos recibidos del formulario:")
            print("Nombre:", form.cleaned_data['nombre_usuario'])
            print("Correo:", form.cleaned_data['correo_electronico_usuario'])
            print("Rol:", form.cleaned_data['rol_usuario'])
            return HttpResponse("Usuario guardado exitosamente")
    else:
        form = UsuarioForm()

    # 👇 Renderiza la plantilla de registro y pasa el formulario al HTML
    return render(request, 'registro.html', {'form': form})

# 👇 Vista para ver perfil de usuario
def ver_perfil(request, id):
    return HttpResponse(f"Perfil del usuario con ID: {id}")
