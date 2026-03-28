# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import ticket_details


class TicketDetails(RESTView):
    process_db = 'query_searchticket'

    def __init__(self):
        super(TicketDetails, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['ticket']

    def get_content_data(self):
        content = super(TicketDetails, self).get_content_data()
        content.set_message_entry('error', 0)
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(TicketDetails, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            ticket_details(
                content=content,
                ticket_pk=self.data_object.get_entry('ticket'),
                session=session,
            )

        return content
