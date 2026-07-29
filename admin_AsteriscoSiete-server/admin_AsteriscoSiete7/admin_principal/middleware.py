# -*- coding: utf-8 -*-

import json

from admin_asterisco7.settings import ACCESO_URL, INDEX_URL, LOGOUT_URL, PAGE_404_URL, REDIS_DB
from admin_juego.models import EventNotification
from admin_mail.models import MessageComer
from admin_permisologia.models import Menu
from admin_principal.security import Security
from django.conf import settings
from django.http import HttpResponseRedirect


def ignore_links(url):
    """
    Funcion que vericica si el link dado debe ingnorarse
    """
    for key in ("ADMIN_URL", "ACCESO_URL", "MEDIA_URL", "STATIC_URL", "THEMES_URL"):
        try:
            if url.startswith(getattr(settings, key)):
                return True
        except Exception:
            pass

    for key in ("/__debug__/", "/api-auth/", "/api/", "/dashboard/", "/taquilla/"):
        try:
            if url.startswith(key):
                return True
        except Exception:
            pass

    try:
        menu = Menu.get_search(url=url)
        return menu.is_public
    except Exception:
        return False


"""
Metodo estatico donde la rutina de verificar
un link dado un user y una comercializadora
se escribe una sola vez.
"""


def check_url(url, object_user, object_session, object_comercializadora):

    try:
        # Consulto el menu al que se esta ingresando
        menu = Menu.get_search(url=url)

        if menu.is_global or menu.is_public:
            # en caso de ser un menu global, o publico
            # no se verifica su permiso
            return True
        else:
            if object_user.get_check_permission(
                session_pk=object_session.pk,
                comercializadora=object_comercializadora,
                menu=menu
            ):
                # tiene permiso :)
                return True
            else:

                # no tiene permiso :(
                # y dependiendo de la variable en el settign se da el permiso o
                # no
                return settings.MENU_VALID

    except Menu.DoesNotExist:
        # no tiene permiso :(
        # y dependiendo de la variable en el settign se da el permiso o no
        return settings.MENU_VALID


