# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import get_last_ticket


class LastTicket(RESTView):
    process_db = 'query_cancelticket'

    def __init__(self):
        super(LastTicket, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = []

    def get_content_data(self):
        content = super(LastTicket, self).get_content_data()
        content.set_message_entry('error', 0)
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(LastTicket, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            get_last_ticket(
                content=content,
                session=session
            )

        return content
