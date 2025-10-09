from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import IntegrityError

User = get_user_model()

class Command(BaseCommand):
    help = 'Crea usuarios de prueba para el sistema EcoFact'

    def handle(self, *args, **options):
        usuarios_prueba = [
            {
                'email': 'admin@ecofact.com',
                'username': 'admin_ecofact',
                'nombre': 'Admin',
                'apellido': 'EcoFact',
                'documento': '12345678',
                'rol': 'admin',
                'password': 'admin123'
            },
            {
                'email': 'vendedor@ecofact.com',
                'username': 'vendedor_ecofact',
                'nombre': 'Vendedor',
                'apellido': 'EcoFact',
                'documento': '87654321',
                'rol': 'vendedor',
                'password': 'vendedor123'
            },
            {
                'email': 'cliente@ecofact.com',
                'username': 'cliente_ecofact',
                'nombre': 'Cliente',
                'apellido': 'EcoFact',
                'documento': '11223344',
                'rol': 'cliente',
                'password': 'cliente123'
            }
        ]

        self.stdout.write(self.style.WARNING('=== CREANDO USUARIOS DE PRUEBA PARA ECOFACT ==='))
        
        created_count = 0
        existing_count = 0

        for user_data in usuarios_prueba:
            try:
                # Verificar si el usuario ya existe
                if User.objects.filter(correo_electronico_usuario=user_data['email']).exists():
                    self.stdout.write(
                        self.style.WARNING(
                            f'⚠️  Usuario {user_data["rol"]} ya existe: {user_data["email"]}'
                        )
                    )
                    existing_count += 1
                    continue

                # Crear el usuario
                usuario = User.objects.create_user(
                    correo_electronico_usuario=user_data['email'],
                    username=user_data['username'],
                    nombre_usuario=user_data['nombre'],
                    apellido_usuario=user_data['apellido'],
                    numero_documento_usuario=user_data['documento'],
                    rol_usuario=user_data['rol'],
                    password=user_data['password']
                )
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'✅ Usuario {user_data["rol"]} creado: {user_data["email"]}'
                    )
                )
                created_count += 1

            except IntegrityError as e:
                if 'numero_documento_usuario' in str(e):
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Error: El documento {user_data["documento"]} ya existe. '
                            f'Usuario {user_data["email"]} no creado.'
                        )
                    )
                else:
                    self.stdout.write(
                        self.style.ERROR(
                            f'❌ Error al crear usuario {user_data["email"]}: {e}'
                        )
                    )

        # Resumen
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=== RESUMEN ==='))
        self.stdout.write(f'✅ Usuarios creados: {created_count}')
        self.stdout.write(f'⚠️  Usuarios existentes: {existing_count}')
        
        if created_count > 0 or existing_count > 0:
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('=== CREDENCIALES DE ACCESO ==='))
            self.stdout.write('Admin: admin@ecofact.com / admin123')
            self.stdout.write('Vendedor: vendedor@ecofact.com / vendedor123')
            self.stdout.write('Cliente: cliente@ecofact.com / cliente123')
            self.stdout.write('')
            self.stdout.write(self.style.SUCCESS('¡Usuarios listos para usar! 🚀'))
        
        # Verificar estado de intentos
        usuarios_con_problemas = User.objects.filter(intentos_fallidos__gt=0)
        if usuarios_con_problemas.exists():
            self.stdout.write('')
            self.stdout.write(self.style.WARNING('⚠️  USUARIOS CON INTENTOS FALLIDOS DETECTADOS:'))
            for user in usuarios_con_problemas:
                estado = "🔒 BLOQUEADO" if user.esta_bloqueado() else f"⚠️  {user.intentos_fallidos} intentos"
                self.stdout.write(f'   - {user.correo_electronico_usuario}: {estado}')
            
            self.stdout.write('')
            self.stdout.write('Para resetear intentos fallidos ejecuta:')
            self.stdout.write(self.style.WARNING('python manage.py unlock_user --all'))