# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta

from admin_apuestas.models import Tickets
from admin_comercializacion.models import Porcentajes, Taquillas
from admin_datamart.models import Hecho2_VentasCadenasLinea, Hecho5_ComisionesCadena
from admin_lib.util_fechas import Funs, hora_23, hora_cero, strFecha
from admin_status.models import Status
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import now
from ws_lib.crypto import CryptoRSA
from ws_sportparley.messages import MESSAGES_GLOBAL
from ws_sportparley.settings import CACHES_CONF_TIME


# =============================================================================#
# Funtions utils
# =============================================================================#


def get_expiration_ticket(ticket):
    tiempoexpiracion = ticket.user.taquilla.agencia.get_preference_value_by_codename(
        'preference_time_expire_max'
    )
    fecha_exp = ticket.fecha + timedelta(days=int(float(tiempoexpiracion)))
    return fecha_exp.date()


def get_fecha_aproximada(ticketsdetail):
    """
    Obtiene la fecha del ultimo juego en la lista de logros
    apostados como fecha aproximada
    """
    fecha_maxima = ticketsdetail.order_by(
        '-jugada__encuentros_modalidad__encuentro__horajuego'
    ).values_list(
        'jugada__encuentros_modalidad__encuentro__horajuego',
        flat=True
    )

    if fecha_maxima.exists():
        fecha_maxima = fecha_maxima[0].date()
        return '{0}/{1}/{2}'.format(
            fecha_maxima.day,
            fecha_maxima.month,
            fecha_maxima.year
        )
    else:
        return 'Indeterminada'


def get_commission_percentage(taquilla=None, agencia=None):
    try:
        porcentaje = Porcentajes.objects.get(
            tipo__codename='porcentaje_comision',
            agencia=agencia,
            taquilla=taquilla,
            fecha_fin=None
        ).porcentaje_ganancia
    except Porcentajes.DoesNotExist:
        porcentaje = 0
    return float(porcentaje)


def ticket_is_valid(content, ticket_pk, session, ticket_serial=None):
    user = session.user
    try:
        if ticket_pk:
            if ticket_serial:
                ticket = Tickets.objects.select_related('ticket_type', 'user__taquilla').get(
                    pk=ticket_pk,
                    key=CryptoRSA.decrypt(
                        ticket_serial,
                        session.user.priv_key
                    )
                )
            else:
                ticket = Tickets.objects.select_related('ticket_type', 'user__taquilla').get(
                    pk=ticket_pk
                )
            if ticket.user.taquilla.agencia_id == user.taquilla.agencia_id:
                return ticket
            else:
                content.set_message_entry('error', 1)
                content.set_message_entry('error_message', 'Para gestionar el ticket diríjase ' +
                                          'a la agencia donde efectuo la compra')
        else:
            content.set_message_entry('error', 1)
            content.set_message_entry('error_message', 'Ticket no valido.')

    except Tickets.DoesNotExist:
        content.set_message_entry('error', 1)
        content.set_message_entry('error_message', 'Ticket no encontrado.')


LIMIT_DAYS = 90


def check_date(fecha, content):
    invalid = False

    if isinstance(fecha, str):
        inicio = datetime.strptime(fecha, '%Y-%m-%d').date()
    elif isinstance(fecha, datetime):
        inicio = fecha.date()
    else:
        inicio = fecha

    hoy = now().date()
    diff_days = (hoy - inicio).days

    if diff_days > LIMIT_DAYS:
        invalid = True
        content.set_message_entry(
            'alert_message',
            MESSAGES_GLOBAL['invalid_date']
        )

    return invalid


def check_filter_valid(taquilla, filter_cadena, content):
    """
    Verifica si es filtro esta permitido para la taquilla
    """
    invalid = False
    filters = Taquillas.objects.only('is_taquilla_master')\
        .get(pk=taquilla.id).get_filters_taquilla()
    if not filters.get(filter_cadena):
        invalid = True
        content.set_message_entry(
            'alert_message',
            MESSAGES_GLOBAL['invalid_filter']
        )
    return invalid


# =============================================================================#
# Funtions reports
# =============================================================================#


def analysis_daily(content, session, fecha, filter_cadena):
    analysis_periodic(
        content=content,
        session=session,
        fecha_inicio=fecha,
        fecha_fin=fecha,
        filter_cadena=filter_cadena
    )


