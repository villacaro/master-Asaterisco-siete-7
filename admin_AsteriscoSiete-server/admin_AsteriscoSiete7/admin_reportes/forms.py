# -*- coding: utf-8 -*-

from datetime import date, timedelta

from admin_apuestas.models import TicketsType
from admin_asterisco7.settings import FORMAT_STR_DATE_REPORTS
from admin_juego.models import TipoProducto, Sorteo, GruposApuesta, ModalidadJuego, Fechas
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import WidgetCustomizeForms
from admin_status.models import Status
from django import forms
from django.utils.timezone import now


class FilterDeportesForm(WidgetCustomizeForms, forms.Form):
    deporte = forms.ModelChoiceField(
        required=False,
        queryset=TipoProducto.objects.all(),
        empty_label='Todos los deportes'
    )
    temporada = forms.ModelChoiceField(
        required=False,
        queryset=Fechas.objects.select_related('torneo').all(),
        empty_label='Todos los torneos',
    )
    encuentro = forms.ModelChoiceField(
        required=False,
        queryset=Sorteo.objects.all(),
        empty_label='Todos los encuentros'
    )

    def __init__(self, *args, **kwargs):
        super(FilterDeportesForm, self).__init__(*args, **kwargs)

        def label_from_instance_temporadas(obj):
            return '{0} - {1}'.format(
                obj.torneo.nombre,
                obj.nombre
            )

        def label_from_instance_encuentros(obj):
            objFecha = strFecha(obj.horajuego)
            campo = 'Referencia: {0} -> Fecha: {1} ->Hora: {2} -> ModalidadJuego: '.format(
                obj.pk,
                objFecha.getFecha(),
                objFecha.getHora(),
            )
            for obj2 in obj.encuentrosdetail_set.all():
                nombre = obj2.equipos_temporadas.equipo.nombre
                campo = campo + ' - ' + nombre

            return campo

        self.fields['temporada'].label_from_instance = label_from_instance_temporadas
        self.fields['encuentro'].label_from_instance = label_from_instance_encuentros

        if not self.data.get('encuentro'):
            self.fields['encuentro'].queryset = Sorteo.objects.none()

    def inicializar(self, temporadas=None, encuentros=None):
        if temporadas:
            self.fields['temporada'].queryset = temporadas

        if encuentros:
            self.fields['encuentro'].queryset = encuentros
        else:
            self.fields['encuentro'].queryset = Sorteo.objects.none()

    def clean(self):

        encuentro = self.cleaned_data.get('encuentro')

        if encuentro:
            self.fields['encuentro'].initial = encuentro

            if 'temporada' in self.fields:
                self.fields['temporada'].initial = encuentro.jornada.temporadas

            if 'deporte' in self.fields:
                self.fields['deporte'].initial = encuentro.jornada.temporadas.torneo.deporte
        else:
            temporada = self.cleaned_data.get('temporada')
            if temporada:
                self.fields['temporada'].initial = temporada

                if 'deporte' in self.fields:
                    self.fields['deporte'].initial = temporada.torneo.deporte
            else:
                deporte = self.cleaned_data.get('deporte')
                if deporte:
                    self.fields['deporte'].initial = deporte

                    if 'temporada' in self.fields:
                        self.fields['temporada'].queryset = Fechas.objects.filter(torneo__deporte=deporte)

        self.is_bound = False
        return self.cleaned_data


