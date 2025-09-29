from django.contrib import admin
from .models import Factura

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'nombre_emisor',   
        'nit_emisor',      
        'nombre_receptor',
        'nit_receptor',
        'correo_cliente',
        'telefono',
        'fecha_factura',
        'metodo_pago_factura',
        'total_factura',
        'estado',
    )
    list_filter = ('estado', 'metodo_pago_factura', 'fecha_factura')
    search_fields = ('nombre_receptor', 'correo_cliente', 'nit_receptor', 'cufe_factura')
    date_hierarchy = 'fecha_factura'
    ordering = ('-fecha_factura',)
