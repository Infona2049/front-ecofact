# 🚀 INSTRUCCIONES PARA COMPAÑEROS DE EQUIPO

## ⚡ Configuración Rápida (5 minutos)

### 1. Actualizar el repositorio
```bash
git pull origin master
```

### 2. Verificar/instalar dependencias
```bash
pip install -r requirements.txt
```

### 3. Aplicar migraciones (si es necesario)
```bash
python manage.py migrate
```

### 4. Crear usuarios de prueba en Neon (IMPORTANTE)
```bash
python manage.py setup_test_users
```

### 5. Ejecutar el servidor
```bash
python manage.py runserver
```

## 🔑 Usuarios de Prueba Disponibles

| Rol | Email | Contraseña | Dashboard |
|-----|-------|------------|-----------|
| **Admin** | admin@ecofact.com | admin123 | `/admin-dashboard/` |
| **Vendedor** | vendedor@ecofact.com | vendedor123 | `/vendedor-dashboard/` |
| **Cliente** | cliente@ecofact.com | cliente123 | `/cliente-dashboard/` |

## 🎯 URLs para Probar

- **Login:** http://127.0.0.1:8000/login/
- **Admin Dashboard:** http://127.0.0.1:8000/admin-dashboard/
- **Vendedor Dashboard:** http://127.0.0.1:8000/vendedor-dashboard/
- **Cliente Dashboard:** http://127.0.0.1:8000/cliente-dashboard/

## ✅ Características Implementadas

- ✅ **Límite de 3 intentos** de login por usuario
- ✅ **Bloqueo por 10 minutos** después de 3 intentos fallidos
- ✅ **Redirección automática** por rol después del login
- ✅ **Protección de URLs** por tipo de usuario
- ✅ **Base de datos Neon** compartida para todo el equipo

## 🔧 Si Hay Problemas

### Error: "Credenciales incorrectas"
```bash
python manage.py setup_test_users
```

### Error: Usuario bloqueado
```bash
python manage.py unlock_user --all
```

### Error de migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

## 🧪 Cómo Probar el Sistema

1. **Ve a:** http://127.0.0.1:8000/login/
2. **Prueba login fallido** 3 veces → debe bloquear por 10 minutos
3. **Login exitoso** con cualquier rol → debe redirigir al dashboard correcto
4. **Intenta acceder** a URL de otro rol → debe redirigir a tu dashboard

## 📞 Soporte

Si tienes problemas, verifica que:
1. ✅ Hiciste `git pull origin master`
2. ✅ Ejecutaste `pip install -r requirements.txt`
3. ✅ Ejecutaste `python manage.py setup_test_users`
4. ✅ El servidor está corriendo en http://127.0.0.1:8000/

---
**¡Sistema listo para trabajar en equipo! 🚀**