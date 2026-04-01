# -*- coding: utf-8 -*-

import json

from admin_banklotsports.settings import DEBUG


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
