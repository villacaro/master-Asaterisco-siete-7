# -*- coding: utf-8 -*-
import datetime
from datetime import timedelta
from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME, FORMAT_STR_DATE_REPORTS
from admin_comercializacion.models import Agencias
from admin_datamart.models import Hecho5_ComisionesCadena, Hecho9_VentasSaldosCadena
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import strFecha
from admin_lib.util_forms import FilterCadenaComercializacionSimpleForm
from admin_lib.util_funtions import get_decimal_is_not_none
from admin_lib.util_views import MyViewBase, ReportsBaseView
from admin_reportes.forms import FilterFechasForm, FilterOrdenPresentacionReporteCuadreForm
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.template import defaultfilters
from django.views.generic import TemplateView


class CuadreParley(MyViewBase, TemplateView):
    template_name = 'admin_reportes/cuadres/cuadre_parley.html'

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(CuadreParley, self).get_context_data(**kwargs)

        if self.request.method == 'GET':
            context['form_agrupado'] = FilterOrdenPresentacionReporteCuadreForm()

            context['form_fecha'] = FilterFechasForm()

            context['form_cadena'] = FilterCadenaComercializacionSimpleForm(
                **self.get_form_kwargs()
            )
            context['form_cadena'].is_valid()

        context['form_fecha'].inicializar(
            tipo='FechasParley',
            comer=self.object_comercializadora.get_object()
        )
        return context


