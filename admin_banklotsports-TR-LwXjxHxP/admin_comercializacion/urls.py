# -*- coding: utf-8 -*-

from admin_banklotsports.settings import ADD_MENU
from admin_comercializacion.views import (
    agencias_views, bancas_views, bloques_views, cupos_views, distribuidores_views, factorriesgo_views,
    operadoras_views, permisos_ventas_views, porcentajes_views, preferencias_views, taquillas_views,
)
from admin_lib.util_print import EmailView, PdfKitView
from admin_permisologia.models import Menu, Permissions
from django.conf.urls import patterns, url

# ===================================================================#
urlpatterns = patterns(
    '',)
# ===================================================================#
#                    Urls de Comercializacion
# ===================================================================#
"""
Los enlaces del menu se registran
"""
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(0)

    comercializacion_titulo = Menu.register(
        name=' Comercializacion',
        codename='admin_comercializacion_title',
        icon='icon-flow-tree',
        content_type=1,  # nivel 1 de titulo
        orden=ORDEN(0),
        is_view=True,
    )

# ===================================================================#
#                    Urls de Operadoras
# ===================================================================#
if ADD_MENU:
    operadoras_subtitulo = Menu.register(
        name='Operadoras',
        codename='admin_comercializacion_operadoras_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-location-city',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(10),
        is_view=True,
    )

if ADD_MENU:
    operadoras_create = Menu.register(
        name='Crear',
        codename='admin_comercializacion_operadoras_create',
        url='/comercializacion/operadora/crear/',
        menu_suc=operadoras_subtitulo,
        icon='icon-squared-plus',
        orden=ORDEN(15),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/operadora/crear/$',
        view=operadoras_views.OperadorasCreateView.as_view(),
        name='admin_comercializacion_operadoras_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    operadoras_list = Menu.register(
        name='Lista',
        codename='admin_comercializacion_operadoras_list',
        url='/comercializacion/operadoras/',
        menu_suc=operadoras_subtitulo,
        icon='icon-list2',
        orden=ORDEN(20),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/operadoras/$',
        view=operadoras_views.OperadorasListView.as_view(),
        name='admin_comercializacion_operadoras_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    operadoras_update = Menu.register(
        name='Actualizar',
        codename='admin_comercializacion_operadoras_update',
        menu_suc=operadoras_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/operadora/(?P<pk>\d+?)/editar/$',
        view=operadoras_views.OperadorasUpdateView.as_view(),
        name='admin_comercializacion_operadoras_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    operadoras_delete = Menu.register(
        name='Eliminar',
        codename='admin_comercializacion_operadoras_delete',
        menu_suc=operadoras_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/operadora/(?P<pk>\d+?)/eliminar/$',
        view=operadoras_views.OperadorasDeleteView.as_view(),
        name='admin_comercializacion_operadoras_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    operadoras_detail = Menu.register(
        name='Detalle',
        codename='admin_comercializacion_operadoras_detail',
        menu_suc=operadoras_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/operadora/(?P<pk>\d+?)/$',
        view=operadoras_views.OperadorasDetailView.as_view(),
        name='admin_comercializacion_operadoras_detail'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de operadoras
# ===================================================================#
if ADD_MENU:
    Permissions.register(
        name='Comercializadoras | Operadoras | Ver',
        codename='admin_comercializacion_operadoras_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            operadoras_subtitulo,
            operadoras_detail,
            operadoras_list,
        ],
        profiles=[
            'userprofile_master',
        ],
    )

    Permissions.register(
        name='Comercializadoras | Operadoras | Crear',
        codename='admin_comercializacion_operadoras_create',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            operadoras_subtitulo,
            operadoras_create,
            operadoras_detail,
            operadoras_list,
        ],
        profiles=[
            'userprofile_master',
        ],
    )

    Permissions.register(
        name='Comercializadoras | Operadoras | Actualizar',
        codename='admin_comercializacion_operadoras_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            operadoras_subtitulo,
            operadoras_detail,
            operadoras_list,
            operadoras_update,
        ],
        profiles=[
            'userprofile_master',
        ],
    )

    Permissions.register(
        name='Comercializadoras | Operadoras | Eliminar',
        codename='admin_comercializacion_operadoras_delete',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            operadoras_subtitulo,
            operadoras_delete,
            operadoras_detail,
            operadoras_list,
        ],
        profiles=[
            'userprofile_master',
        ],
    )
if ADD_MENU:
    bloques_subtitulo = Menu.register(
        name='Multi bancas',
        codename='admin_comercializacion_bloques_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-grain',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(100),
        is_view=True,
    )

