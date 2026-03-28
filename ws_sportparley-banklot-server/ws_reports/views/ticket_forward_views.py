# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import ticket_details


class TicketForward(RESTView):
    process_db = 'query_tickets_forward'

    def __init__(self):
        super(TicketForward, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['ticket']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(TicketForward, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            ticket_details(
                content=content,
                ticket_pk=self.data_object.get_entry('ticket'),
                session=session,
                original=True
            )

        return content
