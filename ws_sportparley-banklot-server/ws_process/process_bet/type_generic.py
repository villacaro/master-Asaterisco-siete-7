# -*- coding: utf-8 -*-

import string
from datetime import timedelta
from decimal import Decimal
from random import choice

from admin_apuestas.models import Tickets, TicketsDetail, TicketsType
from admin_banklotsports.settings import DEBUG, FORMAT_STR_DATE_REPORTS
from admin_comercializacion.models import Cupos, Porcentajes
from admin_juego.models import Encuentros, Jugadas
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_status.models import Status
from django.db.models import Sum
from django.utils.timezone import now
from ws_lib.crypto import CryptoRSA
from ws_sportparley.messages import MESSAGES_GLOBAL


class type_generic(object):
    """
    Modulo de apuesta parley
    """
    key_error_message = None
    kwargs_error_messages = {}
    chars_keys = string.ascii_uppercase + string.digits

    def __init__(self, **kwargs):
        super(type_generic, self).__init__()

        self.session = kwargs.pop('session')
        self.user = self.session.user
        self.content = kwargs.pop('content')
        self.agencia = self.user.taquilla.agencia
        self.distribuidor = self.agencia.get_origen()
        self.banca = self.distribuidor.get_origen()
        self.bloque = self.banca.get_origen()

        self.sistema = kwargs.pop('sistema')
        self.type_bet = TicketsType.get_type_bet_by_codename(
            codename=kwargs.pop('type_bet')
        )
        self.total_bet = round(kwargs.pop('total_bet'), 2)
        self.array_json_bet = kwargs.pop('array_bet')
        self.array_bet = self.get_pks_jugadas()
        self.array_bet_count = len(self.array_bet)

        self.respond = {}

    def finish(self):
        if self.content.error:
            self.content.error = False

            self.content.set_entry('error_bet', 1)
            self.content.set_entry(
                'errormessage_bet',
                MESSAGES_GLOBAL[
                    self.key_error_message
                ]
            )
            if self.kwargs_error_messages:
                self.content.set_entry(
                    'errormessage_bet',
                    self.content.get_entry('errormessage_bet').format(
                        **self.kwargs_error_messages
                    )
                )

            if self.key_error_message == 'invalid_logros_change':
                self.content.set_message_entry(
                    'array_bet',
                    self.errors_logros_pks
                )

            if self.key_error_message == 'restriction_bets':
                self.content.set_message_entry(
                    'restriction_array_bet',
                    self.array_bet
                )

        self.content.set_message_entry(
            'parley_bet',
            self.respond
        )

    def get_pks_jugadas(self):
        pks = []
        self.array_bet_dic = {}
        for pk in self.array_json_bet:
            pks.append(
                pk.get('pk')
            )
            self.array_bet_dic[pk.get('pk')] = {
                'logro': pk.get('logro'),
                'ref': pk.get('ref'),
                'ref_m': pk.get('ref_m'),
            }
        return pks

    def check_exists_porcentajes(self):
        """
        Chekeamos la existencia de porcentajes en la cadena, en caso de que
        sea una agencia que no use el alquiler
        """

        def check_cadena(obj):
            kwargs = {
                'fecha_fin': None
            }
            kwargs[obj.prefix_filter] = obj
            return Porcentajes.objects.filter(
                **kwargs
            ).exclude(
                porcentaje_ganancia=0
            ).exists()

        if not check_cadena(self.bloque):
            return False, self.bloque
        if (self.banca.modelo_negocio_codenames['codename_negocio_alquiler'] !=
                self.banca.modelo_negocio):
            for obj in [self.distribuidor, self.banca]:
                if not check_cadena(obj):
                    return False, obj

        return True, None

    def repeated_bets(self):
        """
        La funcion set de python quita elementos repetidos de una lista,
        entonces si el tamaño de la lista original es distinto
        a la lista generada por python con set,
        significa que hay jugadas repetidas
        """
        if self.array_bet_count != len(list(set(self.array_bet))):
            self.content.error = True
            self.key_error_message = 'repeated_bets'

        return self.content.error

    def restriction_bets(self):
        """
        Se verifica que todas las jugadas pertenescan al sistema
        de juego, ademas tambien que
        permitan la venta de parley y esten habilitadas
        """
        status_habilitado = Status.get_status_by_codename('status_habilitado')
        status_pendiente = Status.get_status_by_codename('status_pendiente')

        fecha_hora = now()
        fecha_str_init = fecha_hora.strftime(FORMAT_STR_DATE_REPORTS)
        fecha = fecha_hora.date()
        if DEBUG:
            fecha_str_fin = (fecha_hora + timedelta(days=30)
                             ).strftime(FORMAT_STR_DATE_REPORTS)
        else:
            fecha_str_fin = fecha_str_init

        querry = Jugadas.objects.filter(
            pk__in=self.array_bet,
            status_id=status_pendiente.pk,
            encuentros_modalidad__encuentro__horajuego__range=(
                fecha_str_init + hora_cero, fecha_str_fin + hora_23),
            encuentros_modalidad__encuentro__horacierre__gt=fecha_hora,
            encuentros_modalidad__encuentro__status_id=status_habilitado.pk,
            encuentros_modalidad__encuentro__jornada__status_id=status_habilitado.pk,
            encuentros_modalidad__encuentro__jornada__temporadas__status_id=status_habilitado.pk,
            encuentros_modalidad__encuentro__jornada__sistema_id=self.sistema.pk,
            encuentros_modalidad__encuentro__jornada__parley=True,
            encuentros_modalidad__encuentro__jornada__fechafin__gte=fecha,
            encuentros_modalidad__encuentro__jornada__temporadas__fechafin__gte=fecha,
        )

        if querry.count() != self.array_bet_count:
            self.content.error = True
            self.key_error_message = 'restriction_bets'
            for pk in querry.values_list('pk', flat=True):
                self.array_bet.remove(pk)

        return self.content.error

    def set_factor_riesgo(self):
        """
        Aqui se aplican todas las rutinas para aplicar el factor de riesgo
        """
        comercializadora = self.agencia.get_comercializadora()
        if len(comercializadora.get_factores_riesgo().factores) > 0:
            for regla in comercializadora.get_factores_riesgo().factores:
                # 0 es el rango inicial
                # 1 es el rango final
                # 2 es el porcentaje a aplicar
                if self.total_bet >= float(
                        regla[0]) and self.total_bet <= float(regla[1]):
                    limite = self.total_bet * float(regla[2])
                    if self.total_gain <= limite:
                        return True
                    else:
                        return False
        else:
            return True

    def check_cupos(self):
        """
        Chekeamos la venta del dia para verificar cupos
        """
        fecha = strFecha(now()).getFecha()

        tickets_filter = Tickets.objects.filter(
            fecha__range=(fecha + hora_cero, fecha + hora_23)
        )

        def verificate(self, cadena, tickets_filter):
            kwargs = {}
            kwargs[
                'user__taquilla__agencia' +
                cadena.get_prefix_kwargs_by_level_agencia()
            ] = cadena

            tickets_filter = tickets_filter.filter(**kwargs)

            sum_cadena = tickets_filter.aggregate(Sum('monto'))['monto__sum']
            sum_cadena = float(sum_cadena) if sum_cadena else float()

            sum_cadena_premio = tickets_filter.aggregate(Sum('monto_premio'))['monto_premio__sum']
            sum_cadena_premio = float(sum_cadena_premio) if sum_cadena_premio else float()
            try:
                kwargs = {}
                kwargs[cadena.prefix_filter] = cadena
                kwargs['fecha_fin'] = None
                _cupo = Cupos.objects.only('monto_diario', 'monto_premio').get(**kwargs)
                if ((sum_cadena + self.total_bet) > float(_cupo.monto_diario)):
                    self.content.error = True
                    self.key_error_message = 'invalid_cupos_limited'
                    self.kwargs_error_messages['cadena'] = cadena.prefix_filter
                    self.kwargs_error_messages['cupo'] = _cupo.monto_diario
                elif _cupo.monto_premio and ((sum_cadena_premio + self.total_gain) > float(_cupo.monto_premio)):
                    self.content.error = True
                    self.key_error_message = 'invalid_cupos_premio_limited'
                    self.kwargs_error_messages['cadena'] = cadena.prefix_filter
                    self.kwargs_error_messages['cupo'] = _cupo.monto_premio
            except Cupos.DoesNotExist:
                self.content.error = True
                self.key_error_message = 'invalid_cupos_no_exists'
                self.kwargs_error_messages['cadena'] = cadena.prefix_filter

            return self.content.error

        # verificando agencia
        if verificate(self, self.agencia, tickets_filter):
            pass
        # verificando distribuidor
        elif verificate(self, self.distribuidor, tickets_filter):
            pass
        # verificando banca
        elif verificate(self, self.banca, tickets_filter):
            pass
        # verificando bloque
        elif verificate(self, self.bloque, tickets_filter):
            pass

        return self.content.error

    def check_permisos_ventas(self):
        """
        Chekeamos que los permisos de ventas se cumplan
        """
        restriction_querry = self.agencia.get_comercializadora().get_restrictions_ventas()
        for jugada in self.jugadas:
            restriccion = False

            # Verificando deporte
            if restriction_querry.filter(
                    deporte_id=jugada.encuentros_modalidad.deporte_grupo.deporte_id,
                    grupo__isnull=True,
                    modalidad__isnull=True).exists():
                restriccion = True

            # Verificando grupo
            elif restriction_querry.filter(
                    deporte_id=jugada.encuentros_modalidad.deporte_grupo.deporte_id,
                    grupo_id=jugada.encuentros_modalidad.deporte_grupo.grupo_id,
                    modalidad__isnull=True).exists():
                restriccion = True

            # Verificando modalidad
            elif restriction_querry.filter(
                    deporte_id=jugada.encuentros_modalidad.deporte_grupo.deporte_id,
                    grupo_id=jugada.encuentros_modalidad.deporte_grupo.grupo_id,
                    modalidad_id=jugada.encuentros_modalidad.modalidad_grupo.modalidad_id).exists():
                restriccion = True

            if restriccion:
                self.content.error = True
                self.key_error_message = 'jugada_restriction'
                self.kwargs_error_messages['jugada'] = str(jugada)
                break

        return self.content.error

    def get_fecha_aproximada(self):
        """
        Obtiene la fecha del ultimo juego en la lista de logros
        apostados como fecha aproximada
        """
        fecha_maxima = self.jugadas.order_by(
            '-encuentros_modalidad__encuentro__horajuego'
        ).values_list(
            'encuentros_modalidad__encuentro__horajuego',
            flat=True
        )[0].date()

        return '{0}/{1}/{2}'.format(
            fecha_maxima.day,
            fecha_maxima.month,
            fecha_maxima.year
        )

    def set_procesar_venta_ticket(self):

        _status_ini = Status.get_status_by_codename('status_anulado')

        _ticket = Tickets.objects.create(
            monto=self.total_bet,
            monto_premio=self.total_gain,
            monto_ganancia=self.total_gain,
            fecha=now(),
            ticket_type=self.type_bet,
            user=self.user,
            key=''.join(choice(self.chars_keys) for i in range(8)),
            pks_jugadas=self.pks_jugadas,
            status=_status_ini,
        )

        _status = Status.get_status_by_codename('status_ticketpendiente')

        json_detalle = {}
        json_detalle['encuentros'] = {}
        monto_div_decimal = Decimal(
            Decimal(
                self.total_bet) /
            self.array_bet_count)
        monto_div_float = round(float(monto_div_decimal), 2)

        for jugada in self.jugadas:
            _ticket_detalle = TicketsDetail.objects.create(
                jugada=jugada,
                ticket=_ticket,
                monto=monto_div_decimal,
                logro_apostado=jugada.valor_americano,
                modalidad_ref=jugada.encuentros_modalidad.etiqueta_ref,
                condicion_ref=jugada.valor_etq_ref,
                status=_status,
            )
            _ticket_detalle.set_new_status(status=_status, initial=True)

            json_jugada = {}
            json_jugada['jugada'] = jugada.pk

            json_jugada['monto'] = monto_div_float

            json_jugada['logro_apostado'] = str(jugada.valor_americano) \
                if jugada.valor_americano <= 0 \
                else str('+') + str(jugada.valor_americano)

            json_jugada['ref_jugada'] = '' if jugada.valor_etq_ref is None \
                else jugada.valor_etq_ref

            encuentro_pk = str(jugada.encuentros_modalidad.encuentro_id)
            if encuentro_pk in json_detalle['encuentros']:
                pass
            else:

                # Se verifica si el encuentro tiene la venta como no activa para
                # proceder a activar la bandera
                if jugada.encuentros_modalidad.encuentro.exists_tickets is False:
                    Encuentros.objects.filter(
                        pk=jugada.encuentros_modalidad.encuentro_id).update(
                        exists_tickets=True)

                json_detalle['encuentros'][encuentro_pk] = {}
                json_detalle['encuentros'][encuentro_pk]['pk'] = encuentro_pk
                objFecha = strFecha(
                    jugada.encuentros_modalidad.encuentro.horajuego
                )
                json_detalle['encuentros'][encuentro_pk]['fecha'] = objFecha.getFecha()

                json_detalle['encuentros'][encuentro_pk]['hora'] = objFecha.getHora()

                json_detalle['encuentros'][encuentro_pk]['encuentro_modalidad'] = {}

            encuentro_modalidad_pk = str(jugada.encuentros_modalidad.pk)
            if encuentro_modalidad_pk in json_detalle['encuentros'][
                encuentro_pk
            ]['encuentro_modalidad']:
                pass
            else:
                json_detalle['encuentros'][encuentro_pk][
                    'encuentro_modalidad'
                ][encuentro_modalidad_pk] = {}

                json_detalle['encuentros'][encuentro_pk][
                    'encuentro_modalidad'
                ][encuentro_modalidad_pk]['pk'] = encuentro_modalidad_pk

                json_detalle['encuentros'][encuentro_pk][
                    'encuentro_modalidad'
                ][encuentro_modalidad_pk]['ref_modalidad'] = '' \
                    if jugada.encuentros_modalidad.etiqueta_ref is None \
                    else jugada.encuentros_modalidad.etiqueta_ref

                json_detalle['encuentros'][encuentro_pk]['encuentro_modalidad'][encuentro_modalidad_pk]['jugadas'] = []

            json_detalle['encuentros'][encuentro_pk]['encuentro_modalidad'][encuentro_modalidad_pk]['jugadas'].append(
                json_jugada
            )

        _ticket.set_new_status(status=_status, initial=True)

        objFecha = strFecha(_ticket.fecha)

        self.respond['ticket'] = {
            'referencia': _ticket.pk,
            'llave': CryptoRSA.encrypt(
                _ticket.key.encode('utf8'),
                self.session.user.pub_key_client
            ),
            'fecha': objFecha.getFecha(),
            'hora': objFecha.getHora(),
            'monto_apostado': self.total_bet,
            'monto_ganancia': _ticket.monto_ganancia,
            'tipo': self.type_bet.nombre,
            'detalle': json_detalle,
            'fecha_aproximada': self.get_fecha_aproximada(),
            'status': _status.name
        }

        # lanzar hilo
        from admin_datamart.task import AsyncGestion_add_ticket_apuesta_En_Linea
        obj = AsyncGestion_add_ticket_apuesta_En_Linea()
        obj.delay(*(), **{'ticket': _ticket.pk, })

        return self.finish()
