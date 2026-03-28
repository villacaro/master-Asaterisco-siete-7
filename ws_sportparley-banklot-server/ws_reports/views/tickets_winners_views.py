# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import tickets_winners


class TicketsWinners(RESTView):
    process_db = 'query_winningtickets'

    def __init__(self):
        super(TicketsWinners, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['date', 'filter']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(TicketsWinners, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            tickets_winners(
                content=content,
                session=session,
                fecha=self.data_object.get_entry('date'),
                filter_cadena=self.data_object.get_entry('filter'),
            )

        return content
