# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import date, datetime, timedelta

from admin_banklotsports.settings import FORMAT_STR_DATE_REPORTS

hora_cero = " 00:00:00"
hora_23 = " 23:59:59"
one_day = timedelta(days=1)


class strFecha(object):
    """docstring for strFecha"""

    def __init__(self, horajuego):
        super(strFecha, self).__init__()

        if str(horajuego).find("+00:00") >= 0:
            horajuego = horajuego - timedelta(hours=4, minutes=00)
        self.fecha = str(horajuego.strftime(FORMAT_STR_DATE_REPORTS))
        self.hora = str(horajuego.strftime("%I:%M %p"))  # + " <UTC -04:00> "
        self.datetime = datetime(horajuego.year, horajuego.month, horajuego.day, 0, 0)

    def getFecha(self):
        return self.fecha

    def getHora(self):
        return self.hora

    def getDateTime(self):
        return self.datetime


class Funs:

    @staticmethod
    def list_days_by_range(ini, end):
        """ List days by a range """
        day = ini
        days = (end - ini).days
        for n in range(days + 1):
            if n > 0:
                day += one_day
            yield day

    @staticmethod
    def get_week_by_date(date):
        """ Get the week by date """
        day_idx = (date.weekday() + 1) % 7
        sunday = date - timedelta(days=day_idx) + one_day
        date = sunday
        for n in range(7):
            yield date
            date += one_day

    @staticmethod
    def get_quincena_by_date(date):
        """ Get the quincena """
        if date.day in range(1, 16):
            # Primera quincena
            date = Funs.first_day_of_month(date)
            for n in range(15):
                yield date
                date += one_day
        else:
            # Segunda quincena
            date = Funs.middle_day_of_month(date)
            middle = Funs.last_day_of_month(date)
            for n in range(15, middle.day - 1):
                yield date
                date += one_day

    @staticmethod
    def get_month_by_date(date):
        """ Get the quincena """
        first = Funs.first_day_of_month(date)
        day = first
        for n in range(Funs.get_month_days(date)[1]):
            if n > 0:
                day += one_day
            yield day

    @staticmethod
    def first_day_of_month(d):
        return date(d.year, d.month, 1)

    @staticmethod
    def middle_day_of_month(d):
        return date(d.year, d.month, 16)

    @staticmethod
    def last_day_of_month(d):
        return Funs.first_day_of_month(d) + timedelta(-1)

    @staticmethod
    def get_month_days(d):
        return monthrange(d.year, d.month)
