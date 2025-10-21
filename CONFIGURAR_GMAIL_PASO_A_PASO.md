# 🔐 CONFIGURAR GMAIL PARA ENVIAR EMAILS REALES - PASO A PASO

## ✅ Lo que vas a lograr:

Después de seguir estos pasos:
- ✅ Los usuarios recibirán el código en su Gmail REAL
- ✅ El código funcionará para restablecer la contraseña
- ✅ La nueva contraseña se guardará en la base de datos
- ✅ El usuario podrá hacer login con la nueva contraseña

---

## 📋 PASO 1: Obtener Contraseña de Aplicación de Google

### 1.1 Ve a tu cuenta de Google
🔗 https://myaccount.google.com/

### 1.2 Habilita la Verificación en 2 pasos
1. En el menú izquierdo, haz clic en **"Seguridad"**
2. Busca **"Verificación en 2 pasos"**
3. Si NO está activada, haz clic en **"Empezar"** y sigue los pasos
4. Verifica tu identidad con tu teléfono

### 1.3 Crea una Contraseña de Aplicación
1. Vuelve a **"Seguridad"**
2. Busca **"Contraseñas de aplicaciones"** (aparece después de activar verificación en 2 pasos)
3. Haz clic en **"Contraseñas de aplicaciones"**
4. Es posible que te pida tu contraseña de nuevo
5. En "Seleccionar app", elige **"Correo"**
6. En "Seleccionar dispositivo", elige **"Otro (nombre personalizado)"**
7. Escribe: **"EcoFact Django"**
8. Haz clic en **"Generar"**

### 1.4 Copia la contraseña
Google te mostrará una contraseña de 16 caracteres como:
```
abcd efgh ijkl mnop
```

**⚠️ IMPORTANTE:**
- Copia esta contraseña AHORA (no podrás verla después)
- Guárdala en un lugar seguro
- Esta NO es tu contraseña normal de Gmail

---

## 🔧 PASO 2: Configurar Django

### 2.1 Abre el archivo de configuración

Archivo: `EcoFactProject/settings.py`

### 2.2 Busca esta sección (al final del archivo):

```python
#CONFIGURACIÓN MAILTRAP

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "sandbox.smtp.mailtrap.io"
EMAIL_HOST_USER = "37784d5fd7e4f7"
EMAIL_HOST_PASSWORD = "d1db56fe8a2834"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = "facturacion@ecofact.com"
```

### 2.3 Reemplázala con esto:

```python
# CONFIGURACIÓN EMAIL REAL - GMAIL
# Los emails llegarán a las bandejas reales de los usuarios

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "TU_EMAIL@gmail.com"  # ← CAMBIA ESTO por tu Gmail
EMAIL_HOST_PASSWORD = "abcd efgh ijkl mnop"  # ← CAMBIA ESTO por tu contraseña de aplicación
DEFAULT_FROM_EMAIL = "TU_EMAIL@gmail.com"  # ← CAMBIA ESTO por tu Gmail
```

### 2.4 Ejemplo real:

Si tu Gmail es `juandavid.dev@gmail.com` y tu contraseña de aplicación es `abcd efgh ijkl mnop`:

```python
# CONFIGURACIÓN EMAIL REAL - GMAIL

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "juandavid.dev@gmail.com"
EMAIL_HOST_PASSWORD = "abcd efgh ijkl mnop"
DEFAULT_FROM_EMAIL = "juandavid.dev@gmail.com"
```

### 2.5 Guarda el archivo

---

## 🧪 PASO 3: Probar que funciona

### 3.1 Ejecuta el script de prueba:

```bash
python test_email.py
```

Esto enviará un email de prueba al primer usuario de tu BD.

### 3.2 Revisa el Gmail del usuario

Si el usuario en tu BD es `sebastiancortez@gmail.com`, revisa ESE Gmail.
El email debería llegar en menos de 1 minuto.

---

## ✅ PASO 4: Probar el flujo completo

### 4.1 Inicia el servidor:

```bash
python manage.py runserver
```

### 4.2 Ve a la página de recuperación:

🔗 http://localhost:8000/olvido_contraseña/

### 4.3 Prueba con un usuario real:

Ejemplo de usuarios en tu BD:
- `juandavid@gmail.com` (vendedor)
- `sebastiancortez@gmail.com` (cliente)
- `superadmin@ecofact.com` (admin)
- `miguelrestrepo0330@gmail.com` (admin)

### 4.4 Sigue el proceso:

1. **Pantalla 1:** Ingresa el email del usuario
   - Ejemplo: `sebastiancortez@gmail.com`
   - Haz clic en "Enviar código"

2. **Revisa el Gmail REAL del usuario:**
   - Ve a https://gmail.com
   - Inicia sesión como ese usuario
   - Busca un email de tu Gmail
   - Copia el código de 6 dígitos

3. **Pantalla 2:** Ingresa el código
   - Pega el código que recibiste
   - Haz clic en "Verificar código"

4. **Pantalla 3:** Nueva contraseña
   - Ingresa una nueva contraseña (mínimo 8 caracteres)
   - Confirma la contraseña
   - Haz clic en "Guardar nueva contraseña"

5. **Pantalla 4:** ¡Éxito!
   - Verás mensaje de éxito
   - Haz clic en "Volver a inicio de sesión"

6. **Prueba el login:**
   - Ve a http://localhost:8000/login/
   - Ingresa el email del usuario
   - Ingresa la NUEVA contraseña que acabas de crear
   - ¡Deberías poder iniciar sesión! ✅

---

## 🔍 Verificar en la Base de Datos

### Opción 1: Django Admin

