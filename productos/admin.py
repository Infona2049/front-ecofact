from django.contrib import admin
from .models import (
    Inventario,
    Producto
)


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'id_producto',
        'nombre_producto',
        'categoria_producto',
        'modelo_producto',
        'capacidad_producto',
        'color_producto',
        'precio_producto',
        'codigo_barras_producto',
    )
    list_filter = ('categoria_producto', 'color_producto', 'modelo_producto', 'capacidad_producto')
    search_fields = ('nombre_producto', 'modelo_producto', 'codigo_barras_producto')
    ordering = ('id_producto',)

@admin.register(Inventario)
class InventarioAdmin(admin.ModelAdmin):
    list_display = (
        'id_inventario',
        'producto',
        'stock_actual_inventario',
        'stock_minimo_inventario',
        'fecha_actualizacion_inventario',
        'codigo_barras_inventario',
    )
    list_filter = ('producto',)
    search_fields = ('producto__nombre_producto', 'codigo_barras_inventario')
    ordering = ('-fecha_actualizacion_inventario',)