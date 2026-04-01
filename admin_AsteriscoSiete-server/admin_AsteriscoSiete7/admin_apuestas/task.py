# -*- coding: utf-8 -*-

from datetime import timedelta
from decimal import Decimal

from admin_apuestas.models import Tickets
# from admin_asterisco7.settings import FORMAT_STR_DATE_REPORTS
from admin_comercializacion.models import Operadoras
from admin_datamart.models import Hecho5_ComisionesCadena
from admin_datamart.task import (
    AsyncGestion_add_MontoPremio, AsyncGestion_add_ticket_apuesta, AsyncGestion_add_ticket_apuesta_En_Linea,
    AsyncGestion_rest_MontoPremio, AsyncGestion_rest_ticket_apuesta, AsyncGestion_rest_ticket_apuesta_En_Linea,
)
from admin_juego.models import Sorteo, SistemaJuego
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_task import AsyncGestionOperationalError
from admin_resultados.models import Anotaciones, AnotacionesDetail, Resultados, ResultadosRestric
from admin_resultados.task import Algorithms
from admin_status.models import Status
try:
    from celery.registry import tasks
except ImportError:
    tasks = {}
from django.core.mail import mail_admins
from django.db.models import Sum
from django.utils.timezone import now


class AsyncProcesarTicketsGanadosNoCobrados(AsyncGestionOperationalError):
    name = 'AsyncProcesarTicketsGanadosNoCobrados'
    queue = 'tickets'

    def run_try(self, *args, **kwargs):
        mensaje = []
        hoy = now()
        fecha = strFecha(hoy - timedelta(days=7))
        fecha_ini = fecha.getFecha() + hora_cero
        fecha = strFecha(hoy - timedelta(days=6))
        fecha_fin = fecha.getFecha() + hora_23
        tickets = Tickets.objects.filter(
            updated_at__range=(fecha_ini, fecha_fin),
            status__codename='status_procesandoganador'
        ).distinct('pk')

        status_new = Status.get_status_by_codename(
            codename='status_ganado_frio'
        )
        mensaje.append('Procesados: {0}'.format(tickets.count()))
        for ticket in tickets:
            mensaje.append(ticket.pk)
            ticket.set_new_status(status_new)
        return mensaje


tasks.register(AsyncProcesarTicketsGanadosNoCobrados)


class AsyncProcesarTicketsGanadosNoConfirmados(AsyncGestionOperationalError):
    name = 'AsyncProcesarTicketsGanadosNoConfirmados'
    queue = 'tickets'

    def run_try(self, *args, **kwargs):
        mensaje = []
        hoy = now()
        fecha = strFecha(hoy - timedelta(days=0))
        fecha_ini = fecha.getFecha() + hora_cero
        fecha_fin = fecha.getFecha() + hora_23
        status_new = Status.get_status_by_codename(
            codename='status_anulado_automatico'
        )
        tickets = Tickets.objects.filter(
            updated_at__range=(fecha_ini, fecha_fin),
            confirmacion=False
        ).exclude(
            status_id=status_new.pk
        ).distinct('pk')

        for ticket in tickets:
            mensaje.append(ticket.pk)
            status_old = ticket.get_new_status()
            ticket.set_new_status(status_new)
            if status_old.status.codename == 'status_ticketpendiente':

                tarea = AsyncGestion_rest_ticket_apuesta_En_Linea()
                tarea.delay(*(), **{'ticket': ticket.pk, })

            elif (status_old.status.codename == 'status_procesandose' or
                    status_old.status.codename == 'status_procesadoperdedor'):

                tarea = AsyncGestion_rest_ticket_apuesta_En_Linea()
                tarea.delay(*(), **{'ticket': ticket.pk, })
                tarea = AsyncGestion_rest_ticket_apuesta()
                tarea.delay(*(), **{'ticket': ticket.pk, })

            elif status_old.status.codename == 'status_procesandoganador':

                tarea = AsyncGestion_rest_ticket_apuesta_En_Linea()
                tarea.delay(*(), **{'ticket': ticket.pk, })
                tarea = AsyncGestion_rest_ticket_apuesta()
                tarea.delay(*(), **{'ticket': ticket.pk, })
                tarea = AsyncGestion_rest_MontoPremio()
                tarea.delay(*(), **{'ticket': ticket.pk, })

        return mensaje


