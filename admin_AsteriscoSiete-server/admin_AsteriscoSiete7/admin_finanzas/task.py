# -*- coding: utf-8 -*-

from datetime import timedelta
from decimal import Decimal

from admin_apuestas.models import Tickets
from admin_asterisco7.settings import FORMAT_STR_DATE_REPORTS, REDIS_DB
from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Operadoras
from admin_datamart.task import (
    AsyncCheckComer_tickets, AsyncGestion_add_MontoPremio, AsyncGestion_add_ticket_apuesta,
    AsyncGestion_rest_MontoPremio, AsyncProcesarSaldos,
)
from admin_finanzas.models import Comercializadora, Dia, EstatoCuenta, Movimiento
from admin_juego.models import Sorteo, Fechas, apuesta, Fechas
from admin_lib.util_task import AsyncGestionOperationalError
from admin_resultados.algorithm_manual_process import AlgorithmsManual
from admin_status.models import Status
try:
    from celery.registry import tasks
except ImportError:
    tasks = {}
from django.db.models import Sum
from django.utils.timezone import now


class AsyncImportSaldosAutomatic(AsyncGestionOperationalError):
    name = 'AsyncImportSaldosAutomatic'
    queue = 'reportes_async'

    def run_try(self, *args, **kwargs):
        mensaje = ['Importando saldos', ]

        comer = Comercializadora.objects.get(
            pk=kwargs.get('id_comer')
        )
        trabajo = comer.get_dia_trabajo()
        if trabajo:
            fecha_trabajo = trabajo.dia.fecha.strftime(FORMAT_STR_DATE_REPORTS)

            if kwargs.get('fecha_ini') != fecha_trabajo:
                mensaje.append('Fecha invalidad')
                mensaje.append(fecha_trabajo)
            else:
                mensaje.append(
                    comer.process_import(
                        force_anulado=kwargs.get('force_anulado')
                    )
                )

                if kwargs.get('fecha_fin'):
                    fecha_fin = now().strptime(
                        kwargs.get('fecha_fin'), FORMAT_STR_DATE_REPORTS
                    ).date()
                    dia_trabajo = comer.get_dia_trabajo()
                    if dia_trabajo.dia.fecha >= fecha_fin:
                        mensaje.append('Fecha limite alcanzada')
                    else:
                        if kwargs.get('close_day'):
                            task = AsyncCloseDayAutomatic()
                            task.run(
                                *args,
                                **kwargs
                            )
                            mensaje.append('Cerrando día.')
        else:
            mensaje.append('Fecha de trabajo invalidad')

        return mensaje


tasks.register(AsyncImportSaldosAutomatic)


class AsyncCloseDayAutomatic(AsyncGestionOperationalError):
    name = 'AsyncCloseDayAutomatic'
    queue = 'reportes_async'

    def run_try(self, *args, **kwargs):
        mensaje = ['Cerrar dia', ]

        comer = Comercializadora.objects.get(
            pk=kwargs.get('id_comer')
        )

        trabajo = comer.get_dia_trabajo()
        if trabajo:
            fecha_trabajo = trabajo.dia.fecha.strftime(FORMAT_STR_DATE_REPORTS)

            if kwargs.get('fecha_ini') != fecha_trabajo:
                mensaje.append('Fecha invalidad')
                mensaje.append(fecha_trabajo)
            else:
                mensaje.append(
                    comer.process_close_day()
                )
                if kwargs.get('fecha_fin'):
                    fecha_fin = now().strptime(
                        kwargs.get('fecha_fin'), FORMAT_STR_DATE_REPORTS
                    ).date()
                    dia_trabajo = comer.get_dia_trabajo()
                    if dia_trabajo.dia.fecha <= fecha_fin:
                        kwargs['fecha_ini'] = dia_trabajo.dia \
                            .fecha.strftime(FORMAT_STR_DATE_REPORTS)
                        AsyncImportSaldosAutomatic.delay(
                            *args,
                            **kwargs
                        )
                        mensaje.append('Importando saldos')
                        mensaje.append(kwargs['fecha_ini'])
        else:
            mensaje.append('Fecha de trabajo invalidad')
        return mensaje


