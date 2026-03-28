# -*- coding: utf-8 -*-
from ws_auth.middleware import get_access_ws
from ws_lib.views import RESTView
from ws_reports.managers import ticket_pay


class TicketPay(RESTView):
    process_db = 'query_payticket'

    def __init__(self):
        super(TicketPay, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['ticket', 'ticket_serial']

    def get_content_data(self):
        content = super(TicketPay, self).get_content_data()
        content.set_message_entry('error', 0)
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(TicketPay, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            access = get_access_ws('WS_MAINTENANCE_PAY', kwargs['comercializadora'])
            if not access:
                content.set_message_entry('error', 1)
                content.set_message_entry(
                    'error_message', 'Esta opción no está disponible, intente más tarde.')
            else:
                ticket_pay(
                    content=content,
                    ticket_pk=self.data_object.get_entry('ticket'),
                    ticket_serial=self.data_object.get_entry('ticket_serial'),
                    session=session,
                )

        return content