tasks.register(AsyncProcesarTicketsGanadosNoConfirmados)


class AsyncProcesarTickets_Soporte_Manual_anular(AsyncGestionOperationalError):
    name = 'AsyncProcesarTickets_Soporte_Manual_anular'
    queue = 'tickets'

    def run_try(self, *args, **kwargs):
        mensaje = []
        try:
            ticket = Tickets.objects.get(pk=kwargs.get('ticket'))
            status_old = ticket.get_new_status()
            process = 0
            if status_old.status.codename == 'status_ticketpendiente':
                tarea = AsyncGestion_rest_ticket_apuesta_En_Linea()
                tarea.delay(*(), **{'ticket': ticket.pk, })

                ticket.set_new_status(
                    Status.get_status_by_codename(
                        codename='status_anulado'
                    )
                )
                process = 1

            elif (status_old.status.codename == 'status_procesandose' or
                    status_old.status.codename == 'status_procesadoperdedor'):
                tarea = AsyncGestion_rest_ticket_apuesta_En_Linea()
                tarea.delay(*(), **{'ticket': ticket.pk, })
                tarea = AsyncGestion_rest_ticket_apuesta()

                ticket.set_new_status(
                    Status.get_status_by_codename(
                        codename='status_anulado'
                    )
                )
                tarea.delay(
                    *(),
                    **{
                        'ticket': ticket.pk,
                        'check_finish': True,
                    }
                )
                process = 1

            elif status_old.status.codename == 'status_procesandoganador':
                tarea = AsyncGestion_rest_ticket_apuesta_En_Linea()
                tarea.delay(*(), **{'ticket': ticket.pk, })
                tarea = AsyncGestion_rest_ticket_apuesta()
                tarea.delay(*(), **{'ticket': ticket.pk, })
                tarea = AsyncGestion_rest_MontoPremio()

                ticket.set_new_status(
                    Status.get_status_by_codename(
                        codename='status_anulado'
                    )
                )
                tarea.delay(
                    *(),
                    **{
                        'ticket': ticket.pk,
                        'check_finish': True,
                    }
                )
                process = 1

            if process == 1:
                mensaje.append('Ticket anulado exitosamente')
            else:
                mensaje.append(
                    'Error, no se puede anular un ticket {0}'.format(
                        status_old.status
                    )
                )

        except Tickets.DoesNotExist:
            mensaje.append('Error, ticket no encontrado')

        return mensaje


tasks.register(AsyncProcesarTickets_Soporte_Manual_anular)


class AsyncProcesarTickets_Soporte_Manual_desanular(
        AsyncGestionOperationalError):
    name = 'AsyncProcesarTickets_Soporte_Manual_desanular'
    queue = 'tickets'

    def run_try(self, *args, **kwargs):
        mensaje = []
        try:
            ticket = Tickets.objects.get(pk=kwargs.get('ticket'))
            status_old = ticket.get_new_status()
            if status_old.status.codename in ['status_anulado', 'status_anulado_automatico']:
                # sacando ultimo status
                status_ultimo = ticket.ticketstatus_set.all().exclude(
                    enddate=None
                ).order_by('-startdate')[0]
                ticket.set_new_status(status_ultimo.status)
                if status_ultimo.status.codename == 'status_ticketpendiente':

                    tarea = AsyncGestion_add_ticket_apuesta_En_Linea()
                    tarea.delay(*(), **{'ticket': ticket.pk, })

                elif (status_ultimo.status.codename == 'status_procesandose' or
                        status_ultimo.status.codename == 'status_procesadoperdedor'):

                    tarea = AsyncGestion_add_ticket_apuesta_En_Linea()
                    tarea.delay(*(), **{'ticket': ticket.pk, })
                    tarea = AsyncGestion_add_ticket_apuesta()
                    tarea.delay(*(), **{'ticket': ticket.pk, })

                elif status_ultimo.status.codename == 'status_procesandoganador':

                    tarea = AsyncGestion_add_ticket_apuesta_En_Linea()
                    tarea.delay(*(), **{'ticket': ticket.pk, })
                    tarea = AsyncGestion_add_ticket_apuesta()
                    tarea.delay(*(), **{'ticket': ticket.pk, })
                    tarea = AsyncGestion_add_MontoPremio()
                    tarea.delay(*(), **{'ticket': ticket.pk, })

                mensaje.append('Ticket desanulado exitosamente')
            else:
                mensaje.append(
                    'Error, no se puede desanular un ticket no anulado'
                )
        except Tickets.DoesNotExist:
            mensaje.append('Error, ticket no encontrado')
        return mensaje


