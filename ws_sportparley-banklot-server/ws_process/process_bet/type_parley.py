# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_apuestas.models import Tickets
from admin_comercializacion.models import AgenciaDataDefault
from admin_comercializacion.views.preferencias_views import LoadPreferences
from admin_juego.models import Jugadas
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from django.db.models import Sum
from django.utils.timezone import now

from .type_generic import type_generic


class type_parley(type_generic):
    """
    Modulo de apuesta parley
    """

    def run(self):

        if self.repeated_bets():
            return self.finish()
        elif self.restriction_bets():
            return self.finish()

        self.total_gain = 1
        array_validation = {}
        self.cantidad_machos = 0
        self.cantidad_hembras = 0
        self.cantidad_empates = 0
        array_validation_restrictions = {}

        self.jugadas = Jugadas.objects.select_related(
            'encuentros_modalidad__encuentro',
            'encuentros_modalidad__modalidad_grupo__modalidad',
            'encuentros_modalidad__deporte_grupo__deporte'
        ).filter(
            pk__in=self.array_bet
        )

        # Llamo esta funcion aqui, apenas hago la consulta de jugadas
        if self.check_change_logros_and_ref():
            return self.finish()

        """
        Validando restricciones de jugadas
        """

        # reservada para guardar la consulta de las restricciones de una
        # modalidad y no repetirla mas
        modalidades_restri = {}

        restricciones_array = self.agencia.get_restrictions_modalidades()

        for jugada in self.jugadas:

            self.total_gain = self.total_gain * float(
                self.convert_americano_europeo(jugada.valor_americano)
            )

            deporte_pk = jugada.encuentros_modalidad.encuentro.jornada.temporadas.torneo.deporte_id
            encuentro_pk = jugada.encuentros_modalidad.encuentro_id
            grupo_pk = jugada.encuentros_modalidad.modalidad_grupo.grupo_id
            modalidad_pk = jugada.encuentros_modalidad.modalidad_grupo.modalidad_id
            modalidad = jugada.encuentros_modalidad.modalidad_grupo.modalidad

            # Contador de apuestas por encuentro
            str_encuentro = 'encuentro_{0}'.format(encuentro_pk)
            if str_encuentro in array_validation:
                array_validation[str_encuentro]['count_bet'] += 1
            else:
                array_validation[str_encuentro] = {
                    'count_bet': 1,
                    # permite verificar un numero de apuestas
                    # por encuentro en cada deporte
                }

            # Grupo para verificar que no vengan 2 apuestas de la misma
            # modalidad en el mismo grupo
            str_grupo = 'grupo_{0}'.format(grupo_pk)
            if str_grupo not in array_validation[str_encuentro]:
                array_validation[str_encuentro][str_grupo] = {}

            str_modalidad = 'modalidad_{0}'.format(modalidad_pk)
            if str_modalidad in array_validation[str_encuentro][str_grupo]:
                self.content.error = True
                self.key_error_message = 'invalid_for_restriction'
                return self.finish()
            else:
                array_validation[str_encuentro][
                    str_grupo][str_modalidad] = True

            # Verificacion de restriccion entre modalidades
            if 'modalidades' not in array_validation[str_encuentro]:
                array_validation[str_encuentro]['modalidades'] = []

            array_validation[str_encuentro]['modalidades'].append(modalidad_pk)

            modalidad_pk_str = '{0}'.format(modalidad_pk)
            _pk_restric_modalidates = modalidades_restri.get(modalidad_pk_str)
            if not _pk_restric_modalidates:
                _pk_restric_modalidates = list(
                    modalidad.restriction.all().values_list(
                        'pk', flat=True
                    )
                )
                modalidades_restri[modalidad_pk_str] = _pk_restric_modalidates

            for _pk_restric in _pk_restric_modalidates:
                if _pk_restric in array_validation[
                        str_encuentro]['modalidades']:
                    self.content.error = True
                    self.key_error_message = 'invalid_for_restriction'
                    return self.finish()

            # Llenando json para validaciones de restricciones por deporte
            str_deporte = '{0}'.format(deporte_pk)
            if str_deporte not in array_validation_restrictions:
                array_validation_restrictions[str_deporte] = {}

            if str_encuentro not in array_validation_restrictions[str_deporte]:
                array_validation_restrictions[str_deporte][str_encuentro] = []

            if modalidad_pk_str not in array_validation_restrictions[
                    str_deporte][str_encuentro]:
                array_validation_restrictions[str_deporte][
                    str_encuentro].append(modalidad_pk_str)

            for str_modalidad in array_validation_restrictions[
                    str_deporte][str_encuentro]:
                if restricciones_array.get(str_deporte):
                    if restricciones_array.get(str_deporte).get(str_modalidad):
                        restricciones_modalidades_array = restricciones_array.get(str_deporte).\
                            get(str_modalidad)
                        for restriction_obj in restricciones_modalidades_array:
                            restriction_obj = str(restriction_obj)
                            if restriction_obj in array_validation_restrictions[
                                    str_deporte][str_encuentro]:
                                self.content.error = True
                                self.key_error_message = 'invalid_for_restriction'
                                return self.finish()

            # Validando numero de apuestas por encuentro
            if array_validation[str_encuentro]['count_bet'] > jugada.encuentros_modalidad \
                    .deporte_grupo.deporte.count_apuesta:
                self.content.error = True
                self.key_error_message = 'invalid_max_count_bet_by_deporte'
                self.kwargs_error_messages['deporte'] = '{0}'.format(
                    jugada.encuentros_modalidad.deporte_grupo.deporte
                )
                self.kwargs_error_messages['max'] = '{0}'.format(
                    jugada.encuentros_modalidad.deporte_grupo.deporte.count_apuesta
                )
                return self.finish()

            if jugada.favorito is True:
                self.cantidad_machos += 1
            elif jugada.favorito is False:
                self.cantidad_hembras += 1
            elif jugada.favorito is None and modalidad.codename == 'empate':
                self.cantidad_empates += 1

        self.total_gain = round(self.total_gain * self.total_bet, 0)
        """
        Aplicamos el factor de riesgo
        """

        if self.set_factor_riesgo() is False:
            self.content.error = True
            self.key_error_message = 'invalid_factor_riesgo'
            return self.finish()

        self.validate = AgenciaDataDefault.get_everyone()
        if self.validate is False:
            self.validate = LoadPreferences(self.agencia)

        if self.check_min_max_apuestas_parley():
            return self.finish()
        elif self.check_min_max_machos_hembras_empate_parley(
            machos_count=self.cantidad_machos,
            hembras_count=self.cantidad_hembras,
            empate_count=self.cantidad_empates
        ):
            return self.finish()
        elif self.check_montos_de_apuestas():
            return self.finish()
        elif self.check_cupos():
            return self.finish()
        elif self.check_tickets_clonados_monto_ganancia():
            return self.finish()
        elif self.check_permisos_ventas():
            return self.finish()

        # Al terminar las validaciones proceso el ticket
        self.set_procesar_venta_ticket()

        return self.respond

    def convert_americano_europeo(self, logro):
        if logro < 0:
            return float(float(-(100 - float(logro))) / float(logro))
        elif logro > 0:
            return float(float((100 + float(logro))) / 100)
        else:
            return logro

    def check_min_max_apuestas_parley(self):
        """
        Chequeamos los minimos y maximos para la modalidad de apuesta parley
        """

        if (self.array_bet_count < self.validate.cantidad_apuesta_min or
                self.array_bet_count < 2):
            self.content.error = True
            self.key_error_message = 'invalid_min'
            self.kwargs_error_messages['min'] = 2 \
                if self.array_bet_count < self.validate.cantidad_apuesta_min \
                else self.validate.cantidad_apuesta_min

        elif (self.array_bet_count > self.validate.cantidad_apuesta_max and
                self.total_gain > self.validate.montomax_ganancia):
            self.content.error = True
            self.key_error_message = 'invalid_max'
            self.kwargs_error_messages[
                'max'] = self.validate.cantidad_apuesta_max

        return self.content.error

    def check_min_max_machos_hembras_empate_parley(
            self, machos_count, hembras_count, empate_count):
        """
        Chequeamos la cantidad de apuestas minimas y maximas
        para los machos y hembras de la apuesta
        """
        if machos_count > self.validate.parley_machos_max:
            self.content.error = True
            self.key_error_message = 'invalid_machos_max'
            self.kwargs_error_messages['max'] = self.validate.parley_machos_max

        elif machos_count < self.validate.parley_machos_min:
            self.content.error = True
            self.key_error_message = 'invalid_machos_min'
            self.kwargs_error_messages['min'] = self.validate.parley_machos_min

        elif hembras_count > self.validate.parley_hembras_max:
            self.content.error = True
            self.key_error_message = 'invalid_hembras_max'
            self.kwargs_error_messages[
                'max'] = self.validate.parley_hembras_max

        elif hembras_count < self.validate.parley_hembras_min:
            self.content.error = True
            self.key_error_message = 'invalid_hembras_min'
            self.kwargs_error_messages[
                'min'] = self.validate.parley_hembras_min

        elif empate_count > self.validate.parley_empates_max:
            self.content.error = True
            self.key_error_message = 'invalid_empates_max'
            self.kwargs_error_messages[
                'max'] = self.validate.parley_empates_max

        return self.content.error

    def check_montos_de_apuestas(self):
        """
        Verificamos los montos de apuestas
        """

        if self.total_bet < self.validate.montomin:
            self.content.error = True
            self.key_error_message = 'invalid_total_bet_min'
            self.kwargs_error_messages['min'] = self.validate.montomin

        elif self.total_bet > self.validate.montomax:
            self.content.error = True
            self.key_error_message = 'invalid_total_bet_max'
            self.kwargs_error_messages['max'] = self.validate.montomax

        elif self.total_gain > self.validate.montomax_ganancia:
            self.content.error = True
            self.key_error_message = 'invalid_total_gain'
            self.kwargs_error_messages['max'] = self.validate.montomax_ganancia

        return self.content.error

    def check_tickets_clonados_monto_ganancia(self):
        self.pks_jugadas = '{0}'.format(sorted(self.array_bet))
        fecha = strFecha(now()).getFecha()

        clonados = Tickets.objects.filter(
            user__taquilla__agencia_id=self.agencia.pk,
            fecha__range=(fecha + hora_cero, fecha + hora_23),
            pks_jugadas=self.pks_jugadas
        ).aggregate(Sum('monto_premio'))['monto_premio__sum']

        if clonados and (clonados + Decimal(self.total_gain)) >= self.validate.parley_clonados_maxima_ganancia:
            self.content.error = True
            self.key_error_message = 'invalid_limited_clonados'

        return self.content.error

    def check_change_logros_and_ref(self):
        """
        Verificamos tanto los logros como las referencias para ver
        si son las mismas que estan en el servidor.
        """

        def get_str_is_none(valor):
            if valor:
                return valor
            else:
                return ''

        self.errors_logros_pks = []
        for jugada in self.jugadas:
            error = False
            if jugada.valor_americano != int(self.array_bet_dic[
                jugada.pk
            ].get('logro')):
                # logro cambiado
                error = True
            elif get_str_is_none(jugada.valor_etq_ref) != self.array_bet_dic[
                jugada.pk
            ].get('ref'):
                # referencia cambiada
                error = True
            elif get_str_is_none(jugada.encuentros_modalidad.etiqueta_ref) != self.array_bet_dic[
                jugada.pk
            ].get('ref_m'):
                # referencia por modalidad cambiada
                error = True

            if error:
                self.errors_logros_pks.append(
                    {
                        'pk': jugada.pk,
                        'logro': jugada.get_logro_americano(),
                        'ref': get_str_is_none(jugada.valor_etq_ref),
                        'ref_m': get_str_is_none(jugada.encuentros_modalidad.etiqueta_ref),
                    }
                )
        if self.errors_logros_pks:
            self.content.error = True
            self.key_error_message = 'invalid_logros_change'
        return self.content.error
