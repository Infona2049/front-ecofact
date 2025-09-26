from django.db import models
from datetime import date

class Factura(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre_emisor = models.CharField(max_length=255)
    nit_emisor = models.CharField(max_length=50)
    nombre_receptor = models.CharField(max_length=255)
    nit_receptor = models.CharField(max_length=50)
    correo_cliente = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=30, default="Pendiente")
    # ✅ Agregar este campo
    fecha = models.DateField(default=date.today)

    fecha_factura = models.DateField(default=date.today)
    metodo_pago_factura = models.CharField(max_length=15, default="Efectivo")
    cufe_factura = models.CharField(max_length=255, unique=True, default="TEMP")
    sutotal_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva_total_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente_id = models.IntegerField(default=1)

    class Meta:
        db_table = "facturas_factura"