tasks.register(AsyncProcesarTickets_Soporte_Manual_desanular)


class AsyncProcesarBoot(AsyncGestionOperationalError):
    name = 'AsyncProcesarBoot'
    queue = 'default'
    result_automatic_for_day = 1

    def run_try(self, *args, **kwargs):
        self.mensaje = []
        self.register_comer = []

        self.fecha = kwargs.get('fecha')
        if not self.fecha:
            self.fecha = strFecha(now() - timedelta(days=1)).getFecha()
        self.fecha_ini = self.fecha + hora_cero
        self.fecha_fin = self.fecha + hora_23

        self.tickets = Tickets.objects.filter(
            fecha__range=(self.fecha_ini, self.fecha_fin),
        )
        self.data_choices_venta = []
        for obj in Status.objects.filter(content_type=8).exclude(
                codename__in=['status_anulado', 'status_anulado_automatico']):
            self.data_choices_venta.append(obj.pk)

        self.data_choices_premios = [
            Status.get_status_by_codename(
                codename='status_procesandoganador').pk,
            Status.get_status_by_codename(codename='status_pagado').pk,
            Status.get_status_by_codename(codename='status_ganado_frio').pk,
        ]

        self.ventas = Hecho5_ComisionesCadena.objects.filter(
            tiempo__fecha=self.fecha
        )

        html_message = ''
        self.process_search(Operadoras.objects.all())
        if self.mensaje:
            html_message += '<!DOCTYPE html><head></head><body><div><h4>Fecha: {0}</h4><hr><ul>'.format(
                self.fecha
            )
            for row in self.mensaje:
                html_message += '{0}'.format(row)
            html_message += '</ul></div></body>'
            mail_admins(
                subject='Descuadre en ventas.',
                message='',
                html_message=html_message,
            )

            # reinicia la tarea en 2 horas = 60*60*2
            kwargs['fecha'] = self.fecha
            self.apply_async(countdown=60 * 60 * 2, kwargs=kwargs)

        # apply result automatic
        self.process_result()

        return html_message

    def process_search(self, queryset):
        for object_comer in queryset:
            filtro = {}
            filtro[
                'user__taquilla__agencia' + object_comer.get_prefix_kwargs_by_level_agencia()
            ] = object_comer.pk
            ticket = self.tickets.filter(**filtro)
            qs_premio = ticket.filter(status_id__in=self.data_choices_premios)
            qs_venta = ticket.filter(status_id__in=self.data_choices_venta)
            total_venta_1 = qs_venta.aggregate(Sum('monto'))['monto__sum']
            if not total_venta_1:
                total_venta_1 = Decimal(0)
            else:
                total_venta_1 = round(total_venta_1, 2)
            total_premio_1 = qs_premio.aggregate(Sum('monto_premio'))[
                'monto_premio__sum']
            if not total_premio_1:
                total_premio_1 = Decimal(0)
            else:
                total_premio_1 = round(total_premio_1, 2)

            venta = self.ventas.filter(
                **object_comer.get_kwargs_hijos_dimension_arco_comercializadora()
            )
            montos_sum = venta.aggregate(
                Sum('venta'),
                Sum('premio'),
            )
            total_venta_2 = montos_sum['venta__sum']
            if not total_venta_2:
                total_venta_2 = Decimal(0)
            else:
                total_venta_2 = round(total_venta_2, 2)
            total_premio_2 = montos_sum['premio__sum']
            if not total_premio_2:
                total_premio_2 = Decimal(0)
            else:
                total_premio_2 = round(total_premio_2, 2)

            error = False
            if total_venta_1 != total_venta_2:
                error = True
                self.mensaje.append(
                    '<li><h5>{5}{0} {1}:</h5> presenta un descuadre en venta, tickest = {2}Bs. '
                    'procesadas = {3}Bs. con una diferencia de {4}Bs.</li>'.format(
                        object_comer.prefix_filter.title(),
                        object_comer,
                        total_venta_1,
                        total_venta_2,
                        (total_venta_1 - total_venta_2).copy_abs(),
                        (2 * object_comer.nivel) * ('*')
                    )
                )

            if total_premio_1 != total_premio_2:
                error = True
                self.mensaje.append(
                    '<li><h5>{5}{0} {1}:</h5> presenta un descuadre en premios, tickest = {2}Bs. '
                    'procesadas = {3}Bs. con una diferencia de {4}Bs.</li>'.format(
                        object_comer.prefix_filter.title(),
                        object_comer,
                        total_premio_1,
                        total_premio_2,
                        (total_premio_1 - total_premio_2).copy_abs(),
                        (2 * object_comer.nivel) * ('*')
                    )
                )

            if error:
                self.mensaje.append('</ul><hr><ul>')

            if error and object_comer.prefix_filter in ['bloque', 'banca']:
                if object_comer.is_sistema_juego is False and object_comer.is_resultados is True:
                    # day = now().strptime(self.fecha, FORMAT_STR_DATE_REPORTS)
                    # limit = (day + timedelta(days=self.result_automatic_for_day)).date()
                    # si la fecha es mayor a el limite establecido en `result_automatic_for_day`,
                    # procedo a registrar la comercializadora, y así procesar sus resultados
                    if True:
                        # now().date() > limit:
                        # Codigo comentado lunes 14 de marzo del 2016, procesar todo de una vez
                        self.register_comer.append(object_comer.get_comercializadora())

            if error and object_comer.prefix_filter != 'agencia':
                self.process_search(object_comer.get_offspring())

    def process_result(self):
        for comercializadora in self.register_comer:
            sistema_juego = SistemaJuego.objects.get_sistema_juego_by_comercializadora(
                comercializadora
            )
            sistema_resultados = SistemaJuego.objects.get_sistema_resultados_by_comercializadora(
                comercializadora
            )
            encuentros = Sorteo.objects.filter(
                jornada__sistema=sistema_juego,
                horajuego__range=(self.fecha_ini, self.fecha_fin),
                exists_tickets=True,
            ).only('pk')
            kwargs_async = {}
            object_comer = comercializadora.get_object()
            key = 'ticket__{0}'.format(object_comer.get_prefix_kwargs_by_level_tickets())
            kwargs_async[key] = object_comer.pk

            if object_comer.user_type_codename == 'userprofile_bloque':
                kwargs_async[key.replace('__bloque_id', '__is_resultados')] = False
                kwargs_async[key.replace('__bloque_id', '__is_sistema_juego')] = False

            for encuentro in encuentros:
                if encuentro.get_exists_resultados(sistema_resultados=sistema_resultados, cache=False) is False:
                    # Al no tener resultados, verificamos que el padre si los tenga
                    if encuentro.get_exists_resultados(sistema_resultados=sistema_juego, cache=False) is True:
                        result_empty = Resultados.get_or_create_or_flush(
                            encuentro=encuentro,
                            sistema=sistema_resultados
                        )
                        result_empty.delete()

                        origin_result = Resultados.get_or_create_or_flush(
                            encuentro=encuentro,
                            sistema=sistema_juego
                        )
                        result_pk_old = origin_result.pk
                        origin_result.pk = None
                        origin_result.sistema_id = sistema_resultados.pk
                        origin_result.save()
                        origin_result.created_at = origin_result.created_at - timedelta(seconds=1)
                        origin_result.save(update_fields=['created_at'])
                        for restri in ResultadosRestric.objects.filter(resultado_id=result_pk_old):
                            restri.pk = None
                            restri.resultado_id = origin_result.pk
                            restri.save()
                        for anotacion in Anotaciones.objects.filter(resultado_id=result_pk_old):
                            anotacion_pk_old = anotacion.pk
                            anotacion.pk = None
                            anotacion.resultado_id = origin_result.pk
                            anotacion.save()
                            for detail in AnotacionesDetail.objects.filter(anotacion_id=anotacion_pk_old):
                                detail.pk = None
                                detail.anotacion_id = anotacion.pk
                                detail.save()
                        Algorithms.delay(
                            *(),
                            **{
                                'encuentro': encuentro.pk,
                                'sistema_resultados': sistema_resultados.pk,
                                'filter_cadena': kwargs_async
                            }
                        )


tasks.register(AsyncProcesarBoot)