1. Ve a: http://localhost:8000/admin/
2. Login como superadmin
3. Ve a: **Core** → **Usuarios**
4. Busca el usuario que cambió su contraseña
5. Verás que la contraseña está hasheada (encriptada) ✅

### Opción 2: Django Shell

```bash
python manage.py shell
```

Luego:

```python
from core.models import Usuario

# Buscar el usuario
usuario = Usuario.objects.get(correo_electronico_usuario='sebastiancortez@gmail.com')

# Ver si la nueva contraseña funciona
usuario.check_password('NuevaPassword123')  # Debería retornar True
```

---

## 🎯 RESUMEN DE LO QUE HACE EL SISTEMA

### Cuando un usuario pide recuperar contraseña:

```
1. Usuario ingresa su email
        ↓
2. Sistema busca el usuario en la BD
        ↓
3. Sistema genera:
   - Token JWT (válido 1 hora)
   - Código de 6 dígitos aleatorios
        ↓
4. Sistema guarda en tabla PasswordResetToken:
   - Usuario
   - Token
   - Código
   - Fecha de expiración
        ↓
5. Sistema envía email vía TU GMAIL a:
   - Email del usuario (ej: sebastiancortez@gmail.com) ✅
        ↓
6. Usuario recibe email en su Gmail REAL ✅
        ↓
7. Usuario ingresa el código de 6 dígitos
        ↓
8. Sistema verifica:
   - Token JWT válido ✅
   - Código correcto ✅
   - No expirado ✅
   - No usado antes ✅
        ↓
9. Usuario ingresa nueva contraseña
        ↓
10. Sistema valida:
    - Mínimo 8 caracteres ✅
    - Al menos 1 mayúscula ✅
    - Al menos 1 minúscula ✅
    - Al menos 1 número ✅
    - Contraseñas coinciden ✅
        ↓
11. Sistema actualiza la contraseña en la BD:
    - usuario.set_password('nueva_password') ✅
    - usuario.save() ✅
        ↓
12. Sistema marca el token como usado
        ↓
13. ¡Contraseña cambiada exitosamente! 🎉
```

---

## 🔐 Seguridad Implementada

✅ **La contraseña se guarda encriptada en la BD**
   - Usa el sistema de hashing de Django
   - No se guarda en texto plano
   - Irreversible

✅ **El token expira en 1 hora**
   - Después de 1 hora, el código no sirve

✅ **El código solo se puede usar una vez**
   - Después de cambiar la contraseña, se marca como "usado"

✅ **Validación de fortaleza de contraseña**
   - Mínimo 8 caracteres
   - Debe tener mayúsculas, minúsculas y números

---

## ❓ Preguntas Frecuentes

### P: ¿Funciona con cualquier email?
**R:** SÍ. El usuario puede tener Gmail, Outlook, Hotmail, Yahoo, etc.
Solo TÚ necesitas Gmail para ENVIAR los emails.

### P: ¿Puedo usar mi Gmail personal?
**R:** SÍ. Puedes usar cualquier Gmail que tengas.

### P: ¿Los emails van a spam?
**R:** A veces. Depende del proveedor de email del usuario.
Para evitarlo, puedes:
- Usar un dominio propio
- Usar SendGrid (más profesional)

### P: ¿Cuántos emails puedo enviar?
**R:** Con Gmail: hasta 500 emails por día (gratis)

### P: ¿Es seguro poner mi contraseña en settings.py?
**R:** NO debes subirlo a GitHub.
Mejor usa variables de entorno (archivo .env)
Ver guía en: CONFIGURAR_EMAIL_REAL.md

### P: ¿Funciona para admin, vendedor y cliente?
**R:** SÍ. Funciona para TODOS los roles. El sistema no distingue roles.

---

## 🚨 Solución de Problemas

### Error: "No se pudo enviar el email"

**Causas posibles:**
1. Email o contraseña de aplicación incorrectos
2. No activaste verificación en 2 pasos
3. Gmail bloqueó el acceso

**Solución:**
1. Verifica que copiaste bien el email y contraseña
2. Asegúrate que sea contraseña de aplicación (no tu contraseña normal)
3. Revisa que verificación en 2 pasos esté activada

### Error: "Token inválido o expirado"

**Causa:** Han pasado más de 1 hora

**Solución:** Solicita un nuevo código

### El email no llega

**Causas posibles:**
1. El email está en spam
2. Gmail del usuario no existe
3. Error de configuración

**Solución:**
1. Revisa la carpeta de spam del usuario
2. Verifica que el email existe en tu BD
3. Ejecuta: `python test_email.py` para verificar configuración

---

## 📝 CHECKLIST FINAL

Antes de usar en producción:

- [ ] Obtuve contraseña de aplicación de Google
- [ ] Actualicé settings.py con mi Gmail
- [ ] Ejecuté test_email.py y funcionó
- [ ] Probé el flujo completo de recuperación
- [ ] El email llega al Gmail real del usuario
- [ ] La contraseña se cambia en la BD
- [ ] Puedo hacer login con la nueva contraseña
- [ ] Configuré variables de entorno (.env) para seguridad

---

## ✅ ¡LISTO!

Después de seguir estos pasos, tendrás:

✅ Emails llegando a Gmails REALES
✅ Código de 6 dígitos funcionando
✅ Contraseñas cambiándose en la BD
✅ Sistema funcionando para admin, vendedor y cliente

---

**Tiempo estimado:** 10 minutos
**Dificultad:** Fácil
**Costo:** Gratis

---

¿Necesitas ayuda? Revisa los otros archivos:
- CONFIGURAR_EMAIL_REAL.md
- README_PASSWORD_RECOVERY.md
- ENTENDER_MAILTRAP.txt
