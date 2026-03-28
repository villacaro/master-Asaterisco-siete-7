# -*- coding: utf-8 -*-

from admin_banklotsports.settings import FORMAT_STR_DATETIME_SECONDS
from admin_comercializacion.models import EventNotificationCadena
from django.db.models import Q
from django.utils.timezone import now
from ws_lib.views import RESTView
from ws_sport_requests.managers import DatosJuegos


class KeepAlive(RESTView):
    process_db = 'conn_keepalive'

    def __init__(self):
        super(KeepAlive, self).__init__()
        self.entrys = ['message', 'session']

    def get_content_data(self):
        # Edito la estructura a la que necesite
        content = super(KeepAlive, self).get_content_data()

        content.set_message_entry(
            'date',
            now().strftime(FORMAT_STR_DATETIME_SECONDS)
        )
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(KeepAlive, self).request_valid(
            content, data, session, *args, **kwargs
        )
        if not content.error:
            # Obteniendo ultima fecha de actualizacion de notificaciones por juegos

            data = DatosJuegos(session.session, kwargs)
            content.set_message_entry(
                'last_updated_date_games',
                data.get_update()
            )

            # Obteniendo ultima fecha de actualizacion por cadena de comercializacion
            date_production_cadena = ''

            pks_cadena = session.user.taquilla.get_values_cadena_notificacions()

            event_notification_cadena = EventNotificationCadena.objects.filter(
                Q(bloque=pks_cadena['bloque']) |
                Q(banca=pks_cadena['banca']) |
                Q(distribuidor=pks_cadena['distribuidor']) |
                Q(agencia=pks_cadena['agencia']) |
                Q(taquilla=pks_cadena['taquilla'])
            ).order_by('-date_production')

            try:
                date_production_cadena = event_notification_cadena[
                    0].date_production.strftime(FORMAT_STR_DATETIME_SECONDS)
            except Exception:
                pass

            content.set_message_entry(
                'last_updated_date_cadena',
                date_production_cadena
            )
            # #######################################################################

        return content
