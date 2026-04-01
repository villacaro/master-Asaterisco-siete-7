# -*- coding: utf-8 -*-

from admin_banklotsports.settings import CACHES_CONF_TIME
from admin_lib.util_crypto import CryptoAes
from django.conf import settings
from django.core.cache import cache


class Security(object):
    """
    Clase encargada de generar, verificar y gestionar
    todo lo relacionado con el
    cookie que mantiene la variable de session.
    """
    crypto = CryptoAes()
    texto = None

    def get_ip(self, request):
        # get real ip
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            ip = request.META['HTTP_X_FORWARDED_FOR']
        elif 'Client-IP' in request.META:
            ip = request.META['Client-IP']
        else:
            ip = request.META['REMOTE_ADDR']
        ip = ip.split(",")[0]
        return ip

    def check(self, request, session):
        return session.cookie == request.session[settings.SESSION_COOKIE_KEY]

    def set_conf(self, request,
                 id_sesion, id_usuario,
                 id_comercializadora,
                 id_sistema_juego):
        """
        Guarda las variables necesarias en variable de session.
        Y asi poder saber quien es, a que cadena pertenece y que
        sistema de juego tiene asociado.
        Los datos que llegan deben ser los puros pks.
        """

        self.texto = '{0},{1},{2},{3}'.format(
            id_sesion,
            id_usuario,
            id_comercializadora,
            id_sistema_juego
        )
        request.session[settings.SESSION_COOKIE_KEY] = self.crypto.Encrypt(
            self.texto
        ).decode("iso-8859-1")

        request.session.set_expiry(0)
        return request.session[settings.SESSION_COOKIE_KEY]

    def _get_key(self, request, pos):
        """
        Devuelve un key, dependiendo de la posicion solicitada
        """
        if self.texto is None:
            if settings.SESSION_COOKIE_KEY in request.session:

                self.texto = self.crypto.Decrypt(
                    request.session[settings.SESSION_COOKIE_KEY].encode("iso-8859-1")
                ).strip().split(",")

            else:

                self.texto = None

        if self.texto is not None:
            return self.texto[pos]
        else:
            # Errro al tratar de obtener la data de session
            raise ValueError("Variable de session vacia")

    def _get_id_sesion(self, request):
        """
        Retorna el id de la session guardado en el cookie de session
        """
        return self._get_key(request, 0)

    def get_session(self, request, get_cache=True):
        """
        Retorna el objeto de session relacionado con el user.
        """
        key = '{0}_{1}_{2}'.format(
            self._get_id_sesion(request),
            self._get_id_user(request),
            self.get_ip(request),
        )
        if get_cache:
            session = cache.get(key)
        else:
            session = None
        if not session:
            from admin_historic.models import Sessions
            session = Sessions.objects.only('pk', 'enddate').get(
                pk=self._get_id_sesion(request),
                user_id=self._get_id_user(request),
                ip=self.get_ip(request)
            )
            cache.set(
                key,
                session,
                CACHES_CONF_TIME['registros_db']['session_expire']
            )
        return session

    def _get_id_user(self, request):
        """
        Retorna el id del usuario guardado en el cookie de session
        """
        return int(self._get_key(request, 1))

    def get_user(self, request):
        """
        Retorna el objeto del usuario en variable de session
        """
        from admin_users.models import Users
        return Users.objects.get(
            pk=self._get_id_user(request)
        )

    def _get_id_Comercializadora(self, request):
        """
        Retorna el id de la comercializadora guardada en el cookie de session
        """
        return int(self._get_key(request, 2))

    def get_comercializadora(self, request):
        """
        Retorna el objeto de comercializadora asociado
        """
        from admin_finanzas.models import Comercializadora
        return Comercializadora.objects.get(
            pk=self._get_id_Comercializadora(request),
        )

    def _get_id_sistemaJuego(self, request):
        """
        Retorna el id del sistema de juego guardada en el cookie de session
        """
        return int(self._get_key(request, 3))

    def get_sistemaJuego(self, request):
        """
        Retorna el objeto del sistema de juego
        """
        from admin_juego.models import SistemaJuego
        return SistemaJuego.objects.get(
            pk=self._get_id_sistemaJuego(request)
        )
