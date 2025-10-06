from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Factura, DetalleFactura
from .services import enviar_a_intermediario
from django.core.mail import send_mail
from datetime import date, datetime, timedelta
import json, traceback
#////////////////////////////////////////////////////////////////////////////////////////////
from django.http import HttpResponse
#from reportlab.pdfgen import canvas
from io import BytesIO
from django.core.paginator import Paginator
# ----------------------------------------------------------------------------------------
def crear_factura(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            #  Validar que vengan todos los campos
            campos_obligatorios = ["nombre_receptor", "nit_receptor", "correo_cliente", "productos"]
            for campo in campos_obligatorios:
                if campo not in data or not data[campo]:
                    return JsonResponse({"status": "error", "message": f"El campo '{campo}' es obligatorio."}, status=400)

            # Validar que haya al menos un producto
            if not isinstance(data["productos"], list) or len(data["productos"]) == 0:
                return JsonResponse({"status": "error", "message": "Debe agregar al menos un producto."}, status=400)

            #  Crear factura con datos iniciales
            factura = Factura.objects.create(
                nombre_receptor=data["nombre_receptor"],
                nit_receptor=data["nit_receptor"],
                correo_cliente=data["correo_cliente"],
                telefono=data.get("telefono", ""),
                direccion=data.get("direccion", ""),
                fecha=date.today(),
                fecha_factura=date.today(),
                metodo_pago_factura=data.get("metodo_pago_factura"),
                sutotal_factura=data.get("sutotal_factura", 0),
                iva_total_factura=data.get("iva_total_factura", 0),
                total_factura=data.get("total_factura", 0),
                cufe_factura="TEMP"
            )

            # Guardar detalle de factura
            for prod in data["productos"]:
                DetalleFactura.objects.create(
                    factura=factura,
                    producto=prod.get("nombre", ""),
                    cantidad=prod.get("cantidad", 0),
                    precio=prod.get("precio", 0),
                    iva=prod.get("iva", 0),
                    total=prod.get("total", 0)
                )

            #  Generar CUFE real
            cufe = enviar_a_intermediario(factura)
            factura.cufe_factura = cufe
            factura.save()

            # 5 Enviar correo (si hay correo del cliente)
            if factura.correo_cliente:
                send_mail(
                    subject=f"Factura #{factura.id} - EcoFact",
                    message=f"Gracias por su compra.\nTotal: {factura.total_factura}\nCUFE: {factura.cufe_factura}",
                    from_email="medinathalia76@gmail.com",
                    recipient_list=[factura.correo_cliente],
                    fail_silently=False,
                )

            #  Respuesta exitosa
            return JsonResponse({
                "status": "ok",
                "id_factura": factura.id,
                "cufe": factura.cufe_factura,
                "total": factura.total_factura
            })

        except Exception as e:
            print("Error al crear factura:", str(e))
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    # Si es GET, renderiza la página normalmente
    return render(request, "facturas/crear_factura.html")

def factura_exitosa(request):
    return render(request, "facturas/factura_exitosa.html")


#---------------------------------------------------------------------------------------------

#NUEVO 06/10/2025


def historial_factura(request):
    """
    Vista que muestra el historial de facturas con:
    - Filtro por fecha
    - Paginación
    """

    # --- 1. Capturamos los parámetros GET de las fechas ---
    fecha_inicial = request.GET.get('fecha_inicial')
    fecha_final = request.GET.get('fecha_final')

    # --- 2. Traemos todas las facturas ordenadas por fecha más reciente ---
    facturas = Factura.objects.all().order_by('-fecha_factura')

    # --- 3. Si el usuario seleccionó fechas, filtramos el queryset ---
    if fecha_inicial and fecha_final:
        facturas = facturas.filter(fecha_factura__range=[fecha_inicial, fecha_final])

    # --- 4. Paginamos el resultado: 5 facturas por página ---
    paginator = Paginator(facturas, 5)
    page_number = request.GET.get('page')  # página actual
    page_obj = paginator.get_page(page_number)  # página seleccionada

    # --- 5. Enviamos a la plantilla la página actual y las fechas para mantener el filtro ---
    context = {
        'facturas': page_obj,                # ahora 'facturas' es una página, no un queryset completo
        'fecha_inicial': fecha_inicial,      # para mantener el valor en los campos
        'fecha_final': fecha_final
    }

    return render(request, 'facturas/historial_factura.html', context)



# -----------------------------
# Vista para ver la factura en HTML (imprimir)
# -----------------------------
def factura_print(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    detalles = DetalleFactura.objects.filter(factura=factura)

    return render(request, "facturas/factura_print.html", {
        "factura": factura,
        "detalles": detalles
    })


# -----------------------------
# Vista para generar PDF
# -----------------------------
def factura_pdf(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    detalles = DetalleFactura.objects.filter(factura=factura)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 11)

    # Encabezado
    p.drawString(100, 800, f"Factura #{factura.id}")
    p.drawString(100, 780, f"Cliente: {factura.nombre_receptor}")
    p.drawString(100, 760, f"NIT: {factura.nit_receptor}")
    p.drawString(100, 740, f"Fecha: {factura.fecha_factura}")
    p.drawString(100, 720, f"Total: ${factura.total_factura}")

    # Tabla de productos
    y = 690
    p.drawString(100, y, "Producto")
    p.drawString(250, y, "Cantidad")
    p.drawString(330, y, "Precio")
    p.drawString(420, y, "IVA")
    p.drawString(480, y, "Total")

    y -= 20
    for d in detalles:
        p.drawString(100, y, d.producto)
        p.drawString(250, y, str(d.cantidad))
        p.drawString(330, y, f"${d.precio}")
        p.drawString(420, y, f"${d.iva}")
        p.drawString(480, y, f"${d.total}")
        y -= 20

    p.showPage()
    p.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="Factura_{factura.id}.pdf"'
    return response


# -----------------------------
# Vista para generar XML (opcional)
# -----------------------------
def factura_xml(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    detalles = DetalleFactura.objects.filter(factura=factura)

    response = HttpResponse(content_type="application/xml")
    response["Content-Disposition"] = f'attachment; filename="Factura_{factura.id}.xml"'

    response.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    response.write("<factura>\n")
    response.write(f"  <id>{factura.id}</id>\n")
    response.write(f"  <cliente>{factura.nombre_receptor}</cliente>\n")
    response.write(f"  <nit>{factura.nit_receptor}</nit>\n")
    response.write(f"  <fecha>{factura.fecha_factura}</fecha>\n")
    response.write(f"  <total>{factura.total_factura}</total>\n")
    response.write("  <detalles>\n")
    for d in detalles:
        response.write("    <detalle>\n")
        response.write(f"      <producto>{d.producto}</producto>\n")
        response.write(f"      <cantidad>{d.cantidad}</cantidad>\n")
        response.write(f"      <precio>{d.precio}</precio>\n")
        response.write(f"      <iva>{d.iva}</iva>\n")
        response.write(f"      <total>{d.total}</total>\n")
        response.write("    </detalle>\n")
    response.write("  </detalles>\n")
    response.write("</factura>\n")

    return response