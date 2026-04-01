# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from decimal import Decimal

from admin_asterisco7.settings import FORMAT_STR_DATE_REPORTS, MESSAGES_GLOBAL
from admin_comercializacion.models import Agencias
from admin_datamart.models import Hecho2_VentasCadenasLinea, Hecho5_ComisionesCadena, Hecho6_ComisionesCadenaJuego
from admin_datamart.task import ObtenerPorcentaje
from admin_juego.models import TipoProducto, Sorteo, apuesta, ModalidadJuego, Fechas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_funtions import get_decimal_is_not_none
from admin_lib.util_views import MyViewBase, ReportsBaseView
from admin_reportes.forms import (
    FilterCodigoForm, FilterDeportesForm, FilterFechasForm, FilterOrdenPresentacionReporteForm,
)
from django.contrib import messages
from django.db.models import Sum
from django.template import defaultfilters
from django.utils.timezone import now
from django.views.generic import TemplateView


class VentasProcesadas(MyViewBase, TemplateView):
    template_name = 'admin_reportes/ventas/ventas-procesadas.html'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        self.context = super(VentasProcesadas, self).get_context_data(**kwargs)
        kwargs_form = {
            'presentacion_add': [('fecha', 'Fechas')]
        }
        if self.request.method == 'GET':
            self.context['form_cadena'] = FilterCadenaComercializacionForm(
                **self.get_form_kwargs()
            )
            self.context['form_deporte'] = FilterDeportesForm()

            self.context['form_fecha'] = FilterFechasForm()

            self.context['form_agrupado'] = FilterOrdenPresentacionReporteForm(
                **kwargs_form
            )

            self.context['form_fecha'].fields['fecha_inicio'].initial = (now() - timedelta(days=1)) \
                .strftime(FORMAT_STR_DATE_REPORTS)

            self.context['form_fecha'].fields['fecha_fin'].initial = \
                self.context['form_fecha'].fields['fecha_inicio'].initial

            self.context['form_codigo'] = FilterCodigoForm()

            return self.context

        return self.context


