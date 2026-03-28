# -*- coding: utf-8 -*-
import django
from admin_banklotsports.settings import FORMAT_STR_DATETIME
from admin_mail.models import Message, MessageComer, MessageSend
from django.core.paginator import Paginator
from django.utils.timezone import now
from ws_lib.views import RESTView


class GetMail(RESTView):
    process_db = 'process_getmail'

    def __init__(self):
        super(GetMail, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['message_ids']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetMail, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            comercializadora = session.user.taquilla.get_comercializadora()
            json_messages = []
            for messagecomer in MessageComer.objects.select_related('message__from_comercializadora').filter(
                comercializadora_id=comercializadora.id,
                message_id__in=self.data_object.get_entry('message_ids'),
            ):
                json_message = {
                    'id': messagecomer.message_id,
                    'read': messagecomer.read,
                    'subject': messagecomer.message.subject,
                    'body': messagecomer.message.body,
                    'priority': messagecomer.message.priority,
                    'send_at': messagecomer.message.send_at.strftime(FORMAT_STR_DATETIME),
                    'from': '{0}'.format(messagecomer.message.from_comercializadora),
                    'adjunts': [],
                }
                for adjunt in messagecomer.message.adjunts.all():
                    json_message['adjunts'].append(adjunt.adjunt.url)

                json_messages.append(json_message)
            content.set_message_entry('messages', json_messages)

        return content


class GetMails(RESTView):
    process_db = 'process_getmails'

    def __init__(self):
        super(GetMails, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['page', 'items', 'group']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetMails, self).request_valid(
            content, data, session, *args, **kwargs
        )
        if not content.error:
            comercializadora = session.user.taquilla.get_comercializadora()
            try:
                messagescomer = MessageComer.objects.select_related('message__from_comercializadora').filter(
                    comercializadora_id=comercializadora.id,
                    tray_group=self.data_object.get_entry('group'),
                ).order_by('-message__send_at')

                messages_paginates = Paginator(
                    messagescomer, self.data_object.get_entry('items'))
                messages_page = messages_paginates.page(
                    self.data_object.get_entry('page'))

                message_list = []
                for message in messages_page.object_list:
                    message_row = {
                        'message_id': message.message.id,
                        'subject': message.message.subject,
                        'send_at': message.message.send_at.strftime(FORMAT_STR_DATETIME),
                        'from': '{0}'.format(message.message.from_comercializadora)
                    }
                    message_list.append(message_row)

                json_message = {
                    'page': messages_page.number,
                    'pages_count': messages_paginates.num_pages,
                    'messages_count': messages_paginates.count,
                    'messages_list': message_list,
                }
                content.set_message_entry('messages_list', json_message)

            except django.core.paginator.EmptyPage:
                content.set_message_entry('error', 1)
                content.set_message_entry(
                    'error_message', 'Valores de paginacion no correctos')

        return content


class ReadMail(RESTView):
    process_db = 'process_readmail'

    def __init__(self):
        super(ReadMail, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['message_id']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(ReadMail, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            comercializadora = session.user.taquilla.get_comercializadora()
            try:
                messagecomer = MessageComer.objects.get(
                    comercializadora_id=comercializadora.id,
                    message_id=self.data_object.get_entry('message_id'),
                )
                messagecomer.read = True
                messagecomer.save(update_fields=['read'])
            except MessageComer.DoesNotExist:
                content.set_message_entry('error', 1)
                content.set_message_entry(
                    'error_message', 'Mensaje no encontrado')
        return content


class SendMail(RESTView):
    process_db = 'process_sendmail'

    def __init__(self):
        super(SendMail, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['subject', 'body', 'priority', 'level']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(SendMail, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            comercializadora = session.user.taquilla.get_comercializadora()

            if self.data_object.get_entry('level') == 'operadora':
                from_comercializadora = session.user.taquilla.agencia.distribuidores \
                    .banca.bloque.operadora.get_comercializadora()
            elif self.data_object.get_entry('level') == 'bloque':
                from_comercializadora = session.user.taquilla.agencia.distribuidores \
                    .banca.bloque.get_comercializadora()
            elif self.data_object.get_entry('level') == 'banca':
                from_comercializadora = session.user.taquilla.agencia.distribuidores.banca.get_comercializadora()
            elif self.data_object.get_entry('level') == 'distribuidor':
                from_comercializadora = session.user.taquilla.agencia.distribuidores.get_comercializadora()
            else:
                from_comercializadora = session.user.taquilla.agencia.get_comercializadora()

            message = Message.objects.create(
                subject=self.data_object.get_entry('subject'),
                body=self.data_object.get_entry('body'),
                priority=self.data_object.get_entry('priority'),
                send_at=now(),
                from_comercializadora=from_comercializadora
            )

            MessageComer.objects.create(
                comercializadora=comercializadora,
                message=message,
                read=True,
                tray_group=MessageComer.TRAY_GROUP_SENT
            )

            MessageComer.objects.create(
                comercializadora=from_comercializadora,
                message=message,
                read=False,
                tray_group=MessageComer.TRAY_GROUP_RECEIVED
            )

            send = MessageSend.objects.create(
                message=message,
                options=MessageSend.SEND_SIMPLE
            )

            send.to_comercializadora.add(
                from_comercializadora
            )

        return content
