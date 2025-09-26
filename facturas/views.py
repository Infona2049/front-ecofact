from django.shortcuts import render
from django.http import JsonResponse
from .models import Factura
from .services import enviar_a_intermediario
import json
import traceback
from datetime import date

from django.core.mail import send_mail #agregado 25/09/2025

def crear_factura(request):
    if request.method == "POST":
        data = json.loads(request.body)

        try:
            # 1. Guardamos la factura con un CUFE temporal
            factura = Factura.objects.create(
                fecha=date.today(),  # ✅ asegura que nunca sea NULL
                fecha_factura=date.today(),
                metodo_pago_factura=data.get("metodo_pago_factura", "Efectivo",),
                cufe_factura="TEMP",   # aquí ya no se llama enviar_a_intermediario(None)
                sutotal_factura=data.get("subtotal", 0),
                iva_total_factura=data.get("iva", 0),
                total_factura=data.get("total", 0),
                cliente_id=data.get("cliente_id", 1)
                
            )

        
            # 2. Ahora sí, llamamos al intermediario con la factura real
            cufe = enviar_a_intermediario(factura)

            # 3. Guardamos el CUFE definitivo
            factura.cufe_factura = cufe
            factura.save()

            if hasattr(factura, "correo_cliente") and factura.correo_cliente: #agregado 25/09/2025

                send_mail(
                    subject=f"Factura #{factura.id} - EcoFact",
                    message=f"Gracias por su compra.\nTotal: {factura.total_factura}\nCUFE: {factura.cufe_factura}",
                    from_email="medinathalia76@gmail.com",
                    recipient_list=[factura.correo_cliente],
                    fail_silently=False,
                )
            #agregado 25/09/2025

            return JsonResponse({
                "status": "ok",
                "id_factura": factura.id,   # revisa si en tu modelo es id_factura o id
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