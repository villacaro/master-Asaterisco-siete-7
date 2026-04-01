# -*- coding: utf-8 -*-

import copy
from datetime import datetime as datetime_date
from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME, FORMAT_STR_DATE_REPORTS
from admin_datamart.models import Hecho5_ComisionesCadena
from admin_datamart.task import ObtenerPorcentaje
from admin_finanzas.models import Comercializadora
from admin_lib.util_forms import FilterCadenaComercializacionSimpleForm
from admin_lib.util_funtions import FiltersCadenaCsv
from admin_lib.util_views import MyViewBase
from admin_reportes.forms import FilterFechasForm
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import now
from django.views.generic import TemplateView


class CuadreGeneralQueda(MyViewBase, TemplateView):
    template_name = 'admin_reportes/cuadres/cuadre_general_queda.html'

    def get_context_data(self, **kwargs):
        context = super(CuadreGeneralQueda, self).get_context_data(**kwargs)

        if self.request.method == 'GET':
            context['form_fecha'] = FilterFechasForm()

            context['form_cadena'] = FilterCadenaComercializacionSimpleForm(
                **self.get_form_kwargs()
            )
            context['form_cadena'].is_valid()

        elif self.request.method == 'POST':
            context['form_fecha'] = FilterFechasForm(
                self.request.POST
            )

            context['form_cadena'] = FilterCadenaComercializacionSimpleForm(
                self.request.POST,
                **self.get_form_kwargs()
            )

            context['form_cadena'].is_valid()

        context['form_fecha'].inicializar(
            tipo='FechasParley',
            comer=self.object_comercializadora.get_object()
        )

        if self.request.REQUEST.get('fecha_inicio'):
            ini = self.request.REQUEST.get('fecha_inicio')
        else:
            ini = context['form_fecha'].fields['fecha_inicio'].initial
        if self.request.REQUEST.get('fecha_fin'):
            fin = self.request.REQUEST.get('fecha_fin')
        else:
            fin = context['form_fecha'].fields['fecha_fin'].initial

        # Rango en formato Date
        self.init_date = datetime_date.strptime(ini, FORMAT_STR_DATE_REPORTS)
        self.final_date = datetime_date.strptime(fin, FORMAT_STR_DATE_REPORTS)

        self._object = self.object_comercializadora.get_object()

        ventas = Hecho5_ComisionesCadena.objects.filter(
            tiempo__fecha__range=(ini, fin)
        )
        context['consulta'] = self.process_agrupado_cadena(ventas)

        if context['consulta']['detalle']:

            detalle = copy.deepcopy(context['consulta']['detalle'][:])
            i = 0
            for obj in detalle[:]:
                if obj['pertenece'][2]['val'] == 0:
                    detalle.remove(obj)
                else:
                    i += 1
                    obj['pertenece'][0]['val'] = i

            footer = context['consulta']['totales']

            var_cache = {
                'filters_cadena': FiltersCadenaCsv(self.request),
                'titulo': 'Reporte - Cuadre por periodos',
                'fecha': ini + '/' + fin,
                'titles': context['consulta']['titles'],
                'content': detalle,
                'footer': footer,
                'comercializador': self.nombre,
                'template_name': 'admin_reportes/cuadres/cuadres-print.html',
            }

            if self.object_sistema_juego is not None:
                sistema = self.object_sistema_juego.get_lower_ascci()
            else:
                sistema = 'todo'

            context['cache_key'] = 'generate_{0}_time_{1}_{2}_por_{3}_{4}_user_{5}'.format(
                var_cache['fecha'].replace('/', '_'),
                now().strftime('%Y-%m-%d-%H-%M'),
                sistema,
                self.pertenece.prefix_filter,
                self.pertenece,
                self.object_user,
            )

            cache.set(
                context['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )
        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_pertenece(self):

        self.force_agencia = None
        if self.request.POST.get('agencia'):
            pertenece = Comercializadora.objects.get(agencia_id=self.request.POST.get('agencia')).get_object()
            self.force_agencia = pertenece
            pertenece = pertenece.distribuidores
        elif self.request.POST.get('distribuidor'):
            pertenece = Comercializadora.objects.get(
                distribuidor_id=self.request.POST.get('distribuidor')).get_object()
        elif self.request.POST.get('banca'):
            pertenece = Comercializadora.objects.get(banca_id=self.request.POST.get('banca')).get_object()
        elif self.request.POST.get('bloque'):
            pertenece = Comercializadora.objects.get(bloque_id=self.request.POST.get('bloque')).get_object()
        elif self.request.POST.get('operadora'):
            pertenece = Comercializadora.objects.get(operadora_id=self.request.POST.get('operadora')).get_object()
        else:
            pertenece = self._object

        self.nombre = '{0}'.format(pertenece)
        # Bandera para las columnas a mostrar
        if pertenece.get_is_apply_comision():
            self.show_comision = True
        else:
            self.show_comision = False

        if pertenece.get_is_apply_regalia():
            self.show_regalia = True
        else:
            self.show_regalia = False

        if pertenece.get_is_apply_participacion():
            self.show_participacion = True
        else:
            self.show_participacion = False

        if pertenece.get_is_apply_queda():
            self.show_queda = True
        else:
            self.show_queda = False

        return pertenece

    def process_agrupado_cadena(self, ventas):
        data = {}
        data['titles'] = []

        self.pertenece = self.get_pertenece()

        if self.force_agencia:
            ventas = ventas.filter(
                ** self.force_agencia.get_kwargs_dimension_arco_comercializadora()
            )
        else:
            ventas = ventas.filter(
                ** self.pertenece.get_kwargs_hijos_dimension_arco_comercializadora()
            )

        if self.force_agencia:
            items = self.pertenece.get_offspring_ventas(ventas).filter(
                agencia_id=self.force_agencia.pk
            )
        else:
            items = self.pertenece.get_offspring_ventas(ventas)

        verbose_name_hijos = ''
        if items:
            verbose_name_hijos = items[0].get_object().get_verbose_name_plural()

        data['titles'].append({'text': 'Nro', 'width': '5%'})
        data['titles'].append({'text': verbose_name_hijos, 'width': '30%'})
        data['titles'].append({'text': 'Venta', 'width': '10%'})
        data['titles'].append({'text': 'Premios', 'width': '10%'})

        if self.show_comision:
            data['titles'].append({'text': 'Comision', 'width': '10%'})

        if self.show_regalia:
            data['titles'].append({'text': 'Servicios', 'width': '10%'})

        data['titles'].append({'text': 'Sub Total', 'width': '10%'})

        if self.show_queda:
            data['titles'].append({'text': 'Queda', 'width': '10%', })

        if self.show_participacion:
            data['titles'].append({'text': 'Saldo', 'width': '15%'})

        data['titles'].append({'text': self.pertenece.get_verbose_name(), 'width': '15%'})

        if self.pertenece.prefix_filter == 'agencia':
            messages.warning(
                self.request,
                'El nivel de taquilla no posee ajustes de porcentajes'
            )

        data['montos_sum'] = ventas.aggregate(
            Sum('venta'),
            Sum('premio'),
            Sum('comision'),
            Sum('regalia'),
            Sum('saldo_bruto'),

            # Sum('saldo_comer'),
            # Sum('saldo_oper')
        )

        if data['montos_sum']['venta__sum'] is None:
            data['montos_sum']['venta__sum'] = 0
            data['montos_sum']['premio__sum'] = 0
            data['montos_sum']['comision__sum'] = 0
            data['montos_sum']['regalia__sum'] = 0
            data['montos_sum']['saldo_bruto__sum'] = 0
            data['montos_sum']['queda_ref__sum'] = 0
            data['montos_sum']['saldo_comer__sum'] = 0
            data['montos_sum']['saldo_oper__sum'] = 0
        else:
            data['montos_sum']['venta__sum'] = round(data['montos_sum']['venta__sum'], 2)
            data['montos_sum']['premio__sum'] = round(data['montos_sum']['premio__sum'], 2)
            data['montos_sum']['comision__sum'] = round(data['montos_sum']['comision__sum'], 2)
            data['montos_sum']['regalia__sum'] = round(data['montos_sum']['regalia__sum'], 2)
            data['montos_sum']['saldo_bruto__sum'] = round(data['montos_sum']['saldo_bruto__sum'], 2)
            data['montos_sum']['queda_ref__sum'] = Decimal(0)
            data['montos_sum']['saldo_comer__sum'] = Decimal(0)  # round(data['montos_sum']['saldo_comer__sum'], 2)
            data['montos_sum']['saldo_oper__sum'] = Decimal(0)  # round(data['montos_sum']['saldo_oper__sum'], 2)

        data_cadena = []

        index = 0
        for item in items:
            item = item.get_object()
            data_interna_cadena = {}
            data_interna_cadena['pertenece'] = []

            texto = ''

            if item.prefix_filter not in ['taquilla', 'agencia']:
                texto = '<a href="#" class="link" onclick="{0}"">{1}</a>'.format(
                    "Navegacion({0},'{1}')".format(
                        item.pk,
                        item.prefix_filter
                    ),
                    item
                )

            else:
                texto = '{0}'.format(item)

            index += 1
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(False, index, '')
            )

            data_interna_cadena['pertenece'].append(
                self.type_html_conf(True, texto, '')
            )

            venta_detalle = ventas.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
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

            if not montos['venta__sum']:
                data_interna_cadena['pertenece'][1]['val'] = \
                    data_interna_cadena['pertenece'][1]['val'].replace('Navegacion', '') \
                    .replace('link', 'link-red').replace('<a', '<span').replace('a>', 'span>')

            # venta
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(0) if montos['venta__sum'] is None
                    else Decimal(round(montos['venta__sum'], 2))
                )
            )

            # premios
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    Decimal(0) if montos['premio__sum'] is None
                    else Decimal(round(montos['premio__sum'], 2)), ' link-red'
                )
            )

            if self.show_comision:
                # comision
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['comision__sum'] is None
                        else Decimal(round(montos['comision__sum'], 2))
                    )
                )

            if self.show_regalia:
                # regalia
                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        Decimal(0) if montos['regalia__sum'] is None
                        else Decimal(round(montos['regalia__sum'], 2))
                    )
                )

            # sub total
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    _type=False,
                    val=Decimal(0) if montos['saldo_bruto__sum'] is None
                    else Decimal(round(montos['saldo_bruto__sum'], 2)),
                )
            )

            queda_calc_porc = 0
            queda_ref = 0
            show_queda_by_range = False
            if self.show_queda:
                queda_ref = Decimal(0) if montos['queda_ref__sum'] is None \
                    else Decimal(round(montos['queda_ref__sum'], 2))
                queda_ref_copia = queda_ref
                if queda_ref < 0:
                    queda_ref = Decimal(0)

                # Luis - 26/08/2015
                show_queda_by_range = item.get_queda_by_range(self.init_date, self.final_date)
                if show_queda_by_range:
                    data['montos_sum']['queda_ref__sum'] += queda_ref

                # QUEDA
                it = {}
                if queda_ref > 0:
                    it = self.type_html_conf(
                        True,
                        queda_ref if show_queda_by_range else 0,
                        add_class='text-align-right text-strong',
                        title='{0}'.format(queda_ref_copia)
                    )
                else:
                    it = self.type_html_conf(
                        False,
                        queda_ref,
                        title='{0}'.format(queda_ref_copia)
                    )
                data_interna_cadena['pertenece'].append(it)

                queda_calc_porc = queda_ref * ObtenerPorcentaje(
                    codename='porcentaje_participacion',
                    cadena=item,
                    fecha=now()
                )

            participacion = 0
            if self.show_participacion:
                # saldo
                participacion = Decimal(0) if montos['saldo_comer__sum'] is None \
                    else Decimal(round(montos['saldo_comer__sum'], 2))

                if show_queda_by_range:
                    participacion -= queda_calc_porc

                data['montos_sum']['saldo_comer__sum'] += participacion

                data_interna_cadena['pertenece'].append(
                    self.type_html_conf(
                        False,
                        round(participacion, 2)
                    )
                )

            # operador
            total = Decimal(0) if montos['saldo_oper__sum'] is None \
                else Decimal(round(montos['saldo_oper__sum'], 2))

            if show_queda_by_range:
                total -= queda_ref - queda_calc_porc

            data['montos_sum']['saldo_oper__sum'] += total
            data_interna_cadena['pertenece'].append(
                self.type_html_conf(
                    False,
                    round(total, 2)
                )
            )

            data_cadena.append(data_interna_cadena)

        data['detalle'] = data_cadena

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

        # queda_sum_porc = data['montos_sum']['queda_ref__sum'] * ObtenerPorcentaje(
        #    codename='porcentaje_participacion',
        #    cadena=pertenece,
        #    fecha=now()
        # )

        if self.show_queda:
            data['totales'].append(
                data['montos_sum']['queda_ref__sum']
            )

        if self.show_participacion:
            data['totales'].append(
                # round(data['montos_sum']['saldo_comer__sum'] + queda_sum_porc, 2)
                round(data['montos_sum']['saldo_comer__sum'], 2)
            )

        data['totales'].append(
            # round(data['montos_sum']['saldo_oper__sum'] - queda_sum_porc, 2)
            round(data['montos_sum']['saldo_oper__sum'], 2)
        )

        return data

    def type_html_conf(self, _type, val, add_class='', title=''):
        item = {}
        item['html'] = _type
        item['html'] = _type
        item['class'] = ' ' if _type else 'text-align-right '
        if _type is False:
            if val < 0:
                item['class'] += ' link-red'
            elif val > 0 and add_class != ' link-red':
                item['class'] += ' link-blue'
            elif val == 0 and add_class != '':
                add_class = ''

        item['val'] = val
        item['class'] += add_class

        if title:
            item['title'] = title

        return item
