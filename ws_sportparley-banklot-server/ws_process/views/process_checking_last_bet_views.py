# -*- coding: utf-8 -*-

from admin_apuestas.models import Tickets
from ws_lib.views import RESTView


class CheckingLastBet(RESTView):
    process_db = 'process_checkinglastbet'

    def __init__(self):
        super(CheckingLastBet, self).__init__()
        self.entrys = ['message', 'session']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(CheckingLastBet, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            try:
                content.set_message_entry(
                    'lastticket',
                    Tickets.objects.only('pk').filter(
                        user_id=session.user.pk
                    ).order_by('-fecha')[0].pk
                )
            except Exception:
                pass

        return content
