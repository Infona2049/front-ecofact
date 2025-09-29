from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_factura, name="crear_factura"),
    path("exitosa/", views.factura_exitosa, name="factura_exitosa"),
    path("historial_factura/", views.historial_factura, name="historial_factura"), #28/09/2025

    # nuevas - 28/09/2025:
    path("<int:pk>/print/", views.factura_print, name="factura_print"),
    path("<int:pk>/pdf/", views.factura_pdf, name="factura_pdf"),
    path("<int:pk>/xml/", views.factura_xml, name="factura_xml"),

]