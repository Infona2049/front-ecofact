from django.db import models
from django.contrib.auth.models import AbstractUser

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

CATEGORIA_PRODUCTO_CHOICES = [
    ('Dispositivo', 'Dispositivo'),
    ('Auricular', 'Auricular'),
    ('Cargador', 'Cargador'),
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

    USERNAME_FIELD = 'correo_electronico_usuario'
    REQUIRED_FIELDS = ['nombre_usuario', 'apellido_usuario', 'rol_usuario']

    def __str__(self):
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

    def __str__(self):
        return self.nombre_empresa

class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)
    categoria_producto = models.CharField(max_length=20, choices=CATEGORIA_PRODUCTO_CHOICES)
    modelo_producto = models.CharField(max_length=50)
    capacidad_producto = models.IntegerField()
    color_producto = models.CharField(max_length=20)
    descripcion_producto = models.TextField()
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras_producto = models.CharField(max_length=100, unique=True)
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2)
    imagen_producto = models.ImageField(upload_to='productos/', unique=True)

    def __str__(self):
        return self.nombre_producto

class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock_actual_inventario = models.IntegerField(default=0)
    stock_minimo_inventario = models.IntegerField(default=1)
    fecha_actualizacion_inventario = models.DateTimeField(auto_now=True)
    codigo_barras_inventario = models.CharField(max_length=100, unique=True)
    imagen_inventario = models.ImageField(upload_to='inventario/', unique=True)

    def __str__(self):
        return f"{self.producto.nombre_producto} - Stock: {self.stock_actual_inventario}"

class Factura(models.Model):
    id_factura = models.AutoField(primary_key=True)
    fecha_factura = models.DateField()
    cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    metodo_pago_factura = models.CharField(max_length=15, choices=METODO_PAGO_CHOICES)
    cufe_factura = models.CharField(max_length=255, unique=True)
    sutotal_factura = models.DecimalField(max_digits=10, decimal_places=2)
    iva_total_factura = models.DecimalField(max_digits=10, decimal_places=2)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Factura {self.id_factura} - Cliente: {self.cliente}"

class DetalleFactura(models.Model):
    id_detalle_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    cantidad_detalle_factura = models.IntegerField()
    precio_unitario_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)
    subtotal_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)
    iva_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)
    total_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Detalle {self.id_detalle_factura} - Factura {self.factura.id_factura}"

class HistorialFactura(models.Model):
    id_historial_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_de_evento = models.DateTimeField(auto_now_add=True)
    evento_historial_factura = models.CharField(max_length=10, choices=EVENTO_HISTORIAL_CHOICES)
    observacion_historial_factura = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Historial {self.id_historial_factura} - Factura {self.factura.id_factura}"