# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
from admin_permisologia.models import Groups, Menu, Permissions
from admin_users.views import filters_views, users_views
from django.urls import include, re_path

# ===================================================================#
urlpatterns = [
]
# ===================================================================#
#                        Urls Users
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
    users_create = Menu.register(
        name="Crear",
        codename="admin_users_users_create",
        url="/usuario/crear/",
        menu_suc=users_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(10),
        is_view=True,
    )
urlpatterns += [
re_path(r'^usuario/crear/$', users_views.UsersCreateView.as_view(), name='admin_users_users_create'),
]
# ===================================================================#
if ADD_MENU:
    users_list = Menu.register(
        name="Listar",
        codename="admin_users_users_list",
        url="/usuarios/",
        menu_suc=users_subtitulo,
        icon="icon-list",
        orden=ORDEN(20),
        is_view=True,
    )
urlpatterns += [
re_path(r'^usuarios/$', users_views.UsersListView.as_view(), name='admin_users_users_list'),
]
# ===================================================================#
if ADD_MENU:
    users_update = Menu.register(
        name="Actualizar",
        codename="admin_users_users_update",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuario/(?P<pk>\d+?)/editar/$', users_views.UsersUpdateView.as_view(), name='admin_users_users_update'),
]
# ===================================================================#
if ADD_MENU:
    users_customize = Menu.register(
        name="Personalizar",
        codename="admin_users_users_customize",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuario/(?P<pk>\d+?)/personalizar/$', users_views.UsersCustomizeView.as_view(), name='admin_users_users_customize'),
]
# ===================================================================#
if ADD_MENU:
    users_update_password = Menu.register(
        name="Actualizar contraseña",
        codename="admin_users_users_update_password",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuario/(?P<pk>\d+?)/editar/password/$', users_views.UsersUpdatePasswordView.as_view(), name='admin_users_users_update_password'),
]
# ===================================================================#
if ADD_MENU:
    users_delete = Menu.register(
        name="Eliminar",
        codename="admin_users_users_delete",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuario/(?P<pk>\d+?)/eliminar/$', users_views.UsersDeleteView.as_view(), name='admin_users_users_delete'),
]
# ===================================================================#
if ADD_MENU:
    users_detail = Menu.register(
        name="Detalle",
        codename="admin_users_users_detail",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuario/(?P<pk>\d+?)/$', users_views.UsersDetailView.as_view(), name='admin_users_users_detail'),
]
# ===================================================================#
if ADD_MENU:
    userslist_list_datatables = Menu.register(
        name="Users lista datatables",
        codename="userslist_list_datatables",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuarios/userslist_list_datatables/$', users_views.UsersDatatableView.as_view(), name='userslist_list_datatables'),
]
# ===================================================================#
if ADD_MENU:
    comercializacion_list_by_user_ajax = Menu.register(
        name="Lista de comercializadoras por usuario",
        codename="admin_users_comercializacion_list_by_user_ajax",
        menu_suc=users_subtitulo,
    )
urlpatterns += [
re_path(r'^usuarios/comercializacion_list_by_user_ajax/$', filters_views.ComercializadorasListbyProfileAjax.as_view(), name='admin_users_comercializacion_list_by_user_ajax'),
]
# ===================================================================#
#       Creado permisos para los urls descritos de users
# ===================================================================#
if ADD_MENU:
    admin_users_users_detail = Permissions.register(
        name="Usuarios | Ver",
        codename="admin_users_users_detail",
        content_type="admin_users",
        menus=[
            users_titulo,
            users_subtitulo,
            users_detail,
            users_list,
            userslist_list_datatables,
            comercializacion_list_by_user_ajax,
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

    admin_users_users_create = Permissions.register(
        name="Usuarios | Crear",
        codename="admin_users_users_create",
        content_type="admin_users",
        menus=[
            users_titulo,
            users_subtitulo,
            users_create,
            users_detail,
            users_list,
            userslist_list_datatables,
            comercializacion_list_by_user_ajax,
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

    admin_users_users_update = Permissions.register(
        name="Usuarios | Editar",
        codename="admin_users_users_update",
        content_type="admin_users",
        menus=[
            users_titulo,
            users_subtitulo,
            users_detail,
            users_list,
            users_update,
            users_update_password,
            userslist_list_datatables,
            comercializacion_list_by_user_ajax,
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

    admin_users_users_customize = Permissions.register(
        name="Usuarios | Personalizar",
        codename="admin_users_users_customize",
        content_type="admin_users",
        menus=[
            users_titulo,
            users_subtitulo,
            users_detail,
            users_list,
            users_customize,
            users_update_password,
            userslist_list_datatables,
            comercializacion_list_by_user_ajax,
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

    admin_users_users_delete = Permissions.register(
        name="Usuarios | Eliminar",
        codename="admin_users_users_delete",
        content_type="admin_users",
        menus=[
            users_titulo,
            users_subtitulo,
            users_detail,
            users_list,
            users_delete,
            userslist_list_datatables,
            comercializacion_list_by_user_ajax,
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
#                     Urls Account
# ===================================================================#
if ADD_MENU:
    users_accont_update_password = Menu.register(
        name="Mi cuenta, actualizar contraseña",
        codename="admin_users_users_password_change",
        url="/account/password_change/",
        menu_suc=users_subtitulo,
        is_global=True
    )
urlpatterns += [
re_path(r'^account/password_change/$', users_views.UsersChangePasswordView.as_view(), name='admin_users_users_password_change'),
]
# ===================================================================#
if ADD_MENU:
    users_accont_detail = Menu.register(
        name="Mi cuenta",
        codename="admin_users_users_account",
        url="/account/",
        menu_suc=users_subtitulo,
        is_global=True
    )
urlpatterns += [
re_path(r'^account/$', users_views.UsersAccountView.as_view(), name='admin_users_users_account'),
]
# ===================================================================#
#      Creado permisos para los urls descritos de account
# ===================================================================#
if ADD_MENU:
    admin_users_users_account = Permissions.register(
        name="My cuenta",
        codename="admin_users_users_account",
        content_type="admin_users",
        menus=[
            users_accont_detail,
            users_accont_update_password,
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
# ####################################################################
# ####################    GRUPOS         #############################
if ADD_MENU:
    Groups.register(
        name="Permisos basicos Operadora",
        codename="userprofile_operadora_basic",
        permissions=[
            admin_users_users_detail,
            admin_users_users_create,
            admin_users_users_update,
            admin_users_users_delete,
            admin_users_users_account,
            admin_users_users_customize,
        ],
    )
