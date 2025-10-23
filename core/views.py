from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from functools import wraps
from .forms import RegistroUsuarioForm, PerfilForm
from .models import Usuario

# ===== Decorador de roles =====
def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('login')
            if request.user.rol_usuario not in allowed_roles:
                messages.error(request, 'No tienes permisos para acceder a esta página')
                return redirect('login')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


# ===== Login =====
def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            # redirecciones por rol
            if user.is_superuser:
                return JsonResponse({'success': True, 'redirect_url': '/admin/'})
            elif user.rol_usuario == 'admin':
                return JsonResponse({'success': True, 'redirect_url': '/visualizacion_admin/'})
            elif user.rol_usuario == 'vendedor':
                return JsonResponse({'success': True, 'redirect_url': '/visualizacion_vendedor/'})
            elif user.rol_usuario == 'cliente':
                return JsonResponse({'success': True, 'redirect_url': '/visualizacion_cliente/'})
        else:
            return JsonResponse({'success': False, 'message': 'Credenciales incorrectas'})

    return render(request, 'core/login.html')


# ===== Logout =====
def logout_view(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente')
    return redirect('login')


# ===== Actualizar Perfil =====
@login_required
def actualizar_perfil_view(request):
    user = request.user

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=user)
        if form.is_valid():
            cleaned = form.cleaned_data

            # normalizar None -> ''
            for k, v in list(cleaned.items()):
                if v in [None, 'None']:
                    cleaned[k] = ''

            new_email = (cleaned.get('correo_electronico_usuario') or '').strip()
            new_direccion = (cleaned.get('direccion_usuario') or '').strip()
            new_telefono = (cleaned.get('telefono_usuario') or '').strip()

            cambios = []
            correo_cambiado = False

            # validar y preparar cambios
            if new_email and new_email != (user.correo_electronico_usuario or ''):
                if Usuario.objects.filter(correo_electronico_usuario=new_email).exclude(id=user.id).exists():
                    messages.error(request, "❌ Ese correo electrónico ya está registrado.")
                    return redirect('actualizar_perfil')
                user.correo_electronico_usuario = new_email
                user.username = new_email
                correo_cambiado = True
                cambios.append('correo electrónico')

            if new_direccion != (user.direccion_usuario or ''):
                user.direccion_usuario = new_direccion
                cambios.append('dirección')

            if new_telefono != (user.telefono_usuario or ''):
                user.telefono_usuario = new_telefono
                cambios.append('teléfono')

            if cambios:
                user.save()
                # mantener sesión: update_session_auth_hash solo para contraseñas; para cambios de email
                # la sesión sigue activa porque no cambiamos password. Aun así refrescamos el user en sesión:
                # login(request, user) reforzado para asegurar backend en sesión
                login(request, user)

                messages.success(request, f"✅ Información actualizada con éxito ({', '.join(cambios)})")
            else:
                messages.info(request, "ℹ️ No realizaste ningún cambio")

            # renderizamos la misma página para mostrar mensaje 3s (el template tiene el JS)
            form = PerfilForm(instance=user)
            return render(request, 'core/actualizar_perfil.html', {'form': form})
        else:
            messages.error(request, "❌ Error al procesar el formulario")
    else:
        form = PerfilForm(instance=user)

    return render(request, 'core/actualizar_perfil.html', {'form': form})


# ===== Otras vistas de apoyo (stubs seguros) =====
def documentos_view(request):
    return render(request, 'core/documentos.html')

def cambiocontraseña_view(request):
    return render(request, 'core/olvido_contraseña.html')

def acerca_nosotros_view(request):
    return render(request, 'core/acerca_nosotros.html')

def historial_factura_view(request):
    return render(request, 'core/historial_factura.html')

def olvido_contraseña_view(request):
    return render(request, 'core/olvido_contraseña.html')

# ===== Registro =====
def registro_view(request):
    if request.method == 'POST':
        form = RegistroUsuarioForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                messages.success(request, 'Usuario registrado exitosamente. Ya puedes iniciar sesión.')
                return redirect('login')
            except Exception as e:
                messages.error(request, f'Error al registrar usuario: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = RegistroUsuarioForm()
    return render(request, 'core/registro.html', {'form': form})


# ===== Dashboards =====
@role_required(['admin'])
def visualizacion_admin_view(request):
    return render(request, 'core/visualizacion_Admin.html')


@role_required(['cliente'])
def visualizacion_cliente_view(request):
    return render(request, 'core/visualizacion_Cliente.html')


@role_required(['vendedor'])
def visualizacion_vendedor_view(request):
    return render(request, 'core/visualizacion_Vendedor.html')