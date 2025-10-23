from django.db import models
from django.contrib.auth.models import AbstractUser
from productos.models import Producto
from facturas.models import Factura

# Opciones para ENUM
TIPO_DOCUMENTO_CHOICES = [
    ('cc', 'Cédula de ciudadanía'),
    ('ce', 'Cédula de extranjería'),
    ('pa', 'Pasaporte'),
    ('ppt', 'Permiso por protección temporal'),
    ('nit', 'NIT'),
    ('cif', 'CIF'),
    ('ruc', 'RUC'),
]

ROL_USUARIO_CHOICES = [
    ('admin', 'Administrador'),
    ('vendedor', 'Vendedor'),
    ('cliente', 'Cliente'),
]

METODO_PAGO_CHOICES = [
    ('Efectivo', 'Efectivo'),
    ('Tarjeta', 'Tarjeta'),
    ('Transferencia', 'Transferencia'),
]

EVENTO_HISTORIAL_CHOICES = [
    ('pendiente', 'Pendiente'),
    ('aprobada', 'Aprobada'),
    ('rechazada', 'Rechazada'),
]

REGIMEN_EMPRESA_CHOICES = [
    ('Simplificado', 'Simplificado'),
    ('Comun', 'Común'),
    ('Especial', 'Especial'),
]

class Usuario(AbstractUser):
    id_usuario = models.AutoField(primary_key=True)
    username = models.CharField(max_length=150, unique=True, null=False, blank=False)
    nombre_usuario = models.CharField(max_length=30)
    segundo_nombre_usuario = models.CharField(max_length=30, blank=True, null=True)
    apellido_usuario = models.CharField(max_length=30)
    segundo_apellido_usuario = models.CharField(max_length=30, blank=True, null=True)
    tipo_documento_usuario = models.CharField(max_length=5, choices=TIPO_DOCUMENTO_CHOICES, default='cc')
    numero_documento_usuario = models.CharField(max_length=15, unique=True)
    correo_electronico_usuario = models.EmailField(max_length=100, unique=True)
    direccion_usuario = models.CharField(max_length=100, blank=True, null=True)
    telefono_usuario = models.CharField(max_length=15, blank=True, null=True)
    rol_usuario = models.CharField(max_length=10, choices=ROL_USUARIO_CHOICES)
    fecha_creacion_usuario = models.DateTimeField(auto_now_add=True)
    intentos_fallidos = models.IntegerField(default=0)

    USERNAME_FIELD = 'correo_electronico_usuario'
    REQUIRED_FIELDS = ['username', 'nombre_usuario', 'apellido_usuario', 'rol_usuario']

    def _str_(self):
        return self.correo_electronico_usuario


class Empresa(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=100)
    nit_empresa = models.CharField(max_length=15, unique=True)
    direccion_empresa = models.CharField(max_length=150)
    telefono_empresa = models.CharField(max_length=15)
    correo_empresa = models.EmailField(max_length=100)
    regimen_empresa = models.CharField(max_length=15, choices=REGIMEN_EMPRESA_CHOICES, default='Comun')
    representante_legal = models.CharField(max_length=100)
    fecha_creacion_empresa = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.nombre_empresa


class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_detalle_factura = models.IntegerField()
    precio_unitario_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)
    iva_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)
    total_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)

    def _str_(self):
        return f"Detalle {self.id_detalle_factura} - Factura {self.factura.id}"


class HistorialFactura(models.Model):
    id_historial_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_de_evento = models.DateTimeField(auto_now_add=True)
    evento_historial_factura = models.CharField(max_length=10, choices=EVENTO_HISTORIAL_CHOICES)
    observacion_historial_factura = models.TextField(blank=True, null=True)

    def _str_(self):
        return f"Historial {self.id_historial_factura} - Factura {self.factura.id}"