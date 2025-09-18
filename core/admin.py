from django.contrib import admin
from .models import (
    Usuario,
    Empresa,
    Producto,
    Inventario,
    Factura,
    DetalleFactura,
    HistorialFactura
)

admin.site.register(Usuario)
admin.site.register(Empresa)
admin.site.register(Producto)
admin.site.register(Inventario)
admin.site.register(Factura)
admin.site.register(DetalleFactura)
admin.site.register(HistorialFactura)