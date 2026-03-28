# -*- coding: utf-8 -*-
class BasicClass(object):
    """
    BasicClass (Clase básica): Contiene funciones globales.
    """
    def get_class_name(self):
        return str(self.__class__.__name__).lower()
