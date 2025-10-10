from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Factura, DetalleFactura
from .services import enviar_a_intermediario
from django.core.mail import send_mail
from datetime import date
from django.core.paginator import Paginator
from io import BytesIO
import json, traceback, os

# === Librerías adicionales ===
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import qrcode       # Generar códigos QR
import base64       # Convertir imágenes a texto base64 para mostrar en HTML

# ----------------------------------------------------------------------------------------
# VISTA: CREAR FACTURA
# ----------------------------------------------------------------------------------------
def crear_factura(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            # Validar campos obligatorios
            campos_obligatorios = ["nombre_receptor", "nit_receptor", "correo_cliente", "productos"]
            for campo in campos_obligatorios:
                if campo not in data or not data[campo]:
                    return JsonResponse({"status": "error", "message": f"El campo '{campo}' es obligatorio."}, status=400)

            # Validar que haya productos
            if not isinstance(data["productos"], list) or len(data["productos"]) == 0:
                return JsonResponse({"status": "error", "message": "Debe agregar al menos un producto."}, status=400)

            # Crear factura principal
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

            # Guardar detalle de productos
            for prod in data["productos"]:
                DetalleFactura.objects.create(
                    factura=factura,
                    producto=prod.get("producto", ""),
                    cantidad=prod.get("cantidad", 0),
                    precio=prod.get("precio", 0),
                    iva=prod.get("iva", 0),
                    total=prod.get("total", 0)
                )

            # Generar CUFE real
            cufe = enviar_a_intermediario(factura)
            factura.cufe_factura = cufe
            factura.save()

            # Enviar correo al cliente
            if factura.correo_cliente:
                send_mail(
                    subject=f"Factura #{factura.id} - EcoFact",
                    message=f"Gracias por su compra.\nTotal: {factura.total_factura}\nCUFE: {factura.cufe_factura}",
                    from_email="medinathalia76@gmail.com",
                    recipient_list=[factura.correo_cliente],
                    fail_silently=False,
                )

            # URLs de descarga
            pdf_url = f"/facturas/pdf/{factura.id}/"
            xml_url = f"/facturas/xml/{factura.id}/"

            return JsonResponse({
                "status": "ok",
                "id_factura": factura.id,
                "cufe": factura.cufe_factura,
                "total": factura.total_factura,
                "pdf_url": pdf_url,
                "xml_url": xml_url
            })

        except Exception as e:
            print("Error al crear factura:", str(e))
            traceback.print_exc()
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

    return render(request, "facturas/crear_factura.html")


# ----------------------------------------------------------------------------------------
# FACTURA EXITOSA
# ----------------------------------------------------------------------------------------
def factura_exitosa(request):
    return render(request, "facturas/factura_exitosa.html")


# ----------------------------------------------------------------------------------------
# HISTORIAL DE FACTURAS
# ----------------------------------------------------------------------------------------
def historial_factura(request):
    fecha_inicial = request.GET.get('fecha_inicial')
    fecha_final = request.GET.get('fecha_final')

    facturas = Factura.objects.all().order_by('-id')

    if fecha_inicial and fecha_final:
        facturas = facturas.filter(fecha_factura__range=[fecha_inicial, fecha_final])

    paginator = Paginator(facturas, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'facturas': page_obj,
        'fecha_inicial': fecha_inicial,
        'fecha_final': fecha_final
    }
    return render(request, 'facturas/historial_factura.html', context)


# ----------------------------------------------------------------------------------------
# FACTURA EN HTML (con código QR)
# ----------------------------------------------------------------------------------------
def factura_print(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    detalles = DetalleFactura.objects.filter(factura=factura)

    # === Generar código QR dinámico ===
    qr_data = f"http://{request.get_host()}/facturas/pdf/{factura.id}/"
    qr_img = qrcode.make(qr_data)

    # Convertir el QR en base64 para mostrarlo en HTML
    buffer = BytesIO()
    qr_img.save(buffer, format="PNG")
    qr_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
    buffer.close()

    return render(request, "facturas/factura_print.html", {
        "factura": factura,
        "detalles": detalles,
        "qr_base64": qr_base64
    })


# ----------------------------------------------------------------------------------------
# FACTURA EN PDF (con logos y código QR debajo del CUFE)
# ----------------------------------------------------------------------------------------
def factura_pdf(request, pk):
    factura = get_object_or_404(Factura, pk=pk)
    detalles = DetalleFactura.objects.filter(factura=factura)

    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 10)

    # === LOGOS ===
    ecofact_logo = os.path.join(settings.STATIC_ROOT, "img/logo azul sin fondo.png")
    empresa_logo = os.path.join(settings.STATIC_ROOT, "img/logo empresa.png")

    y = 800
    try:
        if os.path.exists(ecofact_logo):
            p.drawImage(ImageReader(ecofact_logo), 50, y - 40, width=80, height=40)
        if os.path.exists(empresa_logo):
            p.drawImage(ImageReader(empresa_logo), 450, y - 40, width=80, height=40)
    except:
        pass

    # === DATOS EMPRESA ===
    y -= 60
    p.setFont("Helvetica-Bold", 11)
    p.drawString(200, y, "APPLE PEREIRA S.A.S")
    p.setFont("Helvetica", 9)
    p.drawString(200, y - 15, "NIT: 901.234.567-8")
    p.drawString(200, y - 30, "Dirección: Cra 10 #20-30, Pereira, Risaralda")
    p.drawString(200, y - 45, "Teléfono: +57 606 333 4455")
    p.drawString(200, y - 60, "Correo: contacto@applepereira.com")
    p.drawString(200, y - 75, "Régimen: Común")

    # === ENCABEZADO ===
    y -= 100
    p.setFont("Helvetica-Bold", 12)
    p.drawString(230, y, "FACTURA ELECTRÓNICA")

    y -= 50
    p.setFont("Helvetica", 10)
    p.drawString(50, y, f"N° Factura: {factura.id}")
    p.drawString(50, y - 15, f"Fecha: {factura.fecha_factura}")
    p.drawString(50, y - 30, f"Cliente: {factura.nombre_receptor}")
    p.drawString(50, y - 45, f"NIT: {factura.nit_receptor}")
    p.drawString(50, y - 60, f"CUFE: {factura.cufe_factura}")

    # === CÓDIGO QR debajo del CUFE ===
    qr_data = (
        f"Factura N°: {factura.id}\n"
        f"CUFE: {factura.cufe_factura}\n"
        f"Total: ${factura.total_factura}\n"
        f"Fecha: {factura.fecha_factura}"
    )

    qr_img = qrcode.make(qr_data)
    qr_buffer = BytesIO()
    qr_img.save(qr_buffer, format="PNG")
    qr_buffer.seek(0)

    # Mover hacia abajo del CUFE y a la derecha
    y -= 100
    p.drawString(50, y, "Verificación QR:")
    p.drawImage(ImageReader(qr_buffer), 180, y - 20, width=100, height=100)

    y -= 140  # espacio antes de tabla

    # === DETALLES PRODUCTOS ===
    p.setFont("Helvetica-Bold", 10)
    p.drawString(50, y, "Producto")
    p.drawString(230, y, "Cantidad")
    p.drawString(300, y, "Precio")
    p.drawString(370, y, "IVA")
    p.drawString(450, y, "Total")

    y -= 20
    p.setFont("Helvetica", 9)
    for d in detalles:
        p.drawString(50, y, d.producto)
        p.drawString(230, y, str(d.cantidad))
        p.drawString(300, y, f"${d.precio}")
        p.drawString(370, y, f"${d.iva}")
        p.drawString(450, y, f"${d.total}")
        y -= 15

    # === TOTAL ===
    y -= 20
    p.setFont("Helvetica-Bold", 10)
    p.drawString(370, y, "TOTAL:")
    p.drawString(450, y, f"${factura.total_factura}")

    # === PIE DE PÁGINA ===
    y -= 40
    p.setFont("Helvetica-Oblique", 9)
    p.drawString(50, y, "Gracias por confiar en EcoFact.")
    p.drawString(50, y - 15, "Factura generada electrónicamente - No requiere firma.")

    # Finalizar
    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f'inline; filename="Factura_{factura.id}.pdf"'
    return response


# ----------------------------------------------------------------------------------------
# FACTURA EN XML
# ----------------------------------------------------------------------------------------
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