def analysis_periodic(content, session, fecha_inicio,
                      fecha_fin, filter_cadena):
    user = session.user

    if check_date(fecha_inicio, content):
        # si la fecha es anterior a el limite retorna
        return

    if check_filter_valid(user.get_taquilla(), filter_cadena, content):
        return

    hecho5 = Hecho5_ComisionesCadena.objects.filter(
        tiempo__fecha__range=(fecha_inicio, fecha_fin)
    )

    hecho2_linea = Hecho2_VentasCadenasLinea.objects.filter(
        tiempo__fecha__range=(fecha_inicio, fecha_fin)
    )

    if filter_cadena == 'filter_taquilla':
        kwargs = user.taquilla.get_kwargs_dimension_comercializadora()
        comision = get_commission_percentage(taquilla=user.taquilla)
    else:  # elif filter_cadena == 'filter_agencia':
        kwargs = user.taquilla.agencia.get_kwargs_dimension_comercializadora()
        comision = get_commission_percentage(agencia=user.taquilla.agencia)

    hecho5 = hecho5.filter(**kwargs)
    hecho2_linea = hecho2_linea.filter(**kwargs)

    hecho2_linea_sum = hecho2_linea.aggregate(
        Sum('count_tickets'),
        Sum('monto_total'),
        Sum('monto_premios')
    )

    inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d')
    fin = datetime.strptime(fecha_fin, '%Y-%m-%d')
    dias = fin.timetuple().tm_yday - inicio.timetuple().tm_yday
    hoy = datetime.strptime(now().strftime('%Y-%m-%d'), '%Y-%m-%d')

    frecuencia = user.taquilla.agencia.get_frecuencia_queda()
    tipo_queda = False

    if fin < hoy:
        if frecuencia == 'frecuencia_semanal':
            if dias == 6:
                week = list(Funs.get_week_by_date(inicio))
                if inicio == week[0]:
                    tipo_queda = True
        elif frecuencia == 'frecuencia_quincenal':
            if dias == 14:
                quincena = list(Funs.get_quincena_by_date(fin))
                if inicio == quincena[0]:
                    tipo_queda = True
        elif frecuencia == 'frecuencia_mensual':
            if dias == (Funs.get_month_days(inicio)[1] - 1):
                if date(inicio.year, inicio.month,
                        inicio.day) == Funs.first_day_of_month(inicio):
                    tipo_queda = True

    queda_ref = 0

    hecho5_sum = hecho5.aggregate(
        Sum('queda_ref')
    )

    queda_ref = float(str('0.00')) if hecho5_sum['queda_ref__sum'] is None \
        else float(round(hecho5_sum['queda_ref__sum'], 2))

    if queda_ref < 0:
        queda_ref = float(0)

    respond = {}

    respond['tickets_vendidos'] = hecho2_linea_sum['count_tickets__sum'] \
        if hecho2_linea_sum['count_tickets__sum'] is not None else 0

    respond['monto_venta'] = round(float(hecho2_linea_sum['monto_total__sum']), 2) \
        if hecho2_linea_sum['monto_total__sum'] is not None else float(0)

    respond['monto_premios'] = round(float(hecho2_linea_sum['monto_premios__sum']), 2) \
        if hecho2_linea_sum['monto_premios__sum'] is not None else float(0)

    # puesto que el hecho 1 es en linea, la comision siempre se recalcula
    respond['comision'] = round(respond['monto_venta'] * comision, 2)

    respond['monto_saldo'] = round(
        respond['monto_venta'] -
        respond['monto_premios'] - respond['comision'],
        2
    )

    respond['tipo_queda'] = 1 if tipo_queda else 0
    respond['queda'] = round(queda_ref, 2)

    content.set_message_entry(
        'resumen',
        respond
    )


