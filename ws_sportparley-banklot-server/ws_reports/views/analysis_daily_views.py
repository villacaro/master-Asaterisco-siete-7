# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import analysis_daily


class AnalysisDaily(RESTView):
    process_db = 'query_dailyanalysis'

    def __init__(self):
        super(AnalysisDaily, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['date', 'filter']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(AnalysisDaily, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            analysis_daily(
                content=content,
                session=session,
                fecha=self.data_object.get_entry('date'),
                filter_cadena=self.data_object.get_entry('filter'),
            )

        return content
