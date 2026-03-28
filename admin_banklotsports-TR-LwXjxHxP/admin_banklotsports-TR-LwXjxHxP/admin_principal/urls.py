# -*- coding: utf-8 -*-

import admin_principal.views
from admin_banklotsports.settings import ACCESO_URL, ADD_MENU, INDEX_URL, LOGOUT_URL
from admin_permisologia.models import Menu, Permissions
from django.conf.urls import patterns, url

# ===================================================================#
urlpatterns = patterns('',)
# ===================================================================#
#                        Urls Principal
# ===================================================================#
"""
Los enlaces del menu se registran
"""
# ===================================================================#
if ADD_MENU:
    principal_login = Menu.register(
        name="Login",
        codename="admin_principal_login",
        url=ACCESO_URL,
        is_public=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^' + ACCESO_URL[1:] + '$',
        view=admin_principal.views.PrincipalLoginView.as_view(),
        name='admin_principal_login'
    ),
)
# ===================================================================#
if ADD_MENU:
    principal_index = Menu.register(
        name="Index",
        codename="admin_principal_index",
        url=INDEX_URL,
        is_global=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^' + INDEX_URL[1:] + '$',
        view=admin_principal.views.PrincipalView.as_view(),
        name='admin_principal_index'
    ),
)
# ===================================================================#
if ADD_MENU:
    principal_logout = Menu.register(
        name="Logout",
        codename="admin_principal_logout",
        url=LOGOUT_URL,
        is_global=True,
    )
urlpatterns += patterns('',
                        url(
                            regex=r'^' + LOGOUT_URL[1:] + '$',
                            view=admin_principal.views.PrincipalLogoutView.as_view(),
                            name='admin_principal_logout'
                        ),
                        )
# ===================================================================#
if ADD_MENU:
    principal_change_comercializadora_list = Menu.register(
        name="Ver comercializadoras disponibles",
        codename="admin_principal_change_comercializadora_list",
        is_global=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializadora/defaul/$',
        view=admin_principal.views.PrincipalComercializadoraChangeListView.as_view(),
        name='admin_principal_change_comercializadora_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    principal_change_comercializadora = Menu.register(
        name="Cambiar de comercializadora",
        codename="admin_principal_change_comercializadora_process",
        is_global=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializadora/defaul/(?P<pk>\d+?)/change/$',
        view=admin_principal.views.PrincipalComercializadoraChangeProcessView.as_view(),
        name='admin_principal_change_comercializadora_process'
    ),
)
# ===================================================================#
#       Creado permisos para los urls descritos de principal
# ===================================================================#
if ADD_MENU:
    Permissions.register(
        name="Principal | Acceso",
        codename="admin_principal_accesos",
        content_type="admin_principal",
        menus=[
            principal_index,
            principal_logout,
            principal_change_comercializadora_list,
            principal_change_comercializadora,
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
