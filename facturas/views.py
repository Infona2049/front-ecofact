from django.shortcuts import render
from django.http import JsonResponse
from .models import Factura, DetalleFactura
from .services import enviar_a_intermediario
import json
import traceback
from datetime import date
from django.core.mail import send_mail #agregado 25/09/2025
from datetime import date, timedelta, datetime #agregado 28/09/2025
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

#----------------------------------------------------------------------------------------

def crear_factura(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            # 1. Crear la factura principal
            factura = Factura.objects.create(
                fecha=date.today(),
                fecha_factura=date.today(),
                metodo_pago_factura=data.get("metodo_pago_factura", "Efectivo"),
                cufe_factura="TEMP",
                sutotal_factura=data.get("subtotal", 0),
                iva_total_factura=data.get("iva", 0),
                total_factura=data.get("total", 0),
                cliente_id=data.get("cliente_id", 1),
                nombre_receptor=data.get("nombre_receptor", ""),
                correo_cliente=data.get("correo_cliente", ""),
                telefono=data.get("telefono", ""),
                direccion=data.get("direccion", "")
            )

            # 2. Crear detalles de productos
            items = data.get("items", [])
            for item in items:
                DetalleFactura.objects.create(
                    factura=factura,
                    producto=item.get("producto", ""),
                    cantidad=item.get("cantidad", 0),
                    precio=item.get("precio", 0),
                    iva=item.get("iva", 0),
                    total=item.get("total", 0),
                )

            # 3. Obtener CUFE real
            cufe = enviar_a_intermediario(factura)
            factura.cufe_factura = cufe
            factura.save()

            # 4. Enviar correo (si tiene email)
            if factura.correo_cliente:
                send_mail(
                    subject=f"Factura #{factura.id} - EcoFact",
                    message=f"Gracias por su compra.\nTotal: {factura.total_factura}\nCUFE: {factura.cufe_factura}",
                    from_email="medinathalia76@gmail.com",
                    recipient_list=[factura.correo_cliente],
                    fail_silently=False,
                )

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

    return render(request, "facturas/crear_factura.html")

def factura_exitosa(request):
    return render(request, "facturas/factura_exitosa.html")

#-----------------------------------------------------------------------------------------
#28/09/2025

@property
def fecha_vencimiento(self):
        # por ejemplo vencimiento 30 días después de la fecha de factura
        return self.fecha_factura + timedelta(days=30)

def historial_factura(request):
    qs = Factura.objects.all().order_by("-id")

    fecha_inicial = request.GET.get("fecha_inicial")
    fecha_final = request.GET.get("fecha_final")
    page = request.GET.get("page", 1)

    if fecha_inicial and fecha_final:
        try:
            start = datetime.strptime(fecha_inicial, "%Y-%m-%d").date()
            end = datetime.strptime(fecha_final, "%Y-%m-%d").date()
            qs = qs.filter(fecha_factura__range=[start, end])
        except ValueError:
            # Formato de fecha inválido -> ignorar filtrado o mostrar mensaje
            pass

    # paginación para no mostrar miles de filas
    paginator = Paginator(qs, 12)  # 12 por página (ajusta)
    try:
        facturas = paginator.page(page)
    except PageNotAnInteger:
        facturas = paginator.page(1)
    except EmptyPage:
        facturas = paginator.page(paginator.num_pages)

    return render(request, "facturas/historial_factura.html", {"facturas": facturas})


#iconos de la tabla

def factura_print(request, pk):
    f = get_object_or_404(Factura, pk=pk)
    return render(request, "facturas/print_factura.html", {"factura": f})

def factura_pdf(request, pk):
    # Genera PDF (con reportlab o librería que prefieras)
    ...

def factura_xml(request, pk):
    # Genera XML con ElementTree
    ...
