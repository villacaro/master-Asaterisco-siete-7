# -*- coding: utf-8 -*-

from admin_banklotsports.settings import ADD_MENU
from admin_permisologia.models import Groups, Menu, Permissions
from admin_permisologia.views import groups_views
from django.conf.urls import patterns, url

# ===================================================================#
urlpatterns = patterns(
    '',
)
# ===================================================================#
#                        Urls Permisologia
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

    permisologia_subtitulo = Menu.register(
        name="Grupos",
        codename="admin_permisologia_groups_subtitle",
        menu_suc=users_titulo,
        icon="icon-share2",
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(500),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    permisologia_create = Menu.register(
        name="Crear",
        codename="admin_permisologia_groups_create",
        url="/permisologia/grupos/crear/",
        menu_suc=permisologia_subtitulo,
        icon="icon-squared-plus",
        orden=ORDEN(510),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^permisologia/grupos/crear/$',
        view=groups_views.GroupsCreateView.as_view(),
        name='admin_permisologia_groups_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    permisologia_list = Menu.register(
        name="Listar",
        codename="admin_permisologia_groups_list",
        url="/permisologia/grupos/",
        menu_suc=permisologia_subtitulo,
        icon="icon-list2",
        orden=ORDEN(520),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^permisologia/grupos/$',
        view=groups_views.GroupsListView.as_view(),
        name='admin_permisologia_groups_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    permisologia_update = Menu.register(
        name="Actualizar",
        codename="admin_permisologia_groups_update",
        menu_suc=permisologia_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^permisologia/grupo/(?P<pk>\d+?)/editar/$',
        view=groups_views.GroupsUpdateView.as_view(),
        name='admin_permisologia_groups_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    permisologia_delete = Menu.register(
        name="Eliminar",
        codename="admin_permisologia_groups_delete",
        menu_suc=permisologia_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^permisologia/grupo/(?P<pk>\d+?)/eliminar/$',
        view=groups_views.GroupsDeleteView.as_view(),
        name='admin_permisologia_groups_delete'
    )
)
# ===================================================================#
if ADD_MENU:
    permisologia_detail = Menu.register(
        name="Detalle",
        codename="admin_permisologia_groups_detail",
        menu_suc=permisologia_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^permisologia/grupo/(?P<pk>\d+?)/$',
        view=groups_views.GroupsDetailView.as_view(),
        name='admin_permisologia_groups_detail'
    )
)
# ===================================================================#
#       Creado permisos para los urls descritos de permisologia
# ===================================================================#
if ADD_MENU:
    admin_permisologia_groups_detail = Permissions.register(
        name="Permisologia | Grupos de usuario | Ver",
        codename="admin_permisologia_groups_detail",
        content_type="admin_permisologia",
        menus=[
            users_titulo,
            permisologia_subtitulo,
            permisologia_detail,
            permisologia_list,
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

    admin_permisologia_groups_create = Permissions.register(
        name="Permisologia | Grupos de usuario | Crear",
        codename="admin_permisologia_groups_create",
        content_type="admin_permisologia",
        menus=[
            users_titulo,
            permisologia_subtitulo,
            permisologia_create,
            permisologia_detail,
            permisologia_list,
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

    admin_permisologia_groups_update = Permissions.register(
        name="Permisologia | Grupos de usuario | Actualizar",
        codename="admin_permisologia_groups_update",
        content_type="admin_permisologia",
        menus=[
            users_titulo,
            permisologia_subtitulo,
            permisologia_detail,
            permisologia_list,
            permisologia_update,
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

    admin_permisologia_groups_delete = Permissions.register(
        name="Permisologia | Grupos de usuario | Eliminar",
        codename="admin_permisologia_groups_delete",
        content_type="admin_permisologia",
        menus=[
            users_titulo,
            permisologia_subtitulo,
            permisologia_delete,
            permisologia_detail,
            permisologia_list,
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
        name="Permisos basicos Operadora",
        codename="userprofile_operadora_basic",
        permissions=[
            admin_permisologia_groups_detail,
            admin_permisologia_groups_create,
            admin_permisologia_groups_update,
            admin_permisologia_groups_delete,
        ],
    )
