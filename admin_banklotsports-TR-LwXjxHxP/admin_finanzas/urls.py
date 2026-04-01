# -*- coding: utf-8 -*-

from admin_banklotsports.settings import ADD_MENU
from admin_finanzas.views import (
    cuenta_views, cuentas_operaciones, dia_trabajo_views, movimientos_views, resumen_administrativo_views,
    saldos_views,
)
from admin_lib.util_print import CsvView, PdfView
from admin_permisologia.models import Menu, Permissions
from django.conf.urls import patterns, url

# ===================================================================#
urlpatterns = patterns(
    '',
)
# ===================================================================#
#                    Urls de juegos
# ===================================================================#
'''
Los enlaces del menu se registran
'''
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(2000)

    finanzas_titulo = Menu.register(
        name='Informes',
        codename='admin_finanzas_title',
        icon='icon-documents',
        content_type=1,  # nivel 1 de titulo
        orden=ORDEN(0),
        is_view=True,
    )

# ===================================================================#
#                    Urls de Resumen
# ===================================================================#
if ADD_MENU:
    resumen_subtitulo = Menu.register(
        name='Resumen',
        codename='admin_finanzas_resumen_subtitle',
        menu_suc=finanzas_titulo,
        icon='icon-document',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(200),
        is_view=True,
    )

if ADD_MENU:
    resumenadministrativo_general = Menu.register(
        name='Resumen',
        codename='admin_finanzas_resumenadministrativo_general',
        url='/reportes/comercializadoras/resumen-administrativo/',
        menu_suc=resumen_subtitulo,
        icon='icon-document',
        orden=ORDEN(210),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/$',
        view=resumen_administrativo_views.VentasResumenAdministrativo.as_view(),
        name='admin_finanzas_resumenadministrativo_general'
    ),
)

if ADD_MENU:
    resumenadministrativo_personalizado = Menu.register(
        name='Resumen Personalizado',
        codename='admin_finanzas_resumenadministrativo_personalizado',
        url='/reportes/comercializadoras/resumen-administrativo-personalizado/',
        menu_suc=resumen_subtitulo,
        icon='icon-documents',
        orden=ORDEN(211),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo-personalizado/$',
        view=resumen_administrativo_views.VentasResumenAdministrativoPersonalizado.as_view(),
        name='admin_finanzas_resumenadministrativo_personalizado'
    ),
)

# ===================================================================#
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_general_csv = Menu.register(
        name='Csv Resumen',
        codename='admin_finanzas_resumenadministrativo_general_print_csv',
        menu_suc=resumen_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/csv/(?P<cache_key>.+?)/$',
        view=CsvView,
        name='admin_finanzas_resumenadministrativo_general_print_csv'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_general_pdf = Menu.register(
        name='Pdf Resumen',
        codename='admin_finanzas_resumenadministrativo_general_print_pdf',
        menu_suc=resumen_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/pdf/(?P<cache_key>.+?)/$',
        view=PdfView,
        name='admin_finanzas_resumenadministrativo_general_print_pdf'
    ),
)
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_import = Menu.register(
        name='Resumen | importar saldos',
        codename='admin_finanzas_resumenadministrativo_general_import',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/import/$',
        view=resumen_administrativo_views.VentasResumenAdministrativoImport.as_view(),
        name='admin_finanzas_resumenadministrativo_general_import'
    ),
)
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_comercializadora = Menu.register(
        name='Resumen | por comercializadora',
        codename='admin_finanzas_resumenadministrativo_comercializadora_list',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/(?P<comercializadora>\d+?)/$',
        view=resumen_administrativo_views.VentasResumenAdministrativoByComercializadora.as_view(),
        name='admin_finanzas_resumenadministrativo_comercializadora_list'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_comercializadora_csv = Menu.register(
        name='Csv Resumen por comercializadora',
        codename='admin_finanzas_resumenadministrativo_comercializadora_print_csv',
        menu_suc=resumen_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/comercializadoras/csv/(?P<cache_key>.+?)/$',
        view=CsvView,
        name='admin_finanzas_resumenadministrativo_comercializadora_print_csv'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_comercializadora_pdf = Menu.register(
        name='Pdf Resumen por comercializadora',
        codename='admin_finanzas_resumenadministrativo_comercializadora_print_pdf',
        menu_suc=resumen_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/resumen-administrativo/comercializadoras/pdf/(?P<cache_key>.+?)/$',
        view=PdfView,
        name='admin_finanzas_resumenadministrativo_comercializadora_print_pdf'
    ),
)
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_hojabanco = Menu.register(
        name='Resumen | hoja de banco',
        codename='admin_finanzas_resumenadministrativo_hoja_de_banco_list',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/hoja-de-banco/(?P<comercializadora>\d+?)/$',
        view=resumen_administrativo_views.VentasHojaDeBancoByComercializadora.as_view(),
        name='admin_finanzas_resumenadministrativo_hoja_de_banco_list'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_hojabanco_csv = Menu.register(
        name='Csv Resumen Hoja de banco',
        codename='admin_finanzas_resumenadministrativo_hojabanco_print_csv',
        menu_suc=resumen_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/hoja-de-banco/csv/(?P<cache_key>.+?)/$',
        view=CsvView,
        name='admin_finanzas_resumenadministrativo_hojabanco_print_csv'
    ),
)
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    resumenadministrativo_hojabanco_pdf = Menu.register(
        name='Pdf Resumen Hoja de banco',
        codename='admin_finanzas_resumenadministrativo_hojabanco_print_pdf',
        menu_suc=resumen_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/hoja-de-banco/pdf/(?P<cache_key>.+?)/$',
        view=PdfView,
        name='admin_finanzas_resumenadministrativo_hojabanco_print_pdf'
    ),
)