tasks.register(AsyncCloseDayAutomatic)


class AsyncCloseDayAutomaticGeneral(AsyncGestionOperationalError):
    name = 'AsyncCloseDayAutomaticGeneral'
    queue = 'reportes_async'

    def run_try(self, *args, **kwargs):
        mensaje = []

        if kwargs.get('distribute'):
            """
            Siempre que esta tarea se invoca con el crontab, llega con una comercializadora activa,
            y distribute activo, por eso se ejecutan las otras en paralelo.
            """
            if kwargs.get('tipo') != 'Operadoras':
                AsyncCloseDayAutomaticGeneral.delay(
                    *(),
                    **{
                        'distribute': False,
                        'tipo': 'Operadoras'
                    }
                )
            if kwargs.get('tipo') != 'Bloques':
                AsyncCloseDayAutomaticGeneral.delay(
                    *(),
                    **{
                        'distribute': False,
                        'tipo': 'Bloques'
                    }
                )
            if kwargs.get('tipo') != 'Bancas':
                AsyncCloseDayAutomaticGeneral.delay(
                    *(),
                    **{
                        'distribute': False,
                        'tipo': 'Bancas'
                    }
                )
            if kwargs.get('tipo') != 'Distribuidores':
                AsyncCloseDayAutomaticGeneral.delay(
                    *(),
                    **{
                        'distribute': False,
                        'tipo': 'Distribuidores'
                    }
                )
            if kwargs.get('tipo') != 'Agencias':
                AsyncCloseDayAutomaticGeneral.delay(
                    *(),
                    **{
                        'distribute': False,
                        'tipo': 'Agencias'
                    }
                )

        dicc = {
            'Agencias': Agencias,
            'Distribuidores': Distribuidores,
            'Bancas': Bancas,
            'Bloques': Bloques,
            'Operadoras': Operadoras,
        }

        objeto = dicc[kwargs.get('tipo')]
        querryset = objeto.objects.filter(
            resumen_automatic=True
        ).only('pk')
        i = 0
        for cadena in querryset:
            comer = cadena.get_comercializadora()
            if comer.process_close_day(import_add=True):
                i += 1
        mensaje.append(
            '{0} de {1} - {2}'.format(
                i,
                querryset.count(),
                objeto.prefix_filter_plural
            )
        )
        return mensaje


tasks.register(AsyncCloseDayAutomaticGeneral)


class AsyncCuadreParleyAutomaticGeneral(AsyncGestionOperationalError):
    name = 'AsyncCuadreParleyAutomaticGeneral'
    queue = 'reportes_async'

    def run_try(self, *args, **kwargs):
        mensaje = []

        comercializadoras = Comercializadora.objects.filter(
            operadora_id__isnull=True,
            taquilla_id__isnull=True,
        ).only('pk')

        count = comercializadoras.count()
        fecha = now() - timedelta(days=1)
        fecha = fecha.strftime(FORMAT_STR_DATE_REPORTS)
        for comercializadora in comercializadoras:
            tarea = AsyncProcesarSaldos()
            tarea.run(
                *(),
                **{
                    'comercializadora': comercializadora.pk,
                    'fecha': fecha,
                }
            )
        mensaje.append(
            'el {0} {1} comercializadoras'.format(
                fecha,
                count
            )
        )
        return mensaje


tasks.register(AsyncCuadreParleyAutomaticGeneral)


class AsyncSuspenderEncuentro(AsyncGestionOperationalError):
    name = 'AsyncSuspenderEncuentro'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        encuentro = Sorteo.objects.get(pk=kwargs.get('encuentro'))
        jugadas_count = 0
        for encuentrosmodalidades in encuentro.encuentrosmodalidades_set.only('pk').all():
            jugadas = encuentrosmodalidades.jugadas_set.only('pk').all()
            jugadas_count += jugadas.count()
            for jugada in jugadas:
                tarea = AsyncGestionDeTicketsPorJugada()
                tarea.delay(
                    *(),
                    **{
                        'jugada': jugada.pk,
                        'force_anulado': True,
                        'status': 'status_anulado',
                        'filter_cadena': kwargs.get('filter_cadena'),
                    }
                )
        return '{0} apuesta'.format(jugadas_count)


