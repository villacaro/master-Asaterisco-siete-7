# -*- coding: utf-8 -*-
from admin_asterisco7.settings import ADD_MENU
from admin_juego.views import (
    condiciones_views, loterias_views, sorteos_views, modalidad_tipo_views, eventnotification_views, gruposapuestas_views,
    gruposjuego_views, horarios_views, animalitos_views, animalito_tipo_views, modalidades_views, sistemajuego_views,
    vigencias_views, productos_views,
)
from admin_permisologia.models import Groups, Menu, Permissions
from django.urls import include, re_path

"""Importamos todas las vistas"""


"""
# ===================================================================#
"""
urlpatterns = [
]
"""
# ===================================================================#
#                    Urls de juegos
# ===================================================================#
"""

"""
Los enlaces del menu se registran
"""
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(3000)

    juego_titulo = Menu.register(
        name="Juego",
        codename="admin_juego_title",
        icon="icon-sports-club",
        content_type=1,
        orden=ORDEN(0),
        is_view=True,
    )

"""
# ===================================================================#
#                    Urls de notificaciones
# ===================================================================#
"""
if ADD_MENU:
    eventnotification_subtitulo = Menu.register(
        name="Actualizaciones",
        codename="admin_juego_eventnotification_subtitle",
        menu_suc=juego_titulo,
        icon="icon-notifications",
        content_type=2,
        orden=ORDEN(2),
        is_view=True,
    )
