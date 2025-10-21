# 🔐 Cómo Funciona el Sistema de Recuperación de Contraseña

## 📋 Resumen

Sistema simple y seguro para que los usuarios recuperen su contraseña usando su email real. Los códigos de verificación llegan directamente a Gmail.

---

## 🎯 Flujo Completo del Usuario

### **Paso 1: Solicitar Código**
1. Usuario va a: `/olvido_contraseña/`
2. Ingresa su email (ejemplo: `juandavidmaturanamaturana@gmail.com`)
3. Click en "Enviar código"

**¿Qué pasa detrás?**
- Sistema busca el usuario en la base de datos
- Genera código aleatorio de 6 dígitos
- Guarda el código en tabla `CodigoRecuperacion`
- Envía email a Gmail REAL del usuario
- Código expira en 10 minutos

---

### **Paso 2: Recibir Email**
El usuario recibe un email en su Gmail con:
```
Asunto: Código de recuperación de contraseña - EcoFact

Hola [Nombre],

Tu código de recuperación es: 123456

Este código es válido por 10 minutos.

Si no solicitaste este cambio, ignora este mensaje.
```

**De:** `losmejorereal0@gmail.com`  
**Para:** Email real del usuario

---

### **Paso 3: Verificar Código**
1. Usuario ingresa el código de 6 dígitos
2. Click en "Verificar código"

**¿Qué pasa detrás?**
- Sistema verifica que el código exista
- Verifica que no haya expirado (10 minutos)
- Verifica que no haya sido usado
- Si todo es correcto, permite continuar

---

### **Paso 4: Nueva Contraseña**
1. Usuario ingresa nueva contraseña (mínimo 8 caracteres)
2. Confirma la contraseña
3. Click en "Guardar nueva contraseña"

**¿Qué pasa detrás?**
- Sistema valida que las contraseñas coincidan
- Marca el código como "usado"
- **Actualiza la contraseña en la base de datos**
- Usuario puede iniciar sesión con la nueva contraseña

---

## 🔧 Arquitectura Técnica

### **Backend (Django)**

#### **Modelo: CodigoRecuperacion**
```python
class CodigoRecuperacion(models.Model):
    usuario = ForeignKey(Usuario)
    codigo = CharField(max_length=6)      # 6 dígitos aleatorios
    creado_en = DateTimeField(auto_now_add=True)
    expira_en = DateTimeField()           # creado_en + 10 minutos
    usado = BooleanField(default=False)
```

#### **3 Endpoints API:**

1. **`POST /api/solicitar-recuperacion/`**
   - Input: `{ "email": "usuario@gmail.com" }`
   - Output: `{ "success": true, "message": "Código enviado" }`

2. **`POST /api/verificar-codigo/`**
   - Input: `{ "email": "...", "codigo": "123456" }`
   - Output: `{ "success": true }`

3. **`POST /api/restablecer-password/`**
   - Input: `{ "email": "...", "codigo": "...", "password": "...", "confirm_password": "..." }`
   - Output: `{ "success": true, "message": "Contraseña actualizada" }`

---

### **Frontend (JavaScript)**

```javascript
// Variable global para guardar el email
let userEmail = null;

// 1. Enviar código
async function enviarCodigo() {
    const correo = document.getElementById('correo-input').value;
    const response = await fetch('/api/solicitar-recuperacion/', {
        method: 'POST',
        body: JSON.stringify({ email: correo })
    });
    if(response.ok) {
        userEmail = correo;  // Guardar email
        mostrarPantalla('codigo');
    }
}

// 2. Verificar código
async function verificarCodigo() {
    const codigo = document.getElementById('codigo-input').value;
    const response = await fetch('/api/verificar-codigo/', {
        method: 'POST',
        body: JSON.stringify({ email: userEmail, codigo: codigo })
    });
    if(response.ok) {
        mostrarPantalla('reset');
    }
}

// 3. Guardar nueva contraseña
async function guardarNueva() {
    const password = document.getElementById('newpass').value;
    const confirm = document.getElementById('confpass').value;
    const codigo = document.getElementById('codigo-input').value;
    
    const response = await fetch('/api/restablecer-password/', {
        method: 'POST',
        body: JSON.stringify({ 
            email: userEmail, 
            codigo: codigo,
            password: password,
            confirm_password: confirm 
        })
    });
    if(response.ok) {
        mostrarPantalla('success');
    }
}
```

---

## 📧 Configuración de Email (Gmail)

### **settings.py:**
```python
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = "losmejorereal0@gmail.com"
EMAIL_HOST_PASSWORD = "bamoffqrjaiowxtc"  # Contraseña de aplicación
DEFAULT_FROM_EMAIL = "losmejorereal0@gmail.com"
```

