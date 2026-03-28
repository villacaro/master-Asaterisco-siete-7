# -*- coding: utf-8 -*-

import json

from admin_banklotsports.settings import REDIS_DB
from admin_comercializacion.models import UsuariosTaquilla
from admin_historic.models import TaquillaSessions
from admin_juego.models import SistemaJuego
from admin_status.models import Status
from django.conf import settings
from django.core.cache import cache
from ws_auth.managers import TaquillaSessionDetailManager
from ws_lib.crypto import CryptoRSA


def ignore_links(url, check_admin=False):
    '''
    Verifico los prefijos de los urls en los que no hay auditoria
    '''

    if settings.DEBUG_TOOLBAR:
        for key in ('/__debug__/', ):
            try:
                if url.startswith(key):
                    return True
            except Exception:
                pass

    if check_admin:
        try:
            if url.startswith(getattr(settings, 'ADMIN_URL')):
                return True
        except Exception:
            pass
        return False

    else:
        for key in ('CONN_URL', 'PUBLIC_URL',
                    'MEDIA_URL', 'STATIC_URL', 'UPDATE_URL'):
            try:
                if url.startswith(getattr(settings, key)):
                    return True
            except Exception:
                pass
        return False


def check_status_by_session(session):
    pass


def get_ip(request):
    # get real ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        ip = request.META['HTTP_X_FORWARDED_FOR']
    elif 'Client-IP' in request.META:
        ip = request.META['Client-IP']
    else:
        ip = request.META['REMOTE_ADDR']
    ip = ip.split(',')[0]
    return ip


def get_access_ws(key, comercializadora):
    access = True
    if REDIS_DB.get(key) == b'0':
        access = False
    else:
        origen = comercializadora.get_origen()
        if origen:
            while origen:
                key_redis = '{0}-{1}'.format(key, origen.id)
                value = REDIS_DB.get(key_redis)
                if value == b'0':
                    access = False
                    break
                origen = origen.get_origen()
        else:
            key_redis = '{0}-{1}'.format(key, comercializadora.id)
            value = REDIS_DB.get(key_redis)
            if value == b'0':
                access = False
    return access


