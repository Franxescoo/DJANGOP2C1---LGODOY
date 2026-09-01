from django.shortcuts import render
from .services import cargar_dispositivos

# Create your views here.
from django.http import HttpResponse

def inicio(request):
    return HttpResponse(
        "<h1>EcoEnergy</h1>"
        "<p>Back End en funcionamiento</p>"
)


def dispositivos_zona(request, zona_id):
    if zona_id != 3:
        return HttpResponse(
            "Zona no encontrada", status=404
)
    return HttpResponse(
        f"Dispositivos de la zona {zona_id}"
)


from django.shortcuts import render

def inicio(request):

    contexto = {
    "sistema": "EcoEnergy",
    "mensaje": "Monitoreo energético responsable",
    "asignatura": "Programación Back End",

    }
    return render(
        request,
        "dispositivos/inicio.html",
        contexto,
)

def catalogo(request):
    dispositivos = [
        {"nombre": "Medidor inteligente", "estado": "Activo"},
        {"nombre": "Sensor de temperatura", "estado": "Activo"},
        {"nombre": "Climatizador", "estado": "Revisión"},
    ]
    return render(
        request,
        "dispositivos/catalogo.html",
        {"dispositivos": dispositivos},
    )

def catalogo(request):
    dispositivos = cargar_dispositivos()

    activos = sum(
        1 for item in dispositivos
        if item["estado"] == "Activo"
    )
    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "total_activos": activos,
    }
    return render(
        request, "dispositivos/catalogo.html", contexto
    )