from django.utils.deprecation import MiddlewareMixin
class AuthenticationAndPermissionsMiddleware(MiddlewareMixin):
    """
    Esta clase que es un middleware de django, gestiona las siguientes tareas:
        1) autenticiacion: verifica que el usuarios este autentificado para poder navegar,
            en caso contrario sera redirigido al login
        2) permisos: si el usuario esta autentificado verifica que tenga permisos
            para acceder al url en cuention, sino devolvera un error 404
        3) procesa info basica global:
            1) Se envia info relevante en los view:
                El objeto del usuario en el kawargs con el key "obj_users"

            2) menu e informacion de uaurio y sistema: recibe una bandera "add_info",
                en el context_data que indica si generar o no dicha informacion
    """

    def process_request(self, request):
        """
        Metodo invocado en el request inicial, antes de saber que vista lo procesara
        Verifica que la variable de session exista, en caso contrario redirigira al login
        """

        if ignore_links(request.path) is False:
            # De estar en un link que no debe ser ingnorado se verifica la
            # variable de session o el usuario de django
            if settings.SESSION_COOKIE_KEY in request.session or (getattr(request, 'user', None) and request.user.is_authenticated):
                pass
            else:
                # "No existe la variable de session")
                return self._redirect(request.path, '')

    def process_view(self, request, view_func, view_args, view_kwargs):
        """
        Este metodo de encarga de:
            1) Verifica que la variable de session sea exactamente
                la misma que genero el servidor
            2) Verifica si la session esta expirada,
            3) Verifica que el usuario tenga permisos sobre el enlace visitado
            4) envia en el kawargs la info necesaria del usuario, sistema de juego etc. para
                posibles validaciones en vistas
        """

        if ignore_links(request.path) is False:
            # Estando en urls ignoradas, procedo a generar la data global en los
            # kwargs

            # objeto especial para obtener todos los objetos
            obj = Security()

            # objeto de la session
            try:
                view_kwargs["object_session"] = obj.get_session(request, False)
                if not view_kwargs["object_session"].check_seccion():
                    # "Session invalida ")
                    return self._redirect(request.path, '')
            except Exception:
                # "Excepiton Session invalida")
                return self._redirect(request.path, '')

            # chekeamos que la session en cuestion contenga los mismos datos generados
            # if obj.check(request= request, session=view_kwargs["object_session"]) is False:
            #    return self._redirect(request.path, "Por cookie incorrecta")

            # ip del usuario
            try:
                view_kwargs["object_user_ip"] = obj.get_ip(request)
            except Exception:
                # Fallback to None
                view_kwargs["object_user_ip"] = None

            # objeto del usuario
            try:
                view_kwargs["object_user"] = obj.get_user(request)
                if getattr(view_kwargs["object_user"], 'get_status', None):
                    if view_kwargs["object_user"].get_status().codename != "status_activo":
                        view_kwargs["object_user"].clearSession()
                        return self._redirect(request.path, '')
            except Exception:
                # Fallback to standard request.user
                if getattr(request, 'user', None) and request.user.is_authenticated:
                    view_kwargs["object_user"] = request.user
                else:
                    return self._redirect(request.path, '')

            # objeto de la comercializadora
            try:
                view_kwargs[
                    "object_comercializadora"] = obj.get_comercializadora(request)
            except Exception:
                if view_kwargs["object_user"].profile.codename == "userprofile_master":
                    from admin_comercializacion.models import Master
                    view_kwargs["object_comercializadora"] = Master()
                else:
                    view_kwargs["object_comercializadora"] = None

            if view_kwargs["object_user"].profile.codename != "userprofile_master":
                access = self.get_access_panel(
                    view_kwargs["object_comercializadora"])
                if not access:
                    return self._redirect(request.path, "Sistema en mantenimiento")

            # objeto del sistema de juego asociado
            try:
                view_kwargs[
                    "object_sistema_juego"] = obj.get_sistemaJuego(request)
            except Exception:
                view_kwargs["object_sistema_juego"] = None

            if check_url(url=request.path,
                         object_user=view_kwargs["object_user"],
                         object_session=view_kwargs["object_session"],
                         object_comercializadora=view_kwargs["object_comercializadora"]):
                # hay permisos
                pass
            else:
                from django.http import Http404
                raise Http404

    def process_template_response(self, request, response):
        """
        En este metodo invoco otros metodos que verifican si la
        vista tieneciertas banderas activas,
        por ejemplo si la vista tiene el atributo 'info_user' activo,
        genera la info correspondiente
        para imprimirlo en el template.
        """

        response = self._add_info_system(request, response)
        response = self._add_info_user(request, response)
        response = self._add_info_menu(request, response)

        if response.context_data:
            response.context_data['PAGE_404_URL'] = PAGE_404_URL
            response.context_data['INDEX_URL'] = INDEX_URL
            response.context_data['LOGOUT_URL'] = LOGOUT_URL
            response.context_data['ACCESO_URL'] = ACCESO_URL

        response = self._add_notification(request, response)
        # add themes
        response = self._add_theme(request, response)

        return response

    # =======================================================================
    # Funciones internas
    # =======================================================================

    def _redirect(self, url, verbose=""):
        """
        Redirecciona al login.
        """
        if url == INDEX_URL or url == LOGOUT_URL:
            if verbose:
                verbose = "?error=" + verbose
            return HttpResponseRedirect(ACCESO_URL + verbose)
        else:
            get_var = "?next=" + url
            if verbose:
                get_var += "&error=" + verbose
            return HttpResponseRedirect(ACCESO_URL + get_var)

    def _add_info_system(self, request, response):
        """
        Verifica que la vista ejecutada tenga activa la opcion de mostrar la info del sistema
        """
        if response.context_data and "view" in response.context_data:
            exits = getattr(response.context_data["view"], "info_system", False)
            if exits is True:
                response.context_data['info_system'] = {
                    "name": "Matchpoint Parley",
                    "version": "1.0.2",
                    "footer": "Copyright © 2015."
                    " Todos los derechos reservados."
                }
        return response

    def _add_info_user(self, request, response):
        """
        Verifica que la vista ejecutada tenga activa la opcion
        de mostrar la info del usuario activo
        """
        # print(dir(response.context_data["view"]))
        if response.context_data and "view" in response.context_data:
            exits = getattr(response.context_data["view"], "info_user", False)
            if exits is True:
                response.context_data['info_user'] = {
                    "user": response.context_data["view"].object_user,
                    "comercializadora": response.context_data["view"].object_comercializadora,
                    "session": response.context_data["view"].object_session,
                    "sistema": response.context_data["view"].object_sistema_juego,
                    "ip": response.context_data["view"].object_user_ip
                }
        return response

    def _add_info_menu(self, request, response):
        """
        Verifica que la vista ejecutada tenga activa la opcion de mostrar la info del menu,
        de estar activa se ejecuta un algoritmo para consultar el menu asociado al usuario,
        """
        if response.context_data and "view" in response.context_data:
            exits = getattr(response.context_data["view"], "info_menu", False)
            if exits is True:

                # Ejecuta el algoritmo de consulta para de los permisos en el
                # objeto de users
                user = response.context_data["view"].object_user
                response.context_data['info_menu'] = user.get_permissions(
                    session_pk=response.context_data["view"].object_session.pk,
                    comercializadora=response.context_data[
                        "view"].object_comercializadora
                )

                response.context_data['info_menu_url'] = request.path

        return response

    def _add_notification(self, request, response):
        """
        Verifica que la vista ejecutada tenga activa la opcion de mostrar la info del menu,
        de estar activa se ejecuta un algoritmo para consultar el menu asociado al usuario,
        """
        if response.context_data and "view" in response.context_data:
            exits = getattr(response.context_data["view"], "info_menu", False)
            if exits is True:

                # ==============================================================
                """
                Consultando notificacion
                """
                if response.context_data["view"].object_sistema_juego:
                    response.context_data["view"].get_object_sistema_logros()
                    if response.context_data["view"].object_sistema_juego.pk == response.context_data[
                            "view"].object_sistema_logros.pk:
                        querryset = EventNotification.objects.filter(
                            sistema=response.context_data[
                                "view"].object_sistema_juego.pk,
                            in_production=False
                        )
                    else:
                        querryset = EventNotification.objects.filter(
                            sistema__in=[
                                response.context_data[
                                    "view"].object_sistema_juego.pk,
                                response.context_data[
                                    "view"].object_sistema_logros.pk
                            ],
                            in_production=False
                        )

                    response.context_data[
                        'admin_juego_eventnotification_subtitle'
                    ] = querryset.count()

                if response.context_data["view"].object_comercializadora:

                    querryset = MessageComer.objects.filter(
                        comercializadora_id=response.context_data[
                            "view"].object_comercializadora.pk,
                        read=False,
                        tray_group=MessageComer.TRAY_GROUP_RECEIVED
                    )
                    response.context_data[
                        'admin_mail_message_subtitle'
                    ] = querryset.count()
                # ==============================================================

        return response

    def _add_theme(self, request, response):
        """
        Añade el tema dependiendo de la instancia iniciada
        """

        if response.context_data and "view" in response.context_data:
            themes = {
                "css": ["css/style.css"]
            }
            sistema_juego = getattr(response.context_data["view"], "object_sistema_juego", None)

            if sistema_juego:
                theme = sistema_juego.get_theme()
                if sistema_juego.theme_id:
                    if not theme.is_default():
                        colors = theme.color_set.all().values('color_type', 'color')
                        themes = {
                            "css": ["themes/{0}/style.css".format(theme.codename), ],
                            "colors": json.dumps(list(colors))
                        }

            response.context_data['themes'] = themes
        return response

    def get_access_panel(self, comercializadora):
        access = True
        if REDIS_DB.get('PANEL_MAINTENANCE_GLOBAL') == b'0':
            access = False
        else:
            origen = comercializadora.get_origen()
            if origen:
                while origen:
                    key_redis = 'PANEL_MAINTENANCE_GLOBAL-{0}'.format(origen.id)
                    value = REDIS_DB.get(key_redis)
                    if value == b'0':
                        access = False
                        break
                    origen = origen.get_origen()
            else:
                key_redis = 'PANEL_MAINTENANCE_GLOBAL-{0}'.format(
                    comercializadora.id)
                value = REDIS_DB.get(key_redis)
                if value == b'0':
                    access = False
        return access