class AuthenticationMiddleware(object):
    '''
    Verifica la autentificación del usuario que está accediendo al WS,
    en caso de que la petición sea de conexión (Connection), pasa el middleware.
        1. Auth: Verifica que la taquilla esté en status activo para operar.
        2. Session: Verifica la sesión iniciada por el cliente.
        3. Información básica: En este caso enviará información que siempre
        se intercambiará (sólo global).
    '''

    def process_view(self, request, view_func, view_args, view_kwargs):

        if ignore_links(request.path, check_admin=True):
            # si estoy entrando por el admin, no verifico nada
            return

        if request.method == 'POST' or settings.ACCESS_TO_DEVELOPER:

            data = None
            session = None
            permissions = {
                'permissions': True,
            }

            try:
                # Las variables vienen por post, pero se obtine directamente del body, que es la data original
                # asi la verificacion de la firma de seguridad sera correcta
                body = request.body.decode('utf-8').split('&signature=')
                message_recv = body[0].replace('message=', '')
            except Exception:
                message_recv = None

            if message_recv:
                try:
                    data = json.loads(message_recv)
                except Exception:
                    message_recv = None

            if not message_recv:
                if settings.ACCESS_TO_DEVELOPER and request.method == 'GET':
                    data = {
                        'message': {}
                    }

                    for key in request.GET.keys():
                        if key == 'session':
                            data[key] = request.GET[key]
                        else:
                            data['message'][key] = request.GET[key]
                    if 'session' not in data:
                        if request.resolver_match.url_name != 'ws_auth_auth_url' and not ignore_links(request.path):
                            session = TaquillaSessionDetailManager()
                            client_user = UsuariosTaquilla.objects.get(
                                taquilla_id=settings.ACCESS_TO_DEVELOPER[
                                    'taquilla_id'
                                ]
                            )
                            session.new(client_user, get_ip(request))
                            data['session'] = session.session.pk
                else:
                    permissions = {
                        'permissions': False,
                        'alert': 'Error en la data recibida'
                    }

            if not ignore_links(request.path) and permissions['permissions']:
                # Si la URL es Auth
                if request.resolver_match.url_name == 'ws_auth_auth_url':
                    try:
                        session = TaquillaSessionDetailManager()
                        client_user = UsuariosTaquilla.objects.select_related(
                            'taquilla', 'status'
                        ).get(
                            taquilla_id=data['message']['client_id']
                        )
                        session.new(client_user, get_ip(request))

                    except UsuariosTaquilla.DoesNotExist:
                        permissions = {
                            'permissions': False,
                            'alert': 'El usuario introducido no existe'
                        }
                        session = None
                else:
                    if not TaquillaSessions.objects.filter(
                        pk=data['session'],
                        enddate=None,
                    ).exists():
                        permissions = {
                            'permissions': False,
                            'alert': 'Sesión caducada'
                        }
                    else:
                        try:
                            session_cache = cache.get(
                                'ws_session_{0}'.format(data['session'])
                            )
                            if not session_cache:
                                session_object = TaquillaSessions.objects.select_related(
                                    'user__taquilla__agencia',
                                    'user__status',
                                ).get(
                                    pk=data['session'],
                                    enddate=None
                                )
                                agencia = session_object.user.taquilla.agencia
                                comercializadora = agencia.get_comercializadora()

                                sistema_juego = SistemaJuego.objects \
                                    .get_sistema_juego_by_comercializadora(
                                        comercializadora
                                    )

                                sistema_logros = SistemaJuego.objects \
                                    .get_sistema_logros_by_comercializadora(
                                        comercializadora
                                    )

                                cache_json = {
                                    'user': session_object.user,
                                    'session': session_object,
                                    'sistema_juego': sistema_juego,
                                    'sistema_logros': sistema_logros,
                                    'comercializadora': comercializadora,
                                }

                                # La caché dura 1 hora
                                cache.set(
                                    'ws_session_{0}'.format(data['session']),
                                    cache_json,
                                    settings.CACHES_CONF_TIME['Auth']['ws_session']
                                )

                                session_cache = cache.get(
                                    'ws_session_{0}'.format(data['session'])
                                )

                            view_kwargs['sistema_'] = session_cache['sistema_juego']
                            view_kwargs['sistema_logros'] = session_cache['sistema_logros']
                            view_kwargs['comercializadora'] = session_cache['comercializadora']

                            # Creo una instancia de session
                            session = TaquillaSessionDetailManager(
                                session_cache['session']
                            )

                            if session.user.pub_key_client:
                                # body[1]: tiene la firma de seguridad
                                if CryptoRSA.verify(message_recv, body[1], session.user.pub_key_client):
                                    pass
                                else:
                                    permissions = {
                                        'permissions': False,
                                        'alert': 'Error, Firma incorrecta'
                                    }

                            if permissions['permissions']:
                                permisos = list(UsuariosTaquilla.objects.filter(
                                    pk=session.user.pk
                                ).values_list(
                                    'status_id',
                                    'taquilla__agencia__status_id',
                                    'taquilla__agencia__distribuidores__status_id',
                                    'taquilla__agencia__distribuidores__banca__status_id',
                                    'taquilla__agencia__distribuidores__banca__bloque__status_id',
                                    'taquilla__agencia__distribuidores__banca__bloque__operadora__status_id'
                                ))

                                if len(permisos) == 0:
                                    permissions = {
                                        'permissions': False,
                                        'alert': 'Error al verificar permisos.'
                                    }

                                else:
                                    permisos = permisos[0]
                                    activo = Status.get_status_by_codename(codename='status_activo')
                                    activo_sin_venta = Status.get_status_by_codename(
                                        codename='status_activo_sin_venta')
                                    pks_activo = [activo.pk, activo_sin_venta.pk]
                                    for cadena in set(permisos):
                                        # solo recorro lo necesario con set quito lo repetido :)
                                        if cadena not in pks_activo:
                                            permissions = {
                                                'permissions': False,
                                                'alert': 'No tiene permisos, contacte con soporte técnico.'
                                            }
                                            break

                        except TaquillaSessions.DoesNotExist:
                            permissions = {
                                'permissions': False,
                                'alert': 'Sesión caducada'
                            }

            if view_kwargs.get('comercializadora'):
                access = get_access_ws(
                    'WS_MAINTENANCE_GLOBAL',
                    view_kwargs.get('comercializadora'))

                if not access:
                    permissions = {
                        'permissions': False,
                        'alert': 'El sistema no está disponible, intente más tarde.'
                    }

            return view_func(
                request, data, session, permissions,
                *view_args, **view_kwargs
            )
