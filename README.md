# EcoFact - Sistema de Facturación

Sistema de facturación con autenticación por roles desarrollado en Django.

## 🚀 Configuración Rápida para Nuevos Miembros del Equipo

### ⚡ Pasos Rápidos (5 minutos)

```bash
# 1. Clonar el repositorio
git clone https://github.com/Infona2049/front-ecofact.git
cd front-ecofact

# 2. Crear y activar entorno virtual
python -m venv venv
venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Aplicar migraciones
python manage.py migrate

# 5. Crear usuarios de prueba (¡IMPORTANTE!)
python manage.py setup_test_users

# 6. Ejecutar servidor
python manage.py runserver
```

### 🔑 Usuarios de Prueba Disponibles

| Rol | Email | Contraseña | Dashboard |
|-----|-------|------------|-----------|
| **Admin** | admin@ecofact.com | admin123 | `/admin-dashboard/` |
| **Vendedor** | vendedor@ecofact.com | vendedor123 | `/vendedor-dashboard/` |
| **Cliente** | cliente@ecofact.com | cliente123 | `/cliente-dashboard/` |

## � Sistema de Autenticación Implementado

### ✅ Características de Seguridad
- **Límite de 3 intentos de login** por usuario
- **Bloqueo automático por 10 minutos** después de 3 intentos fallidos
- **Redirección automática por rol** después del login
- **Protección de URLs** por tipo de usuario
- **Middleware de seguridad** para prevenir acceso cruzado

### 🎯 Redirecciones por Rol
- **Admin** → `/admin-dashboard/` (gestión completa)
- **Vendedor** → `/vendedor-dashboard/` (productos y facturas)
- **Cliente** → `/cliente-dashboard/` (visualización)

## 🛠️ Comandos Útiles para Desarrolladores

### Gestión de Usuarios
```bash
# Crear usuarios de prueba
python manage.py setup_test_users

# Desbloquear usuario específico
python manage.py unlock_user --email admin@ecofact.com

# Desbloquear todos los usuarios
python manage.py unlock_user --all

# Ver estado de intentos de login
python manage.py check_login_status

# Ver solo usuarios bloqueados
python manage.py check_login_status --blocked-only
```

### Gestión de Base de Datos
```bash
# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario para Django Admin
python manage.py createsuperuser
```

### Testing y Verificación
```bash
# Verificar sistema completo
python verificar_sistema_completo.py

# Probar solo sistema de login
python test_login_system.py
```

## 🌐 URLs del Sistema

### Públicas (sin login)
- **Login:** `http://127.0.0.1:8000/login/`
- **Registro:** `http://127.0.0.1:8000/registro/`
- **Recuperar contraseña:** `http://127.0.0.1:8000/olvido_contraseña/`

### Admin (solo administradores)
- **Dashboard Admin:** `http://127.0.0.1:8000/admin-dashboard/`
- **Panel Django:** `http://127.0.0.1:8000/admin/`

### Vendedor (solo vendedores)
- **Dashboard Vendedor:** `http://127.0.0.1:8000/vendedor-dashboard/`
- **Crear Factura:** `http://127.0.0.1:8000/crear_factura/`
- **Historial:** `http://127.0.0.1:8000/historial_factura/`

### Cliente (solo clientes)
- **Dashboard Cliente:** `http://127.0.0.1:8000/cliente-dashboard/`

## 🐛 Solución de Problemas Comunes

### ❌ "Credenciales incorrectas" con usuarios conocidos
**Causa:** Los usuarios de prueba no existen en tu base de datos local.
**Solución:**
```bash
python manage.py setup_test_users
```

### ❌ "Usuario bloqueado por 10 minutos"
**Causa:** Demasiados intentos fallidos.
**Solución:**
```bash
python manage.py unlock_user --email admin@ecofact.com
# o para todos:
python manage.py unlock_user --all
```

### ❌ Error de migraciones conflictivas
```bash
python manage.py makemigrations --merge
python manage.py migrate
```

### ❌ Puerto 8000 ocupado
```bash
python manage.py runserver 8001
```

## � Estructura del Proyecto

```
front-ecofact/
├── core/                              # App principal
│   ├── models.py                      # Usuario, Empresa, etc.
│   ├── views.py                       # Login, dashboards, etc.
│   ├── middleware.py                  # Redirección por roles
│   ├── management/commands/           # Comandos personalizados
│   │   ├── setup_test_users.py       # Crear usuarios de prueba
│   │   ├── unlock_user.py            # Desbloquear usuarios
│   │   └── check_login_status.py     # Ver estado de bloqueos
│   ├── templates/core/                # Templates HTML
│   └── static/core/                   # CSS, JS, imágenes
├── productos/                         # Gestión de productos
├── facturas/                          # Gestión de facturas
├── requirements.txt                   # Dependencias Python
├── test_login_system.py              # Script de pruebas básicas
├── verificar_sistema_completo.py     # Script de verificación completa
└── SISTEMA_AUTENTICACION_IMPLEMENTADO.md  # Documentación técnica
```

## 🔧 Tecnologías Utilizadas

- **Backend:** Django 5.2.4
- **Base de datos:** SQLite (desarrollo)
- **Frontend:** HTML5, CSS3, JavaScript (ES6)
- **Autenticación:** Django Auth + Sistema personalizado
- **Librerías:** ReportLab, QRCode, Pillow

## 📈 Estado del Desarrollo

### ✅ Completado
- [x] Sistema de autenticación con bloqueo por intentos
- [x] Redirección automática por roles
- [x] Protección de URLs
- [x] Gestión de usuarios por comandos
- [x] Middleware de seguridad
- [x] Interface de administración mejorada

### 🔄 En Desarrollo
- [ ] Módulo de reportes avanzados
- [ ] API REST para aplicación móvil
- [ ] Integración con sistemas de pago

## 📞 Soporte

Si tienes problemas:

1. **Verifica que seguiste todos los pasos** de instalación
2. **Ejecuta los comandos de verificación** incluidos
3. **Revisa la documentación técnica** en `SISTEMA_AUTENTICACION_IMPLEMENTADO.md`
4. **Contacta al equipo de desarrollo**

---
**Desarrollado por:** Equipo EcoFact  
**Última actualización:** Octubre 2025  
**Sistema de autenticación:** ✅ Implementado y funcionando