def analysis_cash_box(content, session, fecha_inicio,
                      fecha_fin, filter_cadena):
    user = session.user
    if check_date(fecha_inicio, content):
        # si la fecha es anterior a el limite retorna
        return

    if check_filter_valid(user.get_taquilla(), filter_cadena, content):
        return

    hecho2 = Hecho2_VentasCadenasLinea.objects.filter(
        tiempo__fecha__range=(fecha_inicio, fecha_fin)
    )
    hecho5 = Hecho5_ComisionesCadena.objects.filter(
        tiempo__fecha__range=(fecha_inicio, fecha_fin)
    )
    kwargs_2 = {}
    kwargs_5 = {}
    if filter_cadena == 'filter_taquilla':
        kwargs_objects = user.taquilla
    else:  # elif filter_cadena == 'filter_agencia':
        kwargs_objects = user.taquilla.agencia

    kwargs_2 = kwargs_objects.get_kwargs_dimension_comercializadora()
    kwargs_5 = kwargs_objects.get_kwargs_dimension_arco_comercializadora()
    hecho2 = hecho2.filter(**kwargs_2)
    hecho5 = hecho5.filter(**kwargs_5)

    hecho2_sum = hecho2.aggregate(
        Sum('monto_total'),
        Sum('count_tickets'),
        Sum('count_apuestas')
    )
    hecho5_sum = hecho5.aggregate(
        Sum('venta'),
        Sum('premio'),
        Sum('comision'),
        Sum('participacion'),
        Sum('regalia'),
        Sum('queda_ref'),
        Sum('saldo_comer'),
        Sum('saldo_oper')
    )
    data = {}
    data['total_tickets'] = float(hecho2_sum['count_tickets__sum']) \
        if hecho2_sum['count_tickets__sum'] is not None else float()

    data['total_apuestas'] = float(hecho2_sum['count_apuestas__sum']) \
        if hecho2_sum['count_apuestas__sum'] is not None else float()

    venta_procesada = float(hecho5_sum['venta__sum']) \
        if hecho5_sum['venta__sum'] is not None else float()

    venta_en_linea = float(hecho2_sum['monto_total__sum']) \
        if hecho2_sum['monto_total__sum'] is not None else float()

    if venta_procesada != venta_en_linea:
        data['total_ventas'] = venta_en_linea
        if filter_cadena == 'filter_taquilla':
            comision = get_commission_percentage(taquilla=user.taquilla)
        else:  # elif filter_cadena == 'filter_agencia':
            comision = get_commission_percentage(agencia=user.taquilla.agencia)
        data['total_comision'] = round(data['total_ventas'] * comision, 2)
    else:
        data['total_comision'] = float(hecho5_sum['comision__sum']) \
            if hecho5_sum['comision__sum'] is not None else float()

        data['total_ventas'] = venta_procesada

    data['total_premios'] = float(hecho5_sum['premio__sum']) \
        if hecho5_sum['premio__sum'] is not None else float()

    data['total_participacion'] = float(hecho5_sum['participacion__sum']) \
        if hecho5_sum['participacion__sum'] is not None else float()

    data['total_regalia'] = float(hecho5_sum['regalia__sum']) \
        if hecho5_sum['regalia__sum'] is not None else float()

    data['total_saldo_comer'] = float(hecho5_sum['saldo_comer__sum']) \
        if hecho5_sum['saldo_comer__sum'] is not None else float()

    data['total_saldo_oper'] = float(hecho5_sum['saldo_oper__sum']) \
        if hecho5_sum['saldo_oper__sum'] is not None else float()

    queda_ref = float(str('0.00')) if hecho5_sum['queda_ref__sum'] is None \
        else float(round(hecho5_sum['queda_ref__sum'], 2))

    if queda_ref < 0:
        queda_ref = float(0)

    data['queda'] = queda_ref

    content.set_message_entry(
        'cash_box',
        data
    )


def ticket_details(content, ticket_pk, session, original=False):
    ticket = ticket_is_valid(
        content,
        ticket_pk,
        session
    )

    if content.get_message_entry('error') == 1:
        return

    ticket_fecha = strFecha(ticket.fecha)

    respond = {
        'referencia': ticket.pk,
        'fecha': ticket_fecha.getFecha(),
        'hora': ticket_fecha.getHora(),
        'monto': round(float(ticket.monto), 2),
        'tipo': ticket.ticket_type.nombre,
    }

    if original:
        respond['key'] = CryptoRSA.encrypt(
            ticket.key.encode('utf8'),
            session.user.pub_key_client
        )

    status = ticket.get_new_status()
    status_fecha = strFecha(status.updated_at)
    respond['status'] = '{0} {1} {2}'.format(
        status.status.name,
        status_fecha.getFecha(),
        status_fecha.getHora(),
    )

    respond['status_codename'] = '{0}'.format(status.status.codename)

    detalle_ticke = ticket.ticketsdetail_set.all().select_related(
        'jugada__condicion__modalidad',
        'jugada__encuentros_modalidad__modalidad_grupo__grupo',
        'jugada__detalle_encuentro__equipos_temporadas__equipo',
        'jugada__encuentros_modalidad__encuentro__jornada__temporadas__torneo__deporte',
    )
    respond['fecha_aproximada'] = get_fecha_aproximada(
        ticketsdetail=detalle_ticke
    )

    respond['detalle'] = []
    for item in detalle_ticke:
        modalidad_ref = item.jugada.encuentros_modalidad.etiqueta_ref
        condicion_ref = item.jugada.valor_etq_ref
        json_detalle_interno = {
            'monto': round(float(item.monto), 2),
            'logro_apostado': item.logro_apostado,
            'modalidad': item.jugada.condicion.modalidad.modalidad,
            'condicion': item.jugada.condicion.nombre,
            'grupo_modalida': item.jugada.encuentros_modalidad.modalidad_grupo.grupo.nombre,
            'modalidad_ref': '' if not modalidad_ref else modalidad_ref,
            'condicion_ref': '' if not condicion_ref else condicion_ref,
            'pertenece': item.jugada.get_pertenece(),
            'deporte': item.jugada.encuentros_modalidad.encuentro.jornada.temporadas.torneo.deporte.nombre,
            'torneo_temporada_jornada': '{0} - {1} - {2}'.format(
                item.jugada.encuentros_modalidad.encuentro.jornada.temporadas.torneo.nombre,
                item.jugada.encuentros_modalidad.encuentro.jornada.temporadas.nombre,
                item.jugada.encuentros_modalidad.encuentro.jornada.jornada
            ),
            'status': item.status.name,

        }
        encuentro_fecha = strFecha(
            item.jugada.encuentros_modalidad.encuentro.horajuego)
        json_detalle_interno['encuentro'] = {
            'hora': encuentro_fecha.getFecha(),
            'fecha': encuentro_fecha.getHora(),
            'equipos': [
                [
                    {
                        'nombre': equipo.equipos_temporadas.equipo.nombre,
                        'logo': equipo.equipos_temporadas.equipo.get_logo()
                    }
                ]
                for equipo in item.jugada.encuentros_modalidad.encuentro.encuentrosdetail_set.all()
                .select_related('equipos_temporadas__equipo').order_by('-indice')
            ],
        }

        respond['detalle'].append(json_detalle_interno)

    respond['monto_ganancia'] = round(float(ticket.monto_ganancia), 2)
    respond['monto_premio'] = round(float(ticket.monto_premio), 2)
    content.set_message_entry(
        'ticket',
        respond
    )