if ADD_MENU:
    bloques_create = Menu.register(
        name='Crear',
        codename='admin_comercializacion_bloques_create',
        url='/comercializacion/bloque/crear/',
        menu_suc=bloques_subtitulo,
        icon='icon-squared-plus',
        orden=ORDEN(115),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/crear/$',
        view=bloques_views.BloquesCreateView.as_view(),
        name='admin_comercializacion_bloques_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_list = Menu.register(
        name='Lista',
        codename='admin_comercializacion_bloques_list',
        url='/comercializacion/bloques/',
        menu_suc=bloques_subtitulo,
        icon='icon-list2',
        orden=ORDEN(120),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloques/$',
        view=bloques_views.BloquesListView.as_view(),
        name='admin_comercializacion_bloques_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_update = Menu.register(
        name='Actualizar',
        codename='admin_comercializacion_bloques_update',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/(?P<pk>\d+?)/editar/$',
        view=bloques_views.BloquesUpdateView.as_view(),
        name='admin_comercializacion_bloques_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_delete = Menu.register(
        name='Eliminar',
        codename='admin_comercializacion_bloques_delete',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/(?P<pk>\d+?)/eliminar/$',
        view=bloques_views.BloquesDeleteView.as_view(),
        name='admin_comercializacion_bloques_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_detail = Menu.register(
        name='Detalle',
        codename='admin_comercializacion_bloques_detail',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/(?P<pk>\d+?)/$',
        view=bloques_views.BloquesDetailView.as_view(),
        name='admin_comercializacion_bloques_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloque_ajax_by_operadora = Menu.register(
        name='Lista de bloques por comercializadora',
        codename='admin_comercializacion_bloques_by_operadora_ajax',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/operadora/$',
        view=bloques_views.BloquesListbyOperadoraAjax.as_view(),
        name='admin_comercializacion_bloques_by_operadora_ajax'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_send_email = Menu.register(
        name='Email bloque',
        codename='admin_comercializacion_bloques_send_email',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/email/(?P<cache_key>.+?)/$',
        view=EmailView,
        name='admin_comercializacion_bloques_send_email'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_detail_print = Menu.register(
        name='Imprimir bloque',
        codename='admin_comercializacion_bloques_detail_print',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloque/print/(?P<cache_key>.+?)/$',
        view=PdfKitView,
        name='admin_comercializacion_bloques_detail_print'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de bloques
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bloques_detail = Permissions.register(
        name='Comercializadoras | Bloques | Ver',
        codename='admin_comercializacion_bloques_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_detail,
            bloques_list,
            bloques_send_email,
            bloques_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )

    admin_comercializacion_bloques_create = Permissions.register(
        name='Comercializadoras | Bloques | Crear',
        codename='admin_comercializacion_bloques_create',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_create,
            bloques_detail,
            bloques_list,
            bloques_send_email,
            bloques_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )

    admin_comercializacion_bloques_update = Permissions.register(
        name='Comercializadoras | Bloques | Actualizar',
        codename='admin_comercializacion_bloques_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_detail,
            bloques_list,
            bloques_update,
            bloques_send_email,
            bloques_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )

    admin_comercializacion_bloques_delete = Permissions.register(
        name='Comercializadoras | Bloques | Eliminar',
        codename='admin_comercializacion_bloques_delete',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_delete,
            bloques_detail,
            bloques_list,
            bloques_send_email,
            bloques_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )
if ADD_MENU:
    bancas_subtitulo = Menu.register(
        name='Bancas',
        codename='admin_comercializacion_bancas_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-account-balance',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(200),
        is_view=True,
    )

if ADD_MENU:
    bancas_create = Menu.register(
        name='Crear',
        codename='admin_comercializacion_bancas_create',
        url='/comercializacion/banca/crear/',
        menu_suc=bancas_subtitulo,
        icon='icon-squared-plus',
        orden=ORDEN(215),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/banca/crear/$',
        view=bancas_views.BancasCreateView.as_view(),
        name='admin_comercializacion_bancas_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_list = Menu.register(
        name='Lista',
        codename='admin_comercializacion_bancas_list',
        url='/comercializacion/bancas/',
        menu_suc=bancas_subtitulo,
        icon='icon-list2',
        orden=ORDEN(220),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/$',
        view=bancas_views.BancasListView.as_view(),
        name='admin_comercializacion_bancas_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_update = Menu.register(
        name='Actualizar',
        codename='admin_comercializacion_bancas_update',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/banca/(?P<pk>\d+?)/editar/$',
        view=bancas_views.BancasUpdateView.as_view(),
        name='admin_comercializacion_bancas_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_delete = Menu.register(
        name='Eliminar',
        codename='admin_comercializacion_bancas_delete',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/banca/(?P<pk>\d+?)/eliminar/$',
        view=bancas_views.BancasDeleteView.as_view(),
        name='admin_comercializacion_bancas_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_detail = Menu.register(
        name='Detalle',
        codename='admin_comercializacion_bancas_detail',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/banca/(?P<pk>\d+?)/$',
        view=bancas_views.BancasDetailView.as_view(),
        name='admin_comercializacion_bancas_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_ajax_by_bloque = Menu.register(
        name='Lista de bancas por bloque',
        codename='admin_comercializacion_bancas_by_bloque_ajax',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/bloque/$',
        view=bancas_views.BancasListbyBloqueAjax.as_view(),
        name='admin_comercializacion_bancas_by_bloque_ajax'
    ),
)
# ===================================================================#
#     LINKS DATATABLES
# ===================================================================#
if ADD_MENU:
    bancas_list_datatables = Menu.register(
        name='Bancas lista datatables',
        codename='bancas_list_datatables',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/bancas_list_datatables/$',
        view=bancas_views.BancasDatatableView.as_view(),
        name='bancas_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_send_email = Menu.register(
        name='Email banca',
        codename='admin_comercializacion_bancas_send_email',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/banca/email/(?P<cache_key>.+?)/$',
        view=EmailView,
        name='admin_comercializacion_bancas_send_email'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_detail_print = Menu.register(
        name='Imprimir banca',
        codename='admin_comercializacion_bancas_detail_print',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/banca/print/(?P<cache_key>.+?)/$',
        view=PdfKitView,
        name='admin_comercializacion_bancas_detail_print'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de bancas
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bancas_detail = Permissions.register(
        name='Comercializadoras | Bancas | Ver',
        codename='admin_comercializacion_bancas_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_detail,
            bancas_list,
            bancas_ajax_by_bloque,
            bancas_list_datatables,
            bancas_send_email,
            bancas_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_bancas_create = Permissions.register(
        name='Comercializadoras | Bancas | Crear',
        codename='admin_comercializacion_bancas_create',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_create,
            bancas_detail,
            bancas_list,
            bancas_ajax_by_bloque,
            bancas_list_datatables,
            bancas_send_email,
            bancas_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_bancas_update = Permissions.register(
        name='Comercializadoras | Bancas | Actualizar',
        codename='admin_comercializacion_bancas_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_detail,
            bancas_list,
            bancas_update,
            bancas_ajax_by_bloque,
            bancas_list_datatables,
            bancas_send_email,
            bancas_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_bancas_delete = Permissions.register(
        name='Comercializadoras | Bancas | Eliminar',
        codename='admin_comercializacion_bancas_delete',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_delete,
            bancas_detail,
            bancas_list,
            bancas_send_email,
            bancas_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )
if ADD_MENU:
    distribuidores_subtitulo = Menu.register(
        name='Distribuidores',
        codename='admin_comercializacion_distribuidores_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-local-shipping',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(300),
        is_view=True,
    )

if ADD_MENU:
    distribuidores_create = Menu.register(
        name='Crear',
        codename='admin_comercializacion_distribuidores_create',
        url='/comercializacion/distribuidor/crear/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-squared-plus',
        orden=ORDEN(315),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/crear/$',
        view=distribuidores_views.DistribuidoresCreateView.as_view(),
        name='admin_comercializacion_distribuidores_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_list = Menu.register(
        name='Lista',
        codename='admin_comercializacion_distribuidores_list',
        url='/comercializacion/distribuidores/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-list2',
        orden=ORDEN(320),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/$',
        view=distribuidores_views.DistribuidoresListView.as_view(),
        name='admin_comercializacion_distribuidores_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_update = Menu.register(
        name='Actualizar',
        codename='admin_comercializacion_distribuidores_update',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/(?P<pk>\d+?)/editar/$',
        view=distribuidores_views.DistribuidoresUpdateView.as_view(),
        name='admin_comercializacion_distribuidores_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_delete = Menu.register(
        name='Eliminar',
        codename='admin_comercializacion_distribuidores_delete',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/(?P<pk>\d+?)/eliminar/$',
        view=distribuidores_views.DistribuidoresDeleteView.as_view(),
        name='admin_comercializacion_distribuidores_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_detail = Menu.register(
        name='Detalle',
        codename='admin_comercializacion_distribuidores_detail',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/(?P<pk>\d+?)/$',
        view=distribuidores_views.DistribuidoresDetailView.as_view(),
        name='admin_comercializacion_distribuidores_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_ajax_by_bloque = Menu.register(
        name='Lista de distribuidores por bloque',
        codename='admin_comercializacion_distribuidores_by_bloque_ajax',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/bloque/$',
        view=distribuidores_views.DistribuidoresListbyBloqueAjax.as_view(),
        name='admin_comercializacion_distribuidores_by_bloque_ajax'
    ),
)
if ADD_MENU:
    distribuidores_ajax_by_banca = Menu.register(
        name='Lista de distribuidores por banca',
        codename='admin_comercializacion_distribuidores_by_banca_ajax',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/banca/$',
        view=distribuidores_views.DistribuidoresListbyBancaAjax.as_view(),
        name='admin_comercializacion_distribuidores_by_banca_ajax'
    ),
)
# ===================================================================#
#     LINKS DATATABLES
# ===================================================================#
if ADD_MENU:
    distribuidores_list_datatables = Menu.register(
        name='Distribuidores lista datatables',
        codename='distribuidores_list_datatables',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/distribuidores_list_datatables/$',
        view=distribuidores_views.DistribuidoresDatatableView.as_view(),
        name='distribuidores_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_send_email = Menu.register(
        name='Email distribuidor',
        codename='admin_comercializacion_distribuidores_send_email',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/email/(?P<cache_key>.+?)/$',
        view=EmailView,
        name='admin_comercializacion_distribuidores_send_email'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_detail_print = Menu.register(
        name='Imprimir distribuidor',
        codename='admin_comercializacion_distribuidores_detail_print',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidor/print/(?P<cache_key>.+?)/$',
        view=PdfKitView,
        name='admin_comercializacion_distribuidores_detail_print'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de distribuidores
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_distribuidores_detail = Permissions.register(
        name='Comercializadoras | Distribuidores | Ver',
        codename='admin_comercializacion_distribuidores_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_detail,
            distribuidores_list,
            distribuidores_ajax_by_banca,
            distribuidores_ajax_by_bloque,
            distribuidores_list_datatables,
            distribuidores_send_email,
            distribuidores_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_distribuidores_create = Permissions.register(
        name='Comercializadoras | Distribuidores | Crear',
        codename='admin_comercializacion_distribuidores_create',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_create,
            distribuidores_detail,
            distribuidores_list,
            distribuidores_ajax_by_banca,
            distribuidores_ajax_by_bloque,
            distribuidores_list_datatables,
            distribuidores_send_email,
            distribuidores_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_distribuidores_update = Permissions.register(
        name='Comercializadoras | Distribuidores | Actualizar',
        codename='admin_comercializacion_distribuidores_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_detail,
            distribuidores_list,
            distribuidores_update,
            distribuidores_ajax_by_banca,
            distribuidores_ajax_by_bloque,
            distribuidores_list_datatables,
            distribuidores_send_email,
            distribuidores_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_distribuidores_delete = Permissions.register(
        name='Comercializadoras | Distribuidores | Eliminar',
        codename='admin_comercializacion_distribuidores_delete',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_delete,
            distribuidores_detail,
            distribuidores_list,
            distribuidores_send_email,
            distribuidores_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )
if ADD_MENU:
    agencias_subtitulo = Menu.register(
        name='Centros de apuesta',
        codename='admin_comercializacion_agencias_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-store-mall-directory',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(400),
        is_view=True,
    )

if ADD_MENU:
    agencias_create = Menu.register(
        name='Crear',
        codename='admin_comercializacion_agencias_create',
        url='/comercializacion/agencia/crear/',
        menu_suc=agencias_subtitulo,
        icon='icon-squared-plus',
        orden=ORDEN(415),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/crear/$',
        view=agencias_views.AgenciasCreateView.as_view(),
        name='admin_comercializacion_agencias_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_list = Menu.register(
        name='Lista',
        codename='admin_comercializacion_agencias_list',
        url='/comercializacion/agencias/',
        menu_suc=agencias_subtitulo,
        icon='icon-list2',
        orden=ORDEN(420),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/$',
        view=agencias_views.AgenciasListView.as_view(),
        name='admin_comercializacion_agencias_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_update = Menu.register(
        name='Actualizar',
        codename='admin_comercializacion_agencias_update',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/(?P<pk>\d+?)/editar/$',
        view=agencias_views.AgenciasUpdateView.as_view(),
        name='admin_comercializacion_agencias_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_delete = Menu.register(
        name='Eliminar',
        codename='admin_comercializacion_agencias_delete',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/(?P<pk>\d+?)/eliminar/$',
        view=agencias_views.AgenciasDeleteView.as_view(),
        name='admin_comercializacion_agencias_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_detail = Menu.register(
        name='Detalle',
        codename='admin_comercializacion_agencias_detail',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/(?P<pk>\d+?)/$',
        view=agencias_views.AgenciasDetailView.as_view(),
        name='admin_comercializacion_agencias_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_ajax_by_bloque = Menu.register(
        name='Lista de agencias por distribuidor',
        codename='admin_comercializacion_agencias_by_bloque_ajax',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/bloques/$',
        view=agencias_views.AgenciasListbyBloquesAjax.as_view(),
        name='admin_comercializacion_agencias_by_bloque_ajax'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_ajax_by_banca = Menu.register(
        name='Lista de agencias por distribuidor',
        codename='admin_comercializacion_agencias_by_banca_ajax',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/bancas/$',
        view=agencias_views.AgenciasListbyBancasAjax.as_view(),
        name='admin_comercializacion_agencias_by_banca_ajax'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_ajax_by_distribuidor = Menu.register(
        name='Lista de agencias por distribuidor',
        codename='admin_comercializacion_agencias_by_distribuidor_ajax',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/distribuidores/$',
        view=agencias_views.AgenciasListbyDistribuidoresAjax.as_view(),
        name='admin_comercializacion_agencias_by_distribuidor_ajax'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_get_ajax = Menu.register(
        name='Detalle de agencia',
        codename='admin_comercializacion_agencias_get_ajax',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/get/$',
        view=agencias_views.AgenciasListAjax.as_view(),
        name='admin_comercializacion_agencias_get_ajax'
    ),
)
if ADD_MENU:
    agencias_monitor = Menu.register(
        name='Monitor',
        codename='admin_comercializacion_agencias_monitor',
        url='/comercializacion/agencias/monitoreo/',
        menu_suc=agencias_subtitulo,
        icon='icon-cast',
        orden=ORDEN(490),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/monitoreo/$',
        view=agencias_views.AgenciasMonitorView.as_view(),
        name='admin_comercializacion_agencias_monitor'
    ),
)
# ===================================================================#
#     LINKS DATATABLES
# ===================================================================#
if ADD_MENU:
    agencias_list_datatables = Menu.register(
        name='Agencias lista datatables',
        codename='agencias_list_datatables',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/agencias_list_datatables/$',
        view=agencias_views.AgenciasDatatableView.as_view(),
        name='agencias_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_send_email = Menu.register(
        name='Email agencia',
        codename='admin_comercializacion_agencias_send_email',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/email/(?P<cache_key>.+?)/$',
        view=EmailView,
        name='admin_comercializacion_agencias_send_email'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_detail_print = Menu.register(
        name='Imprimir agencia',
        codename='admin_comercializacion_agencias_detail_print',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencia/print/(?P<cache_key>.+?)/$',
        view=PdfKitView,
        name='admin_comercializacion_agencias_detail_print'
    ),
)

# ===================================================================#
#     Creado permisos para los urls descritos de agencias
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_agencias_detail = Permissions.register(
        name='Comercializadoras | Agencias | Ver',
        codename='admin_comercializacion_agencias_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_detail,
            agencias_list,
            agencias_ajax_by_bloque,
            agencias_ajax_by_banca,
            agencias_ajax_by_distribuidor,
            agencias_get_ajax,
            agencias_list_datatables,
            agencias_send_email,
            agencias_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

    admin_comercializacion_agencias_create = Permissions.register(
        name='Comercializadoras | Agencias | Crear',
        codename='admin_comercializacion_agencias_create',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_create,
            agencias_detail,
            agencias_list,
            agencias_ajax_by_bloque,
            agencias_ajax_by_banca,
            agencias_ajax_by_distribuidor,
            agencias_get_ajax,
            agencias_list_datatables,
            agencias_send_email,
            agencias_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

    admin_comercializacion_agencias_update = Permissions.register(
        name='Comercializadoras | Agencias | Actualizar',
        codename='admin_comercializacion_agencias_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_detail,
            agencias_list,
            agencias_update,
            agencias_ajax_by_bloque,
            agencias_ajax_by_banca,
            agencias_ajax_by_distribuidor,
            agencias_get_ajax,
            agencias_list_datatables,
            agencias_send_email,
            agencias_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

    admin_comercializacion_agencias_delete = Permissions.register(
        name='Comercializadoras | Agencias | Eliminar',
        codename='admin_comercializacion_agencias_delete',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_delete,
            agencias_detail,
            agencias_list,
            agencias_send_email,
            agencias_detail_print,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

    admin_comercializacion_agencias_monitor = Permissions.register(
        name='Comercializadoras | Agencias | Monitor',
        codename='admin_comercializacion_agencias_monitor',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_monitor,
            agencias_detail,
        ],
        profiles=[
            'userprofile_master',
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )
if ADD_MENU:
    taquillas_subtitulo = Menu.register(
        name='Taquillas',
        codename='admin_comercializacion_taquillas_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-desktop-windows',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(500),
        is_view=True,
    )

if ADD_MENU:
    taquillas_create = Menu.register(
        name='Crear',
        codename='admin_comercializacion_taquillas_create',
        url='/comercializacion/taquilla/crear/',
        menu_suc=taquillas_subtitulo,
        icon='icon-squared-plus',
        orden=ORDEN(515),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/taquilla/crear/$',
        view=taquillas_views.TaquillasCreateView.as_view(),
        name='admin_comercializacion_taquillas_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    taquillas_list = Menu.register(
        name='Lista',
        codename='admin_comercializacion_taquillas_list',
        url='/comercializacion/taquillas/',
        menu_suc=taquillas_subtitulo,
        icon='icon-list2',
        orden=ORDEN(520),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/taquillas/$',
        view=taquillas_views.TaquillasListView.as_view(),
        name='admin_comercializacion_taquillas_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    taquillas_update = Menu.register(
        name='Actualizar',
        codename='admin_comercializacion_taquillas_update',
        menu_suc=taquillas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/taquilla/(?P<pk>\d+?)/editar/$',
        view=taquillas_views.TaquillasUpdateView.as_view(),
        name='admin_comercializacion_taquillas_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    taquillas_delete = Menu.register(
        name='Eliminar',
        codename='admin_comercializacion_taquillas_delete',
        menu_suc=taquillas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/taquilla/(?P<pk>\d+?)/eliminar/$',
        view=taquillas_views.TaquillasDeleteView.as_view(),
        name='admin_comercializacion_taquillas_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    taquillas_detail = Menu.register(
        name='Detalle',
        codename='admin_comercializacion_taquillas_detail',
        menu_suc=taquillas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/taquilla/(?P<pk>\d+?)/$',
        view=taquillas_views.TaquillasDetailView.as_view(),
        name='admin_comercializacion_taquillas_detail'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de taquillas
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_taquillas_detail = Permissions.register(
        name='Comercializadoras | Taquillas | Ver',
        codename='admin_comercializacion_taquillas_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            taquillas_subtitulo,
            taquillas_detail,
            taquillas_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_comercializacion_taquillas_create = Permissions.register(
        name='Comercializadoras | Taquillas | Crear',
        codename='admin_comercializacion_taquillas_create',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            taquillas_subtitulo,
            taquillas_create,
            taquillas_detail,
            taquillas_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_comercializacion_taquillas_update = Permissions.register(
        name='Comercializadoras | Taquillas | Actualizar',
        codename='admin_comercializacion_taquillas_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            taquillas_subtitulo,
            taquillas_detail,
            taquillas_list,
            taquillas_update,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_comercializacion_taquillas_delete = Permissions.register(
        name='Comercializadoras | Taquillas | Eliminar',
        codename='admin_comercializacion_taquillas_delete',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            taquillas_subtitulo,
            taquillas_delete,
            taquillas_detail,
            taquillas_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
if ADD_MENU:
    bloques_preferencias = Menu.register(
        name='Preferencias',
        codename='admin_comercializacion_bloques_preferencias_list',
        url='/comercializacion/bloques/preferencias/',
        menu_suc=bloques_subtitulo,
        icon='icon-tune',
        orden=ORDEN(150),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloques/preferencias/$',
        view=preferencias_views.BloquesPreferenciasListView.as_view(),
        name='admin_comercializacion_bloques_preferencias_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_preferencias = Menu.register(
        name='Preferencias',
        codename='admin_comercializacion_bancas_preferencias_list',
        url='/comercializacion/bancas/preferencias/',
        menu_suc=bancas_subtitulo,
        icon='icon-tune',
        orden=ORDEN(250),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/preferencias/$',
        view=preferencias_views.BancasPreferenciasListView.as_view(),
        name='admin_comercializacion_bancas_preferencias_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_preferencias = Menu.register(
        name='Preferencias',
        codename='admin_comercializacion_distribuidores_preferencias_list',
        url='/comercializacion/distribuidores/preferencias/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-tune',
        orden=ORDEN(350),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/preferencias/$',
        view=preferencias_views.DistribuidoresPreferenciasListView.as_view(),
        name='admin_comercializacion_distribuidores_preferencias_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_preferencias = Menu.register(
        name='Preferencias',
        codename='admin_comercializacion_agencias_preferencias_list',
        url='/comercializacion/agencias/preferencias/',
        menu_suc=agencias_subtitulo,
        icon='icon-tune',
        orden=ORDEN(450),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/preferencias/$',
        view=preferencias_views.AgenciasPreferenciasListView.as_view(),
        name='admin_comercializacion_agencias_preferencias_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    preferencias_update = Menu.register(
        name='Preferencias | Actualizar',
        codename='admin_comercializacion_preferencias_update',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/(?P<type>\w+?)/preferencias/(?P<pk>\d+?)/$',
        view=preferencias_views.PreferencesFormView.as_view(),
        name='admin_comercializacion_preferencias_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_preferencias_list_datatables = Menu.register(
        name='Preferencias agencias lista datatables',
        codename='agencias_preferencias_list_datatables',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/preferencias/agencias_preferencias_list_datatables/$',
        view=preferencias_views.AgenciasPreferenciasDatatableView.as_view(),
        name='agencias_preferencias_list_datatables'
    ),
)

# ===================================================================#
if ADD_MENU:
    distribuidores_preferencias_list_datatables = Menu.register(
        name='Preferencias distribuidores lista datatables',
        codename='distribuidores_preferencias_list_datatables',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/preferencias/distribuidores_preferencias_list_datatables/$',
        view=preferencias_views.DistribuidoresPreferenciasDatatableView.as_view(),
        name='distribuidores_preferencias_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_preferencias_list_datatables = Menu.register(
        name='Preferencias bancas lista datatables',
        codename='bancas_preferencias_list_datatables',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/preferencias/bancas_preferencias_list_datatables/$',
        view=preferencias_views.BancasPreferenciasDatatableView.as_view(),
        name='bancas_preferencias_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_preferencias_list_datatables = Menu.register(
        name='Preferencias bloques lista datatables',
        codename='bloques_preferencias_list_datatables',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/preferencias/bloques_preferencias_list_datatables/$',
        view=preferencias_views.BloquesPreferenciasDatatableView.as_view(),
        name='bloques_preferencias_list_datatables'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de preferencias
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bloques_preferencias_list = Permissions.register(
        name='Comercializadoras | Bloques | Preferencias',
        codename='admin_comercializacion_bloques_preferencias_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_preferencias,
            bloques_preferencias_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_bancas_preferencias_list = Permissions.register(
        name='Comercializadoras | Bancas | Preferencias',
        codename='admin_comercializacion_bancas_preferencias_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_preferencias,
            bancas_preferencias_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_distribuidores_preferencias_list = Permissions.register(
        name='Comercializadoras | Distribuidores | Preferencias',
        codename='admin_comercializacion_distribuidores_preferencias_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_preferencias,
            distribuidores_preferencias_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_agencias_preferencias_list = Permissions.register(
        name='Comercializadoras | Agencias | Preferencias',
        codename='admin_comercializacion_agencias_preferencias_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_preferencias,
            agencias_preferencias_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor'
        ],
    )

    admin_comercializacion_preferencias_update = Permissions.register(
        name='Comercializadoras | Preferencias',
        codename='admin_comercializacion_preferencias_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            preferencias_update,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
if ADD_MENU:
    bloques_porcentajes_list = Menu.register(
        name='Porcentajes',
        codename='admin_comercializacion_bloques_porcentajes_list',
        url='/comercializacion/bloques/porcentajes/',
        menu_suc=bloques_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(160),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloques/porcentajes/$',
        view=porcentajes_views.BloquesPorcentajesListView.as_view(),
        name='admin_comercializacion_bloques_porcentajes_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_porcentajes_list = Menu.register(
        name='Porcentajes',
        codename='admin_comercializacion_bancas_porcentajes_list',
        url='/comercializacion/bancas/porcentajes/',
        menu_suc=bancas_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(260),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/porcentajes/$',
        view=porcentajes_views.BancasPorcentajesListView.as_view(),
        name='admin_comercializacion_bancas_porcentajes_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_porcentajes_list = Menu.register(
        name='Porcentajes',
        codename='admin_comercializacion_distribuidores_porcentajes_list',
        url='/comercializacion/distribuidores/porcentajes/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(360),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/porcentajes/$',
        view=porcentajes_views.DistribuidoresPorcentajesListView.as_view(),
        name='admin_comercializacion_distribuidores_porcentajes_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_porcentajes_list = Menu.register(
        name='Porcentajes',
        codename='admin_comercializacion_agencias_porcentajes_list',
        url='/comercializacion/agencias/porcentajes/',
        menu_suc=agencias_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(460),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/porcentajes/$',
        view=porcentajes_views.AgenciasPorcentajesListView.as_view(),
        name='admin_comercializacion_agencias_porcentajes_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    porcentajes_update = Menu.register(
        name='Porcentajes | Actualizar',
        codename='admin_comercializacion_porcentajes_update',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/(?P<type>\w+?)/porcentajes/(?P<pk>\d+?)/$',
        view=porcentajes_views.PorcentajesFormView.as_view(),
        name='admin_comercializacion_porcentajes_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_porcentajes_list_datatables = Menu.register(
        name='Porcentajes agencias lista datatables',
        codename='agencias_porcentajes_list_datatables',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/porcentajes/agencias_porcentajes_list_datatables/$',
        view=porcentajes_views.AgenciasPorcentajesDatatableView.as_view(),
        name='agencias_porcentajes_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_porcentajes_list_datatables = Menu.register(
        name='Porcentajes distribuidores lista datatables',
        codename='distribuidores_porcentajes_list_datatables',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/porcentajes/distribuidores_porcentajes_list_datatables/$',
        view=porcentajes_views.DistribuidoresPorcentajesDatatableView.as_view(),
        name='distribuidores_porcentajes_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_porcentajes_list_datatables = Menu.register(
        name='Porcentajes bancas lista datatables',
        codename='bancas_porcentajes_list_datatables',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/porcentajes/bancas_porcentajes_list_datatables/$',
        view=porcentajes_views.BancasPorcentajesDatatableView.as_view(),
        name='bancas_porcentajes_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_porcentajes_list_datatables = Menu.register(
        name='Porcentajes bloques lista datatables',
        codename='bloques_porcentajes_list_datatables',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/porcentajes/bloques_porcentajes_list_datatables/$',
        view=porcentajes_views.BloquesPorcentajesDatatableView.as_view(),
        name='bloques_porcentajes_list_datatables'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de porcentajes
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bloques_porcentajes_list = Permissions.register(
        name='Comercializadoras | Bloques | Porcentajes',
        codename='admin_comercializacion_bloques_porcentajes_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_porcentajes_list,
            bloques_porcentajes_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )

    admin_comercializacion_bancas_porcentajes_list = Permissions.register(
        name='Comercializadoras | Bancas | Porcentajes',
        codename='admin_comercializacion_bancas_porcentajes_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_porcentajes_list,
            bancas_porcentajes_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_distribuidores_porcentajes_list = Permissions.register(
        name='Comercializadoras | Distribuidores | Porcentajes',
        codename='admin_comercializacion_distribuidores_porcentajes_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_porcentajes_list,
            distribuidores_porcentajes_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_agencias_porcentajes_list = Permissions.register(
        name='Comercializadoras | Agencias | Porcentajes',
        codename='admin_comercializacion_agencias_porcentajes_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_porcentajes_list,
            agencias_porcentajes_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor'
        ],
    )

    admin_comercializacion_porcentajes_detail = Permissions.register(
        name='Comercializadoras | Porcentajes',
        codename='admin_comercializacion_porcentajes_detail',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            porcentajes_update,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )
if ADD_MENU:
    bloques_cupos = Menu.register(
        name='Cupos',
        codename='admin_comercializacion_bloques_cupos_list',
        url='/comercializacion/bloques/cupos/',
        menu_suc=bloques_subtitulo,
        icon='icon-credit',
        orden=ORDEN(170),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloques/cupos/$',
        view=cupos_views.BloquesCuposListView.as_view(),
        name='admin_comercializacion_bloques_cupos_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_cupos = Menu.register(
        name='Cupos',
        codename='admin_comercializacion_bancas_cupos_list',
        url='/comercializacion/bancas/cupos/',
        menu_suc=bancas_subtitulo,
        icon='icon-credit',
        orden=ORDEN(270),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/cupos/$',
        view=cupos_views.BancasCuposListView.as_view(),
        name='admin_comercializacion_bancas_cupos_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_cupos = Menu.register(
        name='Cupos',
        codename='admin_comercializacion_distribuidores_cupos_list',
        url='/comercializacion/distribuidores/cupos/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-credit',
        orden=ORDEN(370),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/cupos/$',
        view=cupos_views.DistribuidoresCuposListView.as_view(),
        name='admin_comercializacion_distribuidores_cupos_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_cupos = Menu.register(
        name='Cupos',
        codename='admin_comercializacion_agencias_cupos_list',
        url='/comercializacion/agencias/cupos/',
        menu_suc=agencias_subtitulo,
        icon='icon-credit',
        orden=ORDEN(470),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/cupos/$',
        view=cupos_views.AgenciasCuposListView.as_view(),
        name='admin_comercializacion_agencias_cupos_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    cupos_update = Menu.register(
        name='Cupos | Actualizar',
        codename='admin_comercializacion_cupos_update',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/cupo/(?P<pk>\d+?)/editar/$',
        view=cupos_views.CuposUpdateView.as_view(),
        name='admin_comercializacion_cupos_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    cupos_detail = Menu.register(
        name='Cupos | Detalle',
        codename='admin_comercializacion_cupos_detail',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/cupo/(?P<pk>\d+?)/$',
        view=cupos_views.CuposDetailView.as_view(),
        name='admin_comercializacion_cupos_detail'
    ),
)

# ===================================================================#
if ADD_MENU:
    agencias_cupos_list_datatables = Menu.register(
        name='Cupos agencias lista datatables',
        codename='agencias_cupos_list_datatables',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/cupos/agencias_cupos_list_datatables/$',
        view=cupos_views.AgenciasCuposDatatableView.as_view(),
        name='agencias_cupos_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_cupos_list_datatables = Menu.register(
        name='Cupos distribuidores lista datatables',
        codename='distribuidores_cupos_list_datatables',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/cupos/distribuidores_cupos_list_datatables/$',
        view=cupos_views.DistribuidoresCuposDatatableView.as_view(),
        name='distribuidores_cupos_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_cupos_list_datatables = Menu.register(
        name='Cupos bancas lista datatables',
        codename='bancas_cupos_list_datatables',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/cupos/bancas_cupos_list_datatables/$',
        view=cupos_views.BancasCuposDatatableView.as_view(),
        name='bancas_cupos_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_cupos_list_datatables = Menu.register(
        name='Cupos bloques lista datatables',
        codename='bloques_cupos_list_datatables',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/cupos/bloques_cupos_list_datatables/$',
        view=cupos_views.BloquesCuposDatatableView.as_view(),
        name='bloques_cupos_list_datatables'
    ),
)
# ===================================================================#
#     Creado permisos para los urls descritos de cupos
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bloques_cupos_list = Permissions.register(
        name='Comercializadoras | Bloques | Cupos',
        codename='admin_comercializacion_bloques_cupos_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_cupos,
            bloques_cupos_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )

    admin_comercializacion_bancas_cupos_list = Permissions.register(
        name='Comercializadoras | Bancas | Cupos',
        codename='admin_comercializacion_bancas_cupos_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_cupos,
            bancas_cupos_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_distribuidores_cupos_list = Permissions.register(
        name='Comercializadoras | Distribuidores | Cupos',
        codename='admin_comercializacion_distribuidores_cupos_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_cupos,
            distribuidores_cupos_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_agencias_cupos_list = Permissions.register(
        name='Comercializadoras | Agencias | Cupos',
        codename='admin_comercializacion_agencias_cupos_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_cupos,
            agencias_cupos_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor'
        ],
    )

    admin_comercializacion_cupos_update = Permissions.register(
        name='Comercializadoras | Cupos',
        codename='admin_comercializacion_cupos_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            cupos_update,
            cupos_detail,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

if ADD_MENU:
    bloques_factorriesgo = Menu.register(
        name='Factor de riesgo',
        codename='admin_comercializacion_bloques_factorriesgo_list',
        url='/comercializacion/bloques/factor-riesgo/',
        menu_suc=bloques_subtitulo,
        icon='icon-whatshot',
        orden=ORDEN(180),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloques/factor-riesgo/$',
        view=factorriesgo_views.BloquesFactorRiesgoListView.as_view(),
        name='admin_comercializacion_bloques_factorriesgo_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_factorriesgo = Menu.register(
        name='Factor de riesgo',
        codename='admin_comercializacion_bancas_factorriesgo_list',
        url='/comercializacion/bancas/factor-riesgo/',
        menu_suc=bancas_subtitulo,
        icon='icon-whatshot',
        orden=ORDEN(280),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/factor-riesgo/$',
        view=factorriesgo_views.BancasFactorRiesgoListView.as_view(),
        name='admin_comercializacion_bancas_factorriesgo_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_factorriesgo = Menu.register(
        name='Factor de riesgo',
        codename='admin_comercializacion_distribuidores_factorriesgo_list',
        url='/comercializacion/distribuidores/factor-riesgo/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-whatshot',
        orden=ORDEN(380),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/factor-riesgo/$',
        view=factorriesgo_views.DistribuidoresFactorRiesgoListView.as_view(),
        name='admin_comercializacion_distribuidores_factorriesgo_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_factorriesgo = Menu.register(
        name='Factor de riesgo',
        codename='admin_comercializacion_agencias_factorriesgo_list',
        url='/comercializacion/agencias/factor-riesgo/',
        menu_suc=agencias_subtitulo,
        icon='icon-whatshot',
        orden=ORDEN(480),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/factor-riesgo/$',
        view=factorriesgo_views.AgenciasFactorRiesgoListView.as_view(),
        name='admin_comercializacion_agencias_factorriesgo_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    factorriesgo_update = Menu.register(
        name='Factor de riesgo | Actualizar',
        codename='admin_comercializacion_factorriesgo_update',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/factor-riesgo/(?P<pk>\d+?)/editar/$',
        view=factorriesgo_views.FactorRiesgoUpdateView.as_view(),
        name='admin_comercializacion_factorriesgo_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    factorriesgo_detail = Menu.register(
        name='Factor de riesgo | Detalle',
        codename='admin_comercializacion_factorriesgo_detail',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/factor-riesgo/(?P<pk>\d+?)/$',
        view=factorriesgo_views.FactorRiesgoDetailView.as_view(),
        name='admin_comercializacion_factorriesgo_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_factorriesgo_list_datatables = Menu.register(
        name='Factor Riesgo agencias lista datatables',
        codename='agencias_factorriesgo_list_datatables',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/factorriesgo/agencias_factorriesgo_list_datatables/$',
        view=factorriesgo_views.AgenciasFactorRiesgoDatatableView.as_view(),
        name='agencias_factorriesgo_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_factorriesgo_list_datatables = Menu.register(
        name='Factor Riesgo distribuidores lista datatables',
        codename='distribuidores_factorriesgo_list_datatables',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/factorriesgo/distribuidores_factorriesgo_list_datatables/$',
        view=factorriesgo_views.DistribuidoresFactorRiesgoDatatableView.as_view(),
        name='distribuidores_factorriesgo_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_factorriesgo_list_datatables = Menu.register(
        name='Factor Riesgo bancas lista datatables',
        codename='bancas_factorriesgo_list_datatables',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/factorriesgo/bancas_factorriesgo_list_datatables/$',
        view=factorriesgo_views.BancasFactorRiesgoDatatableView.as_view(),
        name='bancas_factorriesgo_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bloques_factorriesgo_list_datatables = Menu.register(
        name='Factor Riesgo bloques lista datatables',
        codename='bloques_factorriesgo_list_datatables',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/factorriesgo/bloques_factorriesgo_list_datatables/$',
        view=factorriesgo_views.BloquesFactorRiesgoDatatableView.as_view(),
        name='bloques_factorriesgo_list_datatables'
    ),
)


# ===================================================================#
#     Creado permisos para los urls descritos de cupos
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bloques_factorriesgo_list = Permissions.register(
        name='Comercializadoras | Bloques | Factor de riesgo',
        codename='admin_comercializacion_bloques_factorriesgo_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_factorriesgo,
            bloques_factorriesgo_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_bancas_factorriesgo_list = Permissions.register(
        name='Comercializadoras | Bancas | Factor de riesgo',
        codename='admin_comercializacion_bancas_factorriesgo_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_factorriesgo,
            bancas_factorriesgo_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_distribuidores_factorriesgo_list = Permissions.register(
        name='Comercializadoras | Distribuidores | Factor de riesgo',
        codename='admin_comercializacion_distribuidores_factorriesgo_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_factorriesgo,
            distribuidores_factorriesgo_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_agencias_factorriesgo_list = Permissions.register(
        name='Comercializadoras | Agencias | Factor de riesgo',
        codename='admin_comercializacion_agencias_factorriesgo_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_factorriesgo,
            agencias_factorriesgo_list_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor'
        ],
    )

    admin_comercializacion_factorriesgo_update = Permissions.register(
        name='Comercializadoras | Factor de riesgo',
        codename='admin_comercializacion_factorriesgo_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            factorriesgo_update,
            factorriesgo_detail,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )
# ===================================================================#
# Permiso general en ajax
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_ajax = Permissions.register(
        name='Comercializadoras | Peticiones ajax',
        codename='admin_comercializacion_ajax',
        content_type='admin_comercializacion',
        menus=[
            bloque_ajax_by_operadora,
            bancas_ajax_by_bloque,
            distribuidores_ajax_by_bloque,
            distribuidores_ajax_by_banca,
            distribuidores_ajax_by_banca,
            agencias_ajax_by_bloque,
            agencias_ajax_by_banca,
            agencias_ajax_by_distribuidor,
            agencias_get_ajax,
        ],
        profiles=[
            'userprofile_master',
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
if ADD_MENU:
    bloques_permisos_ventas_list = Menu.register(
        name='Permisos de ventas',
        codename='admin_comercializacion_bloques_permisos_ventas_list',
        url='/comercializacion/bloques/permisos/ventas/',
        menu_suc=bloques_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(190),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bloques/permisos/ventas/$',
        view=permisos_ventas_views.BloquesPermissionsSalesListView.as_view(),
        name='admin_comercializacion_bloques_permisos_ventas_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_permisos_ventas_list = Menu.register(
        name='Permisos de ventas',
        codename='admin_comercializacion_bancas_permisos_ventas_list',
        url='/comercializacion/bancas/permisos/ventas/',
        menu_suc=bancas_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(290),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/bancas/permisos/ventas/$',
        view=permisos_ventas_views.BancasPermissionsSalesListView.as_view(),
        name='admin_comercializacion_bancas_permisos_ventas_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_permisos_ventas_list = Menu.register(
        name='Permisos de ventas',
        codename='admin_comercializacion_distribuidores_permisos_ventas_list',
        url='/comercializacion/distribuidores/permisos/ventas/',
        menu_suc=distribuidores_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(390),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/distribuidores/permisos/ventas/$',
        view=permisos_ventas_views.DistribuidoresPermissionsSalesListView.as_view(),
        name='admin_comercializacion_distribuidores_permisos_ventas_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_permisos_ventas_list = Menu.register(
        name='Permisos de ventas',
        codename='admin_comercializacion_agencias_permisos_ventas_list',
        url='/comercializacion/agencias/permisos/ventas/',
        menu_suc=agencias_subtitulo,
        icon='icon-insert-chart',
        orden=ORDEN(490),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/agencias/permisos/ventas/$',
        view=permisos_ventas_views.AgenciasPermissionsSalesListView.as_view(),
        name='admin_comercializacion_agencias_permisos_ventas_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    permisos_ventas_update = Menu.register(
        name='Permisos ventas | Actualizar',
        codename='admin_comercializacion_permisos_ventas_update',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/(?P<type>\w+?)/permisos/ventas/(?P<pk>\d+?)/$',
        view=permisos_ventas_views.PermissionsSalesFormView.as_view(),
        name='admin_comercializacion_permisos_ventas_update'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    permisos_ventas_restrictions = Menu.register(
        name='Permisos ventas restricciones | Actualizar',
        codename='admin_comercializacion_permisos_ventas_restrictions',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/(?P<type>\w+?)/permisos/ventas/restricciones/(?P<pk>\d+?)/$',
        view=permisos_ventas_views.PermissionsSalesRestrictionsFormView.as_view(),
        name='admin_comercializacion_permisos_ventas_restrictions'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    permisos_ventas_restrictions_ajax = Menu.register(
        name='Permisos ventas restricciones | Ajax',
        codename='admin_comercializacion_permisos_ventas_restrictions_ajax',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/permisos/ventas-restrictions/ajax/$',
        view=permisos_ventas_views.PermissionsSalesRestrictionsAjax.as_view(),
        name='admin_comercializacion_permisos_ventas_restrictions_ajax'
    ),
)

# ===================================================================#
if ADD_MENU:
    permisos_ventas_detail = Menu.register(
        name='Permisos ventas | Detalle',
        codename='admin_comercializacion_permisos_ventas_detail',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/(?P<type>\w+?)/permisos/ventas/detail/(?P<pk>\d+?)/$',
        view=permisos_ventas_views.PermissionsSalesDetailView.as_view(),
        name='admin_comercializacion_permisos_ventas_detail'
    ),
)

# ===================================================================#
#   DATATABLES
# ===================================================================#
if ADD_MENU:
    bloques_permisos_ventas_list_datatables = Menu.register(
        name='Permisos ventas bloques lista datatables',
        codename='bloques_permisos_ventas_list_datatables',
        menu_suc=bloques_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/permisos/bloques_permisos_ventas_list_datatables/$',
        view=permisos_ventas_views.BloquesPermissionsSalesDatatableView.as_view(),
        name='bloques_permisos_ventas_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    bancas_permisos_ventas_list_datatables = Menu.register(
        name='Permisos ventas bancas lista datatables',
        codename='bancas_permisos_ventas_list_datatables',
        menu_suc=bancas_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/permisos/bancas_permisos_ventas_list_datatables/$',
        view=permisos_ventas_views.BancasPermissionsSalesDatatableView.as_view(),
        name='bancas_permisos_ventas_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    distribuidores_permisos_ventas_list_datatables = Menu.register(
        name='Permisos ventas distribuidores lista datatables',
        codename='distribuidores_permisos_ventas_list_datatables',
        menu_suc=distribuidores_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/permisos/distribuidores_permisos_ventas_list_datatables/$',
        view=permisos_ventas_views.DistribuidoresPermissionsSalesDatatableView.as_view(),
        name='distribuidores_permisos_ventas_list_datatables'
    ),
)
# ===================================================================#
if ADD_MENU:
    agencias_permisos_ventas_list_datatables = Menu.register(
        name='Permisos ventas agencias lista datatables',
        codename='agencias_permisos_ventas_list_datatables',
        menu_suc=agencias_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/permisos/agencias_permisos_ventas_list_datatables/$',
        view=permisos_ventas_views.AgenciasPermissionsSalesDatatableView.as_view(),
        name='agencias_permisos_ventas_list_datatables'
    ),
)
# =====================================================================#
# ===================================================================#
if ADD_MENU:
    permisos_ventas_ajax = Menu.register(
        name='Permisos de ventas por comercializadora',
        codename='admin_comercializacion_permisos_ventas_ajax',
        menu_suc=comercializacion_titulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^comercializacion/permisos/ventas/ajax/$',
        view=permisos_ventas_views.PermisosVentasAjax.as_view(),
        name='admin_comercializacion_permisos_ventas_ajax'
    ),
)

# ===================================================================#
#     Creado permisos para los urls descritos de permisos de ventas
# ===================================================================#
if ADD_MENU:
    admin_comercializacion_bloques_permisos_ventas_list = Permissions.register(
        name='Comercializadoras | Bloques | Permisos Ventas',
        codename='admin_comercializacion_bloques_permisos_ventas_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bloques_subtitulo,
            bloques_permisos_ventas_list,
            bloques_permisos_ventas_list_datatables,
            permisos_ventas_detail,
        ],
        profiles=[
            'userprofile_operadora',
        ],
    )

    admin_comercializacion_bancas_permisos_ventas_list = Permissions.register(
        name='Comercializadoras | Bancas | Permisos Ventas',
        codename='admin_comercializacion_bancas_permisos_ventas_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            bancas_subtitulo,
            bancas_permisos_ventas_list,
            bancas_permisos_ventas_list_datatables,
            permisos_ventas_detail,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
        ],
    )

    admin_comercializacion_distribuidores_permisos_ventas_list = Permissions.register(
        name='Comercializadoras | Distribuidores | Permisos Ventas',
        codename='admin_comercializacion_distribuidores_permisos_ventas_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            distribuidores_subtitulo,
            distribuidores_permisos_ventas_list,
            distribuidores_permisos_ventas_list_datatables,
            permisos_ventas_detail,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
        ],
    )

    admin_comercializacion_agencias_permisos_ventas_list = Permissions.register(
        name='Comercializadoras | Agencias | Permisos Ventas',
        codename='admin_comercializacion_agencias_permisos_ventas_list',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            agencias_subtitulo,
            agencias_permisos_ventas_list,
            agencias_permisos_ventas_list_datatables,
            permisos_ventas_detail,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

    admin_comercializacion_permisos_ventas_update = Permissions.register(
        name='Comercializadoras | Permisos ventas',
        codename='admin_comercializacion_permisos_ventas_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            permisos_ventas_update,
            permisos_ventas_detail,
            permisos_ventas_ajax,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )

    admin_comercializacion_permisos_ventas_restrictions = Permissions.register(
        name='Comercializadoras | Permisos ventas restricciones',
        codename='admin_comercializacion_permisos_ventas_update',
        content_type='admin_comercializacion',
        menus=[
            comercializacion_titulo,
            permisos_ventas_restrictions,
            permisos_ventas_detail,
            permisos_ventas_restrictions_ajax,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
        ],
    )
