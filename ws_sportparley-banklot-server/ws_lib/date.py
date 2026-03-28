# -*- coding: utf-8 -*-
from datetime import timedelta

hora_cero = " 00:00:00.0000"
hora_23 = " 23:59:59.1000"


class strFecha(object):
    """docstring for strFecha"""

    def __init__(self, horajuego):
        super(strFecha, self).__init__()

        if str(horajuego).find("+00:00") >= 0:
            horajuego = horajuego - timedelta(hours=4, minutes=30)
        self.fecha = str(horajuego.strftime("%Y-%m-%d"))
        self.hora = str(horajuego.strftime("%I:%M %p"))  # + " <UTC -04:30> "

    def getFecha(self):
        return str(self.fecha)

    def getHora(self):
        return str(self.hora)

    def getDateTime(self):
        return "{0} {1}".format(self.fecha, self.hora)