class VentasProcesadasProcessView(ReportsBaseView):
    pdf_url = 'admin_reportes_venta_procesadas_print_pdf'
    csv_url = 'admin_reportes_venta_procesadas_print_csv'
    datatable_url = 'admin_reportes_ventas_procesadas_list_datatable'

    template_print = 'admin_reportes/ventas/ventas-procesadas-print.html'
    name_report = 'Ventas procesadas'
    codename_report = 'ventas_procesadas'

    def get_valid_columns(self):
        super(VentasProcesadasProcessView, self).get_valid_columns()
        self.show_queda = False

    def get_hecho_venta(self):

        keys_use_hecho6 = [
            'deporte',
            'temporada',
            'encuentro',
            'grupo_modalidad',
            'modalidad',
            'condicion'
        ]
        self.use_hecho6 = False
        for pos in range(0, len(keys_use_hecho6)):
            if self.request.GET.get(keys_use_hecho6[pos]):
                self.use_hecho6 = True
                break
        if not self.use_hecho6:
            if self.agrupado == 'parley':
                self.use_hecho6 = True

        if self.use_hecho6:
            self.ventas = Hecho6_ComisionesCadenaJuego.objects.filter(
                tiempo__fecha__range=(
                    self.fecha_inicio,
                    self.fecha_fin
                )
            )
        else:
            if self.request.GET.get('data_process'):
                self.ventas = Hecho5_ComisionesCadena.objects.filter(
                    tiempo__fecha__range=(
                        self.fecha_inicio,
                        self.fecha_fin
                    )
                )
            else:
                self.ventas = Hecho2_VentasCadenasLinea.objects.filter(
                    tiempo__fecha__range=(
                        self.fecha_inicio,
                        self.fecha_fin
                    )
                )

    def get_titles_for_comercializacion(self):
        titles = []
        verbose_name_hijos = ''
        if self.pertenece.get_offspring().exists():
            verbose_name_hijos = self.pertenece.get_offspring()[
                0].get_verbose_name_plural()

        titles.append({'text': 'Nro', 'width': '5%'})
        titles.append({'text': verbose_name_hijos, 'width': '25%'})
        titles.append({'text': 'Venta', 'width': '10%'})
        titles.append({'text': 'Premios', 'width': '10%'})

        if self.show_comision:
            titles.append({'text': 'Comision', 'width': '10%'})

        if self.show_regalia:
            titles.append({'text': 'Servicios', 'width': '10%'})

        if self.show_queda:
            titles.append({'text': 'Queda', 'width': '10%'})

        if self.show_participacion:
            titles.append({'text': 'Saldo', 'width': '15%'})

        titles.append({'text': 'Operador', 'width': '15%'})
        return titles

    def get_titles_for_fecha(self):
        titles = [
            {'text': 'Nro', 'width': '5%'},
            {'text': 'Fecha', 'width': '10%'},
            {'text': 'Dia de la semana', 'width': '15%'},
            {'text': 'Venta', 'width': '10%'},
            {'text': 'Premios', 'width': '10%'},
        ]

        if self.show_comision:
            titles.append(
                {'text': 'Comision', 'width': '10%'},
            )
        if self.show_regalia:
            titles.append(
                {'text': 'Servicios', 'width': '10%'},
            )
        if self.show_queda:
            titles.append(
                {'text': 'Queda', 'width': '10%'},
            )
        if self.show_participacion:
            titles.append(
                {'text': 'Saldo', 'width': '15%'},
            )

        titles.append(
            {'text': 'Operador', 'width': '15%'}
        )
        return titles

    def get_titles_for_parley(self):
        titles = []
        titles.append({'text': 'Nro.', 'width': '5%'})

        if self.modalidad:
            titles.append({"text": "Condicion", "width": "30%"})
        elif self.grupo_modalidad:
            titles.append({"text": "Modalidad", "width": "30%"})
        elif self.encuentro:
            titles.append({"text": "Grupo", "width": "30%"})
        elif self.temporada:
            titles.append({"text": "Sorteo", "width": "30%"})
            titles.append({"text": "Fecha", "width": "10%"})
            titles.append({"text": "Hora", "width": "10%"})
        elif self.deporte:
            titles.append({"text": "Liga", "width": "30%"})
        else:
            titles.append({"text": "Deporte", "width": "30%"})

        titles.append({'text': 'Venta', 'width': '10%'})
        titles.append({'text': 'Premios', 'width': '10%'})

        if self.show_comision:
            titles.append({'text': 'Comision', 'width': '10%'})
        if self.show_regalia:
            titles.append({'text': 'Servicios', 'width': '10%'})
        if self.show_queda:
            titles.append({'text': 'Queda', 'width': '10%'})
        if self.show_participacion:
            titles.append({'text': 'Saldo', 'width': '15%'})

        titles.append({'text': 'Operador', 'width': '15%'})

        return titles

    def get_titles_for_agencia(self):
        titles = []

        titles.append({'text': 'N°', 'width': '5%'})
        if self.all_query:
            titles.append({'text': 'Codigo', 'width': '15%'})
        titles.append({'text': 'Centros de apuesta', 'width': '25%'})
        titles.append({'text': 'Venta', 'width': '10%'})
        titles.append({'text': 'Premios', 'width': '10%'})

        if self.show_comision:
            titles.append({'text': 'Comision', 'width': '10%'})

        if self.show_regalia:
            titles.append({'text': 'Servicios', 'width': '10%'})

        if self.show_queda:
            titles.append({'text': 'Queda', 'width': '10%'})

        if self.show_participacion:
            titles.append({'text': 'Saldo', 'width': '15%'})

        titles.append({'text': 'Operador', 'width': '15%'})

        return titles

    def apply_presentation_for_comercializacion(self):
        data = {}

        if self.request.GET.get('data_process'):
            data['montos_sum'] = self.ventas.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),

                Sum('saldo_comer'),
                Sum('saldo_oper')
            )
            data['montos_sum']['venta__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['venta__sum']),
                2
            )
            data['montos_sum']['premio__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['premio__sum']),
                2
            )
            data['montos_sum']['comision__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['comision__sum']),
                2
            )
            data['montos_sum']['regalia__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['regalia__sum']),
                2
            )

            # Esta queda se inicializa en 0 xq es la sumatoria por
            # comercializadora
            data["montos_sum"]["queda_ref__sum"] = Decimal(0)

            data["montos_sum"]["saldo_comer__sum"] = round(
                get_decimal_is_not_none(
                    data["montos_sum"]["saldo_comer__sum"]),
                2
            )
            data['montos_sum']['saldo_oper__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
                2
            )

        else:
            data['montos_sum'] = self.ventas.aggregate(
                Sum('monto_total'),
                Sum('monto_premios'),
            )
            data['montos_sum']['venta__sum'] = round(
                get_decimal_is_not_none(
                    data['montos_sum']['monto_total__sum']),
                2
            )
            data['montos_sum']['premio__sum'] = round(
                get_decimal_is_not_none(
                    data['montos_sum']['monto_premios__sum']),
                2
            )
            data['montos_sum']['comision__sum'] = Decimal(0)
            data['montos_sum']['regalia__sum'] = Decimal(0)
            data["montos_sum"]["queda_ref__sum"] = 0
            data["montos_sum"]["saldo_comer__sum"] = 0
            data['montos_sum']['saldo_oper__sum'] = 0

        items = self.pertenece.get_offspring_ventas(self.ventas)

        data_cadena = []
        i = 1
        data['column_extra'] = '1'
        for item in items:
            item = item.get_object()
            data_interna_cadena = {}
            data_interna_cadena['pertenece'] = []
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, i, '')
            )
            i += 1

            texto = ''

            if item.prefix_filter != 'taquilla':
                texto = '<a href="#" class="link" onclick="{0}">{1}</a>'.format(
                    "NavegacionComercializacion({0},'{1}')".format(
                        item.pk,
                        item.prefix_filter
                    ),
                    item
                )

            else:
                texto = item.taquilla

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, texto, '')
            )

            venta_detalle = self.ventas.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
            )

            if self.request.GET.get('data_process'):
                montos = venta_detalle.aggregate(
                    Sum('venta'),
                    Sum('premio'),
                    Sum('comision'),
                    Sum('regalia'),
                    Sum('queda_ref'),
                    Sum('saldo_comer'),
                    Sum('saldo_oper')
                )
                if not montos['venta__sum']:
                    data_interna_cadena['pertenece'][1]['val'] = \
                        data_interna_cadena['pertenece'][1]['val'] \
                        .replace('NavegacionComercializacion', '') \
                        .replace('link', 'link-red').replace('<a', '<span').replace('a>', 'span>')

                # venta
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['venta__sum'] is None
                        else Decimal(round(montos['venta__sum'], 2))
                    )
                )

                # premios
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['premio__sum'] is None
                        else Decimal(round(montos['premio__sum'], 2)), ' link-red'
                    )
                )

                if self.show_comision:
                    # comision
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['comision__sum'] is None
                            else Decimal(round(montos['comision__sum'], 2))
                        )
                    )

                if self.show_regalia:
                    # regalia
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['regalia__sum'] is None
                            else Decimal(round(montos['regalia__sum'], 2))
                        )
                    )

                if self.show_queda:
                    # queda
                    queda_val = get_decimal_is_not_none(
                        montos['queda_ref__sum'])

                    if queda_val < 0:
                        queda_val = Decimal(0)

                    data["montos_sum"]["queda_ref__sum"] += queda_val

                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            round(queda_val, 2)
                        )
                    )

                if self.show_participacion:
                    # saldo
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['saldo_comer__sum'] is None
                            else Decimal(round(montos['saldo_comer__sum'], 2))
                        )
                    )

                # operador
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['saldo_oper__sum'] is None
                        else Decimal(round(montos['saldo_oper__sum'], 2))
                    )
                )
            else:
                montos = venta_detalle.aggregate(
                    Sum('monto_total'),
                    Sum('monto_premios'),
                )
                if not montos['monto_total__sum']:
                    data_interna_cadena['pertenece'][1]['val'] = \
                        data_interna_cadena['pertenece'][1]['val'] \
                        .replace('NavegacionComercializacion', '') \
                        .replace('link', 'link-red').replace('<a', '<span').replace('a>', 'span>')

                # venta
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['monto_total__sum'] is None
                        else Decimal(round(montos['monto_total__sum'], 2))
                    )
                )

                # premios
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['monto_premios__sum'] is None
                        else Decimal(round(montos['monto_premios__sum'], 2))
                    )
                )

                if self.show_comision:
                    # comision
                    porc_comision = ObtenerPorcentaje(
                        codename='porcentaje_comision',
                        cadena=item,
                        fecha=self.fecha_inicio
                    )
                    comision = Decimal(0) if montos['monto_total__sum'] is None else Decimal(
                        round(montos['monto_total__sum'] * porc_comision, 2))
                    data['montos_sum']['comision__sum'] += comision

                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            comision
                        )
                    )

                if self.show_regalia:
                    # regalia
                    porc_regalia = ObtenerPorcentaje(
                        codename='porcentaje_regalia',
                        cadena=item,
                        fecha=self.fecha_inicio
                    )
                    regalia = Decimal(0) if montos['monto_total__sum'] is None else Decimal(
                        round(montos['monto_total__sum'] * porc_regalia, 2))
                    data['montos_sum']['regalia__sum'] += regalia

                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            regalia
                        )
                    )

                if self.show_queda:
                    # queda
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            0
                        )
                    )

                if self.show_participacion:
                    # saldo
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal(0)
                        )
                    )

                # operador
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0)
                    )
                )

            data_cadena.append(data_interna_cadena)

        data['detalle'] = data_cadena

        if self.request.GET.get('data_process'):
            data['montos_sum']['queda_ref__sum'] = round(
                data['montos_sum']['queda_ref__sum'],
                2
            )

        # Agrupando totales
        data['totales'] = ['Total']
        for extra in data['column_extra']:
            data['totales'].append(
                ''
            )

        data['totales'].append(data['montos_sum']['venta__sum'])
        data['totales'].append(data['montos_sum']['premio__sum'])

        if self.show_comision:
            data['totales'].append(
                data['montos_sum']['comision__sum']
            )
        if self.show_regalia:
            data['totales'].append(
                data['montos_sum']['regalia__sum']
            )
        if self.show_queda:
            data['totales'].append(
                data['montos_sum']['queda_ref__sum']
            )
        if self.show_participacion:
            data['totales'].append(
                data['montos_sum']['saldo_comer__sum']
            )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        return data

    def apply_presentation_for_agencia(self):
        data = {}

        if self.request.GET.get('data_process'):
            data['montos_sum'] = self.ventas.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('saldo_comer'),
                Sum('saldo_oper'),
            )

            data['montos_sum_queda'] = self.ventas.filter(
                queda_ref__gt=0
            ).aggregate(
                Sum('queda_ref'),
            )

            data['montos_sum']['venta__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['venta__sum']),
                2
            )
            data['montos_sum']['premio__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['premio__sum']),
                2
            )
            data['montos_sum']['comision__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['comision__sum']),
                2
            )
            data['montos_sum']['regalia__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['regalia__sum']),
                2
            )
            data['montos_sum_queda']['queda_ref__sum'] = round(
                get_decimal_is_not_none(
                    data['montos_sum_queda']['queda_ref__sum']),
                2
            )
            data["montos_sum"]["saldo_comer__sum"] = round(
                get_decimal_is_not_none(data["montos_sum"]["saldo_comer__sum"]),
                2
            )
            data['montos_sum']['saldo_oper__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
                2
            )
        else:
            data['montos_sum'] = self.ventas.aggregate(
                Sum('monto_total'),
                Sum('monto_premios'),
            )

            data['montos_sum_queda'] = {}

            data['montos_sum']['venta__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['monto_total__sum']),
                2
            )
            data['montos_sum']['premio__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['monto_premios__sum']),
                2
            )
            data['montos_sum']['comision__sum'] = Decimal(0)
            data['montos_sum']['regalia__sum'] = Decimal(0)
            data['montos_sum_queda']['queda_ref__sum'] = Decimal(0)
            data["montos_sum"]["saldo_comer__sum"] = Decimal(0)
            data['montos_sum']['saldo_oper__sum'] = Decimal(0)

        # Paginacion #
        self.start = int(self.request.REQUEST.get('iDisplayStart', 0))
        if self.all_query is False:
            kwargs_filter = {}
            if self.codigo:
                kwargs_filter['codigo'] = self.codigo
            else:
                if self.pertenece.prefix_filter != 'agencia':
                    agencias_ids = list(self.ventas.distinct(
                        'comercializacion__agencia_id'
                    ).values_list('comercializacion__agencia_id', flat=True))
                    kwargs_filter['pk__in'] = agencias_ids
                else:
                    kwargs_filter['pk'] = self.pertenece.pk

            agencias = Agencias.objects.filter(
                **kwargs_filter).order_by('nombre')

            if self.codigo:
                self.ventas = self.ventas.filter(
                    comercializacion__agencia_id__in=list(
                        agencias.values_list('id', flat=True))
                )
            # Paginacion
            self.total_display_records = agencias.count()
            limit = min(
                int(self.request.REQUEST.get('iDisplayLength', 10)), 100)
            offset = self.start + limit
            self.pagin_process = False

            agencias = agencias[self.start:offset]
        ############################################################
        else:
            agencias = Agencias.objects.filter(
                **self.pertenece.get_kwargs_by_agencia()
            ).order_by('codigo')

        data_cadena = []
        i = self.start + 1
        data['column_extra'] = '1'
        for item in agencias:

            venta_detalle = self.ventas.filter(
                **item.get_kwargs_dimension_arco_comercializadora()
            )

            data_interna_cadena = {}
            data_interna_cadena['pertenece'] = []
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, i, '')
            )
            i += 1

            if self.all_query:
                codigo = item.codigo
                if item.codigo:
                    codigo = item.codigo
                else:
                    codigo = 'No aplica'

                data_interna_cadena["pertenece"].append(
                    self.type_html_conf(True, codigo, "")
                )

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, str(item), '')
            )

            if self.request.GET.get('data_process'):
                montos = venta_detalle.aggregate(
                    Sum('venta'),
                    Sum('premio'),
                    Sum('comision'),
                    Sum('regalia'),
                    Sum('queda_ref'),
                    Sum('saldo_comer'),
                    Sum('saldo_oper')
                )

                # venta
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['venta__sum'] is None
                        else Decimal(round(montos['venta__sum'], 2))
                    )
                )

                # premios
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['premio__sum'] is None
                        else Decimal(round(montos['premio__sum'], 2)), ' link-red'
                    )
                )

                if self.show_comision:
                    # comision
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['comision__sum'] is None
                            else Decimal(round(montos['comision__sum'], 2))
                        )
                    )

                if self.show_regalia:
                    # regalia
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['regalia__sum'] is None
                            else Decimal(round(montos['regalia__sum'], 2))
                        )
                    )

                if self.show_queda:
                    # queda
                    queda_val = get_decimal_is_not_none(montos['queda_ref__sum'])

                    if queda_val < 0:
                        queda_val = Decimal(0)

                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            round(queda_val, 2)
                        )
                    )

                if self.show_participacion:
                    # saldo
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['saldo_comer__sum'] is None
                            else Decimal(round(montos['saldo_comer__sum'], 2))
                        )
                    )

                # operador
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['saldo_oper__sum'] is None
                        else Decimal(round(montos['saldo_oper__sum'], 2))
                    )
                )
            else:
                montos = venta_detalle.aggregate(
                    Sum('monto_total'),
                    Sum('monto_premios'),
                )

                # venta
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['monto_total__sum'] is None
                        else Decimal(round(montos['monto_total__sum'], 2))
                    )
                )

                # premios
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['monto_premios__sum'] is None
                        else Decimal(round(montos['monto_premios__sum'], 2))
                    )
                )

                if self.show_comision:
                    # comision
                    porc_comision = ObtenerPorcentaje(
                        codename='porcentaje_comision',
                        cadena=item,
                        fecha=self.fecha_inicio
                    )
                    comision = Decimal(0) if montos['monto_total__sum'] is None else Decimal(
                        round(montos['monto_total__sum'] * porc_comision, 2))
                    data['montos_sum']['comision__sum'] += comision

                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            comision
                        )
                    )

                if self.show_regalia:
                    # regalia
                    porc_regalia = ObtenerPorcentaje(
                        codename='porcentaje_regalia',
                        cadena=item,
                        fecha=self.fecha_inicio
                    )
                    regalia = Decimal(0) if montos['monto_total__sum'] is None else Decimal(
                        round(montos['monto_total__sum'] * porc_regalia, 2))
                    data['montos_sum']['regalia__sum'] += regalia

                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            regalia
                        )
                    )

                if self.show_queda:
                    # queda
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            0
                        )
                    )

                if self.show_participacion:
                    # saldo
                    data_interna_cadena['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal(0)
                        )
                    )

                # operador
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0)
                    )
                )

            data_cadena.append(data_interna_cadena)

        data['detalle'] = data_cadena

        # Agrupando totales
        data['totales'] = ['Total']
        for extra in data['column_extra']:
            data['totales'].append(
                ''
            )
        if self.all_query:
            data['totales'].append('')
        data['totales'].append(data['montos_sum']['venta__sum'])
        data['totales'].append(data['montos_sum']['premio__sum'])

        if self.show_comision:
            data['totales'].append(
                data['montos_sum']['comision__sum']
            )
        if self.show_regalia:
            data['totales'].append(
                data['montos_sum']['regalia__sum']
            )
        if self.show_queda:
            data['totales'].append(
                data['montos_sum_queda']['queda_ref__sum']
            )
        if self.show_participacion:
            data['totales'].append(
                data['montos_sum']['saldo_comer__sum']
            )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        return data

    def apply_presentation_for_parley(self):
        data = {}

        data['column_extra'] = ''

        if self.modalidad and self.grupo_modalidad and self.encuentro:

            encuentros_modalidades = list(SorteoModalidades.objects.filter(
                encuentro_id=self.encuentro,
                modalidad_grupo__grupo_id=self.grupo_modalidad,
                modalidad_grupo__modalidad_id=self.modalidad
            ).distinct().values_list("pk", flat=True))

            self.ventas = self.ventas.filter(
                juegos__encuentros_modalidad_id__in=encuentros_modalidades,
            )

            filtro_juego = apuesta.objects.filter(
                encuentros_modalidad__encuentro_id=self.encuentro,
                encuentros_modalidad__modalidad_grupo__grupo_id=self.grupo_modalidad,
                condicion__modalidad_id=self.modalidad,
                origen__isnull=True
            )

            tipo = 6

        elif self.grupo_modalidad and self.encuentro:

            encuentro_modalidad_all = SorteoModalidades.objects.filter(
                encuentro_id=self.encuentro,
                modalidad_grupo__grupo_id=self.grupo_modalidad
            ).distinct("pk")

            self.ventas = self.ventas.filter(
                juegos__encuentros_modalidad_id__in=list(
                    encuentro_modalidad_all.values_list("pk", flat=True))
            )

            filtro_juego = ModalidadJuego.objects.filter(
                pk__in=list(
                    encuentro_modalidad_all.values_list(
                        "modalidad_grupo__modalidad_id",
                        flat=True))
            )

            tipo = 5

        elif self.encuentro:

            encuentro = Sorteo.objects.get(pk=self.encuentro)

            filtro_juego = encuentro.encuentrosmodalidades_set.all() \
                .distinct('modalidad_grupo__grupo_id')

            tipo = 4

        elif self.temporada:

            ini = self.fecha_inicio + hora_cero
            fin = self.fecha_fin + hora_23

            kwargs_1 = {}
            kwargs_2 = {}
            if self.pertenece.prefix_filter != 'master':
                kwargs_1['jornada__sistema'] = self.kwargs[
                    'object_sistema_juego']
                kwargs_2['jornada__sistema'] = self.kwargs[
                    'object_sistema_juego']

            kwargs_1['pk__in'] = list(
                self.ventas.filter(
                    juegos__temporada_id=self.temporada).values_list(
                    'juegos__encuentro_id',
                    flat=True).distinct('juegos__encuentro_id'))

            kwargs_2['jornada__temporadas_id'] = self.temporada
            kwargs_2['horajuego__range'] = (ini, fin)

            filtro_juego = Sorteo.objects.filter(
                **kwargs_1
            ).filter(**kwargs_2)

            tipo = 3
            data['column_extra'] = '12'

        elif self.deporte:

            kwargs = {}
            if self.pertenece.prefix_filter != 'master':
                kwargs['jornadas__sistema'] = self.kwargs[
                    'object_sistema_juego']
            kwargs['pk__in'] = list(
                self.ventas.filter(
                    juegos__deporte_id=self.deporte).values_list(
                    'juegos__temporada_id',
                    flat=True).distinct('juegos__temporada_id'))

            filtro_juego = Fechas.objects.filter(
                **kwargs
            ).distinct('pk')

            tipo = 2
        else:
            filtro_juego = TipoProducto.objects.filter(
                pk__in=list(self.ventas.values_list(
                    'juegos__deporte_id',
                    flat=True
                ).distinct('juegos__deporte_id'))
            )
            tipo = 1

        data['montos'] = Decimal('0.00')
        data['premios'] = Decimal('0.00')
        data['apuestas_count'] = 0
        data['montos_sum'] = self.ventas.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('regalia'),

            Sum('saldo_comer'),
            Sum('saldo_oper')
        )

        data['montos_sum']['venta__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['venta__sum']),
            2
        )
        data['montos_sum']['premio__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['premio__sum']),
            2
        )
        data['montos_sum']['comision__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['comision__sum']),
            2
        )
        data['montos_sum']['regalia__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['regalia__sum']),
            2
        )

        # Esta queda se inicializa en 0 xq es la sumatoria por comercializadora
        data["montos_sum"]["queda_ref__sum"] = Decimal(0)

        data["montos_sum"]["saldo_comer__sum"] = round(
            get_decimal_is_not_none(data["montos_sum"]["saldo_comer__sum"]),
            2
        )
        data['montos_sum']['saldo_oper__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
            2
        )

        data['column_extra'] += '1'

        data_juegos = []
        index = 1
        for item in filtro_juego:
            data_interna_juegos = {}
            data_interna_juegos['pertenece'] = []
            data_interna_juegos['pertenece'].append(
                self.type_html_conf(True, index, '')
            )
            index += 1

            if tipo == 1:  # por deporte
                venta_detalle = self.ventas.filter(
                    juegos__deporte_id=item.pk
                )

                texto = '<a href="#" class="link" onclick=Navegaciondeportes({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        item.nombre
                    )

                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto, '')
                )

            elif tipo == 2:  # por temporada
                venta_detalle = self.ventas.filter(
                    juegos__temporada_id=item.pk)

                texto = '<a href="#" class="link" onclick=Navegaciondeportes({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        item.torneo.nombre + " - " + item.nombre
                    )

                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto, '')
                )

            elif tipo == 3:  # por encuentros
                venta_detalle = self.ventas.filter(
                    juegos__encuentro_id=item.pk)

                campo = ''
                d_e = item.encuentrosdetail_set.all()
                equipo_len = d_e.count()
                i = 0
                for obj in d_e:
                    campo += obj.equipos_temporadas.equipo.nombre
                    i += 1
                    if (equipo_len > i):
                        campo += ' Vs. '

                texto = '<a href="#" class="link" onclick=Navegaciondeportes({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        campo
                    )

                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto, '')
                )
                objFecha = strFecha(item.horajuego)
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, objFecha.getFecha(), '')
                )
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, objFecha.getHora(), '')
                )

            elif tipo == 4:  # por grupos

                encuentro_modalidad_all = SorteoModalidades.objects.filter(
                    encuentro=item.encuentro,
                    modalidad_grupo__grupo=item.modalidad_grupo.grupo
                ).distinct()

                venta_detalle = self.ventas.filter(
                    juegos__encuentros_modalidad_id__in=list(
                        encuentro_modalidad_all.values_list('pk', flat=True))
                )

                texto = '<a href="#" class="link" onclick=Navegaciondeportes({0},"{1}")>{2}</a>'\
                    .format(
                        item.modalidad_grupo.grupo_id,
                        item.modalidad_grupo.prefix_filter,
                        item.modalidad_grupo.grupo.nombre
                    )

                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto, '')
                )

            elif tipo == 5:  # por modalidades

                venta_detalle = self.ventas.filter(
                    juegos__modalidad_id=item.pk
                )

                texto = '<a href="#" class="link" onclick=Navegaciondeportes({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        item.modalidad
                    )

            elif tipo == 6:  # por condiciones
                venta_detalle = self.ventas.filter(
                    juegos__pertenece=item.get_pertenece(),
                    juegos__condicion_id=item.condicion.pk,
                    juegos__modalidad_id=item.condicion.modalidad.pk,
                )

                texto = item.get_pertenece()
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, item.get_pertenece(), '')
                )

            montos = venta_detalle.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('queda_ref'),
                Sum('saldo_comer'),
                Sum('saldo_oper')
            )

            if not montos['venta__sum']:
                data_interna_juegos['pertenece'][1]['val'] = \
                    data_interna_juegos['pertenece'][1]['val'].replace('Navegaciondeportes', '') \
                    .replace('link', 'link-red').replace('<a', '<span') \
                    .replace('a>', 'span>')

            # venta
            data_interna_juegos['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal('0.00') if montos['venta__sum'] is None
                    else Decimal(round(montos['venta__sum'], 2))
                )
            )

            # premios
            data_interna_juegos['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal('0.00') if montos['premio__sum'] is None
                    else Decimal(round(montos['premio__sum'], 2))
                )
            )

            if self.show_comision:
                # comision
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['comision__sum'] is None
                        else Decimal(round(montos['comision__sum'], 2))
                    )
                )

            if self.show_regalia:
                # regalia
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['regalia__sum'] is None
                        else Decimal(round(montos['regalia__sum'], 2))
                    )
                )

            if self.show_queda:
                # queda
                queda_val = round(
                    get_decimal_is_not_none(montos['queda_ref__sum']),
                    2
                )

                if queda_val < 0:
                    queda_val = Decimal(0)

                data["montos_sum"]["queda_ref__sum"] += queda_val

                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(
                        False,
                        queda_val
                    )
                )

            if self.show_participacion:
                # saldo
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['saldo_comer__sum'] is None
                        else Decimal(round(montos['saldo_comer__sum'], 2))
                    )
                )

            # operador
            data_interna_juegos['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal('0.00') if montos['saldo_oper__sum'] is None
                    else Decimal(round(montos['saldo_oper__sum'], 2))
                )
            )

            data_juegos.append(data_interna_juegos)

        data['detalle'] = data_juegos

        data['montos_sum']['queda_ref__sum'] = round(
            data['montos_sum']['queda_ref__sum'],
            2
        )

        # Agrupando totales
        data['totales'] = [
            'Total',
        ]

        for extra in data['column_extra']:
            data['totales'].append(
                ' '
            )

        data['totales'].append(
            data['montos_sum']['venta__sum']
        )
        data['totales'].append(
            data['montos_sum']['premio__sum']
        )

        if self.show_comision:
            data['totales'].append(
                data['montos_sum']['comision__sum']
            )
        if self.show_regalia:
            data['totales'].append(
                data['montos_sum']['regalia__sum']
            )
        if self.show_queda:
            data['totales'].append(
                data['montos_sum']['queda_ref__sum']
            )
        if self.show_participacion:
            data['totales'].append(
                data['montos_sum']['saldo_comer__sum']
            )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        return data

    def apply_presentation_for_fecha(self):
        data = {}
        fechas = []
        inicio = datetime.strptime(self.fecha_inicio, FORMAT_STR_DATE_REPORTS)
        fin = datetime.strptime(self.fecha_fin, FORMAT_STR_DATE_REPORTS)
        dias = (fin - inicio).days

        if dias > 0:
            fechas.append(self.fecha_inicio)
            for i in range(1, int(dias)):
                f = inicio + timedelta(days=i)
                fechas.append(strFecha(f).getFecha())
            fechas.append(self.fecha_fin)
        elif dias == 0:
            fechas.append(self.fecha_fin)

        if self.request.GET.get('data_process'):
            data['montos_sum'] = self.ventas.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('queda_ref'),
                Sum('saldo_comer'),
                Sum('saldo_oper')
            )

            data['montos_sum']['venta__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['venta__sum']),
                2
            )
            data['montos_sum']['premio__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['premio__sum']),
                2
            )
            data['montos_sum']['comision__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['comision__sum']),
                2
            )
            data['montos_sum']['regalia__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['regalia__sum']),
                2
            )
            data["montos_sum"]["queda_ref__sum"] = round(
                get_decimal_is_not_none(data["montos_sum"]["queda_ref__sum"]),
                2
            )
            data["montos_sum"]["saldo_comer__sum"] = round(
                get_decimal_is_not_none(data["montos_sum"]["saldo_comer__sum"]),
                2
            )
            data['montos_sum']['saldo_oper__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
                2
            )
        else:
            data['montos_sum'] = self.ventas.aggregate(
                Sum('monto_total'),
                Sum('monto_premios'),
            )

            data['montos_sum']['venta__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['monto_total__sum']),
                2
            )
            data['montos_sum']['premio__sum'] = round(
                get_decimal_is_not_none(data['montos_sum']['monto_premios__sum']),
                2
            )
            data['montos_sum']['comision__sum'] = Decimal(0)
            data['montos_sum']['regalia__sum'] = Decimal(0)
            data["montos_sum"]["queda_ref__sum"] = Decimal(0)
            data["montos_sum"]["saldo_comer__sum"] = Decimal(0)
            data['montos_sum']['saldo_oper__sum'] = Decimal(0)

        data['column_extra'] = '12'
        data_cadena = []
        indice = 1
        for i in fechas:
            json_interno = {}
            fecha = datetime.strptime(i, FORMAT_STR_DATE_REPORTS)
            fecha_date = datetime.date(fecha)

            json_interno['pertenece'] = []
            json_interno['pertenece'].append(
                self.type_html_conf(True, indice, '')
            )
            indice += 1

            venta_detalle = self.ventas.filter(
                tiempo__fecha=i
            )

            if self.request.GET.get('data_process'):
                montos = venta_detalle.aggregate(
                    Sum('venta'),
                    Sum('premio'),
                    Sum('comision'),
                    Sum('regalia'),
                    Sum('queda_ref'),
                    Sum('saldo_comer'),
                    Sum('saldo_oper')
                )

                add_class = ''
                if montos['venta__sum'] is None or montos['venta__sum'] == 0:
                    add_class = ' link-red'

                # ftexto
                json_interno['pertenece'].append(
                    self.type_html_conf(True, i, add_class)
                )
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        True,
                        defaultfilters.date(
                            fecha_date, "l"
                        ).capitalize(),
                        add_class
                    )
                )

                # venta
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['venta__sum'] is None
                        else Decimal(round(montos['venta__sum'], 2))
                    )
                )

                # premios
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['premio__sum'] is None
                        else Decimal(round(montos['premio__sum'], 2)),
                        ' link-red'
                    )
                )

                if self.show_comision:
                    # comision
                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['comision__sum'] is None
                            else Decimal(round(montos['comision__sum'], 2))
                        )
                    )

                if self.show_regalia:
                    # regalia
                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['regalia__sum'] is None
                            else Decimal(round(montos['regalia__sum'], 2))
                        )
                    )

                if self.show_queda:
                    # queda
                    queda_val = get_decimal_is_not_none(montos['queda_ref__sum'])
                    if queda_val < 0:
                        queda_val = Decimal(0)

                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            round(queda_val, 2)
                        )
                    )

                if self.show_participacion:
                    # saldo
                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal('0.00') if montos['saldo_comer__sum'] is None
                            else Decimal(round(montos['saldo_comer__sum'], 2))
                        )
                    )

                # operador
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal('0.00') if montos['saldo_oper__sum'] is None
                        else Decimal(round(montos['saldo_oper__sum'], 2))
                    )
                )
            else:
                montos = venta_detalle.aggregate(
                    Sum('monto_total'),
                    Sum('monto_premios'),
                )

                add_class = ''
                if montos['monto_total__sum'] is None or montos['monto_total__sum'] == 0:
                    add_class = ' link-red'

                # ftexto
                json_interno['pertenece'].append(
                    self.type_html_conf(True, i, add_class)
                )
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        True,
                        defaultfilters.date(
                            fecha_date, "l"
                        ).capitalize(),
                        add_class
                    )
                )

                # venta
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['monto_total__sum'] is None
                        else Decimal(round(montos['monto_total__sum'], 2))
                    )
                )

                # premios
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['monto_premios__sum'] is None
                        else Decimal(round(montos['monto_premios__sum'], 2))
                    )
                )

                if self.show_comision:
                    # comision
                    porc_comision = ObtenerPorcentaje(
                        codename='porcentaje_comision',
                        cadena=self.pertenece,
                        fecha=fecha_date
                    )
                    comision = Decimal(0) if montos['monto_total__sum'] is None else Decimal(
                        round(montos['monto_total__sum'] * porc_comision, 2))
                    data['montos_sum']['comision__sum'] += comision

                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            comision
                        )
                    )

                if self.show_regalia:
                    # regalia
                    porc_regalia = ObtenerPorcentaje(
                        codename='porcentaje_regalia',
                        cadena=self.pertenece,
                        fecha=fecha_date
                    )
                    regalia = Decimal(0) if montos['monto_total__sum'] is None else Decimal(
                        round(montos['monto_total__sum'] * porc_regalia, 2))
                    data['montos_sum']['regalia__sum'] += regalia

                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            regalia
                        )
                    )

                if self.show_queda:
                    # queda
                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            0
                        )
                    )

                if self.show_participacion:
                    # saldo
                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            False,
                            Decimal(0)
                        )
                    )

                # operador
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0)
                    )
                )

            data_cadena.append(json_interno)

        data['detalle'] = data_cadena

        data['montos_sum']['queda_ref__sum'] = round(
            data['montos_sum']['queda_ref__sum'],
            2
        )

        # Agrupando totales
        data['totales'] = [
            'Total',
            ' ',
            ' ',
            data['montos_sum']['venta__sum'],
            data['montos_sum']['premio__sum'],
        ]

        if self.show_comision:
            data['totales'].append(
                data['montos_sum']['comision__sum']
            )
        if self.show_regalia:
            data['totales'].append(
                data['montos_sum']['regalia__sum']
            )
        if self.show_queda:
            data['totales'].append(
                data['montos_sum']['queda_ref__sum']
            )
        if self.show_participacion:
            data['totales'].append(
                data['montos_sum']['saldo_comer__sum']
            )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        return data


