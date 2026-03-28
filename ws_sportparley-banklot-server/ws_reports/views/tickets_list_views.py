# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import tickets_list


class TicketsList(RESTView):
    process_db = 'query_tickets'

    def __init__(self):
        super(TicketsList, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['date', 'filter', 'status']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(TicketsList, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            tickets_list(
                content=content,
                session=session,
                fecha=self.data_object.get_entry('date'),
                filter_cadena=self.data_object.get_entry('filter'),
                filter_status=self.data_object.get_entry('status'),
            )

        return content
