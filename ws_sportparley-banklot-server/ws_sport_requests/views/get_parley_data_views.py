# -*- coding: utf-8 -*-
from ws_lib.views import RESTView
from ws_sport_requests.managers import DatosJuegos


class GetParleyData(RESTView):
    process_db = "process_getgames_initial"

    def __init__(self):
        super(GetParleyData, self).__init__()
        self.entrys = ["message", "session"]

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetParleyData, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            data = DatosJuegos(session.session, kwargs)
            content.set_message_entry(
                "parley_data",
                data.get_juegos_all(),
            )

        return content


class GetParleyDataByDeporte(RESTView):
    process_db = "process_getgames_initial"

    def __init__(self):
        super(GetParleyDataByDeporte, self).__init__()
        self.entrys = ["message", "session"]
        self.message_entrys = ['deporte']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetParleyDataByDeporte, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            data = DatosJuegos(session.session, kwargs)
            content.set_message_entry(
                "parley_databydeporte",
                data.get_juegos_filter(
                    deporte_id=self.data_object.get_entry('deporte'),
                )
            )

        return content
