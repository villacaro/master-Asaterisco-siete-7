from django.core.management.base import BaseCommand
from admin_status.models import Status


INITIAL_STATUSES = [
    # content_type 0 - Actualizacion
    {'name': 'Activo',             'codename': 'actualizacion_activo',     'content_type': 0, 'order': 1},
    {'name': 'Inactivo',           'codename': 'actualizacion_inactivo',   'content_type': 0, 'order': 2},
    # content_type 1 - Usuarios
    {'name': 'Activo',             'codename': 'usuario_activo',           'content_type': 1, 'order': 1},
    {'name': 'Inactivo',           'codename': 'usuario_inactivo',         'content_type': 1, 'order': 2},
    {'name': 'Suspendido',         'codename': 'usuario_suspendido',       'content_type': 1, 'order': 3},
    {'name': 'Bloqueado',          'codename': 'usuario_bloqueado',        'content_type': 1, 'order': 4},
    {'name': 'Nuevo',              'codename': 'status_nuevo',             'content_type': 1, 'order': 5},
    # content_type 2 - Encuentros / Sorteos
    {'name': 'Habilitado',         'codename': 'status_habilitado',        'content_type': 2, 'order': 1},
    {'name': 'Pendiente',          'codename': 'status_pendiente',         'content_type': 2, 'order': 2},
    {'name': 'Reanudado',          'codename': 'status_reanudado',         'content_type': 2, 'order': 3},
    {'name': 'Eliminado',          'codename': 'status_eliminado',         'content_type': 2, 'order': 4},
    {'name': 'Eliminado frio',     'codename': 'status_eliminado_frio',    'content_type': 2, 'order': 5},
    {'name': 'Procesandose',       'codename': 'status_procesandose',      'content_type': 2, 'order': 6},
    {'name': 'Procesado',          'codename': 'status_procesado',         'content_type': 2, 'order': 7},
    {'name': 'Activo',             'codename': 'encuentro_activo',         'content_type': 2, 'order': 8},
    {'name': 'Inactivo',           'codename': 'encuentro_inactivo',       'content_type': 2, 'order': 9},
    {'name': 'Cerrado',            'codename': 'encuentro_cerrado',        'content_type': 2, 'order': 10},
    {'name': 'Suspendido',         'codename': 'encuentro_suspendido',     'content_type': 2, 'order': 11},
    # content_type 3 - Taquillas / Operadoras
    {'name': 'Activo',             'codename': 'taquilla_activo',          'content_type': 3, 'order': 1},
    {'name': 'Inactivo',           'codename': 'taquilla_inactivo',        'content_type': 3, 'order': 2},
    {'name': 'Suspendido',         'codename': 'taquilla_suspendido',      'content_type': 3, 'order': 3},
    {'name': 'Cerrado',            'codename': 'taquilla_cerrado',         'content_type': 3, 'order': 4},
    # content_type 4 - Jugadas
    {'name': 'Activo',             'codename': 'status_activo',            'content_type': 4, 'order': 1},
    {'name': 'Activo sin venta',   'codename': 'status_activo_sin_venta',  'content_type': 4, 'order': 2},
    {'name': 'Bloqueado',          'codename': 'status_bloqueado',         'content_type': 4, 'order': 3},
    {'name': 'Procesando ganador', 'codename': 'status_procesandoganador', 'content_type': 4, 'order': 4},
    {'name': 'Perdedor',           'codename': 'status_perdedor',          'content_type': 4, 'order': 5},
    {'name': 'Activo',             'codename': 'jugada_activo',            'content_type': 4, 'order': 6},
    {'name': 'Anulado',            'codename': 'jugada_anulado',           'content_type': 4, 'order': 7},
    {'name': 'Ganado',             'codename': 'jugada_ganado',            'content_type': 4, 'order': 8},
    {'name': 'Perdido',            'codename': 'jugada_perdido',           'content_type': 4, 'order': 9},
    # content_type 5 - Encuentro resultado
    {'name': 'Pendiente',          'codename': 'resultado_pendiente',      'content_type': 5, 'order': 1},
    {'name': 'Procesado',          'codename': 'resultado_procesado',      'content_type': 5, 'order': 2},
    {'name': 'Anulado',            'codename': 'resultado_anulado',        'content_type': 5, 'order': 3},
    # content_type 6 - Venta de tickets
    {'name': 'Activo',             'codename': 'venta_activo',             'content_type': 6, 'order': 1},
    {'name': 'Anulado',            'codename': 'venta_anulado',            'content_type': 6, 'order': 2},
    {'name': 'Pagado',             'codename': 'venta_pagado',             'content_type': 6, 'order': 3},
    # content_type 7 - General
    {'name': 'Activo',             'codename': 'general_activo',           'content_type': 7, 'order': 1},
    {'name': 'Inactivo',           'codename': 'general_inactivo',         'content_type': 7, 'order': 2},
    # content_type 8 - Tickets
    {'name': 'Emitido',            'codename': 'ticket_emitido',           'content_type': 8, 'order': 1},
    {'name': 'Ganador',            'codename': 'ticket_ganador',           'content_type': 8, 'order': 2},
    {'name': 'Anulado',            'codename': 'ticket_anulado',           'content_type': 8, 'order': 3},
    {'name': 'Cobrado',            'codename': 'ticket_cobrado',           'content_type': 8, 'order': 4},
]


class Command(BaseCommand):
    help = 'Crea los Status iniciales requeridos por el sistema si no existen'

    def handle(self, *args, **options):
        created = 0
        for data in INITIAL_STATUSES:
            _, c = Status.objects.get_or_create(
                codename=data['codename'],
                defaults=data,
            )
            if c:
                created += 1

        total = Status.objects.count()
        self.stdout.write(
            self.style.SUCCESS(
                f'seed_status: {created} creados, {total} total en DB'
            )
        )