def ticket_cancel(content, ticket_pk, session, automatic):
    agencia = session.user.taquilla.agencia

    if not automatic and agencia.get_preference_value_by_codename('preference_cancel_ticket') == 0:
        content.set_message_entry('error', 1)
        content.set_message_entry(
            'error_message',
            'No tiene permisos para anular un ticket')
        return
    else:
        ticket = ticket_is_valid(
            content,
            ticket_pk,
            session
        )

        if content.get_message_entry('error') == 1:
            return

        # 5 minutos
        minutes = int(
            (
                (now() - ticket.fecha).total_seconds()
            ) / 60
        )
        if minutes > 5:
            content.set_message_entry('error', 1)
            content.set_message_entry(
                'error_message',
                'Tiempo expirado para anular el ticket')
            return

        estatus_old = ticket.status

        if estatus_old.codename == 'status_ticketpendiente':

            if automatic:
                codename = 'status_anulado_automatico'
            else:
                codename = 'status_anulado'

            ticket.set_new_status(
                Status.get_status_by_codename(
                    codename=codename
                )
            )

            from admin_datamart.task import AsyncGestion_rest_ticket_apuesta_En_Linea
            task = AsyncGestion_rest_ticket_apuesta_En_Linea()
            task.run(*(), **{'ticket': ticket.pk, })

        else:
            content.set_message_entry('error', 1)
            content.set_message_entry('error_message', 'Error, solo se puede anular un ' +
                                      'ticket en estatus pendiente')


def get_last_ticket(content, session):
    user = session.user
    try:
        # Consulta el detalle del último ticket
        ticket = Tickets.objects.filter(
            user_id=user.pk
        ).values_list('pk').latest('fecha')
        # Cuando no sean taquillas sin tickets
        content.set_message_entry(
            'ticket',
            {
                'referencia': ticket[0]
            }
        )
    except Exception:
        # En caso de que la taquilla halla iniciado por primera vez
        content.set_message_entry('init', 1)


def ticket_pay(content, ticket_pk, ticket_serial, session):
    ticket = ticket_is_valid(
        content,
        ticket_pk,
        session,
        ticket_serial
    )
    if content.get_message_entry('error') == 1:
        return
    estatus_old = ticket.status
    if estatus_old.codename == 'status_procesandoganador':
        # Sesion critica, manejar este estatus adentro otra vez
        if get_expiration_ticket(ticket) >= now().date():

            # revalido el estatus del ticke nuevamente
            estatus_old = ticket.status
            if estatus_old.codename == 'status_procesandoganador':
                ticket.set_new_status(
                    Status.get_status_by_codename(
                        codename='status_pagado'
                    )
                )

                ticket_details(
                    content=content,
                    ticket_pk=ticket.pk,
                    session=session,
                )

                fecha_cobro = strFecha(now())

                content.set_message_entry(
                    'fecha_de_cobro',
                    fecha_cobro.getFecha()
                )
                content.set_message_entry(
                    'hora_de_cobro',
                    fecha_cobro.getHora()
                )
            else:
                content.set_message_entry('error', 1)
                content.set_message_entry('error_message', 'Error, verifique el estatus ' +
                                          'del ticket, ya fue pagado o no es un ticket ganador')

        else:
            content.set_message_entry('error', 1)
            content.set_message_entry(
                'error_message', 'Error, el ticket ha expirado...')

    else:
        content.set_message_entry('error', 1)
        content.set_message_entry('error_message', 'Error, verifique el estatus del ticket, ' +
                                  'ya fue pagado o no es un ticket ganador')


