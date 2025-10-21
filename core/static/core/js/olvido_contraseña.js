// Variable global para almacenar el email del usuario
let userEmail = null;

function mostrarPantalla(id) {
  document.querySelectorAll('.container > div').forEach(div => div.classList.add('hidden'));
  document.getElementById(id).classList.remove('hidden');

  ['correo-error','codigo-error','reset-error'].forEach(idErr => {
    const el = document.getElementById(idErr);
    if(el){ el.classList.add('hidden'); el.textContent = ''; }
  });
}

function mostrarError(elementId, mensaje) {
  const el = document.getElementById(elementId);
  if(el) {
    el.textContent = mensaje;
    el.classList.remove('hidden');
  }
}

function obtenerCSRFToken() {
  const name = 'csrftoken';
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

async function enviarCodigo() {
  const correo = document.getElementById('correo-input').value.trim();
  const err = document.getElementById('correo-error');
  const boton = event.target;
  
  if(!correo) {
    mostrarError('correo-error', 'El correo es obligatorio.');
    return;
  }
  
  // Validar formato de email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  if(!emailRegex.test(correo)) {
    mostrarError('correo-error', 'Ingresa un correo válido.');
    return;
  }
  
  // Deshabilitar botón mientras se procesa
  boton.disabled = true;
  boton.textContent = 'Enviando...';
  
  try {
    const response = await fetch('/api/solicitar-recuperacion/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': obtenerCSRFToken()
      },
      body: JSON.stringify({ email: correo })
    });
    
    const data = await response.json();
    
    if(data.success) {
      // Guardar el email para las siguientes peticiones
      userEmail = correo;
      mostrarPantalla('codigo');
    } else {
      mostrarError('correo-error', data.message || 'Error al enviar el código.');
    }
  } catch(error) {
    console.error('Error:', error);
    mostrarError('correo-error', 'Error de conexión. Intenta de nuevo.');
  } finally {
    boton.disabled = false;
    boton.textContent = 'Enviar código';
  }
}

async function verificarCodigo() {
  const codigo = document.getElementById('codigo-input').value.trim();
  const err = document.getElementById('codigo-error');
  const boton = event.target;
  
  if(!codigo) {
    mostrarError('codigo-error', 'Debes ingresar el código.');
    return;
  }
  
  if(codigo.length !== 6) {
    mostrarError('codigo-error', 'El código debe tener 6 dígitos.');
    return;
  }
  
  if(!userEmail) {
    mostrarError('codigo-error', 'Sesión inválida. Vuelve a solicitar el código.');
    return;
  }
  
  boton.disabled = true;
  boton.textContent = 'Verificando...';
  
  try {
    const response = await fetch('/api/verificar-codigo/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': obtenerCSRFToken()
      },
      body: JSON.stringify({ 
        email: userEmail,
        codigo: codigo 
      })
    });
    
    const data = await response.json();
    
    if(data.success) {
      mostrarPantalla('reset');
    } else {
      mostrarError('codigo-error', data.message || 'Código incorrecto.');
    }
  } catch(error) {
    console.error('Error:', error);
    mostrarError('codigo-error', 'Error de conexión. Intenta de nuevo.');
  } finally {
    boton.disabled = false;
    boton.textContent = 'Verificar código';
  }
}

async function guardarNueva() {
  const p1 = document.getElementById('newpass').value;
  const p2 = document.getElementById('confpass').value;
  const codigo = document.getElementById('codigo-input').value.trim();
  const err = document.getElementById('reset-error');
  const boton = event.target;

  if(!p1 || !p2) {
    mostrarError('reset-error', 'Ambos campos son obligatorios.');
    return;
  }
  
  if(p1 !== p2) {
    mostrarError('reset-error', 'Las contraseñas no coinciden.');
    return;
  }
  
  if(p1.length < 8) {
    mostrarError('reset-error', 'La contraseña debe tener al menos 8 caracteres.');
    return;
  }
  
  if(!userEmail || !codigo) {
    mostrarError('reset-error', 'Sesión inválida. Vuelve a solicitar el código.');
    return;
  }
  
  boton.disabled = true;
  boton.textContent = 'Guardando...';
  
  try {
    const response = await fetch('/api/restablecer-password/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-CSRFToken': obtenerCSRFToken()
      },
      body: JSON.stringify({ 
        email: userEmail,
        codigo: codigo,
        password: p1,
        confirm_password: p2
      })
    });
    
    const data = await response.json();
    
    if(data.success) {
      // Limpiar el email
      userEmail = null;
      mostrarPantalla('success');
    } else {
      mostrarError('reset-error', data.message || 'Error al restablecer la contraseña.');
    }
  } catch(error) {
    console.error('Error:', error);
    mostrarError('reset-error', 'Error de conexión. Intenta de nuevo.');
  } finally {
    boton.disabled = false;
    boton.textContent = 'Guardar nueva contraseña';
  }
}

function irLogin() {
  window.location.href = "/login/"; 
}

// Mostrar pantalla inicial (correo)
mostrarPantalla('correo');

