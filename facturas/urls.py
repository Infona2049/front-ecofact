from django.urls import path
from . import views

urlpatterns = [
    path("crear/", views.crear_factura, name="crear_factura"),
    path("exitosa/", views.factura_exitosa, name="factura_exitosa"),
]