class CuadreParleyProcessView(ReportsBaseView):
    pdf_url = 'admin_reportes_cuadre_parley_print_pdf'
    csv_url = 'admin_reportes_cuadre_parley_print_csv'
    datatable_url = 'admin_reportes_cuadre_parley_list_datatable'

    template_print = 'admin_reportes/cuadres/cuadres-print.html'
    name_report = 'Cuadre Parley'
    codename_report = 'cuadre_parley'

    def execute_all_process(self):
        self.get_hecho_venta()
        if self.agrupado != 'fecha':
            self.apply_filter_cadena()
        self.apply_filter_juego()
        self.execute_query()
        self.set_cache()

        cache.set(
            self.get_key_report(),
            self.cache_key,
            CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
        )

    def get_hecho_venta(self):
        self.ventas = Hecho5_ComisionesCadena.objects.filter(
            tiempo__fecha__range=(self.fecha_inicio, self.fecha_fin)
        )

        self.saldos = Hecho9_VentasSaldosCadena.objects.filter(
            tiempo__fecha__range=(self.fecha_inicio, self.fecha_fin)
        )

    def apply_filter_cadena(self):
        if self.pertenece.prefix_filter == 'master':
            self.ventas = self.ventas.filter(
                comercializacion__operadora_id__in=list(
                    self.pertenece.get_offspring().values_list(
                        'pk', flat=True)),
                comercializacion__bloque_id__isnull=False
            )
            self.saldos = self.saldos.filter(
                comercializacion__operadora_id__in=list(
                    self.pertenece.get_offspring().values_list(
                        'pk', flat=True)),
                comercializacion__bloque_id__isnull=False
            )
        else:
            if self.agrupado == 'agencia' or self.pertenece.prefix_filter == 'agencia':
                self.ventas = self.ventas.filter(
                    ** self.pertenece.get_kwargs_hijos_agencia_dimension_arco_comercializadora()
                )
                self.saldos = self.saldos.filter(
                    ** self.pertenece.get_kwargs_hijos_agencia_dimension_arco_comercializadora()
                )
            else:
                self.ventas = self.ventas.filter(
                    ** self.pertenece.get_kwargs_hijos_dimension_arco_comercializadora()
                )
                self.saldos = self.saldos.filter(
                    ** self.pertenece.get_kwargs_hijos_dimension_arco_comercializadora()
                )

    def get_titles_for_comercializacion(self):
        titles = []

        verbose_name_hijos = ''
        if self.pertenece.get_offspring():
            if self.pertenece.prefix_filter == 'agencia':
                verbose_name_hijos = self.pertenece._meta.verbose_name
            else:
                verbose_name_hijos = self.pertenece.get_offspring()[0].get_verbose_name_plural()

        titles.append({'text': 'Nro', 'width': '5%'})
        titles.append({'text': verbose_name_hijos, 'width': '30%'})
        titles.append({'text': 'Saldo anterior', 'width': '8%'})
        titles.append({'text': 'Utilidad', 'width': '8%'})
        titles.append({'text': 'Queda', 'width': '8%'})
        titles.append({'text': 'Saldo', 'width': '8%'})
        titles.append(
            {'text': self.pertenece.get_verbose_name(), 'width': '8%'})
        titles.append({'text': 'Depositos', 'width': '8%'})
        titles.append({'text': 'Pagos', 'width': '8%'})
        titles.append({'text': 'Ajustes', 'width': '8%'})
        titles.append({'text': 'Cargos', 'width': '8%'})
        titles.append({'text': 'Saldo Actual', 'width': '8%'})

        return titles

    def apply_presentation_for_comercializacion(self):
        data = {}

        # Montos
        data['montos_sum'] = self.ventas.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('regalia'),
            Sum('saldo_bruto'),
            Sum('saldo_comer'),
            Sum('saldo_oper'),
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
        data['montos_sum']['saldo_bruto__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_bruto__sum']),
            2
        )
        data['montos_sum']['saldo_comer__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_comer__sum']),
            2
        )
        data['montos_sum']['saldo_oper__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
            2
        )

        # saldo
        data['saldos_sum'] = self.saldos.aggregate(
            Sum('queda_corte'),
            Sum('saldo_anterior'),
            Sum('depositos'),
            Sum('pagos'),
            Sum('ajustes'),
            Sum('cargos'),
            Sum('saldo_actual')
        )

        data['saldos_sum']['queda_corte__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['queda_corte__sum']),
            2
        )
        data['saldos_sum']['saldo_anterior__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['saldo_anterior__sum']),
            2
        )
        data['saldos_sum']['depositos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['depositos__sum']),
            2
        )
        data['saldos_sum']['pagos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['pagos__sum']),
            2
        )
        data['saldos_sum']['ajustes__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['ajustes__sum']),
            2
        )
        data['saldos_sum']['cargos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['cargos__sum']),
            2
        )
        data['saldos_sum']['saldo_actual__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['saldo_actual__sum']),
            2
        )

        data['montos_sum']['utilidad__sum'] = data[
            'montos_sum']['saldo_bruto__sum']
        data['montos_sum']['queda__sum'] = 0

        if self.pertenece.prefix_filter != 'agencia':
            items = self.pertenece.get_offspring_ventas(self.ventas)
            items = items | self.pertenece.get_offspring_ventas(
                self.saldos.exclude(
                    saldo_anterior=0
                )
            )
        else:
            self.force_agencia = self.pertenece
            self.pertenece = self.pertenece.distribuidores
            items = self.pertenece.get_offspring_ventas(self.ventas).filter(
                agencia_id=self.force_agencia.pk
            )

        # sum_queda = 0
        index = 0
        data_cadena = []
        for item in items:
            index += 1
            item = item.get_object()

            data_interna_cadena = {}
            data_interna_cadena['pertenece'] = []

            texto = ''
            if item.prefix_filter != 'agencia':
                texto = '<a href="#"" class="link" onclick="{0}">{1}</a>'.format(
                    "NavegacionComercializacion({0},'{1}')".format(
                        item.pk,
                        item.prefix_filter
                    ),
                    item
                )
            else:
                texto = str(item)

            # Nro
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(False, index, '')
            )

            # Nombre comercializador
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, texto, '')
            )

            # Filtro datos del hecho5 por cadena
            venta_detalle = self.ventas.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
            )

            montos = venta_detalle.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('queda_ref'),
                Sum('saldo_bruto'),
                Sum('saldo_comer'),
                Sum('saldo_oper'),
            )

            if not montos['venta__sum']:
                data_interna_cadena['pertenece'][1]['val'] = \
                    data_interna_cadena['pertenece'][1]['val'].replace('NavegacionComercializacion', '') \
                    .replace('link', 'link-red').replace('<a', '<span').replace('a>', 'span>')

            saldo_detalle = self.saldos.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
            )

            saldos_montos = saldo_detalle.aggregate(
                Sum('queda_corte'),
                Sum('depositos'),
                Sum('pagos'),
                Sum('ajustes'),
                Sum('cargos'),
            )

            saldo_anterior = 0
            try:
                saldo_anterior = saldo_detalle.get(
                    tiempo__fecha=self.ini).saldo_anterior
            except Exception:
                pass

            # saldo anterior
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    round(saldo_anterior, 2)
                )
            )

            utilidad = Decimal(str('0.00')) if montos['saldo_bruto__sum'] is None \
                else Decimal(round(montos['saldo_bruto__sum'], 2))

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    utilidad
                )
            )

            '''
            # Contamos los días
            dias = (self.fin - self.ini).days
            frecuencia = item.get_frecuencia_queda()
            show_queda = False

            if frecuencia == 'frecuencia_semanal':
                if dias == 6:
                    week = list(Funs.get_week_by_date(self.ini))
                    if self.ini == week[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_quincenal':
                if dias == 14:
                    quincena = list(Funs.get_quincena_by_date(self.fin))
                    if self.ini == quincena[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_mensual':
                if dias == (Funs.get_month_days(self.ini)[1] - 1):
                    if date(self.ini.year, self.ini.month,
                            self.ini.day) == Funs.first_day_of_month(self.ini):
                        show_queda = True


            # queda_corte
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(
                        str('0.00')) if saldos_montos['queda_corte__sum'] is None or not show_queda else Decimal(
                        round(
                            saldos_montos['queda_corte__sum'],
                            2))
                )
            )

            if saldos_montos['queda_corte__sum'] is not None and show_queda:
                sum_queda += saldos_montos['queda_corte__sum']
            '''
            # Cargos representados en queda
            if saldos_montos['cargos__sum'] is None:
                cargos = 0
            else:
                cargos = Decimal(round(saldos_montos['cargos__sum'], 2))
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    cargos
                )
            )

            # saldo
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(str('0.00')) if montos['saldo_comer__sum'] is None
                    else Decimal(round(montos['saldo_comer__sum'], 2))
                )
            )

            # operador
            if montos['saldo_oper__sum'] is None:
                operador = 0
            else:
                operador = Decimal(round(montos['saldo_oper__sum'], 2))

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    operador
                )
            )

            if True:
                # deposito
                if saldos_montos['depositos__sum'] is None:
                    depositos = 0
                else:
                    depositos = Decimal(
                        round(saldos_montos['depositos__sum'], 2))

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        depositos
                    )
                )

                # pago
                if saldos_montos['pagos__sum'] is None:
                    pagos = 0
                else:
                    pagos = Decimal(round(saldos_montos['pagos__sum'], 2))

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        pagos
                    )
                )

                # ajuste
                if saldos_montos['ajustes__sum'] is None:
                    ajustes = 0
                else:
                    ajustes = Decimal(round(saldos_montos['ajustes__sum'], 2))

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        ajustes
                    )
                )

                # cargo
                '''
                if saldos_montos['cargos__sum'] is None:
                    cargos = 0
                else:
                    cargos = Decimal(round(saldos_montos['cargos__sum'], 2))
                '''
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        0
                    )
                )

            # saldo_actual
            saldo_actual = (
                saldo_anterior +
                operador +
                depositos +
                pagos +
                ajustes -
                cargos)
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    round(saldo_actual, 2)
                )
            )

            data_cadena.append(data_interna_cadena)

        data['detalle'] = data_cadena

        # Agrupando totales
        data['totales'] = [
            'Total',
        ]

        data['totales'].append(
            ''
        )

        data['totales'].append(
            ''
        )

        data['totales'].append(
            data['montos_sum']['utilidad__sum']
        )

        data['totales'].append(
            # round(sum_queda, 2)
            data['saldos_sum']['cargos__sum']
        )

        data['totales'].append(
            data['montos_sum']['saldo_comer__sum']
        )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        data['totales'].append(
            data['saldos_sum']['depositos__sum']
        )

        data['totales'].append(
            data['saldos_sum']['pagos__sum']
        )

        data['totales'].append(
            data['saldos_sum']['ajustes__sum']
        )

        data['totales'].append(
            0
            # data['saldos_sum']['cargos__sum']
        )

        data['totales'].append(
            ''
        )

        return data

    def get_titles_for_fecha(self):
        if self.pertenece.nivel > 1:
            verbose_oper = self.pertenece.get_origen().get_verbose_name()
        else:
            verbose_oper = ''

        titles = [
            {
                'text': 'Fecha',
                'width': '15%'
            },
            {
                'text': 'Dia de la semana',
                'width': '15%'
            },
            {
                'text': 'Saldo anterior',
                'width': '10%'
            },
            {
                'text': 'Utilidad',
                'width': '10%'
            },
            {
                'text': 'Queda',
                'width': '10%'
            },
            {
                'text': 'Saldo',
                'width': '10%'
            },
            {
                'text': verbose_oper,
                'width': '10%'
            },
            {
                'text': 'Depositos',
                'width': '10%'
            },
            {
                'text': 'Pagos',
                'width': '10%'
            },
            {
                'text': 'Ajustes',
                'width': '10%'
            },
            {
                'text': 'Cargos',
                'width': '10%'
            },
            {
                'text': 'Saldo actual',
                'width': '10%'
            }
        ]
        return titles

    def apply_presentation_for_fecha(self):
        data = {}

        filtrado = False
        cadena_list = [
            'taquilla',
            'agencia',
            'distribuidor',
            'banca',
            'bloque',
            'operadora']
        for pos in range(0, len(cadena_list)):
            if self.request.GET.get(cadena_list[pos]):
                kwargs = {}
                filtrado = True
                if pos < 5:
                    kwargs[
                        'comercializacion__' +
                        cadena_list[pos + 1] + '_id__isnull'
                    ] = False
                kwargs[
                    'comercializacion__' + cadena_list[pos] + '_id'
                ] = self.request.GET.get(cadena_list[pos])
                self.ventas = self.ventas.filter(**kwargs)
                self.saldos = self.saldos.filter(**kwargs)
                break

        if not filtrado:
            self.apply_filter_cadena()

        fechas = []
        dias = (self.fin - self.ini).days

        if dias > 0:
            fechas.append(self.fecha_inicio)
            for i in range(1, int(dias)):
                f = self.ini + timedelta(days=i)
                fechas.append(strFecha(f).getFecha())
            fechas.append(self.fecha_fin)
        elif dias == 0:
            fechas.append(self.fecha_fin)

        # Montos
        data['montos_sum'] = self.ventas.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('regalia'),
            Sum('queda_ref'),
            Sum('saldo_comer'),
            Sum('saldo_oper'),
        )

        # saldos
        data['saldos_sum'] = self.saldos.aggregate(
            Sum('queda_corte'),
            Sum('saldo_anterior'),
            Sum('depositos'),
            Sum('pagos'),
            Sum('ajustes'),
            Sum('cargos'),
            Sum('saldo_actual')
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
        data['montos_sum']['queda_ref__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['queda_ref__sum']),
            2
        )
        data['montos_sum']['saldo_comer__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_comer__sum']),
            2
        )
        data['montos_sum']['saldo_oper__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
            2
        )

        data['saldos_sum']['queda_corte__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['queda_corte__sum']),
            2
        )

        data['saldos_sum']['saldo_anterior__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['saldo_anterior__sum']),
            2
        )
        data['saldos_sum']['depositos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['depositos__sum']),
            2
        )
        data['saldos_sum']['pagos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['pagos__sum']),
            2
        )
        data['saldos_sum']['ajustes__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['ajustes__sum']),
            2
        )
        data['saldos_sum']['cargos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['cargos__sum']),
            2
        )
        data['saldos_sum']['saldo_actual__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['saldo_actual__sum']),
            2
        )
        data['montos_sum']['utilidad__sum'] = data['montos_sum']['venta__sum'] - data['montos_sum']['premio__sum']\
            - data['montos_sum']['comision__sum'] - \
            data['montos_sum']['regalia__sum']

        data_cadena = []
        for i in fechas:

            fecha = datetime.datetime.strptime(i, FORMAT_STR_DATE_REPORTS)
            fecha_date = datetime.datetime.date(fecha)

            json_interno = {}
            json_interno['pertenece'] = []

            venta_detalle = self.ventas.filter(
                tiempo__fecha=i
            )
            saldo_detalle = self.saldos.filter(
                tiempo__fecha=i
            )

            montos = venta_detalle.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('queda_ref'),
                Sum('saldo_bruto'),
                Sum('saldo_comer'),
                Sum('saldo_oper')
            )

            saldos_montos = saldo_detalle.aggregate(
                Sum('queda_corte'),
                Sum('saldo_anterior'),
                Sum('depositos'),
                Sum('pagos'),
                Sum('ajustes'),
                Sum('cargos'),
                Sum('saldo_actual')
            )

            data['column_extra'] = '1'
            add_class = ''
            if montos['venta__sum'] is None or montos['venta__sum'] == 0:
                add_class = ' link-red'

            # texto
            json_interno['pertenece'].append(
                self.type_html_conf(True, i, add_class)
            )
            json_interno['pertenece'].append(
                self.type_html_conf(
                    True,
                    defaultfilters.date(
                        fecha_date, 'l'
                    ).capitalize(),
                    add_class
                )
            )

            # saldo anterior
            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal('0.00') if saldos_montos['saldo_anterior__sum'] is None
                    else Decimal(round(saldos_montos['saldo_anterior__sum'], 2))
                )
            )

            utilidad = Decimal(str('0.00')) if montos['saldo_bruto__sum'] is None \
                else Decimal(round(montos['saldo_bruto__sum'], 2))

            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    utilidad
                )
            )

            '''
            # Contamos los días
            dias = (self.fin - self.ini).days
            frecuencia = self.pertenece.get_frecuencia_queda()
            show_queda = False

            if frecuencia == 'frecuencia_semanal':
                if dias == 6:
                    week = list(Funs.get_week_by_date(self.ini))
                    if self.ini == week[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_quincenal':
                if dias == 14:
                    quincena = list(Funs.get_quincena_by_date(self.fin))
                    if self.ini == quincena[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_mensual':
                if dias == (Funs.get_month_days(self.ini)[1] - 1):
                    if date(self.ini.year, self.ini.month,
                            self.ini.day) == Funs.first_day_of_month(self.ini):
                        show_queda = True
            # queda
            queda_ref = 0
            queda_ref = 0 if not montos['queda_ref__sum'] \
                else Decimal(round(montos['queda_ref__sum'], 2))

            if queda_ref < 0:
                queda_ref = Decimal(0)

            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(
                        str('0.00')) if saldos_montos['queda_corte__sum'] is None or not show_queda else Decimal(
                        round(
                            saldos_montos['queda_corte__sum'],
                            2))
                )
            )
            '''
            # queda por cargo
            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(str('0.00')) if saldos_montos['cargos__sum'] is None
                    else Decimal(round(saldos_montos['cargos__sum'], 2))
                )
            )

            # saldo
            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(str('0.00')) if montos['saldo_comer__sum'] is None
                    else Decimal(round(montos['saldo_comer__sum'], 2))
                )
            )

            # operador
            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(str('0.00')) if montos['saldo_oper__sum'] is None
                    else Decimal(round(montos['saldo_oper__sum'], 2))
                )
            )

            if True:

                # deposito
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(str('0.00')) if saldos_montos['depositos__sum'] is None
                        else Decimal(round(saldos_montos['depositos__sum'], 2))
                    )
                )

                # pago
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(str('0.00')) if saldos_montos['pagos__sum'] is None
                        else Decimal(round(saldos_montos['pagos__sum'], 2))
                    )
                )

                # ajuste
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(str('0.00')) if saldos_montos['ajustes__sum'] is None
                        else Decimal(round(saldos_montos['ajustes__sum'], 2))
                    )
                )

                # cargo
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        0
                        # Decimal(str('0.00')) if saldos_montos['cargos__sum'] is None
                        # else Decimal(round(saldos_montos['cargos__sum'], 2))
                    )
                )

            # saldo actual
            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(str('0.00')) if saldos_montos['saldo_actual__sum'] is None
                    else Decimal(round(saldos_montos['saldo_actual__sum'], 2))
                )
            )
            data_cadena.append(json_interno)

        data['detalle'] = data_cadena

        # Agrupando totales
        data['totales'] = [
            'Total',
            '',
        ]

        data['totales'].append(
            ''
        )

        data['totales'].append(
            data['montos_sum']['utilidad__sum']
        )

        data['totales'].append(
            data['saldos_sum']['cargos__sum']
            # data['saldos_sum']['queda_corte__sum']
        )

        data['totales'].append(
            data['montos_sum']['saldo_comer__sum']
        )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        data['totales'].append(
            data['saldos_sum']['depositos__sum']
        )

        data['totales'].append(
            data['saldos_sum']['pagos__sum']
        )

        data['totales'].append(
            data['saldos_sum']['ajustes__sum']
        )

        data['totales'].append(
            0
            # data['saldos_sum']['cargos__sum']
        )

        data['totales'].append(
            ''
        )

        return data

    def get_titles_for_agencia(self):
        titles = []

        titles.append({'text': 'Nro', 'width': '5%'})
        if self.all_query:
            titles.append({'text': 'Codigo', 'width': '15%'})
        titles.append({'text': 'Centro de apuesta', 'width': '30%'})
        titles.append({'text': 'Saldo anterior', 'width': '8%'})
        titles.append({'text': 'Utilidad', 'width': '8%'})
        titles.append({'text': 'Queda', 'width': '8%'})
        titles.append({'text': 'Saldo', 'width': '8%'})
        titles.append({'text': 'Distribuidor', 'width': '8%'})
        titles.append({'text': 'Depositos', 'width': '8%'})
        titles.append({'text': 'Pagos', 'width': '8%'})
        titles.append({'text': 'Ajustes', 'width': '8%'})
        titles.append({'text': 'Cargos', 'width': '8%'})
        titles.append({'text': 'Saldo Actual', 'width': '8%'})

        return titles

    def apply_presentation_for_agencia(self):
        data = {}

        # Montos
        data['montos_sum'] = self.ventas.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('regalia'),
            Sum('saldo_bruto'),
            Sum('saldo_comer'),
            Sum('saldo_oper'),
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
        data['montos_sum']['saldo_bruto__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_bruto__sum']),
            2
        )
        data['montos_sum']['saldo_comer__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_comer__sum']),
            2
        )
        data['montos_sum']['saldo_oper__sum'] = round(
            get_decimal_is_not_none(data['montos_sum']['saldo_oper__sum']),
            2
        )

        # saldo
        data['saldos_sum'] = self.saldos.aggregate(
            Sum('queda_corte'),
            Sum('saldo_anterior'),
            Sum('depositos'),
            Sum('pagos'),
            Sum('ajustes'),
            Sum('cargos'),
            Sum('saldo_actual')
        )

        data['saldos_sum']['queda_corte__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['queda_corte__sum']),
            2
        )
        data['saldos_sum']['saldo_anterior__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['saldo_anterior__sum']),
            2
        )
        data['saldos_sum']['depositos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['depositos__sum']),
            2
        )
        data['saldos_sum']['pagos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['pagos__sum']),
            2
        )
        data['saldos_sum']['ajustes__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['ajustes__sum']),
            2
        )
        data['saldos_sum']['cargos__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['cargos__sum']),
            2
        )
        data['saldos_sum']['saldo_actual__sum'] = round(
            get_decimal_is_not_none(data['saldos_sum']['saldo_actual__sum']),
            2
        )

        data['montos_sum']['utilidad__sum'] = data[
            'montos_sum']['saldo_bruto__sum']
        data['montos_sum']['queda__sum'] = 0

        # Paginacion#
        self.start = int(self.request.REQUEST.get('iDisplayStart', 0))
        if self.all_query is False:
            kwargs_filter = {}

            if self.pertenece.prefix_filter != 'agencia':
                agencias_ids = list(self.ventas.distinct(
                    'comercializacion__agencia_id'
                ).values_list('comercializacion__agencia_id', flat=True))
                kwargs_filter['pk__in'] = agencias_ids
            else:
                kwargs_filter['pk'] = self.pertenece.pk

            agencias = Agencias.objects.filter(
                **kwargs_filter).order_by('nombre')
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
            ############################################################

        index = self.start
        data_cadena = []
        for item in agencias:
            index += 1
            data_interna_cadena = {}
            data_interna_cadena['pertenece'] = []

            # Nro
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(False, index, '')
            )
            if self.all_query:
                codigo = item.codigo
                if item.codigo:
                    codigo = item.codigo
                else:
                    codigo = 'No aplica'

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(True, codigo, '')
                )

            # Nombre comercializador
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, str(item), '')
            )

            # Filtro datos del hecho5 por cadena
            venta_detalle = self.ventas.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
            )

            montos = venta_detalle.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('queda_ref'),
                Sum('saldo_bruto'),
                Sum('saldo_comer'),
                Sum('saldo_oper'),
            )

            if not montos['venta__sum']:
                data_interna_cadena['pertenece'][1]['val'] = \
                    data_interna_cadena['pertenece'][1]['val'].replace('NavegacionComercializacion', '') \
                    .replace('link', 'link-red').replace('<a', '<span').replace('a>', 'span>')

            saldo_detalle = self.saldos.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
            )

            saldos_montos = saldo_detalle.aggregate(
                Sum('queda_corte'),
                Sum('depositos'),
                Sum('pagos'),
                Sum('ajustes'),
                Sum('cargos'),
            )

            saldo_anterior = 0
            try:
                saldo_anterior = saldo_detalle.get(
                    tiempo__fecha=self.ini).saldo_anterior
            except Exception:
                pass

            # saldo anterior
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    round(saldo_anterior, 2)
                )
            )

            utilidad = Decimal(str('0.00')) if montos['saldo_bruto__sum'] is None \
                else Decimal(round(montos['saldo_bruto__sum'], 2))

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    utilidad
                )
            )

            '''
            # Contamos los días
            dias = (self.fin - self.ini).days
            frecuencia = item.get_frecuencia_queda()
            show_queda = False

            if frecuencia == 'frecuencia_semanal':
                if dias == 6:
                    week = list(Funs.get_week_by_date(self.ini))
                    if self.ini == week[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_quincenal':
                if dias == 14:
                    quincena = list(Funs.get_quincena_by_date(self.fin))
                    if self.ini == quincena[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_mensual':
                if dias == (Funs.get_month_days(self.ini)[1] - 1):
                    if date(self.ini.year, self.ini.month,
                            self.ini.day) == Funs.first_day_of_month(self.ini):
                        show_queda = True

            # queda_corte
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(
                        str('0.00')) if saldos_montos['queda_corte__sum'] is None or not show_queda else Decimal(
                        round(
                            saldos_montos['queda_corte__sum'],
                            2))
                )
            )
            '''

            # cargo en queda
            if saldos_montos['cargos__sum'] is None:
                cargos = 0
            else:
                cargos = Decimal(round(saldos_montos['cargos__sum'], 2))
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    cargos
                )
            )

            # saldo
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(str('0.00')) if montos['saldo_comer__sum'] is None
                    else Decimal(round(montos['saldo_comer__sum'], 2))
                )
            )

            # operador
            if montos['saldo_oper__sum'] is None:
                operador = 0
            else:
                operador = Decimal(round(montos['saldo_oper__sum'], 2))

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    operador
                )
            )

            if True:
                # deposito
                if saldos_montos['depositos__sum'] is None:
                    depositos = 0
                else:
                    depositos = Decimal(
                        round(saldos_montos['depositos__sum'], 2))

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        depositos
                    )
                )

                # pago
                if saldos_montos['pagos__sum'] is None:
                    pagos = 0
                else:
                    pagos = Decimal(round(saldos_montos['pagos__sum'], 2))

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        pagos
                    )
                )

                # ajuste
                if saldos_montos['ajustes__sum'] is None:
                    ajustes = 0
                else:
                    ajustes = Decimal(round(saldos_montos['ajustes__sum'], 2))

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        ajustes
                    )
                )

                # cargo
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        0
                    )
                )

            # saldo_actual
            saldo_actual = (
                saldo_anterior +
                operador +
                depositos +
                pagos +
                ajustes -
                cargos)
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    round(saldo_actual, 2)
                )
            )

            data_cadena.append(data_interna_cadena)

        data['detalle'] = data_cadena

        # Agrupando totales
        data['totales'] = [
            'Total',
        ]

        data['totales'].append(
            ''
        )

        data['totales'].append(
            ''
        )

        if self.all_query:
            data['totales'].append('')

        data['totales'].append(
            data['montos_sum']['utilidad__sum']
        )

        data['totales'].append(
            # data['montos_sum']['queda__sum']
            data['saldos_sum']['cargos__sum']
        )

        data['totales'].append(
            data['montos_sum']['saldo_comer__sum']
        )

        data['totales'].append(
            data['montos_sum']['saldo_oper__sum']
        )

        data['totales'].append(
            data['saldos_sum']['depositos__sum']
        )

        data['totales'].append(
            data['saldos_sum']['pagos__sum']
        )

        data['totales'].append(
            data['saldos_sum']['ajustes__sum']
        )

        data['totales'].append(
            # data['saldos_sum']['cargos__sum']
            0
        )

        data['totales'].append(
            ''
        )

        return data


class CuadreParleyDatatableView(CuadreParleyProcessView, BaseDatatableView):
    # Orden del filtro
    order_columns = None

    def get_initial_queryset(self):
        if self.agrupado == 'fecha':
            if self.pertenece.nivel < 2:
                messages.warning(
                    self.request,
                    'Debe seleccionar una cadena de comercialización'
                )
                return []

        self.get_hecho_venta()
        if self.agrupado != 'fecha':
            self.apply_filter_cadena()
        self.apply_filter_juego()
        self.execute_query()

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