class VentasProcesadasDatatableView(
        VentasProcesadasProcessView, BaseDatatableView):
    # Orden del filtro
    order_columns = None

    def get_initial_queryset(self):
        if self.pertenece.prefix_filter == 'agencia':
            messages.warning(
                self.request,
                'El nivel de taquilla no posee ajustes de porcentajes'
            )

        fecha_inicio = datetime.strptime(
            self.fecha_inicio, FORMAT_STR_DATE_REPORTS)
        fecha_fin = datetime.strptime(self.fecha_fin, FORMAT_STR_DATE_REPORTS)
        fecha_limite = now()

        if fecha_inicio > fecha_limite or fecha_fin > fecha_limite:
            messages.warning(
                self.request,
                'No hay ventas disponibles para esta fechas'
            )
            return []
        elif (fecha_fin - fecha_inicio).days > 31:
            messages.warning(
                self.request,
                'Solo se puede consultar maximo un mes'
            )
            return []

        self.get_hecho_venta()

        if not self.ventas.exists():
            messages.warning(
                self.request,
                'No hay ventas disponibles para esta fechas'
            )
            return []
        else:
            if self.use_hecho6:
                messages.info(self.request,
                              MESSAGES_GLOBAL['consulta_por_juegos'])

        self.apply_filter_cadena()
        self.apply_filter_juego()
        self.execute_query()

        if self.pertenece.get_exists_get_tickets_is_day_unprocessed(
            fecha=fecha_inicio, fecha_fin=fecha_fin
        ):
            messages.warning(
                self.request,
                'ADVERTENCIA! Aún hay ventas que no han sido procesadas'
            )

        qs = self.content
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        if qs:
            json_data = self.prepare_results_for_venta(qs)
        return json_data

    def prepare_footeresults(self, qs):
        footer = []
        if qs:
            footer = self.prepare_footer_for_venta()
        return footer
