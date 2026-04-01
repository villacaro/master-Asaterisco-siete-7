# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
from admin_lib.util_print import CsvView, PdfView
from admin_permisologia.models import Groups, Menu, Permissions
from admin_reportes.views.cuadres import (
    cuadre_general_queda_views, cuadre_nivel_superior_views, cuadre_parley_views, cuadre_por_fechas_queda_views,
    media_views,
)
from admin_reportes.views.tickets import ListadoDetailTickets, ListadoGeneralTickets, TicketsPorEstatusList
from admin_reportes.views.ventas import (
    ventas_en_linea_views, ventas_monitor_views, ventas_por_Juegos_views, ventas_procesadas_views,
)
from django.urls import include, re_path

# ===================================================================#
urlpatterns = [
]
# ===================================================================#
#                    Urls de juegos
# ===================================================================#
"""
Los enlaces del menu se registran
"""
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(2000)

    finanzas_titulo = Menu.register(
        name="Informes",
        codename="admin_finanzas_title",
        icon="icon-documents",
        content_type=1,
        orden=ORDEN(0),
        is_view=True,
    )
# ===================================================================#
#                    Urls de ventas
# ===================================================================#
if ADD_MENU:
    venta_subtitulo = Menu.register(
        name="Ventas",
        codename="admin_reportes_ventas_subtitle",
        menu_suc=finanzas_titulo,
        icon="icon-trending-up",
        content_type=2,
        orden=ORDEN(100),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    venta_en_linea_list = Menu.register(
        name="Venta en linea",
        codename="admin_reportes_ventas_en_linea_list",
        url="/reportes/ventas/ventas-en-linea/",
        menu_suc=venta_subtitulo,
        icon="icon-area-graph",
        orden=ORDEN(110),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas-en-linea/$', ventas_en_linea_views.VentaEnLineaAgrupadaView.as_view(), name='admin_reportes_ventas_en_linea_list'),
]
# =============================================================================#
# DATATABLE#
# =============================================================================#
if ADD_MENU:
    venta_en_linea_list_datatable = Menu.register(
        name="Ventas en linea lista datatables",
        codename="admin_reportes_venta_en_linea_list_datatable",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/venta-linea-datatable/$', ventas_en_linea_views.VentasLineaDatatableView.as_view(), name='admin_reportes_venta_en_linea_list_datatable'),
]

# ===================================================================#
# ===================================================================#
if ADD_MENU:
    venta_en_linea_print_pdf = Menu.register(
        name="Pdf Ventas en linea",
        codename="admin_reportes_venta_en_linea_print_pdf",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas-en-linea/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_venta_en_linea_print_pdf'),
]
if ADD_MENU:
    venta_en_linea_print_csv = Menu.register(
        name="Csv Ventas en linea",
        codename="admin_reportes_venta_en_linea_print_csv",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas-en-linea/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_venta_en_linea_print_csv'),
]
# ===================================================================#
if ADD_MENU:
    venta_por_juegos_list = Menu.register(
        name="Ventas por juego",
        codename="admin_reportes_ventas_por_juegos_list",
        url="/reportes/ventas/juegos/",
        menu_suc=venta_subtitulo,
        icon="icon-area-graph",
        orden=ORDEN(120),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/juegos/$', ventas_por_Juegos_views.VentasPorJuegos.as_view(), name='admin_reportes_ventas_por_juegos_list'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    venta_por_juegos_print_pdf = Menu.register(
        name="Pdf Ventas por juego",
        codename="admin_reportes_venta_por_juegos_print_pdf",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/juegos/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_venta_por_juegos_print_pdf'),
]
if ADD_MENU:
    venta_por_juegos_print_csv = Menu.register(
        name="Csv Ventas por juego",
        codename="admin_reportes_venta_por_juegos_print_csv",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/juegos/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_venta_por_juegos_print_csv'),
]

# ===================================================================#

if ADD_MENU:
    venta_procesadas_list = Menu.register(
        name="Ventas procesadas",
        codename="admin_reportes_ventas_procesadas_list",
        url="/reportes/ventas/venta-procesadas/",
        menu_suc=venta_subtitulo,
        icon="icon-line-graph",
        orden=ORDEN(130),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/venta-procesadas/$', ventas_procesadas_views.VentasProcesadas.as_view(), name='admin_reportes_ventas_procesadas_list'),
]

# ============================================================================#
# DATATABLE#
# =============================================================================#
if ADD_MENU:
    ventas_procesadas_list_datatable = Menu.register(
        name="Ventas procesadas lista datatables",
        codename="admin_reportes_ventas_procesadas_list_datatable",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/venta-procesadas-datatable/$', ventas_procesadas_views.VentasProcesadasDatatableView.as_view(), name='admin_reportes_ventas_procesadas_list_datatable'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    venta_procesadas_print_csv = Menu.register(
        name="Csv Ventas procesadas",
        codename="admin_reportes_venta_procesadas_print_csv",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas-procesadas/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_venta_procesadas_print_csv'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    venta_procesadas_print_pdf = Menu.register(
        name="Pdf Ventas procesadas",
        codename="admin_reportes_venta_procesadas_print_pdf",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas-procesadas/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_venta_procesadas_print_pdf'),
]

# ===================================================================#
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    venta_monitor_ajax = Menu.register(
        name="Consulta de Monitor ajax",
        codename="admin_reportes_ventas_monitor_ajax",
        menu_suc=venta_subtitulo
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas-monitor/ajax$', ventas_monitor_views.VentaMonitorViewAjax.as_view(), name='admin_reportes_ventas_monitor_ajax'),
]

# ===================================================================#
if ADD_MENU:
    monitor_venta_list = Menu.register(
        name="Monitor de ventas",
        codename="admin_reportes_monitor_ventas_list",
        url="/reportes/ventas/monitor-ventas/",
        menu_suc=venta_subtitulo,
        icon="icon-gauge",
        orden=ORDEN(150),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/monitor-ventas/$', ventas_monitor_views.MonitorVentaView.as_view(), name='admin_reportes_monitor_ventas_list'),
]

"""
# ===================================================================#
"""
if ADD_MENU:
    ventas_monitor_list_datatables = Menu.register(
        name="Monitor ventas datatables",
        codename="ventas_monitor_list_datatables",
        menu_suc=venta_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/ventas_monitor_list_datatables/$', ventas_monitor_views.MonitorDatatableView.as_view(), name='ventas_monitor_list_datatables'),
]

# ===================================================================#
# Creado permisos para los urls descritos de ventas
# ===================================================================#
if ADD_MENU:
    admin_reportes_ventas_en_linea_list = Permissions.register(
        name="Reportes | Ventas | En linea",
        codename="admin_reportes_ventas_en_linea_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            venta_subtitulo,
            venta_en_linea_list,
            venta_en_linea_list_datatable,
            venta_en_linea_print_pdf,
            venta_en_linea_print_csv,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_ventas_por_juegos_list = Permissions.register(
        name="Reportes | Ventas | Por juegos",
        codename="admin_reportes_ventas_por_juegos_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            venta_subtitulo,
            venta_por_juegos_list,
            venta_por_juegos_print_pdf,
            venta_por_juegos_print_csv,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_ventas_procesadas_list = Permissions.register(
        name="Reportes | Ventas | Procesadas",
        codename="admin_reportes_ventas_procesadas_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            venta_subtitulo,
            venta_procesadas_list,
            ventas_procesadas_list_datatable,
            venta_procesadas_print_csv,
            venta_procesadas_print_pdf,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_ventas_monitor_list = Permissions.register(
        name="Reportes | Ventas | Monitor",
        codename="admin_reportes_ventas_monitor_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            venta_subtitulo,
            monitor_venta_list,
            ventas_monitor_list_datatables,
            venta_monitor_ajax,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
# ===================================================================#
#                    Urls de Reportes
# ===================================================================#
if ADD_MENU:
    cuadre_subtitulo = Menu.register(
        name="Reportes",
        codename="admin_reportes_cuadres_subtitle",
        menu_suc=finanzas_titulo,
        icon="icon-documents",
        content_type=2,
        orden=ORDEN(400),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    cuadre_nivel_superior_list = Menu.register(
        name="Cuadre nivel superior",
        codename="admin_reportes_cuadre_nivel_superior_list",
        url="/reportes/ventas/cuadre-nivel-superior/",
        menu_suc=cuadre_subtitulo,
        icon="icon-publish",
        orden=ORDEN(411),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-nivel-superior/$', cuadre_nivel_superior_views.CuadreNivelSuperior.as_view(), name='admin_reportes_cuadre_nivel_superior_list'),
]
# ===================================================================#
if ADD_MENU:
    cuadre_por_fechas_queda_list = Menu.register(
        name="Cuadre por fechas",
        codename="admin_reportes_cuadre_por_fechas_queda_list",
        url="/reportes/ventas/cuadre-queda/fechas/",
        menu_suc=cuadre_subtitulo,
        icon="icon-equalizer",
        orden=ORDEN(415),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-queda/fechas/$', cuadre_por_fechas_queda_views.CuadrePorFechasQueda.as_view(), name='admin_reportes_cuadre_por_fechas_queda_list'),
]
# ===================================================================#
if ADD_MENU:
    cuadre_general_queda_list = Menu.register(
        name="Cuadre por periodos",
        codename="admin_reportes_cuadre_general_queda_list",
        url="/reportes/ventas/cuadre-queda/general/",
        menu_suc=cuadre_subtitulo,
        icon="icon-equalizer",
        orden=ORDEN(416),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-queda/general/$', cuadre_general_queda_views.CuadreGeneralQueda.as_view(), name='admin_reportes_cuadre_general_queda_list'),
]

# ===================================================================#
if ADD_MENU:
    cuadre_parley_list = Menu.register(
        name="Cuadre parley",
        codename="admin_reportes_cuadre_parley_list",
        url="/reportes/ventas/cuadre-parley/",
        menu_suc=cuadre_subtitulo,
        icon="icon-event-available",
        orden=ORDEN(412),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-parley/$', cuadre_parley_views.CuadreParley.as_view(), name='admin_reportes_cuadre_parley_list'),
]
# =============================================================================#
# DATATABLE#
# =============================================================================#
if ADD_MENU:
    cuadre_parley_list_datatable = Menu.register(
        name="Cuadre Parley datatables",
        codename="admin_reportes_cuadre_parley_list_datatable",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-parley-datatable/$', cuadre_parley_views.CuadreParleyDatatableView.as_view(), name='admin_reportes_cuadre_parley_list_datatable'),
]

# ==========================================================
if ADD_MENU:
    cuadre_parley_print_pdf = Menu.register(
        name="Pdf Cuadre parley",
        codename="admin_reportes_cuadre_parley_print_pdf",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-parley/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_cuadre_parley_print_pdf'),
]

# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_parley_print_csv = Menu.register(
        name="Csv Cuadre parley",
        codename="admin_reportes_cuadre_parley_print_csv",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-parley/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_cuadre_parley_print_csv'),
]

# ===================================================================#
if ADD_MENU:
    media_list = Menu.register(
        name="Media",
        codename="admin_reportes_media_list",
        url="/reportes/ventas/media/",
        menu_suc=cuadre_subtitulo,
        icon="icon-flip",
        orden=ORDEN(420),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/ventas/media/$', media_views.Media.as_view(), name='admin_reportes_media_list'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_general_queda_print_csv = Menu.register(
        name="Csv Cuadre por periodos",
        codename="admin_reportes_cuadre_general_queda_print_csv",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-queda/general/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_cuadre_general_queda_print_csv'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_general_queda_print_pdf = Menu.register(
        name="Pdf Cuadre por periodos",
        codename="admin_reportes_cuadre_general_queda_print_pdf",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-queda/general/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_cuadre_general_queda_print_pdf'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_por_fechas_queda_print_csv = Menu.register(
        name="Csv Cuadre por fechas",
        codename="admin_reportes_cuadre_por_fechas_queda_print_csv",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-queda/fechas/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_cuadre_por_fechas_queda_print_csv'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_por_fechas_queda_print_pdf = Menu.register(
        name="Pdf Cuadre por fechas",
        codename="admin_reportes_cuadre_por_fechas_queda_print_pdf",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-queda/fechas/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_cuadre_por_fechas_queda_print_pdf'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_de_nivel_superior_print_csv = Menu.register(
        name="Csv Cuadre de nivel superior",
        codename="admin_reportes_cuadre_de_nivel_superior_print_csv",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-nivel-superior/csv/(?P<cache_key>.+?)/$', CsvView, name='admin_reportes_cuadre_de_nivel_superior_print_csv'),
]
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    cuadre_de_nivel_superior_print_pdf = Menu.register(
        name="Pdf Cuadre de nivel superior",
        codename="admin_reportes_cuadre_de_nivel_superior_print_pdf",
        menu_suc=cuadre_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/ventas/cuadre-nivel-superior/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_reportes_cuadre_de_nivel_superior_print_pdf'),
]
# ===================================================================#
# Creado permisos para los urls descritos de cuadres
# ===================================================================#
if ADD_MENU:
    admin_reportes_cuadre_nivel_superior_list = Permissions.register(
        name="Reportes | Cuadres | Nivel Superior",
        codename="admin_reportes_cuadre_nivel_superior_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            cuadre_subtitulo,
            cuadre_nivel_superior_list,
            cuadre_de_nivel_superior_print_pdf,
            cuadre_de_nivel_superior_print_csv
        ],
        profiles=[
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )

    admin_reportes_cuadre_parley_list = Permissions.register(
        name="Reportes | Cuadres | Parley",
        codename="admin_reportes_cuadre_parley_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            cuadre_subtitulo,
            cuadre_parley_list,
            cuadre_parley_list_datatable,
            cuadre_parley_print_pdf,
            cuadre_parley_print_csv,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )

    admin_reportes_cuade_queda_fechas = Permissions.register(
        name="Reportes | Cuadres | Por fechas",
        codename="admin_reportes_cuade_por_fechas_queda_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            cuadre_subtitulo,
            cuadre_por_fechas_queda_list,
            cuadre_por_fechas_queda_print_csv,
            cuadre_por_fechas_queda_print_pdf,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )

    admin_reportes_cuade_queda_general = Permissions.register(
        name="Reportes | Cuadres | Por periodos",
        codename="admin_reportes_cuadre_general_queda_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            cuadre_subtitulo,
            cuadre_general_queda_list,
            cuadre_general_queda_print_csv,
            cuadre_general_queda_print_pdf,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )

    admin_reportes_media_list = Permissions.register(
        name="Reportes | Cuadres | Media",
        codename="admin_reportes_media_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            cuadre_subtitulo,
            media_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
# ===================================================================#
#                    Urls de Tickets
# ===================================================================#
if ADD_MENU:
    tickets_subtitulo = Menu.register(
        name="Tickets",
        codename="admin_reportes_tickets_subtitle",
        menu_suc=finanzas_titulo,
        icon="icon-ticket",
        content_type=2,
        orden=ORDEN(500),
        is_view=True,
    )
# ===================================================================#
#                    Urls de Tickets
# ===================================================================#

if ADD_MENU:
    tickets_list = Menu.register(
        name="Consulta de Tickets",
        codename="admin_reportes_tickets_list",
        url="/reportes/tickets/listado-tickets/",
        menu_suc=tickets_subtitulo,
        icon="icon-list2",
        orden=ORDEN(540),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/tickets/listado-tickets/$', ListadoGeneralTickets.ListadoTickets.as_view(), name='admin_reportes_tickets_list'),
]
# ===================================================================#
if ADD_MENU:
    tickets_get = Menu.register(
        name="Consulta de Tickets",
        codename="admin_reportes_tickets_get",
        menu_suc=tickets_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/tickets/listado-tickets/get/$', ListadoGeneralTickets.ListadoTicketsAjax.as_view(), name='admin_reportes_tickets_get'),
]
# ===================================================================#
if ADD_MENU:
    tickets_detail = Menu.register(
        name="Consulta de Tickets",
        codename="admin_reportes_tickets_detail",
        menu_suc=tickets_subtitulo,
    )
urlpatterns += [
re_path(r'^reportes/tickets/listado-tickets/(?P<pk>\d+?)/$', ListadoDetailTickets.VentasDetalleTickets.as_view(), name='admin_reportes_tickets_detail'),
]
# ===================================================================#

if ADD_MENU:
    tickets_ganadores_list = Menu.register(
        name="Tickets Ganadores",
        codename="admin_reportes_tickets_ganadores_list",
        url="/reportes/tickets/listado-tickets/ganadores/",
        menu_suc=tickets_subtitulo,
        icon="icon-ticket",
        orden=ORDEN(510),
        is_view=True,
    )
    tickets_pagados_list = Menu.register(
        name="Tickets Pagados",
        codename="admin_reportes_tickets_pagados_list",
        url="/reportes/tickets/listado-tickets/pagados/",
        menu_suc=tickets_subtitulo,
        icon="icon-ticket",
        orden=ORDEN(520),
        is_view=True,
    )
    tickets_anulados_list = Menu.register(
        name="Tickets Anulados",
        codename="admin_reportes_tickets_anulados_list",
        url="/reportes/tickets/listado-tickets/anulados/",
        menu_suc=tickets_subtitulo,
        icon="icon-ticket",
        orden=ORDEN(530),
        is_view=True,
    )
urlpatterns += [
re_path(r'^reportes/tickets/listado-tickets/(?P<estatus>[a-z]+?)/$', TicketsPorEstatusList.ListadoTicketsEstatus.as_view(), name='admin_reportes_tickets_status_list'),
]
# ===================================================================#
# Creado permisos para los urls descritos de tickets
# ===================================================================#
if ADD_MENU:
    admin_reportes_tickets_list = Permissions.register(
        name="Reportes | Tickest | Lista",
        codename="admin_reportes_tickets_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            tickets_subtitulo,
            tickets_list,
            tickets_get,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_tickets_detail = Permissions.register(
        name="Reportes | Tickest | Detalle",
        codename="admin_reportes_tickets_detail",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            tickets_subtitulo,
            tickets_list,
            tickets_get,
            tickets_detail,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_tickets_ganadores_list = Permissions.register(
        name="Reportes | Tickest | Ganadores",
        codename="admin_reportes_tickets_ganadores_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            tickets_subtitulo,
            tickets_ganadores_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_tickets_pagados_list = Permissions.register(
        name="Reportes | Tickest | Pagados",
        codename="admin_reportes_tickets_pagados_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            tickets_subtitulo,
            tickets_pagados_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )
    admin_reportes_tickets_anulados_list = Permissions.register(
        name="Reportes | Tickest | Anulados",
        codename="admin_reportes_tickets_anulados_list",
        content_type="admin_reportes",
        menus=[
            finanzas_titulo,
            tickets_subtitulo,
            tickets_anulados_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
            "userprofile_distribuidor",
            "userprofile_agencia",
        ],
    )

# ===================================================================#
if ADD_MENU:
    Groups.register(
        name="Permisos Reportes",
        codename="admin_reportes_basic",
        permissions=[
            admin_reportes_ventas_en_linea_list,
            admin_reportes_ventas_por_juegos_list,
            admin_reportes_ventas_procesadas_list,
            admin_reportes_ventas_monitor_list,

            admin_reportes_media_list,

            admin_reportes_tickets_list,
            admin_reportes_tickets_detail,
            admin_reportes_tickets_ganadores_list,
            admin_reportes_tickets_pagados_list,
            admin_reportes_tickets_anulados_list,

        ],
    )
