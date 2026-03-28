# -*- coding: utf-8 -*-
import json

from django import http
from ws_lib.crypto import CryptoRSA
from ws_sportparley.settings import DEBUG


def JsonDumps(json_data):
    """
    Retorna el objeto json recibido en una cadena de texto,
    dependiendo de si el proyecto esta en debug, identa el texto.
    """
    indent = 2 if DEBUG else None
    text = json.dumps(json_data, ensure_ascii=True, indent=indent)
    return text.encode("utf-8")


def JsonLoads(json_data):
    """
    Retorna el texto recibido en un objeto json
    """
    return json.loads(json_data)


class JSONObject(object):

    def __init__(self):
        self._json = {}

    @property
    def json(self):
        return self._json

    @json.setter
    def json(self, value):
        self._json = value

    def set_entry(self, key, value):
        self.json[key] = value

    def get_entry(self, key):
        try:
            return self.json[key]
        except Exception:
            return None

    def string_to_json(self, string):
        self.json = json.loads(string)


class JSONMessage(object):

    def __init__(self):
        super(JSONMessage, self).__init__()
        self._message_object = JSONObject()
        self._error = False
        self._error_message = None
        self._message = {
            'message': None,
            'error': 0
        }

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def message_object(self):
        return self._message_object

    @message_object.setter
    def message_object(self, value):
        self._message_object = value

    @property
    def error(self):
        return self._error

    @error.setter
    def error(self, value):
        self._error = value

    @property
    def error_message(self):
        return self._error_message

    @error_message.setter
    def error_message(self, value):
        self._error = True
        self._error_message = value

    def set_entry(self, key, value):
        self.message[key] = value

    def get_entry(self, key):
        return self.message[key]

    def set_message_entry(self, key, value):
        self.message_object.set_entry(key, value)

    def get_message_entry(self, key):
        return self.message_object.get_entry(key)

    def string_to_json(self, string):
        self.message_object.json = json.loads(string)

    def update(self):
        if self.error:
            self.message['error'] = 1
            self.message['error_message'] = self.error_message
            if 'message' in self.message:
                del self.message['message']
        else:
            self.message["message"] = self.message_object.json


class JsonResponse(http.HttpResponse):
    """
    Creates an instance of HttpResponse containing JSON content
    """

    def __init__(self, data, session):
        content_type = "application/json;charset=UTF-8"

        # indent = 1 if DEBUG else None
        indent = None
        body = json.dumps(
            data, sort_keys=False, indent=indent,
            separators=(',', ': '), ensure_ascii=True
        )

        if session and session.user.pub_key_client:
            data_secure = {
                'body': body,
                'signature': CryptoRSA.sign(body, session.user.priv_key),
            }

            body = json.dumps(
                data_secure, sort_keys=False, indent=indent,
                separators=(',', ': '), ensure_ascii=True
            )

        super(JsonResponse, self).__init__(
            content=body,
            content_type=content_type
        )
