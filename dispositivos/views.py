import json
import os
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from .services import cargar_dispositivos


def cargar_datos(archivo):
    ruta = os.path.join(settings.BASE_DIR, 'data', archivo)
    if not os.path.exists(ruta):
        return []
    with open(ruta, 'r', encoding='utf-8') as f:
        return json.load(f)


def inicio(request):
    contexto = {
        "sistema": "EcoEnergy",
        "mensaje": "Monitoreo energético responsable",
        "asignatura": "Programación Back End",
    }
    return render(request, "dispositivos/inicio.html", contexto)


def catalogo(request):
    dispositivos = cargar_dispositivos()
    activos = sum(
        1 for item in dispositivos
        if item.get("estado") == "Activo"
    )
    contexto = {
        "dispositivos": dispositivos,
        "total": len(dispositivos),
        "total_activos": activos,
    }
    return render(request, "dispositivos/catalogo.html", contexto)


def listar_zonas(request):
    zonas = cargar_datos('zonas.json')
    dispositivos = cargar_datos('dispositivos.json')

    for zona in zonas:
        zona['total_dispositivos'] = sum(
            1 for d in dispositivos if d.get('zona_id') == zona.get('id')
        )

    return render(request, 'dispositivos/zonas.html', {'zonas': zonas})


def detalle_zona(request, zona_id):
    zonas = cargar_datos('zonas.json')
    categorias = cargar_datos('categorias.json')
    dispositivos = cargar_datos('dispositivos.json')

    zona_encontrada = next((z for z in zonas if z.get('id') == zona_id), None)
    if not zona_encontrada:
        raise Http404(f"La zona con ID {zona_id} no fue encontrada.")

    nombres_cat = {c.get('id'): c.get('nombre', 'Sin categoría') for c in categorias}

    mis_dispositivos = []
    consumo_acumulado = 0.0

    for d in dispositivos:
        if d.get('zona_id') == zona_id:
            consumo = float(d.get('consumo_kwh', 0.0))
            consumo_acumulado += consumo
            mis_dispositivos.append({
                'nombre': d.get('nombre'),
                'categoria': nombres_cat.get(d.get('categoria_id'), 'General'),
                'consumo_kwh': consumo
            })

    limite = float(zona_encontrada.get('limite_kwh', 0.0))
    if consumo_acumulado > limite:
        estado_energia = "ALERTA"
    else:
        estado_energia = "NORMAL"

    contexto = {
        'zona': zona_encontrada,
        'dispositivos': mis_dispositivos,
        'consumo_total': round(consumo_acumulado, 2),
        'cantidad': len(mis_dispositivos),
        'estado': estado_energia,
    }

    return render(request, 'dispositivos/detalle_zona.html', contexto)


def dispositivos_zona(request, zona_id):
    if zona_id != 3:
        return HttpResponse("Zona no encontrada", status=404)
    return HttpResponse(f"Dispositivos de la zona {zona_id}")


def resumen_zonas(request):
    zonas = cargar_datos('zonas.json')
    dispositivos = cargar_datos('dispositivos.json')

    resumen = []
    consumo_total_general = 0.0

    for zona in zonas:
        zona_id = zona.get('id')
        limite_kwh = float(zona.get('limite_kwh', 0.0))

        dispositivos_de_zona = [
            d for d in dispositivos if d.get('zona_id') == zona_id
        ]

        cantidad = len(dispositivos_de_zona)
        consumo_zona = round(sum(float(d.get('consumo_kwh', 0.0)) for d in dispositivos_de_zona), 2)
        consumo_total_general += consumo_zona

        if consumo_zona <= limite_kwh:
            estado_texto = "DENTRO DEL LÍMITE"
            clase_badge = "bg-success"
        else:
            estado_texto = "LÍMITE SUPERADO"
            clase_badge = "bg-danger"

        resumen.append({
            'id': zona_id,
            'nombre': zona.get('nombre'),
            'dispositivos': cantidad,
            'consumo': consumo_zona,
            'limite': limite_kwh,
            'estado': estado_texto,
            'clase_badge': clase_badge,
        })

    contexto = {
        'total_zonas': len(zonas),
        'total_dispositivos': len(dispositivos),
        'consumo_total_general': round(consumo_total_general, 2),
        'resumen_zonas': resumen,
    }

    return render(request, 'dispositivos/resumen_zonas.html', contexto)