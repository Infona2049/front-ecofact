from django.db import models
from datetime import date
from core.models import Usuario 

# Opciones del historial (ajústalas si ya las tienes definidas en otro archivo)
EVENTO_HISTORIAL_CHOICES = [
    ("CREADA", "Factura creada"),
    ("ACTUALIZADA", "Factura actualizada"),
    ("ELIMINADA", "Factura eliminada"),
    ("ENVIADA", "Factura enviada"),
]


# MODELO DE FACTURA
class Factura(models.Model): 
    id = models.BigAutoField(primary_key=True)
    nombre_emisor = models.CharField(max_length=255, default="Apple S.A.S")
    nit_emisor = models.CharField(max_length=50, default="4587128-141")
    nombre_receptor = models.CharField(max_length=255)
    nit_receptor = models.CharField(max_length=50)
    correo_cliente = models.EmailField()
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    estado = models.CharField(max_length=30, default="Pendiente")
    fecha = models.DateField(default=date.today)
    fecha_factura = models.DateField(default=date.today)
    metodo_pago_factura = models.CharField(max_length=15)
    cufe_factura = models.CharField(max_length=255, unique=True, default="TEMP")
    sutotal_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    iva_total_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_factura = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    cliente_id = models.IntegerField(default=1)

    class Meta:
        db_table = "facturas_factura"

    def __str__(self):
        return f"Factura {self.id} - {self.nombre_receptor}"


# MODELO DE DETALLE DE FACTURA
class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name="detalles", on_delete=models.CASCADE)
    producto = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.producto} (x{self.cantidad}) - Factura {self.factura.id}"


# MODELO DE HISTORIAL DE FACTURA
class HistorialFactura(models.Model):
    id_historial_factura = models.AutoField(primary_key=True)
    factura = models.ForeignKey(Factura, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_de_evento = models.DateTimeField(auto_now_add=True)
    evento_historial_factura = models.CharField(max_length=20, choices=EVENTO_HISTORIAL_CHOICES)
    observacion_historial_factura = models.TextField(blank=True, null=True)

    def __str__(self):  # ✅ corregido
        return f"Historial {self.id_historial_factura} - Factura {self.factura.id}"