tasks.register(AsyncSuspenderEncuentro)


class AsyncSuspenderJornada(AsyncGestionOperationalError):
    name = 'AsyncSuspenderJornada'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        jornada = Fechas.objects.get(pk=kwargs.get('jornada'))
        encuentros = jornada.encuentros_set.all()
        for encuentro in encuentros:
            if encuentro.horacierre <= now():
                suspender_encuentro = AsyncSuspenderEncuentro()
                suspender_encuentro.delay(*(), **{'encuentro': encuentro.pk, })
        return '{0} encuentros'.format(encuentros.count())


tasks.register(AsyncSuspenderJornada)


class AsyncSuspenderTemporada(AsyncGestionOperationalError):
    name = 'AsyncSuspenderTemporada'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        temporada = Fechas.objects.get(pk=kwargs.get('temporada'))
        jornadas = temporada.jornadas_set.all()
        for jornada in jornadas:
            if jornada.fechafin <= now().date():
                suspender_jornada = AsyncSuspenderJornada()
                suspender_jornada.delay(*(), **{'jornada': jornada.pk, })
        return '{0} Fechas'.format(jornadas.count())


tasks.register(AsyncSuspenderTemporada)


class AsyncGenerarEstadosDeCuenta(AsyncGestionOperationalError):
    name = 'AsyncGenerarEstadosDeCuenta'
    queue = 'default'

    def run_try(self, *args, **kwargs):
        mensaje = []
        comercializadora = Comercializadora.objects.get(pk=kwargs.get('comercializadora'))
        dia_old = now().strptime(kwargs.get('dia_old'), FORMAT_STR_DATE_REPORTS)
        dia_new = Dia.objects.get_or_create(fecha=kwargs.get('dia_new'))[0]
        mensaje.append('Comercializadora {0}'.format(comercializadora))
        for cuenta in comercializadora.cuenta_set.all():
            movimientos = Movimiento.objects.filter(
                cuenta=cuenta,
                dia__fecha__year=dia_old.strftime('%Y'),
                dia__fecha__month=dia_old.strftime('%m')
            )
            saldo = movimientos.aggregate(Sum('monto'))['monto__sum']
            saldo = Decimal() if saldo is None else saldo
            try:
                fecha_old = dia_old - timedelta(days=1)
                saldo += EstatoCuenta.objects.get(
                    cuenta=cuenta,
                    dia__fecha__year=fecha_old.strftime('%Y'),
                    dia__fecha__month=fecha_old.strftime('%m')
                ).saldo
            except EstatoCuenta.DoesNotExist:
                pass
            generado = EstatoCuenta.objects.get_or_create(
                dia=dia_new,
                cuenta=cuenta
            )[0]
            generado.saldo = saldo
            generado.save(update_fields=['saldo'])
            mensaje.append(cuenta.pk)
        return mensaje


tasks.register(AsyncGenerarEstadosDeCuenta)


# Codenames de los estatus que ya no deben ser procesados
status_no_process = ['status_pagado', 'status_anulado', 'status_ganado_frio', 'status_anulado_automatico']


