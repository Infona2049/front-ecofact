from django.contrib import admin
from .models import (
    Usuario,
    Empresa,

)
# Se cambió el import del modelo DetalleFactura, ahora se importa desde facturas.models
from facturas.models import DetalleFactura 
from facturas.models import HistorialFactura 

# --- MODELO USUARIO ---
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


# --- MODELO EMPRESA ---
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


# --- MODELO DETALLE FACTURA ---
@admin.register(DetalleFactura)
class DetalleFacturaAdmin(admin.ModelAdmin):
    list_display = (
       'id',
       'factura',
       'producto',
       'cantidad',
        'precio',
       'iva',
      'total',
)
list_filter = ('producto',)
search_fields = ('producto', 'factura__cufe_factura')
ordering = ('id',)



# --- MODELO HISTORIAL FACTURA ---
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
