from django.db import models

# Modelo para la tabla USUARIOS
class Usuario(models.Model):
    id_usuario = models.IntegerField(primary_key=True, db_column='id_usuario')
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
    tipo_documento_usuario = models.CharField(max_length=3, choices=TIPO_DOCUMENTO_CHOICES, db_column='tipo_documento_usuario', default='cc')
    
    numero_documento_usuario = models.CharField(unique=True, max_length=15, db_column='numero_documento_usuario')
    correo_electronico_usuario = models.CharField(unique=True, max_length=100, db_column='correo_electronico_usuario')
    contraseña_usuario = models.CharField(max_length=100, db_column='contraseña_usuario', null=True, blank=True) # Considera usar un campo de contraseña más seguro en Django
    direccion_usuario = models.CharField(max_length=100, db_column='direccion_usuario', null=True, blank=True)
    telefono_usuario = models.CharField(max_length=15, db_column='telefono_usuario', null=True, blank=True)
    
    ROL_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('vendedor', 'Vendedor'),
        ('cliente', 'Cliente'),
    ]
    rol_usuario = models.CharField(max_length=10, choices=ROL_USUARIO_CHOICES, db_column='rol_usuario', null=True, blank=True) # Ajusta si tiene un default en DB
    
    fecha_creacion_usuario = models.DateTimeField(db_column='fecha_creacion_usuario', auto_now_add=True) # auto_now_add para CURRENT_TIMESTAMP

    class Meta:
        managed = False  # Indica a Django que no gestione la creación/modificación de esta tabla
        db_table = 'usuarios' # Nombre exacto de la tabla en PostgreSQL

    def __str__(self):
        return f"{self.nombre_usuario} {self.apellido_usuario} ({self.rol_usuario})"

# Modelo para la tabla PRODUCTOS
class Producto(models.Model):
    id_producto = models.IntegerField(primary_key=True, db_column='id_producto')
    nombre_producto = models.CharField(max_length=50, db_column='nombre_producto', null=True, blank=True)
    
    CATEGORIA_PRODUCTO_CHOICES = [
        ('Dispositivo', 'Dispositivo'),
        ('Auricular', 'Auricular'),
        ('Cargador', 'Cargador'),
    ]
    categoria_producto = models.CharField(max_length=20, choices=CATEGORIA_PRODUCTO_CHOICES, db_column='categoria_producto', null=True, blank=True)
    
    modelo_producto = models.CharField(max_length=50, db_column='modelo_producto', null=True, blank=True)
    capacidad_producto = models.IntegerField(db_column='capacidad_producto', null=True, blank=True)
    color_producto = models.CharField(max_length=20, db_column='color_producto', null=True, blank=True)
    descripcion_producto = models.TextField(db_column='descripcion_producto', null=True, blank=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2, db_column='precio_producto', null=True, blank=True)
    codigo_barras_producto = models.CharField(unique=True, max_length=100, db_column='codigo_barras_producto', null=True, blank=True)
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2, db_column='iva_producto', null=True, blank=True)
    imagen_producto = models.CharField(unique=True, max_length=255, db_column='imagen_producto', null=True, blank=True) # Si almacenas la URL de la imagen

    class Meta:
        managed = False
        db_table = 'productos'

    def __str__(self):
        return self.nombre_producto

