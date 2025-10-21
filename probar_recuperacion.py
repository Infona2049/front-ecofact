"""
Script para probar el sistema de recuperación de contraseña
"""
import os
import django
import requests
import time

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoFactProject.settings')
django.setup()

from core.models import Usuario, CodigoRecuperacion

print("=" * 70)
print("🧪 PRUEBA DEL SISTEMA DE RECUPERACIÓN DE CONTRASEÑA")
print("=" * 70)
print()

# URL base
BASE_URL = "http://127.0.0.1:8000"

# Usuario de prueba
TEST_EMAIL = "juandavidmaturanamaturana@gmail.com"

print("📋 PASO 1: Verificar que el usuario existe")
print("-" * 70)
try:
    usuario = Usuario.objects.get(correo_electronico_usuario=TEST_EMAIL)
    print(f"✅ Usuario encontrado: {usuario.nombre_usuario} {usuario.apellido_usuario}")
    print(f"   Email: {usuario.correo_electronico_usuario}")
    print(f"   Rol: {usuario.rol_usuario}")
except Usuario.DoesNotExist:
    print(f"❌ Usuario {TEST_EMAIL} no existe")
    print("   Ejecuta: python crear_cliente_prueba.py")
    exit(1)

print()
print("📋 PASO 2: Probar endpoint de solicitud de código")
print("-" * 70)

try:
    response = requests.post(
        f"{BASE_URL}/api/solicitar-recuperacion/",
        json={"email": TEST_EMAIL},
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Solicitud de código exitosa")
            print(f"   Mensaje: {data.get('message')}")
        else:
            print(f"❌ Error: {data.get('message')}")
            exit(1)
    else:
        print(f"❌ Error HTTP {response.status_code}")
        exit(1)
        
except requests.exceptions.ConnectionError:
    print("❌ No se pudo conectar al servidor")
    print("   Asegúrate de que el servidor esté corriendo:")
    print("   python manage.py runserver")
    exit(1)
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print()
print("📋 PASO 3: Obtener el código de la base de datos")
print("-" * 70)

# Esperar un momento para que se guarde en BD
time.sleep(1)

try:
    codigo_obj = CodigoRecuperacion.objects.filter(
        usuario=usuario
    ).order_by('-creado_en').first()
    
    if codigo_obj:
        print(f"✅ Código encontrado en BD: {codigo_obj.codigo}")
        print(f"   Creado: {codigo_obj.creado_en}")
        print(f"   Expira: {codigo_obj.expira_en}")
        print(f"   Usado: {codigo_obj.usado}")
        print(f"   Vigente: {codigo_obj.esta_vigente()}")
        
        codigo = codigo_obj.codigo
    else:
        print("❌ No se encontró el código en la BD")
        exit(1)
except Exception as e:
    print(f"❌ Error al buscar código: {e}")
    exit(1)

print()
print("📋 PASO 4: Verificar el código")
print("-" * 70)

try:
    response = requests.post(
        f"{BASE_URL}/api/verificar-codigo/",
        json={
            "email": TEST_EMAIL,
            "codigo": codigo
        },
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Código verificado correctamente")
            print(f"   Mensaje: {data.get('message')}")
        else:
            print(f"❌ Error: {data.get('message')}")
            exit(1)
    else:
        print(f"❌ Error HTTP {response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print()
print("📋 PASO 5: Cambiar la contraseña")
print("-" * 70)

nueva_password = "nuevapass123"

try:
    response = requests.post(
        f"{BASE_URL}/api/restablecer-password/",
        json={
            "email": TEST_EMAIL,
            "codigo": codigo,
            "password": nueva_password,
            "confirm_password": nueva_password
        },
        timeout=10
    )
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("✅ Contraseña cambiada exitosamente")
            print(f"   Mensaje: {data.get('message')}")
            print(f"   Nueva contraseña: {nueva_password}")
        else:
            print(f"❌ Error: {data.get('message')}")
            exit(1)
    else:
        print(f"❌ Error HTTP {response.status_code}")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print()
print("📋 PASO 6: Verificar que el código fue marcado como usado")
print("-" * 70)

codigo_obj.refresh_from_db()
if codigo_obj.usado:
    print("✅ Código marcado como usado correctamente")
else:
    print("❌ El código no fue marcado como usado")

print()
print("📋 PASO 7: Verificar que la contraseña cambió en la BD")
print("-" * 70)

usuario.refresh_from_db()
if usuario.check_password(nueva_password):
    print("✅ Contraseña actualizada correctamente en la base de datos")
else:
    print("❌ La contraseña NO se actualizó en la BD")
    exit(1)

print()
print("📋 PASO 8: Intentar reusar el código (debe fallar)")
print("-" * 70)

try:
    response = requests.post(
        f"{BASE_URL}/api/verificar-codigo/",
        json={
            "email": TEST_EMAIL,
            "codigo": codigo
        },
        timeout=10
    )
    
    data = response.json()
    if not data.get('success'):
        print("✅ Código usado correctamente rechazado")
        print(f"   Mensaje: {data.get('message')}")
    else:
        print("❌ El sistema permitió reusar el código (ERROR)")
        exit(1)
        
except Exception as e:
    print(f"❌ Error: {e}")
    exit(1)

print()
print("=" * 70)
print("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
print("=" * 70)
print()
print("📊 RESUMEN:")
print(f"   ✅ Solicitud de código: OK")
print(f"   ✅ Código generado en BD: OK")
print(f"   ✅ Verificación de código: OK")
print(f"   ✅ Cambio de contraseña: OK")
print(f"   ✅ Código marcado como usado: OK")
print(f"   ✅ Contraseña actualizada en BD: OK")
print(f"   ✅ Rechazo de código usado: OK")
print()
print("💡 PRÓXIMOS PASOS:")
print("   1. Ve a: http://127.0.0.1:8000/login/")
print(f"   2. Email: {TEST_EMAIL}")
print(f"   3. Password: {nueva_password}")
print("   4. Deberías poder iniciar sesión")
print()
print("📧 NOTA: El email fue enviado a:")
print(f"   {TEST_EMAIL}")
print("   Revisa tu Gmail para ver el código real")
print()
print("=" * 70)

# Restaurar contraseña original
print()
print("🔄 Restaurando contraseña original...")
usuario.set_password("cliente123")
usuario.save()
print("✅ Contraseña restaurada a: cliente123")
print()