def tickets_winners(content, session, fecha, filter_cadena):

    user = session.user

    if check_date(fecha, content):
        # si la fecha es anterior a el limite retorna
        return

    if check_filter_valid(user.get_taquilla(), filter_cadena, content):
        return

    fecha_inicio = fecha + hora_cero
    fecha_fin = fecha + hora_23

    codenames = []
    codenames.append('status_pagado')
    codenames.append('status_procesandoganador')

    if filter_cadena == 'filter_taquilla':
        tickets = Tickets.objects.filter(
            user=user,
            fecha__range=(fecha_inicio, fecha_fin),
            status__codename__in=codenames
        )
    else:  # elif filter_cadena == 'filter_agencia':
        tickets = Tickets.objects.filter(
            user__taquilla__agencia=user.taquilla.agencia,
            fecha__range=(fecha_inicio, fecha_fin),
            status__codename__in=codenames
        )

    json_tickets = []
    for ticket in tickets:
        fecha = strFecha(horajuego=ticket.fecha)
        json_interno = {
            'referencia': ticket.pk,
            'fecha': fecha.getFecha(),
            'hora': fecha.getHora(),
            'monto': float(ticket.monto),
            'ganancia': float(ticket.monto_ganancia),
            'premio': float(ticket.get_monto_premio()),
            'tipo': ticket.ticket_type.nombre,
        }
        # Luis - Sep 2, 2015
        _status = ticket.status
        # /luis_sep_2_2015
        json_interno['status'] = _status.name

        if _status.codename == 'status_pagado':
            json_interno['expiration_date'] = ''
        else:
            json_interno['expiration_date'] = str(
                get_expiration_ticket(ticket)
            )

        json_tickets.append(json_interno)

    content.set_message_entry(
        'tickets_winners',
        json_tickets
    )


def tickets_list(content, session, fecha, filter_cadena, filter_status):

    user = session.user

    if check_date(fecha, content):
        # si la fecha es anterior a el limite retorna
        return

    if check_filter_valid(user.get_taquilla(), filter_cadena, content):
        return

    fecha_inicio = fecha + hora_cero
    fecha_fin = fecha + hora_23

    if filter_cadena == 'filter_taquilla':
        tickets = Tickets.objects.filter(
            user=user,
            fecha__range=(fecha_inicio, fecha_fin)
        )
    else:  # elif filter_cadena == 'filter_agencia':
        tickets = Tickets.objects.filter(
            user__taquilla__agencia_id=user.taquilla.agencia_id,
            fecha__range=(fecha_inicio, fecha_fin)
        )

    if filter_status != 'status_all':
        tickets = tickets.filter(
            status__codename=filter_status
        )

    json_tickets = []

    for ticket in tickets:
        json_interno = cache.get(
            'cache_ws_ticktes_list_{0}_{1}'.format(
                ticket.pk,
                ticket.updated_at.strftime('%Y_%m_%d_%I_%M_%p')
            )
        )

        if json_interno is None:
            _status = ticket.status
            fecha = strFecha(horajuego=ticket.fecha)
            json_interno = {
                'referencia': ticket.pk,
                'fecha': fecha.getFecha(),
                'hora': fecha.getHora(),
                'monto': float(ticket.monto),
                'tipo': ticket.ticket_type.nombre,
                'status': _status.name,
                'premio': 0,
            }

            if _status.codename == 'status_pagado' or _status.codename == 'status_procesandoganador':
                json_interno['premio'] = float(ticket.monto_premio)

            cache.set('cache_ws_ticktes_list_{0}_{1}'.format(
                ticket.pk,
                ticket.updated_at.strftime('%Y_%m_%d_%I_%M_%p')
            ),
                json_interno,
                CACHES_CONF_TIME['Consultas']['ListadoTickets']
            )

        json_tickets.append(json_interno)

    content.set_message_entry(
        'tickets_list',
        json_tickets
    )
