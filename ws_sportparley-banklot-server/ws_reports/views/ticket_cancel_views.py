# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import ticket_cancel


class TicketCancel(RESTView):
    process_db = 'query_cancelticket'

    def __init__(self):
        super(TicketCancel, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['ticket']

    def get_content_data(self):
        content = super(TicketCancel, self).get_content_data()
        content.set_message_entry('error', 0)
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(TicketCancel, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            ticket_cancel(
                content=content,
                ticket_pk=self.data_object.get_entry('ticket'),
                session=session,
                automatic=self.data_object.get_entry('automatic'),
            )

        return content
