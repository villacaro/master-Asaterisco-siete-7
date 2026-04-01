# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
from admin_lib.util_print import PdfView
from admin_permisologia.models import Groups, Menu, Permissions
from admin_resultados.views import resultados_views
from django.urls import include, re_path

# ===================================================================#
urlpatterns = [
]
# ===================================================================#
#                   Urls de resultados
# ===================================================================#
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
        icon="icon-soccer",
        content_type=1,  # nivel 1 de titulo
        orden=ORDEN(0),
        is_view=True,
    )

    resultados_subtitulo = Menu.register(
        name="Resultados",
        codename="admin_resultados_subtitle",
        menu_suc=juego_titulo,
        icon="icon-check",
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(700),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    resultados_list_edit = Menu.register(
        name="Cargar resultados",
        codename="admin_resultados_encuentros_resultados_list_edit",
        url="/parley/resultados/administrar-resultados/",
        menu_suc=resultados_subtitulo,
        icon="icon-check",
        orden=ORDEN(710),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/resultados/administrar-resultados/$', resultados_views.ResultadosEncuentrosListView.as_view(), name='admin_resultados_encuentros_resultados_list_edit'),
]
# ===================================================================#
if ADD_MENU:
    resultados_premiar_edit = Menu.register(
        name="Premiar resultados",
        codename="admin_resultados_premiar_edit",
        menu_suc=resultados_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/resultados/(?P<encuentro>\d+?)/premiar/$', resultados_views.ResultadosPremiarView.as_view(), name='admin_resultados_premiar_edit'),
]
# ===================================================================#
if ADD_MENU:
    resultados_create_update = Menu.register(
        name="Actualizar o crear resultados",
        codename="admin_resultados_ecuentros_resultados_create_update",
        menu_suc=resultados_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/resultado/(?P<pk>\d+?)/asignar/$', resultados_views.ResultadosCreateUpdateView.as_view(), name='admin_resultados_ecuentros_resultados_create_update'),
]
# ===================================================================#
if ADD_MENU:
    resultados_change = Menu.register(
        name="Cambiar resultados",
        codename="admin_resultados_resultados_change",
        menu_suc=resultados_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/resultado/(?P<pk>\d+?)/change/$', resultados_views.ResultadosChangeView.as_view(), name='admin_resultados_resultados_change'),
]

# ===================================================================#
if ADD_MENU:
    resultados_list_detail = Menu.register(
        name="Ver resultados",
        codename="admin_resultados_encuentros_resultados_list_detail",
        url="/parley/resultados/lista/",
        menu_suc=resultados_subtitulo,
        icon="icon-list2",
        orden=ORDEN(720),
        is_view=True,
    )
urlpatterns += [
re_path(r'^parley/resultados/lista/$', resultados_views.ResultadosLoadListView.as_view(), name='admin_resultados_encuentros_resultados_list_detail'),
]
# ===================================================================#
if ADD_MENU:
    resultados_list_print = Menu.register(
        name="Imprimir resultados",
        codename="admin_resultados_encuentros_resultados_detail_imprimir",
        menu_suc=resultados_subtitulo,
    )
urlpatterns += [
re_path(r'^parley/resultados/lista/pdf/(?P<cache_key>.+?)/$', PdfView, name='admin_resultados_encuentros_resultados_detail_imprimir'),
]
"""
# ===================================================================#
"""
if ADD_MENU:
    resultados_list_datatables = Menu.register(
        name="Resultados datatables",
        codename="resultados_list_datatables",
        menu_suc=resultados_subtitulo,
    )
urlpatterns += [
re_path(r'^juego/resultados/resultados_list_datatables/$', resultados_views.ResultadosDatatableView.as_view(), name='resultados_list_datatables'),
]
# ===================================================================#
#     Creado permisos para los urls descritos de resultados
# ===================================================================#
if ADD_MENU:
    admin_resultados_manage = Permissions.register(
        name="Juego | Resultados | Gestionar",
        codename="admin_resultados_manage",
        content_type="admin_resultados",
        menus=[
            juego_titulo,
            resultados_subtitulo,
            resultados_list_edit,
            resultados_create_update,
            resultados_list_datatables,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    admin_resultados_print = Permissions.register(
        name="Juego | Resultados | Ver",
        codename="admin_resultados_print",
        content_type="admin_resultados",
        menus=[
            juego_titulo,
            resultados_subtitulo,
            resultados_list_detail,
            resultados_list_print,
            resultados_list_datatables,
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

    admin_resultados_manage = Permissions.register(
        name="Juego | Resultados | Premiar",
        codename="admin_resultados_premio",
        content_type="admin_resultados",
        menus=[
            juego_titulo,
            resultados_subtitulo,
            resultados_premiar_edit,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

    resultados_change = Permissions.register(
        name="Juego | Resultados | Cambiar",
        codename="admin_resultados_change",
        content_type="admin_resultados",
        menus=[
            juego_titulo,
            resultados_subtitulo,
            resultados_change,
        ],
        profiles=[
            "userprofile_operadora",
            "userprofile_bloque",
            "userprofile_banca",
        ],
    )

# ===================================================================#
if ADD_MENU:
    Groups.register(
        name="Permisos Resultados",
        codename="admin_resultados_basic",
        permissions=[
            admin_resultados_manage,
            admin_resultados_print,
        ],
    )