class FilterFechasTimeForm(WidgetCustomizeForms, forms.Form):
    fecha_inicio = forms.DateTimeField(
        label='Desde (*)',
        required=True,
    )
    fecha_fin = forms.DateTimeField(
        label='Hasta (*)',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FilterFechasTimeForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = now().strftime(FORMAT_STR_DATE_REPORTS) + hora_cero
        self.fields['fecha_fin'].initial = now().strftime(FORMAT_STR_DATE_REPORTS) + hora_23


class FilterFechasForm(WidgetCustomizeForms, forms.Form):
    fecha_opcion = forms.ChoiceField(
        label='Tiempo ',
        required=False,
    )
    fecha_inicio = forms.DateField(
        label='Desde (*)',
        required=True,
    )
    fecha_fin = forms.DateField(
        label='Hasta (*)',
        required=True,
    )
    tipo_opcion = forms.ChoiceField(
        label='Tiempo ',
        required=False,
        widget=forms.RadioSelect,
        choices=[('del', 'Del'), ('rango', 'Por Rango')],
        initial='del'
    )

    def __init__(self, *args, **kwargs):
        super(FilterFechasForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = now().strftime(FORMAT_STR_DATE_REPORTS)
        self.fields['fecha_fin'].initial = self.fields['fecha_inicio'].initial

        # del self.fields['fecha_opcion'].widget.attrs['class']
        # del self.fields['fecha_opcion'].widget.attrs['data-placeholder']
        self.fields['tipo_opcion'].widget.attrs['class'] = 'select-periodo'

    def inicializar(self, tipo='', comer=None):
        if tipo == 'Fechas':
            dias_rest = int(now().strftime('%w')) - 1
            if dias_rest == 0:
                dias_rest = 6
            lunes = date.today() - timedelta(days=dias_rest)

            inicio_actual = (lunes).strftime(FORMAT_STR_DATE_REPORTS)
            fin_actual = now().strftime(FORMAT_STR_DATE_REPORTS)

            inicio_anterior = (lunes - timedelta(days=7)).strftime(FORMAT_STR_DATE_REPORTS)
            fin_anterior = (lunes - timedelta(days=1)).strftime(FORMAT_STR_DATE_REPORTS)

            value_actual = inicio_actual + '_' + fin_actual
            value_anterior = inicio_anterior + '_' + fin_anterior

            self.fields['fecha_opcion'].choices = [
                (value_actual, 'Semana actual'),
                (value_anterior, 'Semana anterior')
            ]

            self.fields['fecha_inicio'].initial = inicio_actual

        elif tipo == 'Periodos':
            dia_actual = (now() - timedelta(days=1)).strftime(FORMAT_STR_DATE_REPORTS)
            dia_anterior = (now() - timedelta(days=2)).strftime(FORMAT_STR_DATE_REPORTS)

            dias_rest = int(now().strftime('%d'))
            primer_dia_mes_actual = (
                now() - timedelta(days=dias_rest - 1)
            ).strftime(FORMAT_STR_DATE_REPORTS)

            ultimo_dia_mes_anterior = (
                now() - timedelta(days=dias_rest)
            ).strftime(FORMAT_STR_DATE_REPORTS)

            ultimo_rest = int((
                now() - timedelta(days=dias_rest + 1)
            ).strftime('%d'))

            primer_dia_mes_anterior = (
                now() - timedelta(
                    days=dias_rest + ultimo_rest
                )
            ).strftime(FORMAT_STR_DATE_REPORTS)

            self.fields['fecha_opcion'].choices = [
                (dia_actual + '_' + dia_actual, 'Dia'),
                (dia_anterior + '_' + dia_anterior, 'Dia anterior'),
                (primer_dia_mes_actual + '_' + dia_actual, 'Mes'),
                (primer_dia_mes_anterior + '_' + ultimo_dia_mes_anterior, 'Mes anterior')
            ]
        elif tipo == 'FechasParley':
            dia_actual = now()
            if not comer or not int(comer.pk):
                return

            semana_actual = [
                comer.get_day_queda_is_corte_previous(
                    fecha=dia_actual,
                    frecuencia='frecuencia_semanal'
                ),
                comer.get_day_queda_is_corte_next(
                    fecha=dia_actual,
                    frecuencia='frecuencia_semanal'
                ) - timedelta(days=1),
            ]
            quincena_actual = [
                comer.get_day_queda_is_corte_previous(
                    fecha=dia_actual,
                    frecuencia='frecuencia_quincenal'
                ),
                comer.get_day_queda_is_corte_next(
                    fecha=dia_actual,
                    frecuencia='frecuencia_quincenal'
                ) - timedelta(days=1),
            ]
            mes_actual = [
                comer.get_day_queda_is_corte_previous(
                    fecha=dia_actual,
                    frecuencia='frecuencia_mensual'
                ),
                comer.get_day_queda_is_corte_next(
                    fecha=dia_actual,
                    frecuencia='frecuencia_mensual'
                ) - timedelta(days=1),
            ]

            dia_actual = semana_actual[0] - timedelta(days=1)
            semana_anterior = [
                comer.get_day_queda_is_corte_previous(
                    fecha=dia_actual,
                    frecuencia='frecuencia_semanal'
                ),
                comer.get_day_queda_is_corte_next(
                    fecha=dia_actual,
                    frecuencia='frecuencia_semanal'
                ) - timedelta(days=1),
            ]
            dia_actual = quincena_actual[0] - timedelta(days=1)
            quincena_anterior = [
                comer.get_day_queda_is_corte_previous(
                    fecha=dia_actual,
                    frecuencia='frecuencia_quincenal'
                ),
                comer.get_day_queda_is_corte_next(
                    fecha=dia_actual,
                    frecuencia='frecuencia_quincenal'
                ) - timedelta(days=1),
            ]
            dia_actual = mes_actual[0] - timedelta(days=1)
            mes_anterior = [
                comer.get_day_queda_is_corte_previous(
                    fecha=dia_actual,
                    frecuencia='frecuencia_mensual'
                ),
                comer.get_day_queda_is_corte_next(
                    fecha=dia_actual,
                    frecuencia='frecuencia_mensual'
                ) - timedelta(days=1),
            ]

            hoy = now()

            self.fields['fecha_opcion'].choices = [
                (
                    semana_actual[0].strftime(FORMAT_STR_DATE_REPORTS) + '_' + (
                        semana_actual[1].strftime(FORMAT_STR_DATE_REPORTS) if hoy.date() >= semana_actual[
                            1].date() else hoy.strftime(FORMAT_STR_DATE_REPORTS)),
                    'Semana actual'
                ),
                (
                    semana_anterior[0].strftime(FORMAT_STR_DATE_REPORTS) + '_' +
                    semana_anterior[1].strftime(FORMAT_STR_DATE_REPORTS),
                    'Semana anterior'
                ),
                (
                    quincena_actual[0].strftime(FORMAT_STR_DATE_REPORTS) + '_' + (
                        quincena_actual[1].strftime(FORMAT_STR_DATE_REPORTS) if hoy.date() >= quincena_actual[
                            1].date() else hoy.strftime(FORMAT_STR_DATE_REPORTS)),
                    'Quincena actual'
                ),
                (
                    quincena_anterior[0].strftime(FORMAT_STR_DATE_REPORTS) + '_' +
                    quincena_anterior[1].strftime(FORMAT_STR_DATE_REPORTS),
                    'Quincena anterior'
                ),
                (
                    mes_actual[0].strftime(FORMAT_STR_DATE_REPORTS) + '_' + (
                        mes_actual[1].strftime(FORMAT_STR_DATE_REPORTS) if hoy.date() >= mes_actual[
                            1].date() else hoy.strftime(FORMAT_STR_DATE_REPORTS)),
                    'Mes actual'
                ),
                (
                    mes_anterior[0].strftime(FORMAT_STR_DATE_REPORTS) + '_' +
                    mes_anterior[1].strftime(FORMAT_STR_DATE_REPORTS),
                    'Mes anterior'
                )
            ]

            self.fields['fecha_inicio'].initial = semana_actual[0].strftime(FORMAT_STR_DATE_REPORTS)
            if hoy.date() >= semana_actual[1].date():
                self.fields['fecha_fin'].initial = semana_actual[1].strftime(FORMAT_STR_DATE_REPORTS)
            else:
                self.fields['fecha_fin'].initial = hoy.strftime(FORMAT_STR_DATE_REPORTS)


class FilterTicketsTiposForm(WidgetCustomizeForms, forms.Form):
    tipos_ticket = forms.ModelChoiceField(
        required=False,
        queryset=TicketsType.objects.only('nombre').all().order_by('nombre'),
        empty_label='Todos los tipos'
    )


class FilterTicketsTiposAndStatusForm(FilterTicketsTiposForm):
    status_ticket = forms.ModelChoiceField(
        required=False,
        queryset=Status.objects.only('name').filter(content_type=8).order_by('name'),
        empty_label='Todos los estatus'
    )


class FilterTicketsStatusForm(WidgetCustomizeForms, forms.Form):
    status_ticket_content = forms.ModelChoiceField(
        label='Que contenga en el historico',
        required=False,
        queryset=Status.objects.only('name').filter(content_type=8).order_by('name'),
        empty_label='Todos los estatus'
    )


class FilterModalidadesForm(WidgetCustomizeForms, forms.Form):
    grupo_modalidad = forms.ModelChoiceField(
        required=False,
        queryset=GruposApuesta.objects.only('nombre').all().order_by('nombre'),
        empty_label='Todos los grupos'
    )
    modalidad = forms.ModelChoiceField(
        required=False,
        queryset=ModalidadJuego.objects.only('nombre').all().order_by('nombre'),
        empty_label='Todas las modalidades'
    )


class FilterOrdenPresentacionReporteForm(WidgetCustomizeForms, forms.Form):
    orden = forms.ChoiceField(
        label='Agrupado',
        required=False,
        choices=[
            ('comercializacion', 'Cadena de comercialización'),
            ('agencia', 'Centros de apuesta'),
        ]
    )

    def __init__(self, *args, **kwargs):
        presentacion_add = None
        if 'presentacion_add' in kwargs:
            presentacion_add = kwargs.pop('presentacion_add')
        super(FilterOrdenPresentacionReporteForm, self).__init__(*args, **kwargs)
        if presentacion_add:
            self.fields['orden'].choices += presentacion_add


class FilterOrdenPresentacionReporteMediaForm(WidgetCustomizeForms, forms.Form):
    orden = forms.ChoiceField(
        label='Agrupado',
        required=False,
        choices=[
            ('comercializacion', 'Cadena de comercialización'),
            ('parley', 'Juego parley'),
        ]
    )


class FilterOrdenPresentacionReporteCuadreForm(WidgetCustomizeForms, forms.Form):
    orden = forms.ChoiceField(
        label='Agrupado',
        required=False,
        choices=[
            ('comercializacion', 'Cadena de comercialización'),
            ('fecha', 'Fechas'),
            ('agencia', 'Centros de apuesta'),
        ]
    )

    def __init__(self, *args, **kwargs):
        presentacion_add = None
        if 'presentacion_add' in kwargs:
            presentacion_add = kwargs.pop('presentacion_add')
        super(FilterOrdenPresentacionReporteCuadreForm, self).__init__(*args, **kwargs)
        if presentacion_add:
            self.fields['orden'].choices += presentacion_add


class FilterCodigoForm(WidgetCustomizeForms, forms.Form):
    codigo = forms.CharField(
        required=False,
        label='Codigo agencia '
    )


class FilterOptionMediaForm(WidgetCustomizeForms, forms.Form):
    option = forms.ChoiceField(
        label='Ver media por',
        required=False,
        choices=[
            ('monto_total count_tickets', 'Ventas'),
            ('monto_premios count_apuestas', 'Premios')
        ]
    )
    # En la vista que gestiona este formulario, se hace un aplit para obtener los 2 campos
    # de los cuales se casa la media