### **¿Cómo obtener contraseña de aplicación?**
1. Ve a: https://myaccount.google.com/
2. Seguridad → Verificación en 2 pasos (activar)
3. Seguridad → Contraseñas de aplicaciones
4. Genera una contraseña de 16 caracteres
5. Úsala en `EMAIL_HOST_PASSWORD` (sin espacios)

---

## 🎨 Interfaz de Usuario

### **4 Pantallas:**

1. **Pantalla 1: Ingreso de email**
   - Input: email
   - Botón: "Enviar código"

2. **Pantalla 2: Verificación de código**
   - Input: código de 6 dígitos
   - Botón: "Verificar código"
   - Botón: "Volver"

3. **Pantalla 3: Nueva contraseña**
   - Input: nueva contraseña
   - Input: confirmar contraseña
   - Botón: "Guardar nueva contraseña"
   - Botón: "Volver"

4. **Pantalla 4: Éxito**
   - Mensaje: "¡Hecho! Contraseña restablecida"
   - Botón: "Volver a inicio de sesión"

---

## 🔒 Seguridad

### **Medidas implementadas:**
- ✅ Códigos de un solo uso
- ✅ Expiración automática (10 minutos)
- ✅ Validación de email existente
- ✅ Contraseña mínima de 8 caracteres
- ✅ Confirmación de contraseña
- ✅ Protección CSRF
- ✅ Email real requerido

### **Validaciones:**
- Email debe existir en la base de datos
- Código debe ser válido (6 dígitos)
- Código no debe estar expirado
- Código no debe haber sido usado
- Contraseñas deben coincidir
- Contraseña mínima de 8 caracteres

---

## 🧪 Cómo Probar

### **1. Crear usuario de prueba:**
```bash
python crear_cliente_prueba.py
```

### **2. Probar envío de email:**
```bash
python test_email.py
```

### **3. Flujo completo:**
1. Ir a: http://127.0.0.1:8000/olvido_contraseña/
2. Ingresar: `juandavidmaturanamaturana@gmail.com`
3. Revisar Gmail real
4. Ingresar código recibido
5. Cambiar contraseña
6. Iniciar sesión en: http://127.0.0.1:8000/login/

---

## 📊 Ejemplo Real

### **Usuario de prueba creado:**
- **Email:** `juandavidmaturanamaturana@gmail.com`
- **Nombre:** Juan David Maturana
- **Rol:** Cliente
- **Contraseña inicial:** `cliente123`

### **Proceso de recuperación:**
1. ✅ Usuario solicita código
2. ✅ Sistema genera: `826293`
3. ✅ Email enviado a Gmail real
4. ✅ Usuario recibe email en segundos
5. ✅ Usuario ingresa código
6. ✅ Usuario cambia contraseña a: `nuevapass123`
7. ✅ Usuario inicia sesión con nueva contraseña

---

## 🚨 Troubleshooting

### **Email no llega:**
- ✓ Revisar carpeta SPAM
- ✓ Verificar que EMAIL_HOST_PASSWORD sea correcto
- ✓ Verificar que el email del usuario sea real
- ✓ Esperar 1-2 minutos

### **Código no funciona:**
- ✓ Verificar que no haya expirado (10 min)
- ✓ Verificar que no se haya usado antes
- ✓ Ingresar los 6 dígitos exactos

### **No se puede cambiar contraseña:**
- ✓ Contraseña mínima de 8 caracteres
- ✓ Las contraseñas deben coincidir
- ✓ El código debe ser válido

---

## 📁 Archivos Modificados

```
core/
├── models.py              # Modelo CodigoRecuperacion
├── views.py               # 3 endpoints API
├── admin.py               # Panel admin para códigos
├── templates/core/
│   └── olvido_contraseña.html
└── static/core/
    ├── css/
    │   └── olvido_contraseña.css
    └── js/
        └── olvido_contraseña.js

EcoFactProject/
└── settings.py            # Configuración Gmail

Scripts:
├── crear_cliente_prueba.py
└── test_email.py
```

---

## ✨ Características

- 🎯 **Simple:** Solo email + código de 6 dígitos
- 🔐 **Seguro:** Códigos temporales de un solo uso
- 📧 **Real:** Emails llegan a Gmail real
- 🎨 **Responsive:** Funciona en móvil, tablet y desktop
- ⚡ **Rápido:** Email llega en segundos
- 💾 **Persistente:** Cambios guardados en BD

---

**¡Sistema 100% funcional y probado!** ✅
