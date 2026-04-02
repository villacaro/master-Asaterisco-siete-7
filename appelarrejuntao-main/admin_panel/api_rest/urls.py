"""
api_rest/urls.py  –  Rutas de la API REST
Prefijo: /api/  (definido en admin_panel/urls.py)
"""
from django.urls import path
from . import views

urlpatterns = [
    # ── Scraping y Firebase ────────────────────────────────────────
    path('resultados/',              views.resultados,                name='api_resultados'),
    path('publicar/',                views.publicar,                  name='api_publicar'),
    path('usuarios/',                views.usuarios,                  name='api_usuarios'),
    path('health/',                  views.health,                    name='api_health'),

    # ── Control de Sorteos ─────────────────────────────────────────
    path('sorteos/',                               views.sorteos_estado,           name='api_sorteos'),
    path('sorteos/<int:sorteo_id>/venta/',          views.sorteo_registrar_venta,   name='api_sorteo_venta'),

    # ── Módulo Ventas ──────────────────────────────────────────────
    path('ventas/',                                views.ventas_lista,             name='api_ventas_lista'),
    path('ventas/crear/',                          views.ventas_crear,             name='api_ventas_crear'),
    path('ventas/<int:venta_id>/estado/',          views.ventas_actualizar_estado, name='api_ventas_estado'),

    # ── Módulo Pagos ───────────────────────────────────────────────
    path('pagos/',                                 views.pagos_lista,              name='api_pagos_lista'),
    path('pagos/crear/',                           views.pagos_crear,              name='api_pagos_crear'),
    path('pagos/<int:pago_id>/confirmar/',         views.pagos_confirmar,          name='api_pagos_confirmar'),

    # ── Módulo Premios ─────────────────────────────────────────────
    path('premios/',                               views.premios_lista,            name='api_premios_lista'),
    path('premios/crear/',                         views.premios_crear,            name='api_premios_crear'),
    path('premios/<int:premio_id>/pagar/',         views.premios_pagar,            name='api_premios_pagar'),

    # ── Resumen Financiero ─────────────────────────────────────────
    path('resumen/',                               views.resumen_financiero,       name='api_resumen'),
]