class AsyncGestionDeTicketsPorJugada(AsyncGestionOperationalError):
    name = 'AsyncGestionDeTicketsPorJugada'
    queue = 'tickets_items'

    def run_try(self, *args, **kwargs):
        self.mensaje = []

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho 2 es por taquilla
        key = '{0}_{1}'.format('jugadas', kwargs.get('jugada'))
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================

        jugada = apuesta.objects.get(pk=kwargs.get('jugada'))
        encuentro = jugada.encuentros_modalidad.encuentro

        if kwargs.get('filter_cadena'):
            items = jugada.ticketsdetail_set.filter(
                **kwargs.get('filter_cadena')
            )
        else:
            items = jugada.ticketsdetail_set.all()

        status_ganado = Status.get_status_by_codename(codename='status_procesandoganador')
        status_perdido = Status.get_status_by_codename(codename='status_procesadoperdedor')
        status_anulado = Status.get_status_by_codename(codename='status_anulado')

        # Error humano de todos los tickets vendidos con la hora de encuentro incorrecta
        items_error_humano = items.filter(
            ticket__fecha__gt=encuentro.horacierre
        )

        # Tickest validos
        items_validos = items.filter(
            ticket__fecha__lte=encuentro.horacierre
        )

        for obj in items_error_humano:
            if obj.ticket.status.codename not in status_no_process:
                ticket_detalle_status = obj.get_status()
                status_result = status_anulado
                if ticket_detalle_status.pk != status_result.pk:
                    obj.set_new_status(status_result)
                    recalculo = True
                    tarea = AsyncProcesarTicket()
                    tarea.delay(
                        *(),
                        **{
                            'ticket': obj.ticket.pk,
                            'recalculo': recalculo
                        }
                    )

        for obj in items_validos:
            if obj.ticket.status.codename not in status_no_process:
                ticket_detalle_status = obj.get_status()
                status_result_key = kwargs.get('status')
                # se agrego una variable de anulado forzoso, usada solo cuando se anula el encuentro
                if kwargs.get('force_anulado'):
                    pass
                else:
                    if obj.jugada.condicion.etiqueta_ref or obj.jugada.condicion.modalidad.etiqueta_ref:
                        if obj.modalidad_ref is not None:
                            if obj.modalidad_ref != obj.jugada.encuentros_modalidad.etiqueta_ref:
                                process = AlgorithmsManual(ticket_detail=obj)
                                status_result_key = process.manual()
                        if obj.condicion_ref is not None:
                            if obj.condicion_ref != obj.jugada.valor_etq_ref:
                                process = AlgorithmsManual(ticket_detail=obj)
                                status_result_key = process.manual()

                if status_result_key == 'status_ganado':
                    status_result = status_ganado
                elif status_result_key == 'status_perdido':
                    status_result = status_perdido
                elif status_result_key == 'status_anulado':
                    status_result = status_anulado

                if ticket_detalle_status.pk != status_result.pk:
                    obj.set_new_status(status_result)
                    recalculo = False
                    if (status_result.codename == 'status_anulado' or
                            ticket_detalle_status.codename == 'status_anulado'):
                        recalculo = True
                        # obj.ticket.get_calcular_premio( recalculo = True )
                        # El recalculo se deja para hacerce en la tarea espeficica por ticket,
                        # ya que si era ganador y va a ganador otra ves con
                        # se debe quitar el monto de premio anterior completo
                        # y luego añadir el nuevo o viceversa.
                    tarea = AsyncProcesarTicket()
                    # esta tarea si que se ejecute en segundo plano
                    tarea.delay(
                        *(),
                        **{
                            'ticket': obj.ticket.pk,
                            'recalculo': recalculo
                        }
                    )

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================

        self.mensaje.append('{0} apuestas'.format(items.count()))
        self.mensaje.append('{0} apuestas validad'.format(items_validos.count()))
        self.mensaje.append('{0} apuestas invalidas'.format(items_error_humano.count()))
        return self.mensaje


tasks.register(AsyncGestionDeTicketsPorJugada)


