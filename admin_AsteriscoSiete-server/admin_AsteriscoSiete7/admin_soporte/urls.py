# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
from admin_permisologia.models import Groups, Menu, Permissions
from admin_soporte.views import ListadoGeneralTickets, comercializadoras_views, sistema_views, tickests_views
from django.urls import include, re_path

"""
# ===================================================================#
"""
urlpatterns = [
]
"""
# ===================================================================#
#                      Urls de soporte
# ===================================================================#

Los enlaces del menu se registran
"""
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(7000)

    soporte_titulo = Menu.register(
        name="Soporte",
        codename="admin_soporte_title",
        icon="icon-headset-m",
        content_type=1,
        orden=ORDEN(0),
        is_view=True,
    )

    soporte_subtitulo = Menu.register(
        name="Tickets",
        codename="admin_soporte_tickets_subtitle",
        menu_suc=soporte_titulo,
        icon="icon-ticket",
        content_type=2,
        orden=ORDEN(1),
        is_view=True,
    )
"""
# ===================================================================#
#                   Urls de soporte de tickets
# ===================================================================#
"""
if ADD_MENU:
    tickets_list = Menu.register(
        name="Gestionar",
        codename="admin_soporte_BuscarTicket_url",
        url="/soporte/tickets/gestion/",
        menu_suc=soporte_subtitulo,
        icon="icon-tools2",
        orden=ORDEN(10),
        is_view=True,
    )
urlpatterns += [
re_path(r'^soporte/tickets/gestion/$', tickests_views.BuscarTicket.as_view(), name='admin_soporte_BuscarTicket_url'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    tickets_edit = Menu.register(
        name="Gestionar ticket",
        codename="admin_soporte_DetalleTicket_url",
        menu_suc=soporte_subtitulo,
        orden=ORDEN(20),
    )
urlpatterns += [
re_path(r'^soporte/tickets/gestion/(?P<pk>\d+?)/$', tickests_views.DetalleTicket.as_view(), name='admin_soporte_DetalleTicket_url'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    tickets_list_view = Menu.register(
        name="Consulta de Tickets",
        codename="admin_soporte_consulta_de_tickets_url",
        url="/soporte/tickets/listado/",
        menu_suc=soporte_subtitulo,
        icon="icon-list2",
        orden=ORDEN(20),
        is_view=True,
    )
urlpatterns += [
re_path(r'^soporte/tickets/listado/$', ListadoGeneralTickets.ListadoTickets.as_view(), name='admin_soporte_tickets_list_view_url'),
]
if ADD_MENU:
    tickets_list_ajax = Menu.register(
        name="Consulta de Tickets",
        codename="admin_soporte_tickets_list_ajax_url",
        menu_suc=soporte_subtitulo,
    )
urlpatterns += [
re_path(r'^soporte/tickets/listado/get/$', ListadoGeneralTickets.ListadoTicketsAjax.as_view(), name='admin_soporte_tickets_list_ajax_url'),
]
"""
# ===================================================================#
#   Creado permisos para los urls descritos de soporte de tickets
# ===================================================================#
"""
if ADD_MENU:
    admin_soporte_tickets_manage = Permissions.register(
        name="Soporte | Tickets | Detalle",
        codename="admin_soporte_tickets_manage_edit",
        content_type="admin_soporte",
        menus=[
            soporte_titulo,
            soporte_subtitulo,
            tickets_list,
            tickets_edit,
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
    admin_soporte_tickets_manage = Permissions.register(
        name="Soporte | Tickets | Listado",
        codename="admin_soporte_tickets_manage_list",
        content_type="admin_soporte",
        menus=[
            soporte_titulo,
            soporte_subtitulo,
            tickets_list_view,
            tickets_list_ajax,
            tickets_edit,
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
#                Urls de soporte de sistema
# ===================================================================#
"""
if ADD_MENU:
    soporte_sistema_subtitulo = Menu.register(
        name="Sistema",
        codename="admin_soporte_sistema_subtitle",
        menu_suc=soporte_titulo,
        icon="icon-security",
        content_type=2,
        orden=ORDEN(100),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    sistema_opciones = Menu.register(
        name="Opciones",
        codename="admin_soporte_sistema_opciones",
        url="/soporte/sistema/opciones/",
        menu_suc=soporte_sistema_subtitulo,
        icon="icon-tools2",
        orden=ORDEN(110),
        is_view=True,
    )
urlpatterns += [
re_path(r'^soporte/sistema/opciones/$', sistema_views.OptionsSystem.as_view(), name='admin_soporte_sistema_opciones'),
]
"""
# ===================================================================#
#  Creado permisos para los urls descritos de soporte de sistema
# ===================================================================#
"""
if ADD_MENU:
    admin_soporte_sistema_manage = Permissions.register(
        name="Soporte | Sistema",
        codename="admin_soporte_sistema_manage",
        content_type="admin_soporte",
        menus=[
            soporte_titulo,
            soporte_sistema_subtitulo,
            sistema_opciones,
        ],
        profiles=[
            "userprofile_master",
            "userprofile_operadora",
            "userprofile_bloque",
        ],
    )
"""
# ===================================================================#
#                Urls de soporte para comercializadoras
# ===================================================================#
"""
if ADD_MENU:
    soporte_comercializacion_subtitulo = Menu.register(
        name="Comercializadoras",
        codename="admin_soporte_comercializacion_subtitle",
        menu_suc=soporte_titulo,
        icon="icon-store-mall-directory",
        content_type=2,
        orden=ORDEN(120),
        is_view=True,
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    comercializadora_opciones = Menu.register(
        name="Restaurar",
        codename="admin_soporte_comercializacion_opciones_restaurar",
        url="/soporte/comercializacion/restaurar/",
        menu_suc=soporte_comercializacion_subtitulo,
        icon="icon-restore",
        orden=ORDEN(120),
        is_view=True,
    )
urlpatterns += [
re_path(r'^soporte/comercializacion/restaurar/$', comercializadoras_views.OptionsRestore.as_view(), name='admin_soporte_comercializacion_opciones_restaurar'),
]
"""
# ===================================================================#
#  Creado permisos para los urls descritos de soporte de comercializadoras
# ===================================================================#
"""
if ADD_MENU:
    admin_soporte_sistema_manage = Permissions.register(
        name="Soporte | comercializadoras",
        codename="admin_soporte_comercializadoras_manage",
        content_type="admin_soporte",
        menus=[
            soporte_titulo,
            soporte_comercializacion_subtitulo,
            comercializadora_opciones,
        ],
        profiles=[
            "userprofile_master",
        ],
    )
"""
# ===================================================================#
"""
if ADD_MENU:
    Groups.register(
        name="Permisos basicos Operadora",
        codename="userprofile_operadora_basic",
        permissions=[
            admin_soporte_tickets_manage,
            admin_soporte_sistema_manage,
        ],
    )
