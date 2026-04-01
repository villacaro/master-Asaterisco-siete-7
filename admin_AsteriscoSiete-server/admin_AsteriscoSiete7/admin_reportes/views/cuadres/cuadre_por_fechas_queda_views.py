# -*- coding: utf-8 -*-

from datetime import datetime, timedelta
from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME, FORMAT_STR_DATE_REPORTS
from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Operadoras
from admin_datamart.models import Hecho5_ComisionesCadena
from admin_datamart.task import ObtenerPorcentaje
from admin_lib.util_fechas import strFecha
from admin_lib.util_forms import FilterCadenaComercializacionSimpleForm
from admin_lib.util_funtions import FiltersCadenaCsv, get_decimal_is_not_none
from admin_lib.util_views import MyViewBase
from admin_reportes.forms import FilterFechasForm
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.template import defaultfilters
from django.utils.timezone import now
from django.views.generic import TemplateView


class CuadrePorFechasQueda(MyViewBase, TemplateView):
    template_name = 'admin_reportes/cuadres/cuadre_por_fechas_queda.html'

    def get_context_data(self, **kwargs):
        self.data = super(
            CuadrePorFechasQueda,
            self).get_context_data(
            **kwargs)

        if self.request.method == 'GET':
            self.data['form_cadena'] = FilterCadenaComercializacionSimpleForm(
                **self.get_form_kwargs()
            )
            self.data['form_cadena'].is_valid()

            self.data['form_fecha'] = FilterFechasForm()
        elif self.request.method == 'POST':
            self.data['form_cadena'] = FilterCadenaComercializacionSimpleForm(
                self.request.POST,
                **self.get_form_kwargs()
            )
            self.data['form_cadena'].is_valid()

            self.data['form_fecha'] = FilterFechasForm(
                self.request.POST
            )

        self.data['form_fecha'].inicializar(
            tipo='FechasParley',
            comer=self.object_comercializadora.get_object()
        )

        if self.request.REQUEST.get('fecha_inicio'):
            ini = self.request.REQUEST.get('fecha_inicio')
        else:
            ini = self.data['form_fecha'].fields['fecha_inicio'].initial
        if self.request.REQUEST.get('fecha_fin'):
            fin = self.request.REQUEST.get('fecha_fin')
        else:
            fin = self.data['form_fecha'].fields['fecha_fin'].initial

        ventas = Hecho5_ComisionesCadena.objects.filter(
            tiempo__fecha__range=(ini, fin)
        )

        self.data['consulta'] = self.process_agrupado_fechas(ventas, ini, fin)

        if self.data['consulta']:

            footer = self.data['consulta']['totales']

            var_cache = {
                'filters_cadena': FiltersCadenaCsv(self.request),
                'titulo': 'Reporte - Cuadre por fechas',
                'fecha': ini + '/' + fin,
                'titles': self.titles,
                'content': self.data['consulta']['detalle'],
                'footer': footer,
                'comercializador': self.object_comercializadora.get_object().nombre,
                'template_name': 'admin_reportes/cuadres/cuadres-print.html',
            }

            if self.object_sistema_juego is not None:
                sistema = self.object_sistema_juego.get_lower_ascci()
            else:
                sistema = 'todo'

            self.data['cache_key'] = 'generate_{0}_time_{1}_{2}_por_{3}_{4}_user_{5}'.format(
                var_cache['fecha'].replace('/', '_'),
                now().strftime('%Y-%m-%d-%H-%M'),
                sistema,
                self.pertenece.prefix_filter,
                self.pertenece,
                self.object_user,
            )

            cache.set(
                self.data['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )

        return self.data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def process_agrupado_fechas(self, ventas, fecha_inicio, fecha_fin):

        data = {}
        fechas = []

        cadena_list = [
            'taquilla',
            'agencia',
            'distribuidor',
            'banca',
            'bloque',
            'operadora']
        filtrado = False
        for pos in range(0, len(cadena_list)):
            if self.request.POST.get(cadena_list[pos]):
                kwargs = {}
                filtrado = True
                if pos < 5:
                    # para acceder a la dimencion de la comercializadora por ejemplo,
                    # basta con saber que su hijo en nulo
                    kwargs[
                        'comercializacion__' +
                        cadena_list[pos + 1] + '_id__isnull'
                    ] = False
                kwargs[
                    'comercializacion__' + cadena_list[pos] + '_id'
                ] = self.request.POST.get(cadena_list[pos])
                ventas = ventas.filter(**kwargs)
                break

        if not filtrado:
            self.pertenece = self.object_comercializadora.get_object()
            if self.pertenece.prefix_filter == 'master':
                ventas = ventas.filter(
                    comercializacion__operadora_id__in=list(
                        self.pertenece.get_offspring().values_list(
                            'pk', flat=True)),
                    comercializacion__bloque_id__isnull=False
                )
            else:
                ventas = ventas.filter(
                    ** self.pertenece.get_kwargs_dimension_arco_comercializadora()
                )
        else:
            if self.request.POST.get('agencia'):
                self.pertenece = Agencias.objects.get(
                    pk=self.request.POST.get('agencia')
                )
            elif self.request.POST.get('distribuidor'):
                self.pertenece = Distribuidores.objects.get(
                    pk=self.request.POST.get('distribuidor')
                )
            elif self.request.POST.get('banca'):
                self.pertenece = Bancas.objects.get(
                    pk=self.request.POST.get('banca')
                )
            elif self.request.POST.get('bloque'):
                self.pertenece = Bloques.objects.get(
                    pk=self.request.POST.get('bloque')
                )
            elif self.request.POST.get('operadora'):
                self.pertenece = Operadoras.objects.get(
                    pk=self.request.POST.get('operadora')
                )

        if self.pertenece.nivel > 1:
            verbose_oper = self.pertenece.get_origen().get_verbose_name()
        else:
            verbose_oper = ''

        # Bandera para las columnas a mostrar
        if self.pertenece.get_is_apply_comision():
            self.show_comision = True
        else:
            self.show_comision = False

        if self.pertenece.get_is_apply_regalia():
            self.show_regalia = True
        else:
            self.show_regalia = False

        if self.pertenece.get_is_apply_participacion():
            self.show_participacion = True
        else:
            self.show_participacion = False

        if self.pertenece.get_is_apply_queda():
            self.show_queda = True
        else:
            self.show_queda = False

        self.titles = [
            {
                'text': 'Fecha',
                'width': '15%'
            },
            {
                'text': 'Dia de la semana',
                'width': '15%'
            },
            {
                'text': 'Venta',
                'width': '10%'
            },
            {
                'text': 'Premios',
                'width': '10%'
            },
        ]

        separador = {}
        separador['is_corte'] = True
        separador['color'] = '#e0e0e0;'
        separador['pertenece'] = [
            '',
            self.type_html_conf(
                True,
                'Desde',
                'text-align-center'
            ),
            self.type_html_conf(
                True,
                'Hasta',
                'text-align-center'
            ),
            ''
        ]

        if self.show_comision:
            self.titles.append(
                {
                    'text': 'Comision',
                    'width': '10%'
                }
            )
            separador['pertenece'].append('')
        if self.show_regalia:
            self.titles.append(
                {
                    'text': 'Servicios',
                    'width': '10%'
                }
            )
            separador['pertenece'].append('')

        self.titles.append(
            {
                'text': 'Sub Total',
                'width': '15%'
            }
        )
        separador['pertenece'].append(
            self.type_html_conf(
                True,
                'Sub Total',
                'text-align-center'
            )
        )

        if self.show_queda:
            self.titles.append(
                {
                    'text': 'Queda',
                    'width': '10%',
                    'title': 'Representa la queda que tomare como comercializadora.'
                },
            )
            separador['pertenece'].append(
                self.type_html_conf(
                    True,
                    'Queda',
                    'text-align-center'
                )
            )

        if self.show_participacion:
            self.titles.append(
                {
                    'text': 'Saldo',
                    'width': '10%'
                }
            )
            separador['pertenece'].append('')

        self.titles.append(
            {
                'text': verbose_oper,
                'width': '10%'
            }
        )
        separador['pertenece'].append('')

        self.data['titles'] = self.titles

        if self.pertenece.nivel < 2:
            messages.warning(
                self.request,
                'Debe seleccionar una cadena de comercialización'
            )
            return {}
        else:
            """
            if not self.pertenece.get_is_apply_queda():
                messages.warning(
                    self.request,
                    'Para la comercializadora seleccionada no aplican ajustes con Queda'
                )
                return {}
            """

        inicio = datetime.strptime(fecha_inicio, FORMAT_STR_DATE_REPORTS)
        fin = datetime.strptime(fecha_fin, FORMAT_STR_DATE_REPORTS)
        dias = (fin - inicio).days

        if dias > 0:
            fechas.append(fecha_inicio)
            for i in range(1, int(dias)):
                f = inicio + timedelta(days=i)
                fechas.append(strFecha(f).getFecha())
            fechas.append(fecha_fin)
        elif dias == 0:
            fechas.append(fecha_fin)

        data['montos_sum'] = ventas.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('regalia'),
            Sum('saldo_bruto'),
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
        data['montos_sum']['queda_ref__sum'] = Decimal()
        data['montos_sum']['saldo_comer__sum'] = Decimal()
        data['montos_sum']['saldo_oper__sum'] = Decimal()

        participacion_porc = ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=self.pertenece,
            fecha=now()
        )

        data_cadena = []
        inicio_corte = inicio
        fin_corte = None
        data['cortes'] = []

        appli_corte = False
        for i in fechas:
            fecha = datetime.strptime(i, FORMAT_STR_DATE_REPORTS)
            fecha_date = datetime.date(fecha)
            if self.pertenece.get_frecuencia_queda_is_corte_day_early(fecha_date):
                appli_corte = True
                break

        for i in fechas:

            fecha = datetime.strptime(i, FORMAT_STR_DATE_REPORTS)
            fecha_date = datetime.date(fecha)

            json_interno = {}
            json_interno['pertenece'] = []

            venta_detalle = ventas.filter(
                tiempo__fecha=i
            )

            montos = venta_detalle.aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('saldo_bruto'),
                Sum('queda_ref'),
                Sum('saldo_comer'),
                Sum('saldo_oper')
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

            # saldo bruto
            json_interno['pertenece'].append(
                self.type_html_conf(
                    _type=False,
                    val=Decimal('0.00') if montos['saldo_bruto__sum'] is None
                    else Decimal(round(montos['saldo_bruto__sum'], 2)),
                )
            )

            queda_ref = 0
            if self.show_queda:
                queda_ref = 0 if not montos['queda_ref__sum'] \
                    else Decimal(round(montos['queda_ref__sum'], 2))

                if queda_ref < 0:
                    queda_ref = Decimal(0)

                # queda
                json_interno['pertenece'].append(
                    self.type_html_conf(
                        _type=False,
                        val=queda_ref if appli_corte else 0,
                        title='Queda: {0}'.format(queda_ref),
                    )
                )

            day_is_corte = self.pertenece.get_frecuencia_queda_is_corte_day_early(fecha_date)
            if day_is_corte:
                montos_is_corte = ventas.filter(
                    tiempo__fecha__range=[inicio_corte, fecha_date]
                ).aggregate(
                    Sum('queda_ref'),
                )

                queda_ref_acum = 0
                if self.show_queda:
                    queda_ref_acum = 0 if not montos_is_corte['queda_ref__sum'] \
                        else Decimal(round(montos_is_corte['queda_ref__sum'], 2))

                    if queda_ref_acum < 0:
                        queda_ref_acum = Decimal(0)

            queda_calc_porc = 0
            if self.show_participacion:
                # saldo
                participacion = Decimal('0.00') if montos['saldo_comer__sum'] is None \
                    else Decimal(round(montos['saldo_comer__sum'], 2))

                if day_is_corte:
                    queda_calc_porc = queda_ref_acum * participacion_porc
                    participacion -= queda_calc_porc

                data['montos_sum']['saldo_comer__sum'] += participacion

                json_interno['pertenece'].append(
                    self.type_html_conf(
                        False,
                        round(participacion, 2)
                    )
                )

            # operador
            total = Decimal('0.00') if montos['saldo_oper__sum'] is None \
                else Decimal(round(montos['saldo_oper__sum'], 2))

            if day_is_corte:
                total -= queda_ref_acum - queda_calc_porc

            data['montos_sum']['saldo_oper__sum'] += total
            json_interno['pertenece'].append(
                self.type_html_conf(
                    False,
                    round(total, 2)
                )
            )

            json_interno['is_corte'] = False
            data_cadena.append(json_interno)

            # Verificanso si agregar cintillo
            if day_is_corte:
                fin_corte = fecha_date

                venta_detalle = ventas.filter(
                    tiempo__fecha__range=[inicio_corte, fin_corte]
                )

                montos = venta_detalle.aggregate(
                    Sum('venta'),
                    Sum('premio'),
                    Sum('comision'),
                    Sum('regalia'),
                    Sum('saldo_bruto'),
                    Sum('queda_ref'),
                    Sum('saldo_comer'),
                    Sum('saldo_oper')
                )

                json_interno = {}
                json_interno['is_corte'] = True
                json_interno['color'] = '#f0f0f0;'
                json_interno['pertenece'] = [
                    self.type_html_conf(
                        True,
                        'Corte aplicado',
                        ''),
                    self.type_html_conf(
                        True,
                        '{0}'.format(strFecha(inicio_corte).getFecha()),
                        ''
                    ),
                    self.type_html_conf(
                        True,
                        '{0}'.format(strFecha(fin_corte).getFecha()),
                        ''
                    ),
                    ''
                ]

                if self.show_comision:
                    json_interno['pertenece'].append(
                        ''
                    )
                if self.show_regalia:
                    json_interno['pertenece'].append(
                        ''
                    )

                json_interno['pertenece'].append(
                    self.type_html_conf(
                        _type=False,
                        val=Decimal('0.00') if montos['saldo_bruto__sum'] is None
                        else Decimal(round(montos['saldo_bruto__sum'], 2)),
                    )
                )

                queda_ref = 0
                if self.show_queda:
                    queda_ref = 0 if not montos['queda_ref__sum'] \
                        else Decimal(round(montos['queda_ref__sum'], 2))

                    if queda_ref < 0:
                        queda_ref = Decimal(0)

                    data['montos_sum']['queda_ref__sum'] += queda_ref

                    # queda
                    json_interno['pertenece'].append(
                        self.type_html_conf(
                            _type=False,
                            val=queda_ref,
                        )
                    )

                if self.show_participacion:
                    json_interno['pertenece'].append(
                        ''
                    )

                json_interno['pertenece'].append(
                    ''
                )
                data['cortes'].append(json_interno)

                inicio_corte = fin_corte + timedelta(days=1)
                fin_corte = None

        data['detalle'] = data_cadena
        if data['cortes']:
            data['detalle'].append(separador)
        data['detalle'] += data['cortes']

        data['object'] = self.pertenece

        data['montos_sum']['queda_ref__sum'] = round(
            data['montos_sum']['queda_ref__sum'],
            2
        )
        data['montos_sum']['saldo_comer__sum'] = round(
            data['montos_sum']['saldo_comer__sum'],
            2
        )
        data['montos_sum']['saldo_oper__sum'] = round(
            data['montos_sum']['saldo_oper__sum'],
            2
        )

        if data['montos_sum']['queda_ref__sum'] < 0:
            data['montos_sum']['queda_ref__sum'] = 0

        data['totales'] = [
            'Total',
            '',
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

        data['totales'].append(
            data['montos_sum']['saldo_bruto__sum']
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

    def type_html_conf(self, _type, val, add_class='', title=''):
        item = {}
        item['html'] = _type
        item['html'] = _type
        item['class'] = ' ' if _type else 'text-align-right '
        if _type is False:
            if add_class.find('link-gray') >= 0:
                item['class'] += add_class
            else:
                if val < 0:
                    item['class'] += ' link-red'
                elif val > 0 and add_class != ' link-red':
                    item['class'] += ' link-blue'
                elif val == 0:
                    add_class = ''

        item['val'] = val
        item['class'] += add_class

        if title:
            item['title'] = title
        return item
