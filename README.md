# EcoFact - Sistema de Facturación

Sistema de facturación con autenticación por roles desarrollado en Django.

## 🚀 Instalación y Configuración

### Requisitos previos
- Python 3.11 o superior
- Git
- PostgreSQL (opcional, recomendado para equipos)

### 1. Clonar el repositorio
```bash
git clone https://github.com/Infona2049/front-ecofact.git
cd front-ecofact
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual
**En Windows:**
```bash
venv\Scripts\activate
```

**En Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno
Copia el archivo de ejemplo y configúralo:
```bash
copy .env.example .env
```

**Para usar SQLite (más fácil para desarrollo individual):**
```
USE_POSTGRESQL=False
```

**Para usar PostgreSQL (recomendado para equipos):**
```
USE_POSTGRESQL=True
DB_NAME=ecofact
DB_USER=tu_usuario_postgres
DB_PASSWORD=tu_contraseña_postgres
DB_HOST=localhost
DB_PORT=5432
```

### 6. Configurar base de datos
```bash
python manage.py migrate
```

### 7. Crear usuarios de prueba
```bash
python manage.py create_test_users
```

### 8. Ejecutar el servidor
```bash
python manage.py runserver 8001
```

## 🔗 Configuración para Equipos

### Opción A: SQLite (Individual)
- Cada desarrollador tiene su propia base de datos
- Los usuarios de prueba se crean con `python manage.py create_test_users`
- Fácil setup, ideal para desarrollo individual

### Opción B: PostgreSQL (Equipos)
- Base de datos compartida entre todo el equipo
- Todos acceden a los mismos usuarios
- Requiere configurar PostgreSQL en cada máquina

#### Para configurar PostgreSQL:
1. Instalar PostgreSQL en tu máquina
2. Crear base de datos: `createdb ecofact`
3. Cambiar `.env`: `USE_POSTGRESQL=True`
4. Configurar usuario y contraseña en `.env`
5. Ejecutar migraciones: `python manage.py migrate`
6. Crear usuarios: `python manage.py create_test_users`

## 🔐 Usuarios de Prueba

| Rol | Email | Contraseña | URL de acceso |
|-----|-------|------------|---------------|
| **Administrador** | admin@ecofact.com | admin123 | `/admin-dashboard/` |
| **Vendedor** | vendedor@ecofact.com | vendedor123 | `/vendedor-dashboard/` |
| **Cliente** | cliente@ecofact.com | cliente123 | `/cliente-dashboard/` |

## 🌐 URLs Principales

- **Página principal:** `http://127.0.0.1:8001/` (redirige al login)
- **Login:** `http://127.0.0.1:8001/login/`
- **Registro:** `http://127.0.0.1:8001/registro/`
- **Admin Panel:** `http://127.0.0.1:8001/admin/`

## 📱 Funcionalidades

### ✅ Implementadas
- [x] Sistema de autenticación por email
- [x] Registro de nuevos usuarios (solo clientes)
- [x] Login con redirección automática por rol
- [x] Dashboards específicos por rol
- [x] Control de acceso por decoradores
- [x] Gestión de archivos estáticos
- [x] Base de datos con SQLite

### 🔄 Sistema de Roles
- **Admin:** Acceso completo al sistema
- **Vendedor:** Gestión de productos y ventas
- **Cliente:** Visualización de productos y facturas

## 🛠️ Estructura del Proyecto

```
front-ecofact/
├── core/                   # App principal
│   ├── models.py          # Modelos de usuario y facturación
│   ├── views.py           # Vistas de login, registro, dashboards
│   ├── forms.py           # Formularios de registro
│   ├── templates/         # Templates HTML
│   └── static/            # CSS y JS
├── productos/             # App de productos
├── static/                # Archivos estáticos globales
├── EcoFactProject/        # Configuración del proyecto
├── manage.py
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
```

## 🐛 Solución de Problemas

### Error de puerto ocupado
Si el puerto 8000 está ocupado, usa otro puerto:
```bash
python manage.py runserver 8001
```

### Error de migraciones
Si hay problemas con la base de datos:
```bash
python manage.py makemigrations
python manage.py migrate
```

### Error de archivos estáticos
Si las imágenes no cargan, verifica que el servidor esté ejecutándose y que las rutas en los templates usen `{% static 'img/nombre-imagen.png' %}`.

## 📝 Notas de Desarrollo

- **Base de datos:** SQLite (para desarrollo)
- **Puerto por defecto:** 8001 (evita conflictos)
- **Archivos de media:** Las imágenes están en `static/img/`
- **Registro:** Solo permite crear usuarios con rol "Cliente"

## 🤝 Colaboración

1. Crear rama para tu feature: `git checkout -b feature/mi-feature`
2. Hacer commits descriptivos: `git commit -m "feat: agregar nueva funcionalidad"`
3. Push a tu rama: `git push origin feature/mi-feature`
4. Crear Pull Request

## 📞 Contacto

Si tienes problemas con la instalación o ejecución, contacta al equipo de desarrollo.

---
**Desarrollado por:** Equipo EcoFact  
**Última actualización:** Septiembre 2025