# Modelo para la tabla INVENTARIO
class Inventario(models.Model):
    id_inventario = models.IntegerField(primary_key=True, db_column='id_inventario')
    # Clave foránea a Producto
    id_producto = models.ForeignKey(Producto, models.DO_NOTHING, db_column='id_producto')
    stock_actual_inventario = models.IntegerField(db_column='stock_actual_inventario', default=0)
    stock_minimo_inventario = models.IntegerField(db_column='stock_minimo_inventario', default=1)
    fecha_actualizacion_inventario = models.DateTimeField(db_column='fecha_actualizacion_inventario', auto_now=True) # auto_now para ON UPDATE CURRENT_TIMESTAMP
    codigo_barras_inventario = models.CharField(unique=True, max_length=100, db_column='codigo_barras_inventario', null=True, blank=True)
    imagen_inventario = models.CharField(unique=True, max_length=255, db_column='imagen_inventario', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'inventario'

    def __str__(self):
        return f"Inventario de {self.id_producto.nombre_producto} (Stock: {self.stock_actual_inventario})"

# Modelo para la tabla FACTURA
class Factura(models.Model):
    id_factura = models.IntegerField(primary_key=True, db_column='id_factura')
    fecha_factura = models.DateField(db_column='fecha_factura', null=True, blank=True)
    # Clave foránea a Usuario (cliente)
    id_cliente = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_cliente')
    
    METODO_PAGO_CHOICES = [
        ('Efectivo', 'Efectivo'),
        ('Tarjeta', 'Tarjeta'),
        ('Transferencia', 'Transferencia'),
    ]
    metodo_pago_factura = models.CharField(max_length=15, choices=METODO_PAGO_CHOICES, db_column='metodo_pago_factura', null=True, blank=True)
    
    cufe_factura = models.CharField(unique=True, max_length=255, db_column='cufe_factura', null=True, blank=True)
    sutotal_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='sutotal_factura', null=True, blank=True)
    iva_total_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='iva_total_factura', null=True, blank=True)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, db_column='total_factura', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'factura' # Asegúrate que el nombre de la tabla sea 'factura' en minúsculas si es así en DB

    def __str__(self):
        return f"Factura #{self.id_factura} - Cliente: {self.id_cliente.nombre_usuario}"

# Modelo para la tabla DETALLE FACTURA
class DetalleFactura(models.Model):
    id_detalle_factura = models.IntegerField(primary_key=True, db_column='id_detalle_factura')
    # Clave foránea a Factura
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura')
    # Clave foránea a Producto
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

# Modelo para la tabla HISTORIAL_FACTURA
class HistorialFactura(models.Model):
    id_historial_factura = models.IntegerField(primary_key=True, db_column='id_historial_factura')
    # Clave foránea a Factura
    id_factura = models.ForeignKey(Factura, models.DO_NOTHING, db_column='id_factura')
    # Clave foránea a Usuario (quien realizó el evento)
    id_usuario = models.ForeignKey(Usuario, models.DO_NOTHING, db_column='id_usuario')
    fecha_de_evento = models.DateTimeField(db_column='fecha_de_evento', auto_now_add=True)
    
    EVENTO_HISTORIAL_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]
    evento_historial_factura = models.CharField(max_length=10, choices=EVENTO_HISTORIAL_CHOICES, db_column='evento_historial_factura', null=True, blank=True)
    
    observacion_historial_factura = models.TextField(db_column='observacion_historial_factura', null=True, blank=True)

    class Meta:
        managed = False
        db_table = 'historial_factura'

    def __str__(self):
        return f"Historial Factura #{self.id_factura.id_factura} - Evento: {self.evento_historial_factura}"

# Modelo para la tabla EMPRESA
class Empresa(models.Model):
    id_empresa = models.IntegerField(primary_key=True, db_column='id_empresa')
    nombre_empresa = models.CharField(max_length=100, db_column='nombre_empresa', null=True, blank=True)
    nit_empresa = models.CharField(unique=True, max_length=15, db_column='nit_empresa', null=True, blank=True)
    direccion_empresa = models.CharField(max_length=150, db_column='direccion_empresa', null=True, blank=True)
    telefono_empresa = models.CharField(max_length=15, db_column='telefono_empresa', null=True, blank=True)
    correo_empresa = models.CharField(max_length=100, db_column='correo_empresa', null=True, blank=True)
    
    REGIMEN_EMPRESA_CHOICES = [
        ('Simplificado', 'Simplificado'),
        ('Comun', 'Común'),
        ('Especial', 'Especial'),
    ]
    regimen_empresa = models.CharField(max_length=15, choices=REGIMEN_EMPRESA_CHOICES, db_column='regimen_empresa', default='Comun')
    
    representante_legal = models.CharField(max_length=100, db_column='representante_legal', null=True, blank=True)
    fecha_creacion_empresa = models.DateTimeField(db_column='fecha_creacion_empresa', auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'empresa' # ¡Ojo! El nombre de la tabla en tu DB es 'emprpesa' con 'p' extra. Asegúrate de que sea correcto.

    def __str__(self):
        return self.nombre_empresa

