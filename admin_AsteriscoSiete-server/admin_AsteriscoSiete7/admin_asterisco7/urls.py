# -*- coding: utf-8 -*-

from django.conf import settings
from django.urls import include, re_path, path
from django.views.static import serve
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from admin_asterisco7.dashboard_views import dashboard, dashboard_stats, dashboard_api, dashboard_crud, taquilla_view, reportes_page, candidatos_page, monitor_api, liquidacion_page, taquilla_login_api, taquilla_venta_api, taquilla_ventas_lista_api, taquilla_scrape_tuazar, liquidaciones_sorteo_api, candidatos_riesgo_api, cuadre_nivel_superior_api, taquilla_resultados_hoy, taquilla_mi_ip, taquilla_cambiar_clave_api, taquilla_reporte_diario, taquilla_reporte_periodo, taquilla_reporte_caja, taquilla_reporte_tickets, taquilla_reporte_ganadores, taquilla_proxy_resultados
from admin_asterisco7.reportes_views import (
    api_lista_linea, api_por_producto, api_riesgo_venta, api_sorteos_disponibles,
    api_cuadre, api_liquidaciones, api_resumen_admin, api_dias_trabajo,
)

from django.http import HttpResponse
from django.views.generic import RedirectView

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    re_path(r'^health/?$', health_check, name='health_check'),
    re_path(r'^salud/?$', health_check, name='health_check_es'),
    re_path(r'^$', RedirectView.as_view(url='/taquilla/', permanent=False), name='index'),
    # ── Taquilla Venta en Línea (Asterisco *7) ──────────────────────────────────
    # Accesible en: http://127.0.0.1:8001/taquilla/
    re_path(r'^taquilla/$', taquilla_view, name='taquilla'),
    re_path(r'^taquilla/login/$', taquilla_login_api, name='taquilla_login'),
    re_path(r'^taquilla/venta/$', taquilla_venta_api, name='taquilla_venta'),
    re_path(r'^api/taquilla/ventas/$', taquilla_ventas_lista_api, name='taquilla_ventas_lista'),
    re_path(r'^api/taquilla/$', taquilla_ventas_lista_api, name='taquilla_ventas_alias'),
    re_path(r'^api/taquilla/resultados-hoy/$', taquilla_resultados_hoy, name='taquilla_resultados_hoy'),
    path('api/taquilla/api-resultados/', taquilla_proxy_resultados, name='taquilla_proxy_resultados'),
    path('api/taquilla/scrape-tuazar/', taquilla_scrape_tuazar, name='taquilla_scrape_tuazar'),
    re_path(r'^api/taquilla/mi-ip/$', taquilla_mi_ip, name='taquilla_mi_ip'),
    re_path(r'^taquilla/cambiar-clave/$', taquilla_cambiar_clave_api, name='taquilla_cambiar_clave'),
    # ── APIs de Reportes Taquilla → Supabase ───────────────────────────────────
    re_path(r'^taquilla/reportes/analisis-diario/$',  taquilla_reporte_diario,   name='taquilla_rpt_diario'),
    re_path(r'^taquilla/reportes/analisis-periodo/$', taquilla_reporte_periodo,  name='taquilla_rpt_periodo'),
    re_path(r'^taquilla/reportes/cuadre-caja/$',      taquilla_reporte_caja,     name='taquilla_rpt_caja'),
    re_path(r'^taquilla/reportes/tickets/$',          taquilla_reporte_tickets,  name='taquilla_rpt_tickets'),
    re_path(r'^taquilla/reportes/ganadores/$',        taquilla_reporte_ganadores,name='taquilla_rpt_ganadores'),

    # Dashboard de gestión
    re_path(r'^dashboard/$',               dashboard,       name='dashboard'),
    re_path(r'^dashboard/stats/$',         dashboard_stats, name='dashboard_stats'),
    re_path(r'^dashboard/api/(?P<modulo>[\w-]+)/$', dashboard_api, name='dashboard_api'),
    re_path(r'^dashboard/crud/(?P<modulo>[\w-]+)/$', dashboard_crud, name='dashboard_crud'),

    # ── Reportes de Venta (dentro del dashboard) ───────────────────────────────
    re_path(r'^dashboard/reportes/$',                       reportes_page,          name='dashboard_reportes'),
    re_path(r'^dashboard/reportes/api/lista-linea/$',       api_lista_linea,        name='api_lista_linea'),
    re_path(r'^dashboard/reportes/api/por-producto/$',      api_por_producto,       name='api_por_producto'),
    re_path(r'^dashboard/reportes/api/riesgo-venta/$',      api_riesgo_venta,       name='api_riesgo_venta'),
    re_path(r'^dashboard/reportes/api/sorteos/$',           api_sorteos_disponibles,name='api_sorteos'),
    re_path(r'^dashboard/reportes/api/cuadre/$',            api_cuadre,             name='api_cuadre'),
    re_path(r'^dashboard/reportes/api/liquidaciones/$',     api_liquidaciones,      name='api_liquidaciones'),
    re_path(r'^dashboard/reportes/api/resumen-admin/$',     api_resumen_admin,      name='api_resumen_admin'),
    re_path(r'^dashboard/reportes/api/dias-trabajo/$',      api_dias_trabajo,       name='api_dias_trabajo'),
    re_path(r'^dashboard/candidatos/$',                     candidatos_page,        name='dashboard_candidatos'),
    re_path(r'^dashboard/liquidaciones/$',                  liquidacion_page,       name='dashboard_liquidaciones'),
    re_path(r'^dashboard/monitor/api/$',                    monitor_api,            name='dashboard_monitor_api'),
    re_path(r'^api/liquidaciones-sorteo/$',                 liquidaciones_sorteo_api,   name='api_liquidaciones_sorteo'),
    re_path(r'^api/candidatos-riesgo/$',                     candidatos_riesgo_api,       name='api_candidatos_riesgo'),
    re_path(r'^api/cuadre-nivel-superior/$',                  cuadre_nivel_superior_api,   name='api_cuadre_nivel_superior'),

    # Urls del admin de django
    re_path(r'^' + settings.ADMIN_URL[1:], admin.site.urls),

    # urls de las app desarrolladas
    re_path(r'^', include('admin_comercializacion.urls')),
    re_path(r'^', include('admin_finanzas.urls')),
    re_path(r'^', include('admin_historic.urls')),
    re_path(r'^', include('admin_juego.urls')),
    re_path(r'^', include('admin_logros.urls')),
    re_path(r'^', include('admin_mail.urls')),
    re_path(r'^', include('admin_permisologia.urls')),
    re_path(r'^', include('admin_profiles.urls')),
    re_path(r'^', include('admin_principal.urls')),
    re_path(r'^', include('admin_reportes.urls')),
    re_path(r'^', include('admin_resultados.urls')),
    re_path(r'^', include('admin_soporte.urls')),
    re_path(r'^', include('admin_themes.urls')),
    re_path(r'^', include('admin_users.urls')),
    re_path(r'^', include('api.urls')),
    # urls de archivos media (solo en desarrollo)
    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,
    }),
]

urlpatterns += staticfiles_urlpatterns()

if getattr(settings, 'DEBUG_TOOLBAR', False):
    try:
        import debug_toolbar
        urlpatterns += [
            re_path(r'^__debug__/', include(debug_toolbar.urls)),
        ]
    except ImportError:
        pass
