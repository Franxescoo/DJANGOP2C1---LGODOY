"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

app_name = "dispositivos"

urlpatterns = [
    path("", views.inicio, name="inicio"),
    path("dispositivos/", views.catalogo, name="catalogo"),
    
    # Rutas para las Zonas
    path("zonas/", views.listar_zonas, name="zonas"),
    path("zonas/<int:zona_id>/", views.detalle_zona, name="detalle_zona"),
    
    # Tu ruta anterior (opcional por si la usas en otro lado)
    path("zonas/<int:zona_id>/dispositivos/", views.dispositivos_zona, name="por_zona"),
]