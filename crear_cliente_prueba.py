"""
Script para crear un cliente de prueba para recuperación de contraseña
"""
import os
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'EcoFactProject.settings')
django.setup()

from core.models import Usuario

# Datos del cliente
EMAIL = "juandavidmaturanamaturana@gmail.com"
NOMBRE = "Juan David"
APELLIDO = "Maturana"
PASSWORD = "cliente123"  # Contraseña inicial
ROL = "cliente"
DOCUMENTO = "1234567890"
TELEFONO = "3001234567"

print("=" * 70)
print("CREANDO CLIENTE DE PRUEBA PARA RECUPERACIÓN DE CONTRASEÑA")
print("=" * 70)
print()

# Verificar si el usuario ya existe
if Usuario.objects.filter(correo_electronico_usuario=EMAIL).exists():
    print(f"⚠️  El usuario con email {EMAIL} ya existe.")
    print()
    usuario_existente = Usuario.objects.get(correo_electronico_usuario=EMAIL)
    print("📋 DATOS DEL USUARIO EXISTENTE:")
    print(f"   📧 Email: {usuario_existente.correo_electronico_usuario}")
    print(f"   👤 Nombre: {usuario_existente.nombre_usuario} {usuario_existente.apellido_usuario}")
    print(f"   🏷️  Rol: {usuario_existente.rol_usuario}")
    print()
    print("✅ Puedes usar este usuario para las pruebas")
    print()
else:
    # Crear el nuevo usuario
    try:
        usuario = Usuario.objects.create_user(
            username=EMAIL.split('@')[0],  # Usar parte del email como username
            correo_electronico_usuario=EMAIL,
            nombre_usuario=NOMBRE,
            apellido_usuario=APELLIDO,
            password=PASSWORD,
            rol_usuario=ROL,
            numero_documento_usuario=DOCUMENTO,
            telefono_usuario=TELEFONO,
            is_active=True
        )
        
        print("✅ ¡CLIENTE CREADO EXITOSAMENTE!")
        print()
        print("📋 DATOS DEL CLIENTE:")
        print(f"   📧 Email: {usuario.correo_electronico_usuario}")
        print(f"   👤 Nombre: {usuario.nombre_usuario} {usuario.apellido_usuario}")
        print(f"   🔑 Contraseña inicial: {PASSWORD}")
        print(f"   🏷️  Rol: {usuario.rol_usuario}")
        print(f"   📱 Teléfono: {usuario.telefono_usuario}")
        print(f"   ✅ Activo: {usuario.is_active}")
        print()
        
    except Exception as e:
        print(f"❌ Error al crear el usuario: {e}")
        print()
        exit()

print("=" * 70)
print("🎯 PRÓXIMOS PASOS PARA PROBAR:")
print("=" * 70)
print()
print("1️⃣  Ve a: http://127.0.0.1:8000/olvido_contraseña/")
print()
print(f"2️⃣  Ingresa el email: {EMAIL}")
print()
print("3️⃣  Revisa tu Gmail real: juandavidmaturanamaturana@gmail.com")
print("    📨 Llegará un código de 6 dígitos")
print()
print("4️⃣  Ingresa el código que recibiste")
print()
print("5️⃣  Establece una nueva contraseña (mínimo 8 caracteres)")
print()
print("6️⃣  Ve a: http://127.0.0.1:8000/login/")
print("    🔐 Inicia sesión con tu nueva contraseña")
print()
print("=" * 70)
print()
print("💡 TIPS:")
print("   • Si no llega el email, revisa la carpeta de SPAM")
print("   • El código expira en 10 minutos")
print("   • Solo se puede usar una vez")
print("   • La contraseña se guarda en la base de datos")
print()
print("=" * 70)
