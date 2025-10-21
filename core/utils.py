"""
Utilidades para el sistema de recuperación de contraseña
"""
import jwt
import random
import string
from datetime import datetime, timedelta
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone


def generar_codigo_verificacion():
    """Genera un código de verificación de 6 dígitos"""
    return ''.join(random.choices(string.digits, k=6))


def generar_token_jwt(usuario_id, expiracion_horas=1):
    """
    Genera un token JWT para recuperación de contraseña
    
    Args:
        usuario_id: ID del usuario
        expiracion_horas: Horas de validez del token (default: 1 hora)
    
    Returns:
        str: Token JWT
    """
    payload = {
        'usuario_id': usuario_id,
        'exp': datetime.utcnow() + timedelta(hours=expiracion_horas),
        'iat': datetime.utcnow(),
        'tipo': 'password_reset'
    }
    
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


def verificar_token_jwt(token):
    """
    Verifica y decodifica un token JWT
    
    Args:
        token: Token JWT a verificar
    
    Returns:
        dict: Datos del payload si es válido, None si es inválido
    """
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        
        # Verificar que sea un token de recuperación de contraseña
        if payload.get('tipo') != 'password_reset':
            return None
            
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def enviar_email_recuperacion(email_destino, nombre_usuario, codigo_verificacion):
    """
    Envía un email con el código de verificación para recuperar contraseña
    
    Args:
        email_destino: Email del usuario
        nombre_usuario: Nombre del usuario
        codigo_verificacion: Código de 6 dígitos
    
    Returns:
        bool: True si se envió correctamente, False en caso contrario
    """
    asunto = 'Recuperación de Contraseña - EcoFact'
    
    # Contexto para el template
    contexto = {
        'nombre_usuario': nombre_usuario,
        'codigo': codigo_verificacion,
        'vigencia': '1 hora'
    }
    
    # Renderizar el template HTML
    try:
        mensaje_html = render_to_string('core/emails/recuperacion_password.html', contexto)
        mensaje_texto = strip_tags(mensaje_html)
    except:
        # Fallback a mensaje de texto plano si el template no existe
        mensaje_texto = f"""
    Hola {nombre_usuario},
    
    Has solicitado recuperar tu contraseña en EcoFact.
    
    Tu código de verificación es: {codigo_verificacion}
    
    Este código es válido por 1 hora.
    
    Si no solicitaste este cambio, puedes ignorar este mensaje.
    
    Saludos,
    Equipo EcoFact
    """
        mensaje_html = None
    
    try:
        from django.core.mail import EmailMultiAlternatives
        
        email = EmailMultiAlternatives(
            asunto,
            mensaje_texto,
            settings.DEFAULT_FROM_EMAIL,
            [email_destino]
        )
        
        if mensaje_html:
            email.attach_alternative(mensaje_html, "text/html")
        
        email.send(fail_silently=False)
        return True
    except Exception as e:
        print(f"Error al enviar email: {str(e)}")
        return False


def validar_fortaleza_password(password):
    """
    Valida que la contraseña cumpla con requisitos mínimos de seguridad
    
    Args:
        password: Contraseña a validar
    
    Returns:
        tuple: (bool, str) - (es_valida, mensaje_error)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres"
    
    if not any(char.isdigit() for char in password):
        return False, "La contraseña debe contener al menos un número"
    
    if not any(char.isupper() for char in password):
        return False, "La contraseña debe contener al menos una letra mayúscula"
    
    if not any(char.islower() for char in password):
        return False, "La contraseña debe contener al menos una letra minúscula"
    
    return True, "Contraseña válida"
