# Create your views here.
from admin_historic.models import HechoConnectionsComer
from django.conf import settings
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.generic import View
from ws_lib.json import JSONMessage, JSONObject, JsonResponse


class RESTView(View):

    def __init__(self):
        self._data_object = JSONObject()
        self._entrys = ['message', ]
        self._message_entrys = []

    @property
    def data_object(self):
        return self._data_object

    @data_object.setter
    def data_object(self, value):
        self._data_object = value

    @property
    def entrys(self):
        return self._entrys

    @entrys.setter
    def entrys(self, value):
        self._entrys = value

    @property
    def message_entrys(self):
        return self._message_entrys

    @message_entrys.setter
    def message_entrys(self, value):
        self._message_entrys = value

    def get_content_data(self):
        content = JSONMessage()  # Crea una instancia de JSONMessage
        # content.update() # Se actualiza el objecto para transformarlo en JSON
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        set_entrys = [x for x in list(data.keys()) if x not in self.entrys]

        if not set_entrys:

            set_message_entrys = \
                [x for x in self.message_entrys if x not in data['message']]

            if set_message_entrys:
                # Faltan variables de message
                content.error_message = 'Algunas variables están perdidas'
                content.error = True
                # Se actualiza el objecto para transformarlo en JSON
                content.update()
        else:
            # Faltan variables de la estructura
            content.error_message = 'Algunas variables están perdidas'
            content.error = True
            # Se actualiza el objecto para transformarlo en JSON
            content.update()

        if not content.error:
            # verificamos que los keys esten inicializados
            for key in self.message_entrys:
                val = data['message'][key]
                if val is None or val == '':
                    content.error_message = "El key: '{key}' no puede estar vacio ".format(
                        key=key
                    )

                    content.error = True
                    break
            if not content.error:
                # Si el content no generó error,
                # asigno data_object para manipulación
                self.data_object.json = data['message']
        return content

    def process_session_detail(
            self, session, process, style_class="error",
            callback_message=None, error_message=None):
        if callback_message:
            session.callback_message = callback_message
            session.style_class = style_class
        if error_message:
            session.error_message = error_message
        session.load(process)
        return session

    def get(
            self, request, data=None, session=None,
            permissions=None, *args, **kwargs):
        if settings.ACCESS_TO_DEVELOPER:
            return self.exe(
                request, data, session,
                permissions, *args, **kwargs)
        else:
            from django.http import Http404
            raise Http404

    def post(self, request, data, session, permissions, *args, **kwargs):
        return self.exe(
            request, data, session,
            permissions, *args, **kwargs)

    def exe(self, request, data, session, permissions, *args, **kwargs):
        """
        Retorna data que es la información que llega desde el cliente
        """
        # Permisos generales
        if permissions:
            # No tiene permisos para ejecutar código
            if permissions['permissions'] is False:
                content = self.get_content_data()
                content.error_message = permissions['alert']
            else:

                content = self.request_valid(
                    self.get_content_data(), data, session, *args, **kwargs
                )

        if session:
            # Error con las credenciales del usuario
            '''
            if hasattr(self, 'process_db'):
                session = self.process_session_detail(
                    session=session,
                    process=self.process_db,
                    error_message=content.error_message
                )
            '''

            HechoConnectionsComer.register_connection(
                session.user.taquilla
            )

            if content.error:
                session.session.enddate = now()
                session.session.save(update_fields=['enddate', 'updated_at'])
            session.save()

        content.update()
        if request.method == 'GET' and settings.DEBUG_TOOLBAR:
            return HttpResponse('<html lang="es"><head></head><body><div>{0}</div></body></html>'.format(
                content.message
            )
            )
        else:
            return JsonResponse(content.message, session)