class AsyncProcesarTicket(AsyncGestionOperationalError):
    name = 'AsyncProcesarTicket'
    queue = 'tickets'

    def check_tickets_finish(self):
        task = AsyncCheckComer_tickets()
        task.run(
            *(),
            **{
                'id_comer': self.ticket.user.taquilla.agencia.get_comercializadora().pk,
                'tipo': self.ticket.user.taquilla.agencia.prefix_filter,
                'fecha': self.ticket.fecha.strftime(FORMAT_STR_DATE_REPORTS),
                'start_delay': True,
            }
        )

    def add_tasks_pending(self, task):
        self.mensaje.append('tasks exe: {0}'.format(task.task_id))

    def process_tiket(self, kwargs):
        estatus_old = self.ticket.get_status()
        self.mensaje.append('Old Status: {0}'.format(estatus_old))
        recalculo = kwargs.get('recalculo')

        if estatus_old.codename == 'status_ticketpendiente':
            hecho = AsyncGestion_add_ticket_apuesta()
            hecho.delay(*(), **{'ticket': self.ticket.pk, })
            self.mensaje.append('Proceso venta')
            self.ticket.set_new_status(Status.get_status_by_codename(codename='status_procesandose'))

        items = self.ticket.ticketsdetail_set.all()
        total_items = items.count()
        total_items_perdidos = items.filter(
            ticketsdetailstatus__enddate=None,
            ticketsdetailstatus__status__codename='status_procesadoperdedor'
        ).count()
        total_items_ganados = items.filter(
            ticketsdetailstatus__enddate=None,
            ticketsdetailstatus__status__codename='status_procesandoganador'
        ).count()
        total_items_anulados = items.filter(
            ticketsdetailstatus__enddate=None,
            ticketsdetailstatus__status__codename='status_anulado'
        ).count()

        process_tickets_finish = False

        if total_items_perdidos > 0:

            if estatus_old.codename != 'status_procesadoperdedor':
                self.ticket.set_new_status(
                    Status.get_status_by_codename(codename='status_procesadoperdedor')
                )
                process_tickets_finish = True

            if estatus_old.codename == 'status_procesandoganador':
                hecho = AsyncGestion_rest_MontoPremio()
                self.add_tasks_pending(
                    task=hecho.delay(
                        *(),
                        **{
                            'ticket': self.ticket.pk,
                            'monto_premio': float(self.ticket.monto_premio),
                            'check_finish': True,
                        }
                    ),
                )
                self.mensaje.append('Resto premio')

                # coloco la bandera en False, ya que la tarea asincrona procesa
                # internamente si los tickets se procesaron todos
                process_tickets_finish = False

        else:

            estatus_new = None

            if (total_items - total_items_anulados) == (total_items_perdidos + total_items_ganados):
                if total_items_ganados == (total_items - total_items_anulados):
                    estatus_new = Status.get_status_by_codename(codename='status_procesandoganador')
                else:
                    # aqui falta verificar si es quiniela para ver q
                    # porcetaje de aciertos hay y decir si gano o no
                    # estatus_new =  Status.get_status_by_codename(codename='status_procesadoperdedor')
                    pass

                if estatus_old.pk != estatus_new.pk:
                    # si el ticket cambio de estatus
                    self.ticket.set_new_status(estatus_new)
                    if (estatus_old.codename == 'status_procesandoganador' and
                            estatus_new.codename == 'status_procesadoperdedor'):
                        hecho = AsyncGestion_rest_MontoPremio()
                        self.add_tasks_pending(
                            task=hecho.delay(
                                *(),
                                **{
                                    'ticket': self.ticket.pk,
                                    'monto_premio': float(self.ticket.monto_premio),
                                    'check_finish': True,
                                }
                            ),
                        )
                        self.mensaje.append('Resto premio')
                    elif estatus_new.codename == 'status_procesandoganador':

                        if recalculo:
                            # ponemos bandera en false para q no anule mas abajo
                            recalculo = False
                            # verificamos si hay un recalculo para poner el nuevo
                            # monto de premio, y agregar el monto de premio correcto
                            self.mensaje.append(
                                'Old premio: {0}'.format(round(self.ticket.monto_premio, 2))
                            )
                            self.ticket.get_calcular_premio(recalculo=True)
                            self.mensaje.append(
                                'New premio: {0}'.format(round(self.ticket.monto_premio, 2))
                            )

                        hecho = AsyncGestion_add_MontoPremio()
                        self.add_tasks_pending(
                            task=hecho.delay(
                                *(),
                                **{
                                    'ticket': self.ticket.pk,
                                    'monto_premio': float(self.ticket.monto_premio),
                                    'check_finish': True,
                                }
                            ),
                        )
                        self.mensaje.append('Sumo premio')
                else:
                    if (estatus_old.codename == 'status_procesandoganador' and
                            estatus_new.codename == 'status_procesandoganador'):
                        # Esto ocurre cuando un ticket es ganador y se anulan o se
                        # desanulan jugadas,

                        # Verificamos si hay recalculo, en caso de haberlo
                        # se debe restart el monto de premio anterior,
                        # y sumar el nuevo monto de premio.
                        if recalculo:
                            # ponemos bandera en false para q no anule mas abajo
                            recalculo = False
                            # Restamos el anterior monto de premio pero en primer plano,
                            # ya que si se lo dejamos a las tareas, puede q los montos
                            # de premios varien en en los milesegundos q se tardan en
                            # procesarse
                            self.mensaje.append(
                                'Old premio: {0}'.format(round(self.ticket.monto_premio, 2))
                            )
                            hecho = AsyncGestion_rest_MontoPremio()
                            self.add_tasks_pending(
                                task=hecho.delay(
                                    *(),
                                    **{
                                        'ticket': self.ticket.pk,
                                        'monto_premio': float(self.ticket.monto_premio),
                                    }
                                ),
                            )
                            self.mensaje.append('Resto premio')

                            self.ticket.get_calcular_premio(recalculo=True)
                            self.mensaje.append(
                                'New premio: {0}'.format(round(self.ticket.monto_premio, 2))
                            )
                            hecho = AsyncGestion_add_MontoPremio()
                            self.add_tasks_pending(
                                task=hecho.delay(
                                    *(),
                                    **{
                                        'ticket': self.ticket.pk,
                                        'monto_premio': float(self.ticket.monto_premio),
                                        'check_finish': True,
                                    }
                                ),
                            )
                            self.mensaje.append('Sumo premio')
                            # ya luego se puede agregar el nuevo monto de premio
                            # en segundo plano, debido a que el premio anterior
                            # ya fue removido directamente

            if estatus_old.codename == 'status_procesadoperdedor' and estatus_new is None:
                # si el ticke era perdedor lo pone procesandose,
                # en caso de que aun le falten cosas por aplicar
                self.ticket.set_new_status(Status.get_status_by_codename(codename='status_procesandose'))

        if recalculo:
            # esta bandera cuando llega activa, enrealidad no hace diferencias
            # de si fue ganador o perdedor, el estatus anterior se mantiene,
            # pero si antes era ganador y ahora es perdedor, y luego
            # se anulo una jugada, es necesario siempre estar recalculando
            # el monto de premio, por si fue q colocaron mal resultados,
            # y luego pasa a ganador; entonces su monto de premio
            # siempre q sea necesario se recalculara para mantener coherencias
            # en los datamart
            self.mensaje.append('Old premio: {0}'.format(round(self.ticket.monto_premio, 2)))
            self.ticket.get_calcular_premio(recalculo=True)
            self.mensaje.append('New premio: {0}'.format(round(self.ticket.monto_premio, 2)))

        if process_tickets_finish:
            self.check_tickets_finish()

        self.mensaje.append('New Status: {0}'.format(self.ticket.get_status()))

    def run_try(self, *args, **kwargs):
        self.mensaje = []

        # ================================================================================================
        # Obtenemos y activamos el candado
        # Sincronizamos por el id de taquilla, ya que el hecho en linea y hecho 2 es por taquilla
        key = '{0}_{1}'.format('tickets', kwargs.get('ticket'))
        self.padlock = REDIS_DB.lock(key)
        self.set_acquire()
        # ================================================================================================

        self.ticket = Tickets.objects.get(pk=kwargs.get('ticket'))
        if self.ticket.status.codename not in status_no_process:
            self.process_tiket(kwargs)
        else:
            self.mensaje.append('Ticket no procesado, Status: {0}'.format(self.ticket.get_status()))

        # ================================================================================================
        # Quitamos el candado
        self.set_release()
        # ================================================================================================
        return self.mensaje


tasks.register(AsyncProcesarTicket)