# ===================================================================#
if ADD_MENU:
    resumenadministrativo_moviemientos = Menu.register(
        name='Resumen | movimientos',
        codename='admin_finanzas_resumenadministrativo_movimientos_list',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^reportes/comercializadoras/(?P<movimiento>[a-z]+?)/(?P<comercializadora>\d+?)/'
        '(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$',
        view=resumen_administrativo_views.MovimientosForComercializadoraToFecha.as_view(),
        name='admin_finanzas_resumenadministrativo_movimientos_list'
    ),
)

# ==================================================================#
#   Creado permisos para los urls descritos de resumen administrativo
# ===================================================================#
if ADD_MENU:
    admin_finanzas_resumenadministrativo_general = Permissions.register(
        name='Finanzas | Resumen admnistrativo',
        codename='admin_finanzas_resumenadministrativo_general',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            resumenadministrativo_general,
            resumenadministrativo_general_csv,
            resumenadministrativo_general_pdf,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_resumenadministrativo_personalizado = Permissions.register(
        name='Finanzas | Resumen admnistrativo personalizado',
        codename='admin_finanzas_resumenadministrativo_personalizado',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            resumenadministrativo_personalizado,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_resumenadministrativo_general_import = Permissions.register(
        name='Finanzas | Resumen admnistrativo | Importar saldos',
        codename='admin_finanzas_resumenadministrativo_general_import',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            resumenadministrativo_general,
            resumenadministrativo_import,
            resumenadministrativo_general_csv,
            resumenadministrativo_general_pdf,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_resumenadministrativo_comercalizadora = Permissions.register(
        name='Finanzas | Resumen admnistrativo | Por comercializadoras',
        codename='admin_finanzas_resumenadministrativo_comercalizadora',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            resumenadministrativo_comercializadora,
            resumenadministrativo_comercializadora_pdf,
            resumenadministrativo_comercializadora_csv,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_resumenadministrativo_hoja = Permissions.register(
        name='Finanzas | Resumen admnistrativo | Hoja de banco',
        codename='admin_finanzas_resumenadministrativo_hoja',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            resumenadministrativo_hojabanco,
            resumenadministrativo_hojabanco_csv,
            resumenadministrativo_hojabanco_pdf,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_resumenadministrativo_movimientos = Permissions.register(
        name='Finanzas | Resumen admnistrativo | Movimientos',
        codename='admin_finanzas_resumenadministrativo_movimientos',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            resumenadministrativo_moviemientos,
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
    cuenta_list = Menu.register(
        name='Cuentas',
        codename='admin_finanzas_cuenta_list',
        url='/operaciones_financieras/cuentas/',
        menu_suc=resumen_subtitulo,
        icon='icon-account-balance-wallet',
        orden=ORDEN(220),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/$',
        view=cuenta_views.CuentaListView.as_view(),
        name='admin_finanzas_cuenta_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    cuenta_delete = Menu.register(
        name='Eliminar',
        codename='admin_finanzas_cuenta_delete',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/(?P<pk>\d+?)/eliminar/$',
        view=cuenta_views.CuentaDeleteView.as_view(),
        name='admin_finanzas_cuenta_delete'
    ),
)
# ===================================================================#
if ADD_MENU:
    cuenta_create = Menu.register(
        name='Crear',
        codename='admin_finanzas_cuenta_create',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/crear/$',
        view=cuenta_views.CuentaCreateView.as_view(),
        name='admin_finanzas_cuenta_create'
    ),
)
# ===================================================================#
if ADD_MENU:
    cuenta_detail = Menu.register(
        name='Detalle',
        codename='admin_finanzas_cuenta_detail',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/(?P<pk>\d+?)/$',
        view=cuenta_views.CuentaDetailView.as_view(),
        name='admin_finanzas_cuenta_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    cuenta_update = Menu.register(
        name='Actualizar',
        codename='admin_finanzas_cuenta_update',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/(?P<pk>\d+?)/editar/$',
        view=cuenta_views.CuentaUpdateView.as_view(),
        name='admin_finanzas_cuenta_update'
    ),
)
# ===================================================================#
# Creado permisos para los urls descritos de cuentas
# ===================================================================#
if ADD_MENU:
    admin_finanzas_cuenta_detail = Permissions.register(
        name='Finanzas | Cuentas | Ver',
        codename='admin_finanzas_cuenta_detail',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            cuenta_detail,
            cuenta_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_cuenta_create = Permissions.register(
        name='Finanzas | Cuentas | Crear',
        codename='admin_finanzas_cuenta_create',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            cuenta_create,
            cuenta_detail,
            cuenta_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_cuenta_update = Permissions.register(
        name='Finanzas | Cuentas | Actualizar',
        codename='admin_finanzas_cuenta_update',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            cuenta_detail,
            cuenta_list,
            cuenta_update
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_cuenta_delete = Permissions.register(
        name='Finanzas | Cuentas | Eliminar',
        codename='admin_finanzas_cuenta_delete',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            cuenta_delete,
            cuenta_detail,
            cuenta_list,
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
    movimiento_list = Menu.register(
        name='Movimientos',
        codename='admin_finanzas_movimiento_list',
        url='/operaciones_financieras/cuentas/movimientos/',
        menu_suc=resumen_subtitulo,
        icon='icon-swap',
        orden=ORDEN(230),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/movimientos/$',
        view=movimientos_views.MovimientosListView.as_view(),
        name='admin_finanzas_movimiento_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    movimiento_detail = Menu.register(
        name='Detalle',
        codename='admin_finanzas_movimiento_detail',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/movimientos/(?P<pk>\d+?)/$',
        view=movimientos_views.MovimientosDetailView.as_view(),
        name='admin_finanzas_movimiento_detail'
    ),
)
# ===================================================================#
if ADD_MENU:
    movimiento_delete = Menu.register(
        name='Eliminar',
        codename='admin_finanzas_movimiento_delete',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/movimiento/(?P<pk>\d+?)/eliminar/$',
        view=movimientos_views.MovimientoDeleteView.as_view(),
        name='admin_finanzas_movimiento_delete'
    ),
)
# ===================================================================#
# Creado permisos para los urls descritos de cuentas
# ===================================================================#
if ADD_MENU:
    admin_finanzas_movimiento_list = Permissions.register(
        name='Finanzas | Movimientos | Ver',
        codename='admin_finanzas_movimiento_list',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            movimiento_list,
            movimiento_detail,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_movimiento_delete = Permissions.register(
        name='Finanzas | Movimientos | Eliminar',
        codename='admin_finanzas_movimiento_delete',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            movimiento_list,
            movimiento_delete,
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
    saldoinicial_list = Menu.register(
        name='Saldo inicial',
        codename='admin_finanzas_saldoinicial_list',
        url='/operaciones_financieras/saldo_inicial/',
        menu_suc=resumen_subtitulo,
        icon='icon-trending-neutral',
        orden=ORDEN(240),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/saldo_inicial/$',
        view=saldos_views.ComercializadoraListView.as_view(),
        name='admin_finanzas_saldoinicial_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    saldoinicial_reset = Menu.register(
        name='Reiniciar',
        codename='admin_finanzas_saldoinicial_reset',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/saldo_inicial/(?P<pk>\d+?)/reiniciar/$',
        view=saldos_views.ComercializadoraResetView.as_view(),
        name='admin_finanzas_saldoinicial_reset'
    ),
)
# ===================================================================#
if ADD_MENU:
    saldoinicial_update = Menu.register(
        name='Actualizar',
        codename='admin_finanzas_saldoinicial_update',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/saldo_inicial/(?P<pk>\d+?)/editar/$',
        view=saldos_views.ComercializadoraUpdateView.as_view(),
        name='admin_finanzas_saldoinicial_update'
    ),
)
# ===================================================================#
if ADD_MENU:
    saldoinicial_register = Menu.register(
        name='Registrar',
        codename='admin_finanzas_saldoinicial_register',
        menu_suc=resumen_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/saldo_inicial/registrar/$',
        view=saldos_views.ComercializadoraRegisterView.as_view(),
        name='admin_finanzas_saldoinicial_register'
    ),
)
# ===================================================================#
# Creado permisos para los urls descritos de saldo inicial
# ===================================================================#
if ADD_MENU:
    admin_finanzas_saldoinicial_detail = Permissions.register(
        name='Finanzas | Saldo inicial | Ver',
        codename='admin_finanzas_saldoinicial_detail',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            saldoinicial_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_saldoinicial_update = Permissions.register(
        name='Finanzas | Saldo inicial | Actualizar',
        codename='admin_finanzas_saldoinicial_update',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            saldoinicial_list,
            saldoinicial_update
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_saldoinicial_reset = Permissions.register(
        name='Finanzas | Saldo inicial | Reiniciar',
        codename='admin_finanzas_saldoinicial_reset',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            saldoinicial_list,
            saldoinicial_reset
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_saldoinicial_reset = Permissions.register(
        name='Finanzas | Saldo inicial | Registrar',
        codename='admin_finanzas_saldoinicial_register',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            saldoinicial_list,
            saldoinicial_register
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
    diatrabajo_update = Menu.register(
        name='Fecha de Trabajo',
        codename='admin_finanzas_diatrabajo_update',
        url='/operaciones_financieras/fecha_de_trabajo/',
        menu_suc=resumen_subtitulo,
        icon='icon-clock',
        orden=ORDEN(250),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/fecha_de_trabajo/$',
        view=dia_trabajo_views.DiaTrabajoView.as_view(),
        name='admin_finanzas_diatrabajo_update'
    ),
)
if ADD_MENU:
    diatrabajo_close = Menu.register(
        name='Fecha de Cierre',
        codename='admin_finanzas_diatrabajo_close',
        url='/operaciones_financieras/cerrar_dia/',
        menu_suc=resumen_subtitulo,
        icon='icon-scissors',
        orden=ORDEN(260),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cerrar_dia/$',
        view=dia_trabajo_views.CerrarDiaTrabajoView.as_view(),
        name='admin_finanzas_diatrabajo_close'
    ),
)
# ===================================================================#
# Creado permisos para los urls descritos de dia de trabajo
# ===================================================================#
if ADD_MENU:
    admin_finanzas_diatrabajo_update = Permissions.register(
        name='Finanzas | Dia de trabajo | Cambiar',
        codename='admin_finanzas_diatrabajo_update',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            diatrabajo_update
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_diatrabajo_close = Permissions.register(
        name='Finanzas | Dia de trabajo | Cerrar',
        codename='admin_finanzas_diatrabajo_close',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            resumen_subtitulo,
            diatrabajo_close
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
# ===================================================================#
#                    Urls de Operaciones financieras
# ===================================================================#
if ADD_MENU:
    operaciones_subtitulo = Menu.register(
        name='Oper. Financieras',
        codename='admin_finanzas_operaciones_subtitle',
        menu_suc=finanzas_titulo,
        icon='icon-swap',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(300),
        is_view=True,
    )
if ADD_MENU:
    operaciones_deposito_list = Menu.register(
        name='Depositos',
        codename='admin_finanzas_operaciones_deposito_list',
        url='/operaciones_financieras/depositos/',
        menu_suc=operaciones_subtitulo,
        icon='icon-level-down',
        orden=ORDEN(310),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/depositos/$',
        view=movimientos_views.MovimientoDepositoView.as_view(),
        name='admin_finanzas_operaciones_deposito_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_deposito_create = Menu.register(
        name='Cargar',
        codename='admin_finanzas_operaciones_deposito_create',
        menu_suc=operaciones_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/depositos/(?P<comercializadora>\d+?)/$',
        view=movimientos_views.MovimientoDepositoView.as_view(),
        name='admin_finanzas_operaciones_deposito_create'
    ),
)
if ADD_MENU:
    operaciones_pago_list = Menu.register(
        name='Pagos',
        codename='admin_finanzas_operaciones_pago_list',
        url='/operaciones_financieras/pagos/',
        menu_suc=operaciones_subtitulo,
        icon='icon-level-up',
        orden=ORDEN(320),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/pagos/$',
        view=movimientos_views.MovimientoPagoView.as_view(),
        name='admin_finanzas_operaciones_pago_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_pago_create = Menu.register(
        name='Cargar',
        codename='admin_finanzas_operaciones_pago_create',
        menu_suc=operaciones_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/pagos/(?P<comercializadora>\d+?)/$',
        view=movimientos_views.MovimientoPagoView.as_view(),
        name='admin_finanzas_operaciones_pago_create'
    ),
)
if ADD_MENU:
    operaciones_ajuste_list = Menu.register(
        name='Ajustes',
        codename='admin_finanzas_operaciones_ajuste_list',
        url='/operaciones_financieras/ajustes/',
        menu_suc=operaciones_subtitulo,
        icon='icon-loop2',
        orden=ORDEN(330),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/ajustes/$',
        view=movimientos_views.MovimientoAjusteView.as_view(),
        name='admin_finanzas_operaciones_ajuste_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_ajuste_create = Menu.register(
        name='Cargar',
        codename='admin_finanzas_operaciones_ajuste_create',
        menu_suc=operaciones_subtitulo,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/ajustes/(?P<comercializadora>\d+?)/$',
        view=movimientos_views.MovimientoAjusteView.as_view(),
        name='admin_finanzas_operaciones_ajuste_create'
    ),
)
# ===================================================================#
# Creado permisos para los urls descritos de operaciones
# ===================================================================#
if ADD_MENU:
    admin_finanzas_operaciones_deposito = Permissions.register(
        name='Finanzas | Oper. financieras  | Depositos',
        codename='admin_finanzas_operaciones_deposito',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            operaciones_subtitulo,
            operaciones_deposito_list,
            operaciones_deposito_create
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_operaciones_pago = Permissions.register(
        name='Finanzas | Oper. financieras  | Pagos',
        codename='admin_finanzas_operaciones_pago',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            operaciones_subtitulo,
            operaciones_pago_list,
            operaciones_pago_create
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_operaciones_ajuste = Permissions.register(
        name='Finanzas | Oper. financieras  | Ajustes',
        codename='admin_finanzas_operaciones_ajuste',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            operaciones_subtitulo,
            operaciones_ajuste_list,
            operaciones_ajuste_create
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
    operaciones_configuracion_pagar_cobrar_list = Menu.register(
        name='Configuración Cuentas por Pagar/Cobrar',
        codename='admin_finanzas_operaciones_configuracion_pagar_cobrar_list',
        url='/operaciones_financieras/configuracion/pagar-cobrar/',
        menu_suc=operaciones_subtitulo,
        icon='icon-edit',
        orden=ORDEN(339),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/configuracion/pagar-cobrar/$',
        view=cuentas_operaciones.ConfiguracionPorPagarCobrarView.as_view(),
        name='admin_finanzas_operaciones_configuracion_pagar_cobrar_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    admin_finanzas_operaciones_deposito = Permissions.register(
        name='Finanzas | Oper. financieras  | Configuración Cuentas por Pagar/Cobrar',
        codename='admin_finanzas_operaciones_configuracion_pagar_cobrar',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            operaciones_subtitulo,
            operaciones_configuracion_pagar_cobrar_list,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
# ===================================================================#
# ===================================================================#
if ADD_MENU:
    operaciones_cuentas_pagar_list = Menu.register(
        name='Cuentas por pagar',
        codename='admin_finanzas_operaciones_cuentas_pagar_list',
        url='/operaciones_financieras/cuentas/pagar/',
        menu_suc=operaciones_subtitulo,
        icon='icon-align-left',
        orden=ORDEN(340),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/pagar/$',
        view=cuentas_operaciones.CuentasPorPagarView.as_view(),
        name='admin_finanzas_operaciones_cuentas_pagar_list'
    ),
)
if ADD_MENU:
    operaciones_cuentas_cobrar_list = Menu.register(
        name='Cuentas por cobrar',
        codename='admin_finanzas_operaciones_cuentas_cobrar_list',
        url='/operaciones_financieras/cuentas/cobrar/',
        menu_suc=operaciones_subtitulo,
        icon='icon-align-right',
        orden=ORDEN(341),
        is_view=True,
    )
urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/cobrar/$',
        view=cuentas_operaciones.CuentasPorCobrarView.as_view(),
        name='admin_finanzas_operaciones_cuentas_cobrar_list'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_cuentas_cobrar_list_csv = Menu.register(
        name='Csv cuentas por cobrar',
        codename='admin_finanzas_operaciones_cuentas_cobrar_list_print_csv',
        menu_suc=operaciones_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/cobrar/csv/(?P<cache_key>.+?)/$',
        view=CsvView,
        name='admin_finanzas_operaciones_cuentas_cobrar_list_print_csv'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_cuentas_cobrar_list_pdf = Menu.register(
        name='Pdf cuentas por cobrar',
        codename='admin_finanzas_operaciones_cuentas_cobrar_list_print_pdf',
        menu_suc=operaciones_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/cobrar/pdf/(?P<cache_key>.+?)/$',
        view=PdfView,
        name='admin_finanzas_operaciones_cuentas_cobrar_list_print_pdf'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_cuentas_pagar_list_csv = Menu.register(
        name='Csv cuentas por pagar',
        codename='admin_finanzas_operaciones_cuentas_pagar_list_print_csv',
        menu_suc=operaciones_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/pagar/csv/(?P<cache_key>.+?)/$',
        view=CsvView,
        name='admin_finanzas_operaciones_cuentas_pagar_list_print_csv'
    ),
)
# ===================================================================#
if ADD_MENU:
    operaciones_cuentas_pagar_list_pdf = Menu.register(
        name='Pdf cuentas por pagar',
        codename='admin_finanzas_operaciones_cuentas_pagar_list_print_pdf',
        menu_suc=operaciones_subtitulo,
    )

urlpatterns += patterns(
    '',
    url(
        regex=r'^operaciones_financieras/cuentas/pagar/pdf/(?P<cache_key>.+?)/$',
        view=PdfView,
        name='admin_finanzas_operaciones_cuentas_pagar_list_print_pdf'
    ),
)
# ===================================================================#
# Creado permisos para los urls descritos de operaciones financieras
# ===================================================================#
if ADD_MENU:
    admin_finanzas_operaciones_deposito = Permissions.register(
        name='Finanzas | Oper. financieras  | Cuentas por cobrar',
        codename='admin_finanzas_operaciones_cuentas_pagar',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            operaciones_subtitulo,
            operaciones_cuentas_cobrar_list,
            operaciones_cuentas_cobrar_list_csv,
            operaciones_cuentas_cobrar_list_pdf,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_finanzas_operaciones_pago = Permissions.register(
        name='Finanzas | Oper. financieras  | Cuentas por pagar',
        codename='admin_finanzas_operaciones_cuentas_cobrar',
        content_type='admin_finanzas',
        menus=[
            finanzas_titulo,
            operaciones_subtitulo,
            operaciones_cuentas_pagar_list,
            operaciones_cuentas_pagar_list_csv,
            operaciones_cuentas_pagar_list_pdf,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
# ===================================================================#
