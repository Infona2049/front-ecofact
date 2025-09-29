
from django.contrib import admin
from .models import Factura

# Register your models here.

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'id',                   # antes 'id_factura'
        'fecha_factura',
        'metodo_pago_factura',
        'cufe_factura',
        'sutotal_factura',
        'iva_total_factura',
        'total_factura',
        'cliente_id',
)