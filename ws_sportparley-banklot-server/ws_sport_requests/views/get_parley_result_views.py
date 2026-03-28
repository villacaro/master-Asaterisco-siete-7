# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_reports.managers import check_date
from ws_sport_requests.managers import ParleyResult


class GetParleyResult(RESTView):
    process_db = 'process_getgames_result'

    def __init__(self):
        super(GetParleyResult, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['start_date', 'end_date', 'filter']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetParleyResult, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            fecha_ini = self.data_object.get_entry('start_date')
            if check_date(fecha_ini, content):
                # si la fecha es anterior a el limite no consulta
                pass
            else:
                data = ParleyResult(session)
                content.set_message_entry(
                    'parley_result',
                    data.get_result_by_deports(
                        fecha_ini=fecha_ini,
                        fecha_fin=self.data_object.get_entry('end_date'),
                        deporte=self.data_object.get_entry('filter'),
                    )
                )

        return content


class GetParleyResultTable(RESTView):
    process_db = 'process_getgames_result'

    def __init__(self):
        super(GetParleyResultTable, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['date', 'filter']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetParleyResultTable, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            fecha = self.data_object.get_entry('date')
            if check_date(fecha, content):
                # si la fecha es anterior a el limite no consulta
                pass
            else:
                data = ParleyResult(session)
                content.set_message_entry(
                    'parley_resulttable',
                    data.get_resulttable_by_deports(
                        fecha=fecha,
                        deporte=self.data_object.get_entry('filter'),
                    )
                )

        return content
