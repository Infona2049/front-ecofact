from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid

CATEGORIA_PRODUCTO_CHOICES = [
    ('Dispositivo', 'Dispositivo'),
    ('Auricular', 'Auricular'),
    ('Cargador', 'Cargador'),
]

COLOR_PRODUCTO_CHOICES = [
    ('negro', 'Negro'),
    ('blanco', 'Blanco'),
    ('dorado', 'Dorado'),
]


class Producto(models.Model):
    id_producto = models.AutoField(primary_key=True)
    nombre_producto = models.CharField(max_length=50)
    categoria_producto = models.CharField(max_length=20, choices=CATEGORIA_PRODUCTO_CHOICES)
    modelo_producto = models.CharField(max_length=50)
    capacidad_producto = models.CharField(max_length=20, choices=[('No Aplica', 'No Aplica'),('128GB', '128GB'), ('256GB', '256GB'), ('512GB', '512GB')])
    color_producto = models.CharField(max_length=20, choices=COLOR_PRODUCTO_CHOICES)
    descripcion_producto = models.TextField(blank=True, null=True)
    precio_producto = models.DecimalField(max_digits=10, decimal_places=2)
    codigo_barras_producto = models.CharField(max_length=100, unique=True, blank=True)
    iva_producto = models.DecimalField(max_digits=10, decimal_places=2, default=19.00, editable=False)
    imagen_producto = models.ImageField(upload_to='productos/',blank=True, null=True,)

    def save(self, *args, **kwargs):
        if not self.codigo_barras_producto:
            self.codigo_barras_producto = str(uuid.uuid4()).replace('-', '')[:12].upper()
        
        self.iva_producto = 19.00
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre_producto
    
class Inventario(models.Model):
    id_inventario = models.AutoField(primary_key=True)
    producto = models.ForeignKey(Producto, on_delete=models.CASCADE)
    stock_actual_inventario = models.IntegerField(default=0)
    stock_minimo_inventario = models.IntegerField(default=1)
    fecha_actualizacion_inventario = models.DateTimeField(auto_now=True)
    codigo_barras_inventario = models.CharField(max_length=100, unique=True)
    imagen_inventario = models.ImageField(upload_to='inventario/', blank=True, null=True,)

    def __str__(self):
        return f"{self.producto.nombre_producto} - Stock: {self.stock_actual_inventario}"