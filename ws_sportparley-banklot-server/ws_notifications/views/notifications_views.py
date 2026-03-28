# -*- coding: utf-8 -*-
from datetime import timedelta

from admin_banklotsports.settings import FORMAT_STR_DATETIME_SECONDS
from admin_comercializacion.models import EventNotificationCadena
from django.db.models import Q
from django.utils.timezone import now
from ws_lib.views import RESTView
from ws_sport_requests.managers import DatosJuegos


class Notifications(RESTView):
    process_db = 'process_getnotifications'

    def __init__(self):
        super(Notifications, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['last_date', 'new_date']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(Notifications, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            data = DatosJuegos(session.session, kwargs)
            content.set_message_entry(
                'parley_data',
                data.get_notifications(
                    self.data_object.get_entry('last_date'),
                    self.data_object.get_entry('new_date')
                )
            )
        return content


class NotificationsLost(RESTView):
    process_db = 'process_getnotificationslost'

    def __init__(self):
        super(NotificationsLost, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['pk_origin', 'data_origin']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(NotificationsLost, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            data = DatosJuegos(session.session, kwargs)
            content.set_message_entry(
                'parley_data',
                data.get_notifications_lost(
                    self.data_object.get_entry('pk_origin'),
                    self.data_object.get_entry('data_origin')
                )
            )
        return content


class NotificationsCadena(RESTView):
    process_db = 'process_getnotificationscadena'

    def __init__(self):
        super(NotificationsCadena, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['last_date', 'new_date']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(NotificationsCadena, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            pks_cadena = session.user.taquilla.get_values_cadena_notificacions()

            fecha_old = now().strptime(
                self.data_object.get_entry('last_date'),
                FORMAT_STR_DATETIME_SECONDS
            )
            fecha_new = now().strptime(
                self.data_object.get_entry('new_date'),
                FORMAT_STR_DATETIME_SECONDS
            )

            event_notification_cadena = EventNotificationCadena.objects.filter(
                Q(bloque=pks_cadena['bloque']) |
                Q(banca=pks_cadena['banca']) |
                Q(distribuidor=pks_cadena['distribuidor']) |
                Q(agencia=pks_cadena['agencia']) |
                Q(taquilla=pks_cadena['taquilla'])
            ).filter(
                # Sumamos un segundo a la fecha de inicio para no bajar actualizaciones ya descargadas
                # Sumamos un segundo a la fecha de fin, para abarcar error de redondeo
                date_production__range=(fecha_old + timedelta(seconds=1), fecha_new + timedelta(seconds=1))
            ).order_by('date_production')

            message = []
            for obj in event_notification_cadena:
                message.append(
                    {
                        'data_origin': obj.data_origin,
                        'data': obj.data,
                    }
                )

            content.set_message_entry(
                'cadena_data',
                message
            )
        return content
