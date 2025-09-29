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
    # Agregar este campo
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
        app_label = "facturas"  # fuerza a que se registre bajo facturas


#EN ESTA PARTE SE SIGUE TRABAJANDO YA QUE SE NECESITA MODIFICAR LA BASE DE DATOS

class DetalleFactura(models.Model):
    factura = models.ForeignKey(Factura, related_name="detalles", on_delete=models.CASCADE)
    producto = models.CharField(max_length=200)
    cantidad = models.IntegerField()
    precio = models.DecimalField(max_digits=12, decimal_places=2)
    iva = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.producto} (x{self.cantidad}) - Factura {self.factura.id}"

