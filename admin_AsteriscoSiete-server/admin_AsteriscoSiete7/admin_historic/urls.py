# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
from admin_historic.views import filter_views, historic_user_views, historic_views
from admin_permisologia.models import Menu, Permissions
from django.urls import include, re_path

# ===================================================================#
urlpatterns = [
]
# ===================================================================#
#                    Urls Historic
# ===================================================================#
"""
Los enlaces del menu se registran
"""
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(5000)

    users_titulo = Menu.register(
        name="Usuarios",
        codename="admin_users_users_title",
        icon="icon-users",
        content_type=1,  # nivel 1 de titulo
        orden=ORDEN(0),
        is_view=True,
    )

    users_subtitulo = Menu.register(
        name="Usuarios",
        codename="admin_users_users_subtitle",
        menu_suc=users_titulo,
        icon="icon-users",
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(1),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    users_auditoria_list = Menu.register(
        name="Auditoria",
        codename="admin_historic_users_list",
        url="/auditoria/usuarios/",
        menu_suc=users_subtitulo,
        icon="icon-location-history",
        orden=ORDEN(30),  # continua numeracion de los url de users
        is_view=True,
    )
urlpatterns += [
re_path(r'^auditoria/usuarios/$', historic_user_views.HistoricUsersListView.as_view(), name='admin_historic_users_list'),
]
# ===================================================================#
if ADD_MENU:
    users_list_datatables = Menu.register(
        name="Users lista datatables",
        codename="users_list_datatables",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/usuarios/datatable/$', historic_user_views.HistoricUsersDatatableView.as_view(), name='users_list_datatables'),
]
# ===================================================================#
if ADD_MENU:
    comercializacion_list = Menu.register(
        name="Lista de comercializadoras por usuario",
        codename="admin_historic_users_list_filter_comer",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/comercializadoras/filter/$', filter_views.ComercializadorasListbyProfileAjax.as_view(), name='admin_historic_users_list_filter_comer'),
]
# ===================================================================#
if ADD_MENU:
    users_auditoria_detalle = Menu.register(
        name="Detalle de auditoria por usuario",
        codename="admin_historic_users_detail",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/usuario/(?P<pk>\d+?)/$', historic_user_views.HistoricUsersDetailView.as_view(), name='admin_historic_users_detail'),
]
# ===================================================================#
if ADD_MENU:
    users_auditoria_detalle_datatables = Menu.register(
        name="Auditoria lista por usuario datatables",
        codename="users_auditoria_detalle_datatables",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/usuarios/detalle/datatable/$', historic_user_views.HistoricUsersDetailDatatableView.as_view(), name='users_auditoria_detalle_datatables'),
]
# ===================================================================#
if ADD_MENU:
    users_auditoria_2 = Menu.register(
        name="Detalle de auditoria por usuario y app",
        codename="admin_historic_users_detail_detail",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/usuario/(?P<pk>\d+?)/(?P<key>\w+?)/$', historic_views.HistoricUsersDetailDetailView.as_view(), name='admin_historic_users_detail_detail'),
]
# ===================================================================#
if ADD_MENU:
    users_auditoria_3 = Menu.register(
        name="Detalle de auditoria por app y modelo",
        codename="admin_historic_app_model_ref",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/(?P<app>\w+?)/model/(?P<model>\w+?)/(?P<ref>\w+?)/$', historic_views.HistoricAppModelRefView.as_view(), name='admin_historic_app_model_ref'),
]
# ===================================================================#
if ADD_MENU:
    users_auditoria_4 = Menu.register(
        name="Detalle maximo de auditoria",
        codename="admin_historic_app_model_ref_detail",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/(?P<app>\w+?)/model/(?P<model>\w+?)/(?P<ref>\w+?)/(?P<pk>\w+?)/$', historic_views.HistoricAppModelRefDetailView.as_view(), name='admin_historic_app_model_ref_detail'),
]
# ===================================================================#
if ADD_MENU:
    app_model_list_datatables = Menu.register(
        name="App Model lista datatables",
        codename="app_model_list_datatables",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^auditoria/app_model_list_datatables/$', historic_views.HistoricAppModelRefDatatableView.as_view(), name='app_model_list_datatables'),
]

# ===================================================================#
#       Creado permisos para los urls descritos de auditoria
# ===================================================================#
if ADD_MENU:
    Permissions.register(
        name="Auditoria | Ver",
        codename="admin_historic_auditoria",
        content_type="admin_historic",
        menus=[
            users_titulo,
            users_subtitulo,
            users_auditoria_list,
            users_auditoria_detalle,
            users_auditoria_2,
            users_auditoria_3,
            users_auditoria_4,
            users_auditoria_detalle_datatables,
            users_list_datatables,
            app_model_list_datatables,
            comercializacion_list,
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
#                        Urls Account
# ===================================================================#
if ADD_MENU:
    users_accont_auditoria = Menu.register(
        name="Mi cuenta, ver auditoria",
        codename="admin_historic_account_detail",
        url="/account/auditoria/",
        menu_suc=users_subtitulo,
        is_global=True
    )
urlpatterns += [
re_path(r'^account/auditoria/$', historic_user_views.HistoricAccountDetailView.as_view(), name='admin_historic_account_detail'),
]
# ===================================================================#
if ADD_MENU:
    users_accont_auditoria_1 = Menu.register(
        name="Mi cuenta, ver detalle de auditoria",
        codename="admin_historic_account_detail_detail",
        menu_suc=users_subtitulo,
        is_global=True
    )
urlpatterns += [
re_path(r'^account/auditoria/(?P<key>\w+?)/$', historic_views.HistoricAccountDetailDetailView.as_view(), name='admin_historic_account_detail_detail'),
]
# ===================================================================#
#       Creado permisos para los urls descritos de account
# ===================================================================#
if ADD_MENU:
    Permissions.register(
        name="My cuenta",
        codename="admin_users_users_account",
        content_type="admin_users",
        menus=[
            users_accont_auditoria,
            users_accont_auditoria_1,
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
