# -*- coding: utf-8 -*-

from admin_asterisco7.settings import ADD_MENU
# ===================================================================#
#                    Urls de Mails
# ===================================================================#
from admin_mail.views import message_views
from admin_permisologia.models import Menu, Permissions
from django.urls import include, re_path

# ===================================================================#
urlpatterns = [
]
# ===================================================================#
#                    Urls de Comercializacion
# ===================================================================#
'''
Los enlaces del menu se registran
'''
if ADD_MENU:
    def next_orden(n):
        return lambda x: x + n
    ORDEN = next_orden(0)

    comercializacion_titulo = Menu.register(
        name=' Comercializacion',
        codename='admin_comercializacion_title',
        icon='icon-sitemap',
        content_type=1,  # nivel 1 de titulo
        orden=ORDEN(0),
        is_view=True,
    )
if ADD_MENU:
    mail_subtitulo = Menu.register(
        name='Mensajes',
        codename='admin_mail_message_subtitle',
        menu_suc=comercializacion_titulo,
        icon='icon-mail',
        content_type=2,  # nivel 2 de sutitulo
        orden=ORDEN(550),
        is_view=True,
    )
# ===================================================================#
if ADD_MENU:
    mail_create = Menu.register(
        name='Nuevo',
        codename='admin_mail_message_create',
        url='/mail/nuevo/',
        menu_suc=mail_subtitulo,
        icon='icon-message',
        orden=ORDEN(551),
        is_view=True,
    )
urlpatterns += [
re_path(r'^mail/nuevo/$', message_views.MessajeCreateView.as_view(), name='admin_mail_message_create'),
                        ]
# ===================================================================#
if ADD_MENU:
    mail_list_recibidos = Menu.register(
        name='Mail Recibidos',
        codename='admin_mail_message_list_recibidos',
        url='/mail/recibidos/',
        menu_suc=mail_subtitulo,
        icon='icon-inbox',
        orden=ORDEN(552),
        is_view=True,
    )
    mail_list_recibidos_datatables = Menu.register(
        name="Mail Recibidos datatables",
        codename="admin_mail_message_list_recibidos_datatables",
        menu_suc=mail_list_recibidos,
    )
urlpatterns += [
re_path(r'^mail/recibidos/$', message_views.MessajeRecibidosListView.as_view(), name='admin_mail_message_list_recibidos'),
                        ]
urlpatterns += [
re_path(r'^mail/recibidos/datatables/$', message_views.MessajeRecibidosListDatatableView.as_view(), name='admin_mail_message_list_recibidos_datatables'),
]
# ===================================================================#
if ADD_MENU:
    mail_list_enviados = Menu.register(
        name='Mail Enviados',
        codename='admin_mail_message_list',
        url='/mail/enviados/',
        menu_suc=mail_subtitulo,
        icon='icon-send',
        orden=ORDEN(553),
        is_view=True,
    )
    mail_list_enviados_datatables = Menu.register(
        name="Mail Enviados datatables",
        codename="admin_mail_message_list_enviados_datatables",
        menu_suc=mail_list_enviados,
    )
urlpatterns += [
re_path(r'^mail/enviados/$', message_views.MessajeEnviadosListView.as_view(), name='admin_mail_message_list'),
                        ]
urlpatterns += [
re_path(r'^mail/enviados/datatables/$', message_views.MessajeEnviadosListDatatableView.as_view(), name='admin_mail_message_list_enviados_datatables'),
]
# ===================================================================#
if ADD_MENU:
    mail_list_archivados = Menu.register(
        name='Mail Archivados',
        codename='admin_mail_message_list_archivados',
        url='/mail/archivados/',
        menu_suc=mail_subtitulo,
        icon='icon-save',
        orden=ORDEN(554),
        is_view=True,
    )
    mail_list_archivados_datatables = Menu.register(
        name="Mail Archivados datatables",
        codename="admin_mail_message_list_archivados_datatables",
        menu_suc=mail_list_archivados,
    )
urlpatterns += [
re_path(r'^mail/archivados/$', message_views.MessajeArchivadosListView.as_view(), name='admin_mail_message_list_archivados'),
                        ]
urlpatterns += [
re_path(r'^mail/archivados/datatables/$', message_views.MessajeArchivadosListDatatableView.as_view(), name='admin_mail_message_list_archivados_datatables'),
]
# ===================================================================#
if ADD_MENU:
    mail_list_papelera = Menu.register(
        name='Papelera',
        codename='admin_mail_message_list_papelera',
        url='/mail/papelera/',
        menu_suc=mail_subtitulo,
        icon='icon-delete',
        orden=ORDEN(555),
        is_view=True,
    )
    mail_list_papelera_datatables = Menu.register(
        name="Mail Papelera datatables",
        codename="admin_mail_message_list_papelera_datatables",
        menu_suc=mail_list_papelera,
    )
urlpatterns += [
re_path(r'^mail/papelera/$', message_views.MessajePapeleraListView.as_view(), name='admin_mail_message_list_papelera'),
                        ]
urlpatterns += [
re_path(r'^mail/papelera/datatables/$', message_views.MessajePapeleraListDatatableView.as_view(), name='admin_mail_message_list_papelera_datatables'),
]
# ===================================================================#
if ADD_MENU:
    mail_delete = Menu.register(
        name='Eliminar',
        codename='admin_mail_message_delete',
        menu_suc=mail_subtitulo,
    )
urlpatterns += [
re_path(r'^mail/eliminar/$', message_views.MessajeDeleteView.as_view(), name='admin_mail_message_delete'),
                        ]
# ===================================================================#
if ADD_MENU:
    mail_detail = Menu.register(
        name='Detalle',
        codename='admin_mail_message_detail',
        menu_suc=mail_subtitulo,
    )
urlpatterns += [
re_path(r'^mail/(?P<pk>\d+?)/$', message_views.MessajeDetailView.as_view(), name='admin_mail_message_detail'),
                        ]
# ===================================================================#
#     Creado permisos para los urls descritos de mail
# ===================================================================#
if ADD_MENU:
    admin_mail_message_detail = Permissions.register(
        name='Mensajes | Ver',
        codename='admin_mail_message_detail',
        content_type='admin_mail',
        menus=[
            comercializacion_titulo,
            mail_subtitulo,
            mail_detail,
            mail_list_recibidos,
            mail_list_recibidos_datatables,
            mail_list_enviados,
            mail_list_enviados_datatables,
            mail_list_archivados,
            mail_list_archivados_datatables,
            mail_list_papelera,
            mail_list_papelera_datatables,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_mail_message_create = Permissions.register(
        name='Mensajes | Crear',
        codename='admin_mail_message_create',
        content_type='admin_mail',
        menus=[
            comercializacion_titulo,
            mail_subtitulo,
            mail_create,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )

    admin_mail_message_delete = Permissions.register(
        name='Mensajes | Eliminar',
        codename='admin_mail_message_delete',
        content_type='admin_mail',
        menus=[
            comercializacion_titulo,
            mail_subtitulo,
            mail_delete,
        ],
        profiles=[
            'userprofile_operadora',
            'userprofile_bloque',
            'userprofile_banca',
            'userprofile_distribuidor',
            'userprofile_agencia',
        ],
    )