if ADD_MENU:
    eventnotification_list = Menu.register(
        name="Gestionar",
        codename="admin_juego_eventnotification_list",
        url="/juego/actualizaciones/",
        menu_suc=eventnotification_subtitulo,
        icon="icon-notifications-on",
        orden=ORDEN(3),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/actualizaciones/$', eventnotification_views.EventNotificationListView.as_view(), name='admin_juego_eventnotification_list'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de sistemajuego
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_eventnotification_list = Permissions.register(
        name="Juego | Actualizaciones | Gestionar",
        codename="admin_juego_eventnotification_list",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            eventnotification_subtitulo,
            eventnotification_list,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )
"""
# ===================================================================#
#                    Urls de sistemajuego
# ===================================================================#
"""
if ADD_MENU:
    sistemajuego_subtitulo = Menu.register(
        name="Sistema de juego",
        codename="admin_juego_sistemajuego_subtitle",
        menu_suc=juego_titulo,
        icon="icon-games",
        content_type=2,
        orden=ORDEN(5),
        is_view=True,
    )
if ADD_MENU:
    sistemajuego_list = Menu.register(
        name="Lista",
        codename="admin_juego_sistemajuego_list",
        url="/juego/sistemajuego/",
        menu_suc=sistemajuego_subtitulo,
        icon="icon-list2",
        orden=ORDEN(8),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/sistemajuego/$', sistemajuego_views.SistemaJuegoListView.as_view(), name='admin_juego_sistemajuego_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    sistemajuego_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_sistemajuego_update",
        menu_suc=sistemajuego_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/sistemajuego/(?P<pk>\d+?)/editar/$', sistemajuego_views.SistemaJuegoUpdateView.as_view(), name='admin_juego_sistemajuego_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    sistemajuego_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_sistemajuego_detail",
        menu_suc=sistemajuego_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/sistemajuego/(?P<pk>\d+?)/$', sistemajuego_views.SistemaJuegoDetailView.as_view(), name='admin_juego_sistemajuego_detail'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de sistemajuego
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_sistemajuego_detail = Permissions.register(
        name="Juego | Sistema de juego | Ver",
        codename="admin_juego_sistemajuego_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            sistemajuego_subtitulo,
            sistemajuego_detail,
            sistemajuego_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_juego_sistemajuego_update = Permissions.register(
        name="Juego | Sistema de juego | Actualizar",
        codename="admin_juego_sistemajuego_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            sistemajuego_subtitulo,
            sistemajuego_detail,
            sistemajuego_list,
            sistemajuego_update,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    deporte_subtitulo = Menu.register(
        name="TipoProducto",
        codename="admin_juego_deportes_subtitle",
        menu_suc=juego_titulo,
        icon="icon-baseball",
        content_type=2,
        orden=ORDEN(10),
        is_view=True,
    )
"""
# ===================================================================#
#                    Urls de deportes
# ===================================================================#
"""

if ADD_MENU:
    deporte_create = Menu.register(
        name="Crear",
        codename="admin_juego_deportes_create",
        url="/juego/deporte/crear/",
        menu_suc=deporte_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(15),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/deporte/crear/$', loterias_views.DeportesCreateView.as_view(), name='admin_juego_deportes_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    deporte_list = Menu.register(
        name="Lista",
        codename="admin_juego_deportes_list",
        url="/juego/deportes/",
        menu_suc=deporte_subtitulo,
        icon="icon-list2",
        orden=ORDEN(20),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/deportes/$', loterias_views.DeportesListView.as_view(), name='admin_juego_deportes_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    deporte_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_deportes_update",
        menu_suc=deporte_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/deporte/(?P<pk>\d+?)/editar/$', loterias_views.DeportesUpdateView.as_view(), name='admin_juego_deportes_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    deporte_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_deportes_delete",
        menu_suc=deporte_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/deporte/(?P<pk>\d+?)/eliminar/$', loterias_views.DeportesDeleteView.as_view(), name='admin_juego_deportes_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    deporte_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_deportes_detail",
        menu_suc=deporte_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/deporte/(?P<pk>\d+?)/$', loterias_views.DeportesDetailView.as_view(), name='admin_juego_deportes_detail'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de deportes
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_deportes_detail = Permissions.register(
        name="Juego | TipoProducto | Ver",
        codename="admin_juego_deportes_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            deporte_subtitulo,
            deporte_detail,
            deporte_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_deportes_create = Permissions.register(
        name="Juego | TipoProducto | Crear",
        codename="admin_juego_deportes_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            deporte_subtitulo,
            deporte_create,
            deporte_detail,
            deporte_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_deportes_update = Permissions.register(
        name="Juego | TipoProducto | Actualizar",
        codename="admin_juego_deportes_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            deporte_subtitulo,
            deporte_detail,
            deporte_list,
            deporte_update,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_deportes_delete = Permissions.register(
        name="Juego | TipoProducto | Eliminar",
        codename="admin_juego_deportes_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            deporte_subtitulo,
            deporte_delete,
            deporte_detail,
            deporte_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de ligas
# ===================================================================#
"""

if ADD_MENU:
    liga_subtitulo = Menu.register(
        name="Ligas",
        codename="admin_juego_torneos_subtitle",
        menu_suc=juego_titulo,
        icon="icon-trophy",
        content_type=2,
        orden=ORDEN(30),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_create = Menu.register(
        name="Crear",
        codename="admin_juego_torneos_create",
        url="/juego/liga/crear/",
        menu_suc=liga_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(40),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/liga/crear/$', productos_views.TorneosCreateView.as_view(), name='admin_juego_torneos_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_list = Menu.register(
        name="Lista",
        codename="admin_juego_torneos_list",
        url="/juego/ligas/",
        menu_suc=liga_subtitulo,
        icon="icon-list2",
        orden=ORDEN(50),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/ligas/$', productos_views.TorneosListView.as_view(), name='admin_juego_torneos_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_torneos_update",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/(?P<pk>\d+?)/editar/$', productos_views.TorneosUpdateView.as_view(), name='admin_juego_torneos_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_torneos_delete",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/(?P<pk>\d+?)/eliminar/$', productos_views.TorneosDeleteView.as_view(), name='admin_juego_torneos_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_torneos_detail",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/(?P<pk>\d+?)/$', productos_views.TorneosDetailView.as_view(), name='admin_juego_torneos_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_ajax_list_by_deporte = Menu.register(
        name="Lista de torneos dado un deporte",
        codename="admin_juego_torneos_by_deporte_ajax",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/ligas-by-deporte/$', productos_views.TorneosListbyDeporteAjax.as_view(), name='admin_juego_torneos_by_deporte_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    liga_ajax_get = Menu.register(
        name="Obtener torneo",
        codename="admin_juego_torneos_get_ajax",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga-get/$', productos_views.TorneoGetAjax.as_view(), name='admin_juego_torneos_get_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    torneos_list_datatables = Menu.register(
        name="TipoProducto datatables",
        codename="torneos_list_datatables",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/torneos/torneos_list_datatables/$', productos_views.TorneosDatatableView.as_view(), name='torneos_list_datatables'),
]

"""
# ===================================================================#
#Creado permisos para los urls descritos de ligas
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_torneos_detail = Permissions.register(
        name="Juego | Ligas | Ver",
        codename="admin_juego_torneos_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            liga_detail,
            liga_list,
            liga_ajax_list_by_deporte,
            liga_ajax_get,
            torneos_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_torneos_create = Permissions.register(
        name="Juego | Ligas | Crear",
        codename="admin_juego_torneos_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            liga_create,
            liga_detail,
            liga_list,
            torneos_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_torneos_update = Permissions.register(
        name="Juego | Ligas | Actualizar",
        codename="admin_juego_torneos_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            liga_update,
            liga_detail,
            liga_list,
            torneos_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_torneos_delete = Permissions.register(
        name="Juego | Ligas | Eliminar",
        codename="admin_juego_torneos_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            liga_delete,
            liga_detail,
            liga_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_torneos_ajax = Permissions.register(
        name="Juego | Ligas | Ver Ajax",
        codename="admin_juego_torneos_ajax",
        content_type="admin_juego",
        menus=[
            liga_ajax_list_by_deporte,
            liga_ajax_get,
            torneos_list_datatables
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_banca"
        ],
    )
"""
# ===================================================================#
#                    Urls de jornadas
# ===================================================================#
"""
if ADD_MENU:
    jornadas_list = Menu.register(
        name="Fechas",
        codename="admin_juego_jornadas_list",
        url="/juego/liga/jornadas/",
        menu_suc=liga_subtitulo,
        icon="icon-view-week",
        orden=ORDEN(60),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/liga/jornadas/$', horarios_views.JornadasListView.as_view(), name='admin_juego_jornadas_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jornadas_create = Menu.register(
        name="Crear",
        codename="admin_juego_jornadas_create",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/jornada/crear/$', horarios_views.JornadasCreateView.as_view(), name='admin_juego_jornadas_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jornadas_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_jornadas_update",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/jornada/(?P<pk>\d+?)/editar/$', horarios_views.JornadasUpdateView.as_view(), name='admin_juego_jornadas_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jornadas_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_jornadas_delete",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/jornada/(?P<pk>\d+?)/eliminar/$', horarios_views.JornadasDeleteView.as_view(), name='admin_juego_jornadas_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jornadas_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_jornadas_detail",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/jornada/(?P<pk>\d+?)/$', horarios_views.JornadasDetailView.as_view(), name='admin_juego_jornadas_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jornadas_ajax_list_by_temporada = Menu.register(
        name="Fechas por temporada",
        codename="admin_juego_jornadas_by_temporada_ajax",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/jornadas-by-temporada/$', horarios_views.JornadasListbyTemporadaAjax.as_view(), name='admin_juego_jornadas_by_temporada_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jornadas_list_datatables = Menu.register(
        name="Fechas datatables",
        codename="jornadas_list_datatables",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jornadas/jornadas_list_datatables/$', horarios_views.JornadasDatatableView.as_view(), name='jornadas_list_datatables'),
]
"""
# ===================================================================#
#Creado permisos para los urls descritos de jornadas
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_jornadas_detail = Permissions.register(
        name="Juego | Fechas | Ver",
        codename="admin_juego_jornadas_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            jornadas_list,
            jornadas_detail,
            jornadas_ajax_list_by_temporada,
            jornadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            # "userprofile_bloque",
            # "userprofile_banca",
        ],
    )

    admin_juego_jornadas_create = Permissions.register(
        name="Juego | Fechas | Crear",
        codename="admin_juego_jornadas_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            jornadas_list,
            jornadas_detail,
            jornadas_create,
            jornadas_ajax_list_by_temporada,
            jornadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            # "userprofile_bloque",
            # "userprofile_banca",
        ],
    )

    admin_juego_jornadas_update = Permissions.register(
        name="Juego | Fechas | Actualizar",
        codename="admin_juego_jornadas_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            jornadas_list,
            jornadas_detail,
            jornadas_update,
            jornadas_ajax_list_by_temporada,
            jornadas_list_datatables
        ],
        profiles=[
            "userprofile_operadora",
            # "userprofile_bloque",
            # "userprofile_banca",
        ],
    )

    admin_juego_jornadas_delete = Permissions.register(
        name="Juego | Fechas | Eliminar",
        codename="admin_juego_jornadas_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            jornadas_delete,
            jornadas_list,
            jornadas_detail,
            jornadas_ajax_list_by_temporada,
            jornadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            # "userprofile_bloque",
            # "userprofile_banca",
        ],
    )
"""
# ===================================================================#
#                    Urls de grupos de gruposjuego
# ===================================================================#
"""

if ADD_MENU:
    gruposjuego_list = Menu.register(
        name="Grupos",
        codename="admin_juego_gruposjuego_list",
        url="/juego/liga/grupos/",
        menu_suc=liga_subtitulo,
        icon="icon-group-work",
        orden=ORDEN(70),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/liga/grupos/$', gruposjuego_views.GruposJuegoListView.as_view(), name='admin_juego_gruposjuego_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposjuego_create = Menu.register(
        name="Crear",
        codename="admin_juego_gruposjuego_create",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/grupo/crear/$', gruposjuego_views.GruposJuegoCreateView.as_view(), name='admin_juego_gruposjuego_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposjuego_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_gruposjuego_update",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/grupo/(?P<pk>\d+?)/editar/$', gruposjuego_views.GruposJuegoUpdateView.as_view(), name='admin_juego_gruposjuego_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposjuego_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_gruposjuego_delete",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/grupo/(?P<pk>\d+?)/eliminar/$', gruposjuego_views.GruposJuegoDeleteView.as_view(), name='admin_juego_gruposjuego_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposjuego_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_gruposjuego_detail",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/grupo/(?P<pk>\d+?)/$', gruposjuego_views.GruposJuegoDetailView.as_view(), name='admin_juego_gruposjuego_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposjuego_ajax_list_by_temporada = Menu.register(
        name="Grupos de juego por temporada",
        codename="admin_juego_gruposjuego_by_temporada_ajax",
        menu_suc=liga_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/liga/grupos/temporada/$', gruposjuego_views.GruposJuegoListbyTemporadaAjax.as_view(), name='admin_juego_gruposjuego_by_temporada_ajax'),
]
"""
# ===================================================================#
#Creado permisos para los urls descritos de gruposjuego
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_gruposjuego_detail = Permissions.register(
        name="Juego | Grupos de Juego | Ver",
        codename="admin_juego_gruposjuego_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            gruposjuego_list,
            gruposjuego_detail,
            gruposjuego_ajax_list_by_temporada
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_gruposjuego_create = Permissions.register(
        name="Juego | Grupos de Juego | Crear",
        codename="admin_juego_gruposjuego_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            gruposjuego_list,
            gruposjuego_detail,
            gruposjuego_create,
            gruposjuego_ajax_list_by_temporada
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_gruposjuego_update = Permissions.register(
        name="Juego | Grupos de Juego | Editar",
        codename="admin_juego_gruposjuego_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            gruposjuego_list,
            gruposjuego_detail,
            gruposjuego_update,
            gruposjuego_ajax_list_by_temporada
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_gruposjuego_delete = Permissions.register(
        name="Juego | Grupos de Juego | Eliminar",
        codename="admin_juego_gruposjuego_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            liga_subtitulo,
            gruposjuego_list,
            gruposjuego_detail,
            gruposjuego_delete,
            gruposjuego_ajax_list_by_temporada
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de equipos
# ===================================================================#
"""

if ADD_MENU:
    equipos_subtitulo = Menu.register(
        name="ModalidadJuego",
        codename="admin_juego_equipos_subtitle",
        menu_suc=juego_titulo,
        icon="icon-stars",
        content_type=2,
        orden=ORDEN(80),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_create = Menu.register(
        name="Crear",
        codename="admin_juego_equipos_create",
        url="/juego/equipo/crear/",
        menu_suc=equipos_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(90),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/equipo/crear/$', modalidad_tipo_views.EquiposCreateView.as_view(), name='admin_juego_equipos_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_list = Menu.register(
        name="Lista",
        codename="admin_juego_equipos_list",
        url="/juego/equipos/",
        menu_suc=equipos_subtitulo,
        icon="icon-list2",
        orden=ORDEN(100),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/equipos/$', modalidad_tipo_views.EquiposListView.as_view(), name='admin_juego_equipos_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_equipos_update",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipo/(?P<pk>\d+?)/editar/$', modalidad_tipo_views.EquiposUpdateView.as_view(), name='admin_juego_equipos_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_equipos_delete",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipo/(?P<pk>\d+?)/eliminar/$', modalidad_tipo_views.EquiposDeleteView.as_view(), name='admin_juego_equipos_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_equipos_detail",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipo/(?P<pk>\d+?)/$', modalidad_tipo_views.EquiposDetailView.as_view(), name='admin_juego_equipos_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_ajax_list_by_temporada_1 = Menu.register(
        name="ModalidadJuego por temporada 1",
        codename="admin_juego_equipos_by_temporada_1_ajax",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/temporada/$', modalidad_tipo_views.EquiposListbyTemporadaAjax.as_view(), name='admin_juego_equipos_by_temporada_1_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_ajax_list_by_temporada_2 = Menu.register(
        name="ModalidadJuego por temporada 2",
        codename="admin_juego_equipos_by_temporada_2_ajax",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/temporada2/$', modalidad_tipo_views.EquiposListbyTemporada2Ajax.as_view(), name='admin_juego_equipos_by_temporada_2_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_ajax_list_by_temporada_3 = Menu.register(
        name="ModalidadJuego por temporada 3",
        codename="admin_juego_equipos_by_temporada_3_ajax",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/temporada3/$', modalidad_tipo_views.EquiposListbyTemporada3Ajax.as_view(), name='admin_juego_equipos_by_temporada_3_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_ajax_list_by_grupo = Menu.register(
        name="ModalidadJuego por grupos",
        codename="admin_juego_equipos_by_grupo_ajax",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/grupo/$', modalidad_tipo_views.EquiposListbyGrupoAjax.as_view(), name='admin_juego_equipos_by_grupo_ajax'),
]
if ADD_MENU:
    equipos_list_datatables = Menu.register(
        name="ModalidadJuego datatables",
        codename="equipos_list_datatables",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/equipos_list_datatables/$', modalidad_tipo_views.EquiposDatatableView.as_view(), name='equipos_list_datatables'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    equipos_ajax_list_by_deporte = Menu.register(
        name="ModalidadJuego por deporte",
        codename="admin_juego_equipos_by_deporte_ajax",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/deporte/$', modalidad_tipo_views.EquiposListbyDeporteAjax.as_view(), name='admin_juego_equipos_by_deporte_ajax'),
]
if ADD_MENU:
    equipos_ajax_list_by_deporte_simple = Menu.register(
        name="ModalidadJuego por deporte (simple)",
        codename="admin_juego_equipos_by_deporte_ajax_simple",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/deporte/simple$', modalidad_tipo_views.EquiposListbyDeporteAjaxSimple.as_view(), name='admin_juego_equipos_by_deporte_ajax_simple'),
]
if ADD_MENU:
    equipos_ajax_list_by_liga = Menu.register(
        name="ModalidadJuego por liga",
        codename="juego_equipos_by_liga_ajax",
        menu_suc=equipos_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/equipos/liga/$', modalidad_tipo_views.EquiposListbyligaAjax.as_view(), name='juego_equipos_by_liga_ajax'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de equipos
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_equipos_detail = Permissions.register(
        name="Juego | ModalidadJuego | Ver",
        codename="admin_juego_equipos_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            equipos_subtitulo,
            equipos_detail,
            equipos_list,
            equipos_ajax_list_by_temporada_1,
            equipos_ajax_list_by_temporada_2,
            equipos_ajax_list_by_temporada_3,
            equipos_ajax_list_by_grupo,
            equipos_ajax_list_by_deporte,
            equipos_ajax_list_by_deporte_simple,
            equipos_ajax_list_by_liga,
            equipos_list_datatables
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_equipos_create = Permissions.register(
        name="Juego | ModalidadJuego | Crear",
        codename="admin_juego_equipos_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            equipos_subtitulo,
            equipos_create,
            equipos_detail,
            equipos_list,
            equipos_ajax_list_by_temporada_1,
            equipos_ajax_list_by_temporada_2,
            equipos_ajax_list_by_temporada_3,
            equipos_ajax_list_by_grupo,
            equipos_ajax_list_by_deporte,
            equipos_ajax_list_by_liga,
            equipos_list_datatables
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_equipos_update = Permissions.register(
        name="Juego | ModalidadJuego | Editar",
        codename="admin_juego_equipos_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            equipos_subtitulo,
            equipos_detail,
            equipos_list,
            equipos_update,
            equipos_ajax_list_by_temporada_1,
            equipos_ajax_list_by_temporada_2,
            equipos_ajax_list_by_temporada_3,
            equipos_ajax_list_by_grupo,
            equipos_ajax_list_by_deporte,
            equipos_ajax_list_by_liga,
            equipos_list_datatables
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_equipos_delete = Permissions.register(
        name="Juego | ModalidadJuego | Eliminar",
        codename="admin_juego_equipos_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            equipos_subtitulo,
            equipos_detail,
            equipos_list,
            equipos_delete,
            equipos_ajax_list_by_temporada_1,
            equipos_ajax_list_by_temporada_2,
            equipos_ajax_list_by_temporada_3,
            equipos_ajax_list_by_grupo,
            equipos_ajax_list_by_deporte,
            equipos_ajax_list_by_liga,
            equipos_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_equipos_ajax = Permissions.register(
        name="Juego | ModalidadJuego | Ver ajax",
        codename="admin_juego_equipos_ajax",
        content_type="admin_juego",
        menus=[
            equipos_ajax_list_by_temporada_1,
            equipos_ajax_list_by_temporada_2,
            equipos_ajax_list_by_temporada_3,
            equipos_ajax_list_by_grupo,
            equipos_ajax_list_by_deporte,
            equipos_ajax_list_by_liga,
            equipos_list_datatables
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_banca"
        ],
    )
"""
# ===================================================================#
#                    Urls de jugadores
# ===================================================================#
"""

if ADD_MENU:
    jugador_subtitulo = Menu.register(
        name="Jugadores",
        codename="admin_juego_jugador_subtitle",
        menu_suc=juego_titulo,
        icon="icon-recent-actors",
        content_type=2,
        orden=ORDEN(110),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    jugador_create = Menu.register(
        name="Crear",
        codename="admin_juego_jugador_create",
        url="/juego/jugador/crear/",
        menu_suc=jugador_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(120),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/jugador/crear/$', animalitos_views.JugadorCreateView.as_view(), name='admin_juego_jugador_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugador_list = Menu.register(
        name="Lista",
        codename="admin_juego_jugador_list",
        url="/juego/jugador/",
        menu_suc=jugador_subtitulo,
        icon="icon-list2",
        orden=ORDEN(130),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/jugador/$', animalitos_views.JugadorListView.as_view(), name='admin_juego_jugador_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugador_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_jugador_update",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/(?P<pk>\d+?)/editar/$', animalitos_views.JugadorUpdateView.as_view(), name='admin_juego_jugador_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugador_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_jugador_delete",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/(?P<pk>\d+?)/eliminar/$', animalitos_views.JugadorDeleteView.as_view(), name='admin_juego_jugador_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugador_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_jugador_detail",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/(?P<pk>\d+?)/$', animalitos_views.JugadorDetailView.as_view(), name='admin_juego_jugador_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugador_ajax_list_by_tipo = Menu.register(
        name="Jugadores por tipo",
        codename="admin_juego_jugador_by_tipo_ajax",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/tipo/$', animalitos_views.JugadorListbyTipoAjax.as_view(), name='admin_juego_jugador_by_tipo_ajax'),
]
if ADD_MENU:
    jugador_ajax_list_by_equipo = Menu.register(
        name="Jugadores por equipo",
        codename="admin_juego_jugador_by_equipo_ajax",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/equipo/$', animalitos_views.JugadorListbyEquipoAjax.as_view(), name='admin_juego_jugador_by_equipo_ajax'),
]
if ADD_MENU:
    jugador_ajax_list_by_equipo_and_tipo = Menu.register(
        name="Jugadores por equipo y tipo",
        codename="admin_juego_jugador_by_equipo_and_tipo_ajax",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/equipo-and-tipo/$', animalitos_views.JugadorListbyEquipoAndTipoAjax.as_view(), name='admin_juego_jugador_by_equipo_and_tipo_ajax'),
]
if ADD_MENU:
    admin_juego_tipo_by_deporte_ajax = Menu.register(
        name="Tipo jugadores por deporte",
        codename="admin_juego_tipo_by_deporte_ajax",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/tipobydeporte/$', animalitos_views.TipoListbyDeporteAjax.as_view(), name='admin_juego_tipo_by_deporte_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugadores_list_datatables = Menu.register(
        name="Jugadores datatables",
        codename="jugadores_list_datatables",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugadores/jugadores_list_datatables/$', animalitos_views.JugadoresDatatableView.as_view(), name='jugadores_list_datatables'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de jugadores
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_jugador_detail = Permissions.register(
        name="Juego | Jugadores | Ver",
        codename="admin_juego_jugador_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugador_detail,
            jugador_list,
            admin_juego_tipo_by_deporte_ajax,
            jugador_ajax_list_by_tipo,
            jugador_ajax_list_by_equipo,
            jugador_ajax_list_by_equipo_and_tipo,
            jugadores_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_jugador_create = Permissions.register(
        name="Juego | Jugadores | Crear",
        codename="admin_juego_jugador_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugador_create,
            jugador_detail,
            jugador_list,
            jugador_ajax_list_by_tipo,
            equipos_ajax_list_by_deporte_simple,
            jugadores_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_jugador_update = Permissions.register(
        name="Juego | Jugadores | Actualizar",
        codename="admin_juego_jugador_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugador_detail,
            jugador_list,
            jugador_update,
            jugador_ajax_list_by_tipo,
            jugadores_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_jugador_delete = Permissions.register(
        name="Juego | Jugadores | Eliminar",
        codename="admin_juego_jugador_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugador_delete,
            jugador_detail,
            jugador_list,
            jugador_ajax_list_by_tipo,
            jugadores_list_datatables,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de grupos de tipos de jugadores
# ===================================================================#
"""
if ADD_MENU:
    jugadortipo_list = Menu.register(
        name="Tipos",
        codename="admin_juego_jugadortipo_list",
        url="/juego/jugador-tipo/",
        menu_suc=jugador_subtitulo,
        icon="icon-person-outline",
        orden=ORDEN(140),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/jugador-tipo/$', animalito_tipo_views.JugadorTipoListView.as_view(), name='admin_juego_jugadortipo_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugadortipo_create = Menu.register(
        name="Crear",
        codename="admin_juego_jugadortipo_create",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador-tipo/crear/$', animalito_tipo_views.JugadorTipoCreateView.as_view(), name='admin_juego_jugadortipo_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugadortipo_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_jugadortipo_update",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador-tipo/(?P<pk>\d+?)/editar/$', animalito_tipo_views.JugadorTipoUpdateView.as_view(), name='admin_juego_jugadortipo_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugadortipo_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_jugadortipo_delete",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador-tipo/(?P<pk>\d+?)/eliminar/$', animalito_tipo_views.JugadorTipoDeleteView.as_view(), name='admin_juego_jugadortipo_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugadortipo_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_jugadortipo_detail",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador-tipo/(?P<pk>\d+?)/$', animalito_tipo_views.JugadorTipoDetailView.as_view(), name='admin_juego_jugadortipo_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    jugadortipo_ajax_list_by_deporte = Menu.register(
        name="Tipos de jugadores por deporte",
        codename="admin_juego_jugadortipo_by_deporte_ajax",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador-tipo/deporte/$', animalito_tipo_views.JugadorTipoListbyDeporteAjax.as_view(), name='admin_juego_jugadortipo_by_deporte_ajax'),
]
if ADD_MENU:
    jugador_ajax_list_by_equipo = Menu.register(
        name="Jugadores por equipo",
        codename="admin_juego_jugador_by_equipo_ajax",
        menu_suc=jugador_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugador/equipo/ajax$', animalitos_views.JugadorListbyEquipoAjax.as_view(), name='admin_juego_jugador_by_equipo_ajax'),
]


"""
# ===================================================================#
#Creado permisos para los urls descritos de jugadortipo
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_jugadortipo_detail = Permissions.register(
        name="Juego | Tipos de jugadores | Ver ",
        codename="admin_juego_jugadortipo_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugadortipo_list,
            jugadortipo_detail,
            jugadortipo_update,
            jugadortipo_create,
            jugadortipo_ajax_list_by_deporte
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_jugadortipo_create = Permissions.register(
        name="Juego | Tipos de jugadores | Crear ",
        codename="admin_juego_jugadortipo_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugadortipo_list,
            jugadortipo_detail,
            jugadortipo_create,
            jugadortipo_ajax_list_by_deporte
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_jugadortipo_update = Permissions.register(
        name="Juego | Tipos de jugadores | Actualizar ",
        codename="admin_juego_jugadortipo_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugadortipo_list,
            jugadortipo_detail,
            jugadortipo_update,
            jugadortipo_ajax_list_by_deporte
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_jugadortipo_delete = Permissions.register(
        name="Juego | Tipos de jugadores | Eliminar ",
        codename="admin_juego_jugadortipo_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            jugador_subtitulo,
            jugadortipo_list,
            jugadortipo_detail,
            jugadortipo_delete,
            jugadortipo_ajax_list_by_deporte
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de temporadas
# ===================================================================#
"""
if ADD_MENU:
    temporadas_subtitulo = Menu.register(
        name="Fechas",
        codename="admin_juego_temporadas_subtitle",
        menu_suc=juego_titulo,
        icon="icon-event-note",
        content_type=2,
        orden=ORDEN(150),
        is_view=True,
    )

"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_create = Menu.register(
        name="Crear",
        codename="admin_juego_temporadas_create",
        url="/juego/temporada/crear/",
        menu_suc=temporadas_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(160),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/temporada/crear/$', vigencias_views.TemporadasCreateView.as_view(), name='admin_juego_temporadas_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_list = Menu.register(
        name="Lista",
        codename="admin_juego_temporadas_list",
        url="/juego/temporadas/",
        menu_suc=temporadas_subtitulo,
        icon="icon-list2",
        orden=ORDEN(170),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/temporadas/$', vigencias_views.TemporadasListView.as_view(), name='admin_juego_temporadas_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_temporadas_update",
        menu_suc=temporadas_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/temporadas/(?P<pk>\d+?)/editar/$', vigencias_views.TemporadasUpdateView.as_view(), name='admin_juego_temporadas_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_temporadas_delete",
        menu_suc=temporadas_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/temporadas/(?P<pk>\d+?)/eliminar/$', vigencias_views.TemporadasDeleteView.as_view(), name='admin_juego_temporadas_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_temporadas_detail",
        menu_suc=temporadas_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/temporadas/(?P<pk>\d+?)/$', vigencias_views.TemporadasDetailView.as_view(), name='admin_juego_temporadas_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_ajax_list_by_torneo = Menu.register(
        name="Fechas por liga",
        codename="admin_juego_temporadas_by_torneo_ajax",
        menu_suc=temporadas_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/temporadas-by-liga/$', vigencias_views.TemporadasListbyTorneoAjax.as_view(), name='admin_juego_temporadas_by_torneo_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_ajax_list_by_deporte = Menu.register(
        name="Fechas por deporte",
        codename="admin_juego_temporadas_by_deporte_ajax",
        menu_suc=temporadas_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/temporadas-by-deporte/$', vigencias_views.TemporadasListbyDeporteAjax.as_view(), name='admin_juego_temporadas_by_deporte_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    temporadas_list_datatables = Menu.register(
        name="Fechas datatables",
        codename="temporadas_list_datatables",
        menu_suc=temporadas_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/jugadores/temporadas_list_datatables/$', vigencias_views.TemporadasDatatableView.as_view(), name='temporadas_list_datatables'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de temporadas
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_temporadas_detail = Permissions.register(
        name="Juego | Fechas | Ver",
        codename="admin_juego_temporadas_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            temporadas_subtitulo,
            temporadas_detail,
            temporadas_list,
            temporadas_ajax_list_by_torneo,
            temporadas_ajax_list_by_deporte,
            temporadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
        ],
    )

    admin_juego_temporadas_create = Permissions.register(
        name="Juego | Fechas | Crear",
        codename="admin_juego_temporadas_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            temporadas_subtitulo,
            temporadas_create,
            temporadas_detail,
            temporadas_list,
            temporadas_ajax_list_by_torneo,
            temporadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
        ],
    )

    admin_juego_temporadas_update = Permissions.register(
        name="Juego | Fechas | Actualizar",
        codename="admin_juego_temporadas_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            temporadas_subtitulo,
            temporadas_detail,
            temporadas_list,
            temporadas_update,
            temporadas_ajax_list_by_torneo,
            temporadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
        ],
    )

    admin_juego_temporadas_delete = Permissions.register(
        name="Juego | Fechas | Eliminar",
        codename="admin_juego_temporadas_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            temporadas_subtitulo,
            temporadas_detail,
            temporadas_list,
            temporadas_delete,
            temporadas_ajax_list_by_torneo,
            temporadas_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de encuentros
# ===================================================================#
"""

if ADD_MENU:
    encuentros_subtitulo = Menu.register(
        name="Sorteo",
        codename="admin_juego_encuentros_subtitle",
        menu_suc=juego_titulo,
        icon="icon-event",
        content_type=2,
        orden=ORDEN(180),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_create = Menu.register(
        name="Crear",
        codename="admin_juego_encuentros_create",
        url="/juego/encuentro/crear/",
        menu_suc=encuentros_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(190),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/encuentro/crear/$', sorteos_views.EncuentrosCreateView.as_view(), name='admin_juego_encuentros_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_list = Menu.register(
        name="Lista",
        codename="admin_juego_encuentros_list",
        url="/juego/encuentros/",
        menu_suc=encuentros_subtitulo,
        icon="icon-list2",
        orden=ORDEN(200),
        is_view=True,
    )
urlpatterns += [
re_path(r'^juego/encuentros/$', sorteos_views.EncuentrosListView.as_view(), name='admin_juego_encuentros_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_encuentros_update",
        menu_suc=encuentros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/encuentro/(?P<pk>\d+?)/editar/$', sorteos_views.EncuentrosUpdateView.as_view(), name='admin_juego_encuentros_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_encuentros_delete",
        menu_suc=encuentros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/encuentro/(?P<pk>\d+?)/eliminar/$', sorteos_views.EncuentrosDeleteView.as_view(), name='admin_juego_encuentros_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_encuentros_detail",
        menu_suc=encuentros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/encuentro/(?P<pk>\d+?)/$', sorteos_views.EncuentrosDetailView.as_view(), name='admin_juego_encuentros_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_restriction = Menu.register(
        name="Restriccion",
        codename="admin_juego_encuentros_restriction",
        menu_suc=encuentros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/encuentro/restriction/(?P<pk>\d+?)/$', sorteos_views.EncuentrosRestrictionView.as_view(), name='admin_juego_encuentros_restriction'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_ajax_list_by_temporada = Menu.register(
        name="Sorteo por temporada",
        codename="admin_juego_encuentros_by_temporada_ajax",
        menu_suc=encuentros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/encuentro-by-temporada/$', sorteos_views.EncuentrosListbyTemporadaAjax.as_view(), name='admin_juego_encuentros_by_temporada_ajax'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    encuentros_list_datatables = Menu.register(
        name="Sorteo datatables",
        codename="encuentros_list_datatables",
        menu_suc=encuentros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/encuentros/encuentros_list_datatables/$', sorteos_views.EncuentrosDatatableView.as_view(), name='encuentros_list_datatables'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de encuentros
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_encuentros_detail = Permissions.register(
        name="Juego | Sorteo | Ver",
        codename="admin_juego_encuentros_detail",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            encuentros_subtitulo,
            encuentros_detail,
            encuentros_list,
            encuentros_ajax_list_by_temporada,
            encuentros_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_juego_encuentros_create = Permissions.register(
        name="Juego | Sorteo | Crear",
        codename="admin_juego_encuentros_create",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            encuentros_subtitulo,
            encuentros_create,
            encuentros_detail,
            encuentros_list,
            encuentros_list_datatables,
            jugador_ajax_list_by_equipo,
            jugador_ajax_list_by_equipo_and_tipo,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_juego_encuentros_update = Permissions.register(
        name="Juego | Sorteo | Actualizar",
        codename="admin_juego_encuentros_update",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            encuentros_subtitulo,
            encuentros_detail,
            encuentros_list,
            encuentros_update,
            encuentros_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_juego_encuentros_delete = Permissions.register(
        name="Juego | Sorteo | Eliminar",
        codename="admin_juego_encuentros_delete",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            encuentros_subtitulo,
            encuentros_detail,
            encuentros_delete,
            encuentros_list,
            encuentros_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_juego_encuentros_restriction = Permissions.register(
        name="Juego | Sorteo | Restriccion",
        codename="admin_juego_encuentros_restriction",
        content_type="admin_juego",
        menus=[
            juego_titulo,
            encuentros_subtitulo,
            encuentros_detail,
            encuentros_restriction,
            encuentros_list,
            encuentros_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )
"""
# ===================================================================#
#                    Urls de modalidades
# ===================================================================#
"""
if ADD_MENU:
    ORDEN = next_orden(4000)
    parlay_titulo = Menu.register(
        name="Parlay",
        codename="admin_logros_title",
        icon="icon-game-controller",
        content_type=1,
        orden=ORDEN(0),
        is_view=True,
    )
if ADD_MENU:
    modalidades_subtitulo = Menu.register(
        name="ModalidadJuego",
        codename="admin_juego_modalidades_subtitle",
        menu_suc=parlay_titulo,
        icon="icon-flow-line",
        content_type=2,
        orden=ORDEN(10),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_create = Menu.register(
        name="Crear",
        codename="admin_juego_modalidades_create",
        url="/parley/modalidad/crear/",
        menu_suc=modalidades_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(20),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/modalidad/crear/$', modalidades_views.ModalidadesCreateView.as_view(), name='admin_juego_modalidades_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_list = Menu.register(
        name="Lista",
        codename="admin_juego_modalidades_list",
        url="/parley/modalidades/",
        menu_suc=modalidades_subtitulo,
        icon="icon-list2",
        orden=ORDEN(30),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/modalidades/$', modalidades_views.ModalidadesListView.as_view(), name='admin_juego_modalidades_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_modalidades_update",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/(?P<pk>\d+?)/editar/$', modalidades_views.ModalidadesUpdateView.as_view(), name='admin_juego_modalidades_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_update_deportes = Menu.register(
        name="Actualizar",
        codename="admin_juego_modalidades_update_deportes",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/(?P<pk>\d+?)/editar/deportes/$', modalidades_views.ModalidadesDeportesUpdateView.as_view(), name='admin_juego_modalidades_update_deportes'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_update_referecias = Menu.register(
        name="Actualizar",
        codename="admin_juego_modalidades_update_referencias",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/(?P<pk>\d+?)/editar/referencias/$', modalidades_views.RestriccionesReferenciasModalidadView.as_view(), name='admin_juego_modalidades_update_referencias'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_modalidades_delete",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/(?P<pk>\d+?)/eliminar/$', modalidades_views.ModalidadesDeleteView.as_view(), name='admin_juego_modalidades_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_modalidades_detail",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/(?P<pk>\d+?)/$', modalidades_views.ModalidadesDetailView.as_view(), name='admin_juego_modalidades_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    modalidades_grupos_ajax = Menu.register(
        name="ModalidadJuego por grupo",
        codename="admin_juego_modalidades_by_grupo_ajax",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/modalidad-by-grupo/$', modalidades_views.ModalidadListbyGrupoAjax.as_view(), name='admin_juego_modalidades_by_grupo_ajax'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de modalidades
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_modalidades_detail = Permissions.register(
        name="Juego | ModalidadJuego | Ver",
        codename="admin_juego_modalidades_detail",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            modalidades_detail,
            modalidades_list,
            modalidades_grupos_ajax,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_modalidades_create = Permissions.register(
        name="Juego | ModalidadJuego | Crear",
        codename="admin_juego_modalidades_create",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            modalidades_create,
            modalidades_detail,
            modalidades_list,
            modalidades_update_deportes,
            modalidades_update_referecias,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_modalidades_update = Permissions.register(
        name="Juego | ModalidadJuego | Actualizar",
        codename="admin_juego_modalidades_update",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            modalidades_detail,
            modalidades_list,
            modalidades_update,
            modalidades_update_deportes,
            modalidades_update_referecias,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_modalidades_delete = Permissions.register(
        name="Juego | ModalidadJuego | Eliminar",
        codename="admin_juego_modalidades_delete",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            modalidades_detail,
            modalidades_list,
            modalidades_delete,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de grupos de apuesta
# ===================================================================#
"""

if ADD_MENU:
    gruposapuestas_create = Menu.register(
        name="Crear",
        codename="admin_juego_gruposapuestas_create",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/grupo/crear/$', gruposapuestas_views.GruposApuestasCreateView.as_view(), name='admin_juego_gruposapuestas_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposapuestas_list = Menu.register(
        name="Lista",
        codename="admin_juego_gruposapuestas_list",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidades/grupos/$', gruposapuestas_views.GruposApuestasListView.as_view(), name='admin_juego_gruposapuestas_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposapuestas_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_gruposapuestas_update",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/grupo/(?P<pk>\d+?)/editar/$', gruposapuestas_views.GruposApuestasUpdateView.as_view(), name='admin_juego_gruposapuestas_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposapuestas_update_logros = Menu.register(
        name="Actualizar",
        codename="admin_juego_gruposapuestas_update_logros",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/grupo/(?P<pk>\d+?)/editar/logros/$', gruposapuestas_views.RestriccionesReferenciasGrupoView.as_view(), name='admin_juego_gruposapuestas_update_logros'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposapuestas_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_gruposapuestas_delete",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/grupo/(?P<pk>\d+?)/eliminar/$', gruposapuestas_views.GruposApuestasDeleteView.as_view(), name='admin_juego_gruposapuestas_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposapuestas_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_gruposapuestas_detail",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/modalidad/grupo/(?P<pk>\d+?)/$', gruposapuestas_views.GruposApuestasDetailView.as_view(), name='admin_juego_gruposapuestas_detail'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    gruposapuestas_by_deporte_ajax = Menu.register(
        name="Grupo de apuesta por deporte",
        codename="admin_juego_gruposapuestas_by_deporte_ajax",
        menu_suc=modalidades_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/grupo-by-deporte/$', gruposapuestas_views.GruposListbyDeporteAjax.as_view(), name='admin_juego_gruposapuestas_by_deporte_ajax'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de grupos de apuesta
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_gruposapuestas_detail = Permissions.register(
        name="Juego | Grupos de apuesta | Ver",
        codename="admin_juego_gruposapuestas_detail",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            gruposapuestas_detail,
            gruposapuestas_list,
            gruposapuestas_by_deporte_ajax,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_gruposapuestas_create = Permissions.register(
        name="Juego | Grupos de apuesta | Crear",
        codename="admin_juego_gruposapuestas_create",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            gruposapuestas_create,
            gruposapuestas_detail,
            gruposapuestas_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_gruposapuestas_update = Permissions.register(
        name="Juego | Grupos de apuesta | Actualizar",
        codename="admin_juego_gruposapuestas_update",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            gruposapuestas_detail,
            gruposapuestas_list,
            gruposapuestas_update,
            gruposapuestas_update_logros
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_gruposapuestas_delete = Permissions.register(
        name="Juego | Grupos de apuesta | Eliminar",
        codename="admin_juego_gruposapuestas_delete",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            modalidades_subtitulo,
            gruposapuestas_delete,
            gruposapuestas_detail,
            gruposapuestas_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
#                    Urls de condiciones
# ===================================================================#
"""
if ADD_MENU:
    condiciones_subtitulo = Menu.register(
        name="Condiciones",
        codename="admin_juego_condiciones_subtitle",
        menu_suc=parlay_titulo,
        icon="icon-flow-parallel",
        content_type=2,
        orden=ORDEN(100),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    condiciones_create = Menu.register(
        name="Crear",
        codename="admin_juego_condiciones_create",
        url="/parley/condicion/crear/",
        menu_suc=condiciones_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(110),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/condicion/crear/$', condiciones_views.CondicionesCreateView.as_view(), name='admin_juego_condiciones_create'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    condiciones_list = Menu.register(
        name="Lista",
        codename="admin_juego_condiciones_list",
        url="/parley/condiciones/",
        menu_suc=condiciones_subtitulo,
        icon="icon-list2",
        orden=ORDEN(120),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/condiciones/$', condiciones_views.CondicionesListView.as_view(), name='admin_juego_condiciones_list'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    condiciones_update = Menu.register(
        name="Actualizar",
        codename="admin_juego_condiciones_update",
        menu_suc=condiciones_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/condicion/(?P<pk>\d+?)/editar/$', condiciones_views.CondicionesUpdateView.as_view(), name='admin_juego_condiciones_update'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    condiciones_update_referecias = Menu.register(
        name="Actualizar",
        codename="admin_juego_condiciones_update_referencias",
        menu_suc=condiciones_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/condicion/(?P<pk>\d+?)/editar/referencias/$', condiciones_views.RestriccionesReferenciasCondicionView.as_view(), name='admin_juego_condiciones_update_referencias'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    condiciones_delete = Menu.register(
        name="Eliminar",
        codename="admin_juego_condiciones_delete",
        menu_suc=condiciones_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/condicion/(?P<pk>\d+?)/eliminar/$', condiciones_views.CondicionesDeleteView.as_view(), name='admin_juego_condiciones_delete'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    condiciones_detail = Menu.register(
        name="Detalle",
        codename="admin_juego_condiciones_detail",
        menu_suc=condiciones_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/condicion/(?P<pk>\d+?)/$', condiciones_views.CondicionesDetailView.as_view(), name='admin_juego_condiciones_detail'),
]
"""
# ===================================================================#
#     Creado permisos para los urls descritos de condiciones
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_condiciones_detail = Permissions.register(
        name="Juego | Condiciones | Ver",
        codename="admin_juego_condiciones_detail",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            condiciones_subtitulo,
            condiciones_create,
            condiciones_detail,
            condiciones_list,
            condiciones_update,
            condiciones_update_referecias,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_condiciones_create = Permissions.register(
        name="Juego | Condiciones | Crear",
        codename="admin_juego_condiciones_create",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            condiciones_subtitulo,
            condiciones_create,
            condiciones_detail,
            condiciones_list,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_condiciones_update = Permissions.register(
        name="Juego | Condiciones | Actualizar",
        codename="admin_juego_condiciones_update",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            condiciones_subtitulo,
            condiciones_detail,
            condiciones_list,
            condiciones_update,
            condiciones_update_referecias,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )

    admin_juego_condiciones_delete = Permissions.register(
        name="Juego | Condiciones | Eliminar",
        codename="admin_juego_condiciones_delete",
        content_type="admin_juego",
        menus=[
            parlay_titulo,
            condiciones_subtitulo,
            condiciones_detail,
            condiciones_list,
            condiciones_delete
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
        ],
    )
"""
# ===================================================================#
# grupo de urls por ajax
# ===================================================================#
"""
if ADD_MENU:
    admin_juego_ajax = Permissions.register(
        name="Juego | Peticiones ajax",
        codename="admin_juego_ajax",
        content_type="admin_juego",
        menus=[
            liga_ajax_list_by_deporte,
            liga_ajax_get,
            jornadas_ajax_list_by_temporada,
            gruposjuego_ajax_list_by_temporada,
            equipos_ajax_list_by_temporada_1,
            equipos_ajax_list_by_temporada_2,
            equipos_ajax_list_by_temporada_3,
            equipos_ajax_list_by_grupo,
            equipos_ajax_list_by_deporte,
            equipos_ajax_list_by_liga,
            jugador_ajax_list_by_tipo,
            jugadortipo_ajax_list_by_deporte,
            temporadas_ajax_list_by_torneo,
            temporadas_ajax_list_by_deporte,
            encuentros_ajax_list_by_temporada,
            modalidades_grupos_ajax,
            gruposapuestas_by_deporte_ajax,
            equipos_list_datatables,
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
"""
# ===================================================================#
"""
if ADD_MENU:
    Groups.register(
        name="Permisos Juegos",
        codename="admin_juego_basic",
        permissions=[
            admin_juego_eventnotification_list,

            admin_juego_sistemajuego_detail,
            admin_juego_sistemajuego_update,

            admin_juego_deportes_detail,
            admin_juego_deportes_create,
            admin_juego_deportes_update,
            admin_juego_deportes_delete,

            admin_juego_torneos_detail,
            admin_juego_torneos_create,
            admin_juego_torneos_update,
            admin_juego_torneos_delete,
            admin_juego_torneos_ajax,

            admin_juego_jornadas_detail,
            admin_juego_jornadas_create,
            admin_juego_jornadas_update,
            admin_juego_jornadas_delete,

            admin_juego_gruposjuego_detail,
            admin_juego_gruposjuego_create,
            admin_juego_gruposjuego_update,
            admin_juego_gruposjuego_delete,

            admin_juego_equipos_detail,
            admin_juego_equipos_create,
            admin_juego_equipos_update,
            admin_juego_equipos_delete,
            admin_juego_equipos_ajax,

            admin_juego_jugador_detail,
            admin_juego_jugador_create,
            admin_juego_jugador_update,
            admin_juego_jugador_delete,

            admin_juego_jugadortipo_detail,
            admin_juego_jugadortipo_create,
            admin_juego_jugadortipo_update,
            admin_juego_jugadortipo_delete,

            admin_juego_temporadas_detail,
            admin_juego_temporadas_create,
            admin_juego_temporadas_update,
            admin_juego_temporadas_delete,

            admin_juego_encuentros_detail,
            admin_juego_encuentros_create,
            admin_juego_encuentros_update,
            admin_juego_encuentros_delete,
            admin_juego_encuentros_restriction,

            admin_juego_modalidades_detail,
            admin_juego_modalidades_create,
            admin_juego_modalidades_update,
            admin_juego_modalidades_delete,

            admin_juego_gruposapuestas_detail,
            admin_juego_gruposapuestas_create,
            admin_juego_gruposapuestas_update,
            admin_juego_gruposapuestas_delete,

            admin_juego_condiciones_detail,
            admin_juego_condiciones_create,
            admin_juego_condiciones_update,
            admin_juego_condiciones_delete,

            admin_juego_ajax,
        ],
    )
