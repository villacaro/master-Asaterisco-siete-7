
from admin_asterisco7.settings import FORMAT_STR_DATETIME
from admin_comercializacion.models import EventNotificationCadena, types_notification_cadena
from admin_lib.util_task import AsyncGestionOperationalError
from admin_mail.models import MessageComer, MessageSend
try:
    from celery.registry import tasks
except ImportError:
    tasks = {}
from django.utils.timezone import now


class AsyncSendMail(AsyncGestionOperationalError):
    name = 'AsyncSendMail'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        message = MessageSend.objects.get(pk=kwargs.get('message_send'))
        message_object = message.message

        def send(comer):
            return MessageComer.objects.create(
                comercializadora_id=comer.pk,
                message=message_object,
                read=False,
                tray_group=MessageComer.TRAY_GROUP_RECEIVED
            )

        data = {
            'pk': message_object.pk,
            'priority': message_object.priority,
            'from': '{0}'.format(message_object.from_comercializadora),
            'send_at': message_object.send_at.strftime(FORMAT_STR_DATETIME),
            'subject': message_object.subject,
            'body': message_object.body,
            'adjunts': [],
        }
        for adjunt in message_object.adjunts.all():
            data['adjunts'].append(adjunt.adjunt.url)

        def send_notificacion(cadena):
            kwargs = {
                'data': data,
                'date_production': now(),
                'data_origin': types_notification_cadena['mensajes'][0],
            }
            kwargs[cadena.prefix_filter] = cadena.pk
            EventNotificationCadena.objects.create(
                **kwargs
            )

        i = 0
        for comer in message.to_comercializadora.all():
            if MessageSend.SEND_SIMPLE == message.options:
                send(comer)
                i += 1
                if comer.get_object().prefix_filter == 'taquilla':
                    send_notificacion(comer.get_object())
            elif MessageSend.SEND_MASIVO == message.options:
                for masive in comer.get_offspring_level1().only('pk'):
                    send(masive)
                    i += 1
                if comer.get_object().prefix_filter in ['agencia', 'taquilla']:
                    send_notificacion(comer.get_object())
            elif MessageSend.SEND_TAQUILLAS == message.options:
                for taquilla in comer.get_offspring_taquillas().only('pk'):
                    send(taquilla)
                    i += 1
                send_notificacion(comer.get_object())
        return 'se enviaron {0} mensajes'.format(i)


tasks.register(AsyncSendMail)
