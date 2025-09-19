from django.contrib import admin
from .models import (
    Usuario,
    Empresa,
    Factura,
    DetalleFactura,
    HistorialFactura
)

@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = (
        'id_usuario',
        'username',
        'nombre_usuario',
        'apellido_usuario',
        'correo_electronico_usuario',
        'rol_usuario',
        'fecha_creacion_usuario',
    )
    list_filter = ('rol_usuario', 'tipo_documento_usuario')
    search_fields = (
        'username',
        'nombre_usuario',
        'apellido_usuario',
        'correo_electronico_usuario',
        'numero_documento_usuario',
    )
    ordering = ('id_usuario',)

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = (
        'id_empresa',
        'nombre_empresa',
        'nit_empresa',
        'regimen_empresa',
        'representante_legal',
        'fecha_creacion_empresa',
    )
    list_filter = ('regimen_empresa',)
    search_fields = ('nombre_empresa', 'nit_empresa', 'representante_legal')
    ordering = ('id_empresa',)

@admin.register(Factura)
class FacturaAdmin(admin.ModelAdmin):
    list_display = (
        'id_factura',
        'fecha_factura',
        'cliente',
        'metodo_pago_factura',
        'cufe_factura',
        'sutotal_factura',
        'iva_total_factura',
        'total_factura',
    )
    list_filter = ('fecha_factura', 'metodo_pago_factura')
    search_fields = ('cliente__nombre_usuario', 'cliente__apellido_usuario', 'cufe_factura')
    date_hierarchy = 'fecha_factura'
    ordering = ('-fecha_factura',)

@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = (
        'id_detalle_factura',
        'factura',
        'producto',
        'cantidad_detalle_factura',
        'precio_unitario_detalle_factura',
        'subtotal_detalle_factura',
        'iva_detalle_factura',
        'total_detalle_factura',
    )
    list_filter = ('producto',)
    search_fields = ('producto__nombre_producto', 'factura__cufe_factura')
    ordering = ('id_detalle_factura',)

@admin.register(HistorialFactura)
class HistorialFacturaAdmin(admin.ModelAdmin):
    list_display = (
        'id_historial_factura',
        'factura',
        'usuario',
        'fecha_de_evento',
        'evento_historial_factura',
        'observacion_historial_factura',
    )
    list_filter = ('evento_historial_factura', 'fecha_de_evento')
    search_fields = ('factura__cufe_factura', 'usuario__correo_electronico_usuario')
    date_hierarchy = 'fecha_de_evento'
    ordering = ('-fecha_de_evento',)