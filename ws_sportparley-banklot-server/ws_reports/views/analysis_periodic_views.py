# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import analysis_periodic


class AnalysisPeriodic(RESTView):
    process_db = 'query_periodicanalysis'

    def __init__(self):
        super(AnalysisPeriodic, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['start_date', 'end_date', 'filter']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(AnalysisPeriodic, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            analysis_periodic(
                content=content,
                session=session,
                fecha_inicio=self.data_object.get_entry('start_date'),
                fecha_fin=self.data_object.get_entry('end_date'),
                filter_cadena=self.data_object.get_entry('filter')
            )

        return content
