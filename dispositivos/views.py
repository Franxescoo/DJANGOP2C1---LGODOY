import json
import os
from django.conf import settings
from django.http import Http404, HttpResponse
from django.shortcuts import render
from .services import cargar_dispositivos


def cargar_datos(archivo):
    """Función para abrir y cargar datos desde la carpeta data/."""
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
    """Muestra todas las tarjetas con las zonas y la cantidad de dispositivos."""
    zonas = cargar_datos('zonas.json')
    dispositivos = cargar_datos('dispositivos.json')

    # Cuenta cuántos dispositivos pertenecen a cada zona
    for zona in zonas:
        zona['total_dispositivos'] = sum(
            1 for d in dispositivos if d.get('zona_id') == zona.get('id')
        )

    return render(request, 'dispositivos/zonas.html', {'zonas': zonas})


def detalle_zona(request, zona_id):
    """Muestra métricas, estado de energía y tabla de dispositivos de la zona."""
    zonas = cargar_datos('zonas.json')
    categorias = cargar_datos('categorias.json')
    dispositivos = cargar_datos('dispositivos.json')

    # Busca la zona por su ID; si no existe, genera error 404 controlado
    zona_encontrada = next((z for z in zonas if z.get('id') == zona_id), None)
    if not zona_encontrada:
        raise Http404(f"La zona con ID {zona_id} no fue encontrada.")

    # Diccionario para mapear ID de categoría a su nombre
    nombres_cat = {c.get('id'): c.get('nombre', 'Sin categoría') for c in categorias}

    # Filtra dispositivos de la zona y suma consumos
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

    # Regla: ALERTA si supera el límite, NORMAL en caso contrario
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