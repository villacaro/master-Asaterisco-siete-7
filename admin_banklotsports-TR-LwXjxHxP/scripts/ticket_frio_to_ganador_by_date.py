# -*- coding: utf-8 -*-

from admin_apuestas.models import Tickets
from admin_lib.util_fechas import hora_23, hora_cero
from admin_status.models import Status


def run(*args):
    """
        Uso:
         >> python manage.py runscript ticket_frio_to_ganador_by_date --script-args=2016-03-20 2016-03-20
    """
    if len(args) != 2:
        print('Faltan argumentos')
        return
    print('Iniciando proceso')

    tickets_filter = Tickets.objects.filter(
        fecha__range=(args[0] + hora_cero, args[1] + hora_23),
        status__codename='status_ganado_frio'
    )
    new_status = Status.objects.get(codename='status_procesandoganador')
    total = tickets_filter.count()
    i = 1
    for ticket in tickets_filter:
        print('Procesando {0} de {1}'.format(i, total))
        ticket.set_new_status(new_status)
        i += 1

    print('Proceso terminado...')
