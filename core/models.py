from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin, BaseUserManager
from django.utils import timezone

# Manager personalizado para el modelo Usuario
class UsuarioManager(BaseUserManager):
    def create_user(self, correo_electronico_usuario, numero_documento_usuario, contraseña_usuario=None, **extra_fields):
        """
        Crea y guarda un usuario con el correo electrónico y número de documento proporcionados.
        """
        if not correo_electronico_usuario:
            raise ValueError('El correo electrónico es obligatorio')
        if not numero_documento_usuario:
            raise ValueError('El número de documento es obligatorio')

        correo_electronico_usuario = self.normalize_email(correo_electronico_usuario)
        usuario = self.model(
            correo_electronico_usuario=correo_electronico_usuario,
            numero_documento_usuario=numero_documento_usuario,
            **extra_fields
        )
        usuario.set_password(contraseña_usuario)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo_electronico_usuario, numero_documento_usuario, contraseña_usuario=None, **extra_fields):
        """
        Crea y guarda un superusuario con los permisos adecuados.
        """
        extra_fields.setdefault('rol_usuario', 'admin')
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('rol_usuario') != 'admin':
            raise ValueError('El superusuario debe tener rol "admin"')
        if not extra_fields.get('is_staff'):
            raise ValueError('El superusuario debe tener is_staff=True')
        if not extra_fields.get('is_superuser'):
            raise ValueError('El superusuario debe tener is_superuser=True')

        return self.create_user(correo_electronico_usuario, numero_documento_usuario, contraseña_usuario, **extra_fields)


class Usuario(AbstractBaseUser , PermissionsMixin):
    """
    Modelo personalizado de usuario que extiende AbstractBaseUser  para autenticación.
    """
    id_usuario = models.AutoField(primary_key=True, db_column='id_usuario')
    nombre_usuario = models.CharField(max_length=30, db_column='nombre_usuario', null=True, blank=True)
    segundo_nombre_usuario = models.CharField(max_length=30, db_column='segundo_nombre_usuario', null=True, blank=True)
    apellido_usuario = models.CharField(max_length=30, db_column='apellido_usuario', null=True, blank=True)
    segundo_apellido_usuario = models.CharField(max_length=30, db_column='segundo_apellido_usuario', null=True, blank=True)

    TIPO_DOCUMENTO_CHOICES = [
        ('cc', 'Cédula de ciudadanía'),
        ('ce', 'Cédula de extranjería'),
        ('pa', 'Pasaporte'),
        ('ppt', 'PPT'),
        ('nit', 'NIT'),
        ('cif', 'CIF'),
        ('ruc', 'RUC'),
    ]
    tipo_documento_usuario = models.CharField(
        max_length=3,
        choices=TIPO_DOCUMENTO_CHOICES,
        db_column='tipo_documento_usuario',
        default='cc'
    )

    numero_documento_usuario = models.CharField(
        unique=True,
        max_length=15,
        db_column='numero_documento_usuario'
    )
    correo_electronico_usuario = models.EmailField(
        unique=True,
        max_length=100,
        db_column='correo_electronico_usuario'
    )
    # La contraseña se maneja con AbstractBaseUser  (campo password)
    direccion_usuario = models.CharField(max_length=100, db_column='direccion_usuario', null=True, blank=True)
    telefono_usuario = models.CharField(max_length=15, db_column='telefono_usuario', null=True, blank=True)

    ROL_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('cliente', 'Cliente'),
    ]
    rol_usuario = models.CharField(
        max_length=10,
        choices=ROL_USUARIO_CHOICES,
        db_column='rol_usuario',
        null=True,
        blank=True
    )

    fecha_creacion_usuario = models.DateTimeField(db_column='fecha_creacion_usuario', auto_now_add=True)

    # Campos requeridos para AbstractBaseUser 
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'correo_electronico_usuario'
    REQUIRED_FIELDS = ['numero_documento_usuario']

    class Meta:
        managed = False
        db_table = 'usuarios'

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido_usuario} ({self.rol_usuario})"


class Producto(models.Model):
    """
    Modelo que representa un producto electrodoméstico.
    """
    id_producto = models.AutoField(primary_key=True, db_column='id_producto')
    nombre_producto = models.CharField(max_length=50, db_column='nombre_producto', null=True, blank=True)

    CATEGORIA_PRODUCTO_CHOICES = [
        ('Dispositivo', 'Dispositivo'),
        ('Auricular', 'Auricular'),
        ('Cargador', 'Cargador'),
    ]
    categoria_producto = models.CharField(
        max_length=20,
        choices=CATEGORIA_PRODUCTO_CHOICES,
        db_column='categoria_producto',
        null=True,
        blank=True
    )

    modelo_producto = models.CharField(max_length=50, db_column='modelo_producto', null=True, blank=True)
    capacidad_producto = models.IntegerField(db_column='capacidad_producto', null=True, blank=True)
    color_producto = models.CharField(max_length=20, db_column='color_producto', null=True, blank=True)
    descripcion_producto = models.TextField(db_column='descripcion_producto', null=True, blank=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_producto', null=True, blank=True)
    codigo_barras_producto = models.CharField(unique=True, max_length=100, db_column='codigo_barras_producto')
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2, db_column='iva_producto', null=True, blank=True)
    imagen_producto = models.ImageField(
        upload_to='productos/',
        db_column='imagen_producto',
        null=True,
        blank=True,
        unique=True
    )

    class Meta:
        managed = False
        db_table = 'productos'

    def __str__(self):
        return self.nombre_producto or "Producto sin nombre"


