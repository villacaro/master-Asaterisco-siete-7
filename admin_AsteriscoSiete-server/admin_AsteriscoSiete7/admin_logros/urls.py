# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
from admin_lib.util_print import PdfView
from admin_logros.views import calculadora_views, logros_views
from admin_permisologia.models import Groups, Menu, Permissions
from django.urls import include, re_path

# ===================================================================#
urlpatterns = [
]
# ===================================================================#
#                          Urls de logros
# ===================================================================#
"""
Los enlaces del menu se registran
"""
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(4000)

    parlay_titulo = Menu.register(
        name="Parlay",
        codename="admin_logros_title",
        icon="icon-star",
        content_type=1,  # nivel 1 de titulo
        orden=ORDEN(0),
        is_view=True,
    )

    parley_logros_subtitulo = Menu.register(
        name="Logros",
        codename="admin_logros_parlay_subtitle",
        menu_suc=parlay_titulo,
        icon="icon-star",
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(300),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    logros_list_edit = Menu.register(
        name="Cargar logros",
        codename="admin_logros_encuentros_list_edit",
        url="/parley/logros/administrar-logros/",
        menu_suc=parley_logros_subtitulo,
        icon="icon-star-half",
        orden=ORDEN(310),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/logros/administrar-logros/$', logros_views.LogrosListView.as_view(), name='admin_logros_encuentros_list_edit'),
]
# ===================================================================#
if ADD_MENU:
    logros_create_update = Menu.register(
        name="Actualizar o crear logros",
        codename="admin_logros_ecuentros_create_update",
        menu_suc=parley_logros_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/logro/(?P<pk>\d+?)/asignar/$', logros_views.LogrosCreateUpdateView.as_view(), name='admin_logros_ecuentros_create_update'),
]
# ===================================================================#
if ADD_MENU:
    logros_list_detail = Menu.register(
        name="Ver logros",
        codename="admin_logros_encuentros_list_detail",
        url="/parley/logros/lista/",
        menu_suc=parley_logros_subtitulo,
        icon="icon-star-outline",
        orden=ORDEN(320),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/logros/lista/$', logros_views.LogrosListDetailView.as_view(), name='admin_logros_encuentros_list_detail'),
]
# ===================================================================#
if ADD_MENU:
    logros_list_print = Menu.register(
        name="Imprimir logros",
        codename="admin_logros_encuentros_detail_imprimir",
        menu_suc=parley_logros_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/logros/lista/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_logros_encuentros_detail_imprimir'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    logros_list_datatables = Menu.register(
        name="Logros datatables",
        codename="logros_list_datatables",
        menu_suc=parley_logros_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/logros/logros_list_datatables/$', logros_views.LogrosDatatableView.as_view(), name='logros_list_datatables'),
]

"""
# ===================================================================#
"""
if ADD_MENU:
    calculadora = Menu.register(
        name="Calculadora parley",
        codename="admin_logros_calculadora",
        url="/parley/logros/calculadora/",
        menu_suc=parley_logros_subtitulo,
        icon="icon-star-outline",
        orden=ORDEN(330),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/logros/calculadora/$', calculadora_views.CalculadoraView.as_view(), name='admin_logros_calculadora'),
]

# ===================================================================#
#       Creado permisos para los urls descritos de logros
# ===================================================================#
if ADD_MENU:
    admin_logros_manage = Permissions.register(
        name="Juego | Logros | Gestionar",
        codename="admin_logros_manage",
        content_type="admin_logros",
        menus=[
            parlay_titulo,
            parley_logros_subtitulo,
            logros_list_edit,
            logros_create_update,
            logros_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_logros_print = Permissions.register(
        name="Juego | Logros | Ver",
        codename="admin_logros_print",
        content_type="admin_logros",
        menus=[
            parlay_titulo,
            parley_logros_subtitulo,
            logros_list_detail,
            logros_list_print,
            logros_list_datatables,
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

    admin_logros_calculadora = Permissions.register(
        name="Juego | Logros | Calculadora",
        codename="admin_logros_calculadora",
        content_type="admin_logros",
        menus=[
            calculadora
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
        name="Permisos Logros",
        codename="admin_logro_basic",
        permissions=[
            admin_logros_manage,
            admin_logros_print,
            admin_logros_calculadora,
        ],
    )
