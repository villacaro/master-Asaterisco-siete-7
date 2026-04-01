"""
api_rest/urls.py  –  Rutas de la API REST
Prefijo: /api/  (definido en admin_panel/urls.py)
"""
from django.urls import path
from . import views

urlpatterns = [
    path('resultados/',              views.resultados,            name='api_resultados'),
    path('publicar/',                views.publicar,              name='api_publicar'),
    path('usuarios/',                views.usuarios,              name='api_usuarios'),
    path('health/',                  views.health,                name='api_health'),
    # Control de sorteos
    path('sorteos/',                 views.sorteos_estado,        name='api_sorteos'),
    path('sorteos/<int:sorteo_id>/venta/', views.sorteo_registrar_venta, name='api_sorteo_venta'),
]
