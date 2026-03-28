# -*- coding: utf-8 -*-

from admin_banklotsports.settings import ADD_MENU
from admin_permisologia.models import Menu, Permissions
from admin_profiles import views
from django.conf.urls import patterns, url

# ===================================================================#
urlpatterns = patterns('',)
# ===================================================================#
#                        Urls profiles
# ===================================================================#
"""
Los enlaces del menu se registran
"""
if ADD_MENU:
    profiles_capitales_ajax = Menu.register(
        name="Ajax | Ver Capitales",
        codename="admin_profiles_capitales_by_estado_ajax",
        is_global=True
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^capitales/list/$',
        view=views.CapitalesListAjax.as_view(),
        name='admin_profiles_capitales_by_estado_ajax'
    ),
)

if ADD_MENU:
    profiles_municipio_ajax = Menu.register(
        name="Ajax | Ver Municipio",
        codename="admin_profiles_municipios_by_capital_ajax",
        is_global=True
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^municipio/list/$',
        view=views.MunicipioListAjax.as_view(),
        name='admin_profiles_municipios_by_capital_ajax'
    ),
)

if ADD_MENU:
    profiles_municipios_ajax = Menu.register(
        name="Ajax | Ver municipio",
        codename="admin_profiles_municipios_by_estado_ajax",
        is_global=True
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^municipios/list/$',
        view=views.MunicipiosListAjax.as_view(),
        name='admin_profiles_municipios_by_estado_ajax'
    ),
)

# ===================================================================#
if ADD_MENU:
    profiles_ciudades_ajax = Menu.register(
        name="Ajax | Ver ciudades",
        codename="admin_profiles_ciudades_by_municipio_ajax",
        is_global=True
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^ciudades/list/$',
        view=views.CiudadesListAjax.as_view(),
        name='admin_profiles_ciudades_by_municipio_ajax'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de profiles
# ===================================================================#
if ADD_MENU:
    Permissions.register(
        name="Ubicacion | Municipios | ver (ajax)",
        codename="admin_profiles_ciudades_ajax",
        content_type="admin_profiles",
        menus=[
            profiles_municipios_ajax,
            profiles_capitales_ajax,
            profiles_municipio_ajax,
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

    Permissions.register(
        name="Ubicacion | Ciudades | ver (ajax)",
        codename="admin_profiles_ciudades_ajax",
        content_type="admin_profiles",
        menus=[
            profiles_ciudades_ajax,
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