class Inventario(models.Model):
    """
    Modelo que representa el inventario de productos.
    """
    id_inventario = models.AutoField(primary_key=True, db_column='id_inventario')
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto')
    stock_actual_inventario = models.IntegerField(db_column='stock_actual_inventario', default=0)
    stock_minimo_inventario = models.IntegerField(db_column='stock_minimo_inventario', default=1)
    fecha_actualizacion_inventario = models.DateTimeField(db_column='fecha_actualizacion_inventario', auto_now=True)
    codigo_barras_inventario = models.CharField(unique=True, max_length=100, db_column='codigo_barras_inventario')
    imagen_inventario = models.ImageField(
        upload_to='inventario/',
        db_column='imagen_inventario',
        null=True,
        blank=True,
        unique=True
    )

    class Meta:
        managed = False
        db_table = 'inventario'

    def __str__(self):
        return f"Inventario de {self.id_producto.nombre_producto} (Stock: {self.stock_actual_inventario})"


class Factura(models.Model):
    """
    Modelo que representa una factura electrónica.
    """
    id_factura = models.AutoField(primary_key=True, db_column='id_factura')
    fecha_factura = models.DateField(db_column='fecha_factura', null=True, blank=True)
    id_cliente = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_cliente')

    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]
    metodo_pago_factura = models.CharField(
        max_length=15,
        choices=METODO_PAGO_CHOICES,
        db_column='metodo_pago_factura',
        null=True,
        blank=True
    )

    cufe_factura = models.CharField(unique=True, max_length=255, db_column='cufe_factura', null=True, blank=True)
    subtotal_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='subtotal_factura', null=True, blank=True)
    iva_total_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='iva_total_factura', null=True, blank=True)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_factura', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'factura'

    def __str__(self):
        return f"Factura #{self.id_factura} - Cliente: {self.id_cliente.nombre_usuario}"


class DetalleFactura(models.Model):
    """
    Modelo que representa el detalle de cada factura.
    """
    id_detalle_factura = models.AutoField(primary_key=True, db_column='id_detalle_factura')
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura')
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto')
    cantidad_detalle_factura = models.IntegerField(db_column='cantidad_detalle_factura', null=True, blank=True)
    precio_unitario_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_unitario_detalle_factura', null=True, blank=True)
    subtotal_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='subtotal_detalle_factura', null=True, blank=True)
    iva_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='iva_detalle_factura', null=True, blank=True)
    total_detalle_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_detalle_factura', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'detalle_factura'

    def __str__(self):
        return f"Detalle Factura #{self.id_factura.id_factura} - Producto: {self.id_producto.nombre_producto}"


class HistorialFactura(models.Model):
    """
    Modelo que registra el historial de eventos de una factura.
    """
    id_historial_factura = models.AutoField(primary_key=True, db_column='id_historial_factura')
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura')
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    fecha_de_evento = models.DateTimeField(db_column='fecha_de_evento', auto_now_add=True)

    EVENTO_HISTORIAL_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    evento_historial_factura = models.CharField(
        max_length=10,
        choices=EVENTO_HISTORIAL_CHOICES,
        db_column='evento_historial_factura',
        null=True,
        blank=True
    )
    observacion_historial_factura = models.TextField(db_column='observacion_historial_factura', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'historial_factura'

    def __str__(self):
        return f"Historial Factura #{self.id_factura.id_factura} - Evento: {self.evento_historial_factura}"


class Empresa(models.Model):
    """
    Modelo que representa la empresa que usa el sistema.
    """
    id_empresa = models.AutoField(primary_key=True, db_column='id_empresa')
    nombre_empresa = models.CharField(max_length=100, db_column='nombre_empresa', null=True, blank=True)
    nit_empresa = models.CharField(unique=True, max_length=15, db_column='nit_empresa', null=True, blank=True)
    direccion_empresa = models.CharField(max_length=150, db_column='direccion_empresa', null=True, blank=True)
    telefono_empresa = models.CharField(max_length=15, db_column='telefono_empresa', null=True, blank=True)
    correo_empresa = models.EmailField(max_length=100, db_column='correo_empresa', null=True, blank=True)

    REGIMEN_EMPRESA_CHOICES = [
        ('Simplificado', 'Simplificado'),
        ('Comun', 'Común'),
        ('Especial', 'Especial'),
    ]
    regimen_empresa = models.CharField(
        max_length=15,
        choices=REGIMEN_EMPRESA_CHOICES,
        db_column='regimen_empresa',
        default='Comun'
    )

    representante_legal = models.CharField(max_length=100, db_column='representante_legal', null=True, blank=True)
    fecha_creacion_empresa = models.DateTimeField(db_column='fecha_creacion_empresa', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'empresa'

    def __str__(self):
        return self.nombre_empresa or "Empresa sin nombre"