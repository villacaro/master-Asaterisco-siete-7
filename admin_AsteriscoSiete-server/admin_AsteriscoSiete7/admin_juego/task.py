# -*- coding: utf-8 -*-

from datetime import date

from admin_comercializacion.models import EventNotificationCadena
from admin_juego.models import EventNotification, Fechas
from admin_lib.util_task import AsyncGestionOperationalError
from admin_status.models import Status
try:
    from celery.registry import tasks
except ImportError:
    class _NoOpTaskRegistry:
        def register(self, *args, **kwargs):
            pass
    tasks = _NoOpTaskRegistry()
from dateutil.relativedelta import relativedelta
from django.db import connection


class AsyncTruncarEventNotification(AsyncGestionOperationalError):
    name = 'AsyncTruncarEventNotification'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        cursor = connection.cursor()
        if cursor.db.settings_dict.get('ENGINE') == 'django.db.backends.postgresql_psycopg2':
            count_juego = EventNotification.objects.all().count()
            cursor.execute('TRUNCATE TABLE "{0}"'.format(EventNotification._meta.db_table))
            cursor.execute("SELECT setval('admin_juego_eventnotification_id_seq', 1)")

            count_cadena = EventNotificationCadena.objects.all().count()
            cursor.execute('TRUNCATE TABLE "{0}"'.format(EventNotificationCadena._meta.db_table))
            cursor.execute("SELECT setval('admin_comercializacion_eventnotificationcadena_id_seq', 1)")

            return 'juego: {0}, cadena: {1}'.format(count_juego, count_cadena)
        else:
            return 'Analizar la compatibilidad del manejador de base de datos'


tasks.register(AsyncTruncarEventNotification)


class AsyncCreateAutomaticTemporadas(AsyncGestionOperationalError):
    name = 'AsyncCreateAutomaticTemporadas'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        today = date.today()
        year = today.year

        status_habilitado = Status.get_status_by_codename('status_habilitado')
        count = 0
        for last in Fechas.objects.filter(fechafin=today):
            nombre = 'Temporada {0}'.format(year + 1)
            temp = Fechas.objects.filter(nombre=nombre, torneo_id=last.torneo.id)
            if not temp.exists():
                count += 1
                Fechas.objects.create(
                    nombre=nombre,
                    fechaini=last.fechaini + relativedelta(years=1),
                    fechafin=last.fechafin + relativedelta(years=1),
                    status=status_habilitado,
                    torneo_id=last.torneo.id
                )

        return '{0} temporadas creadas'.format(count)


tasks.register(AsyncCreateAutomaticTemporadas)
