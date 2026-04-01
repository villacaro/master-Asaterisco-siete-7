# -*- coding: utf-8 -*-

import copy
from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME
from admin_finanzas.forms import FilterMesesForm
from admin_finanzas.models import Comercializadora, Movimiento, ResumenAdministrativo
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.cache import cache
from django.urls import reverse
from django.db.models import Sum
from django.http import Http404, HttpResponseRedirect
from django.template import defaultfilters
from django.utils.timezone import now
from django.views.generic import DetailView, TemplateView


class VentasResumenAdministrativo(MyViewBase, TemplateView):

    template_name = 'admin_finanzas/resumen_administrativo' + \
                    '/ventas-resumen-administrativo.html'

    def get_context_data(self, **kwargs):
        self.data = super(
            VentasResumenAdministrativo,
            self).get_context_data(
            **kwargs)

        self.data['importar_saldo'] = True
        self.data['personalizado'] = False
        self.data['tabuladores'] = '1'
        self.data['verbose'] = 'Resumen Administrativo'
        self.data['next_url'] = 'admin_finanzas_resumenadministrativo_general'
        self.data['dia_trabajo'] = self.object_comercializadora.get_dia_trabajo()
        if self.data['dia_trabajo']:
            self.data['consulta'] = self.resumen()

        return self.data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = self.object_comercializadora.get_offspring_level1().filter(
            resumen_personalizado=False
        ).order_by(
            'operadora__nombre',
            'bloque__nombre',
            'banca__nombre',
            'distribuidor__nombre',
            'agencia__nombre',
            'taquilla__taquilla',
        )
        return queryset

    def resumen(self):

        object_comer = self.object_comercializadora.get_object()

        json = {}
        verbose_name = ''
        queryset = self.get_queryset()

        if queryset.exists():
            verbose_name = queryset[0].get_object().get_verbose_name_plural()

        json['titles'] = []
        json['titles'].append({'text': 'N°', 'width': '5%'})

        if self.data['personalizado']:
            json['titles'].append({'text': 'Tipo', 'width': '10%'})
            json['titles'].append({'text': 'Comer', 'width': '10%'})
        else:
            json['titles'].append({'text': verbose_name, 'width': '10%'})

        json['titles'].append({'text': 'Saldo Anterior', 'width': '7%'})
        json['titles'].append({'text': 'Venta', 'width': '7%'})
        json['titles'].append({'text': 'Premio', 'width': '7%'})
        json['titles'].append({'text': '% ' + verbose_name, 'width': '7%'})
        json['titles'].append({'text': 'Servicios', 'width': '7%'})
        json['titles'].append({'text': 'Saldo', 'width': '7%'})
        json['titles'].append(
            {'text': object_comer.get_verbose_name(), 'width': '7%'})
        json['titles'].append({'text': 'Deposito', 'width': '7%'})
        json['titles'].append({'text': 'Pago', 'width': '7%'})
        json['titles'].append({'text': 'Ajustes', 'width': '7%'})
        json['titles'].append({'text': 'Cargos', 'width': '7%'})
        json['titles'].append({'text': 'Saldo Actual', 'width': '7%'})

        json_cadena = []

        json['totales'] = {}

        json['totales']['venta'] = Decimal()
        json['totales']['premio'] = Decimal()
        json['totales']['comision'] = Decimal()
        json['totales']['regalia'] = Decimal()
        json['totales']['saldo'] = Decimal()
        json['totales']['operador'] = Decimal()
        json['totales']['depositos'] = Decimal()
        json['totales']['pagos'] = Decimal()
        json['totales']['ajustes'] = Decimal()
        json['totales']['cargos'] = Decimal()

        dia = self.data['dia_trabajo'].dia
        i = 1

        for comercializadora_relate in queryset:
            object_relate = comercializadora_relate.get_object()

            try:
                venta = ResumenAdministrativo.objects.get(
                    dia=dia,
                    comercializacion=object_relate.get_dimension_arco_comercializadora()
                )
            except ResumenAdministrativo.DoesNotExist:
                continue

            if comercializadora_relate.saldo_fecha:
                if comercializadora_relate.saldo_fecha > dia.fecha:
                    # si tiene saldo inicial pero es mayor al dia de trabajo
                    # actual
                    continue
            else:
                continue

            json_interna_cadena = []

            json_interna_cadena.append(
                self.set_type_html_conf(_type=True, val=i)
            )

            if self.data['personalizado']:
                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=True, val=object_relate.get_verbose_name())
                )

            texto = '<a class="link" href="{0}">{1}</a>'.format(
                reverse(
                    'admin_finanzas_resumenadministrativo_comercializadora_list',
                    kwargs={
                        'comercializadora': comercializadora_relate.pk
                    }
                ),
                comercializadora_relate.get_object(),
            )

            json_interna_cadena.append(
                self.set_type_html_conf(_type=True, val=texto)
            )

            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(
                        venta.saldo_anterior, 2))
            )
            json_interna_cadena.append(
                self.set_type_html_conf(_type=False, val=round(venta.venta, 2))
            )
            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(venta.premio, 2),
                    add_class=' link-red 'if venta.premio > 0 else ' '
                )
            )
            # if self.show_comision:
            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(
                        venta.comision, 2))
            )
            # if self.show_regalia:
            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(
                        venta.regalia, 2))
            )
            # if self.show_participacion:
            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(
                        venta.saldo_comer, 2))
            )
            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(
                        venta.saldo_oper, 2))
            )

            movimientos = Movimiento.objects.filter(
                dia=dia,
                comercializadora_id=comercializadora_relate.pk
            )

            resultado = movimientos.filter(tipo__codename='tipo_deposito')
            depositos = resultado.aggregate(Sum('monto'))['monto__sum']
            depositos = Decimal() if depositos is None else depositos
            add_class = ''
            if depositos < 0:
                add_class = ' link-red '
            elif depositos > 0:
                add_class = ' link-blue '
            else:
                depositos = 0

            texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                add_class,
                reverse(
                    'admin_finanzas_operaciones_deposito_create',
                    kwargs={
                        'comercializadora': comercializadora_relate.pk
                    }
                ),
                depositos
            )

            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=True, val=texto, not_number=False)
            )

            resultado = movimientos.filter(tipo__codename='tipo_pago')
            pagos = resultado.aggregate(Sum('monto'))['monto__sum']
            pagos = Decimal() if pagos is None else pagos
            add_class = ''
            if pagos < 0:
                add_class = ' link-red '
            elif pagos > 0:
                add_class = ' link-blue '
            else:
                pagos = 0

            texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                add_class,
                reverse(
                    'admin_finanzas_operaciones_pago_create',
                    kwargs={
                        'comercializadora': comercializadora_relate.pk
                    }
                ),
                pagos
            )
            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=True, val=texto, not_number=False)
            )

            resultado = movimientos.filter(
                tipo__codename__in=('tipo_ajuste_cobrar', 'tipo_ajuste_pagar')
            )
            ajustes = resultado.aggregate(Sum('monto'))['monto__sum']
            ajustes = Decimal() if ajustes is None else ajustes
            add_class = ''
            if ajustes < 0:
                add_class = ' link-red '
            elif ajustes > 0:
                add_class = ' link-blue '
            else:
                ajustes = 0

            texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                add_class,
                reverse(
                    'admin_finanzas_operaciones_ajuste_create',
                    kwargs={
                        'comercializadora': comercializadora_relate.pk
                    }
                ),
                ajustes
            )

            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=True, val=texto, not_number=False)
            )

            cargos = venta.cargo
            json_interna_cadena.append(
                self.set_type_html_conf(_type=False, val=round(cargos, 2))
            )

            saldo_actual = venta.saldo_anterior + venta.saldo_oper + \
                depositos + pagos + ajustes - cargos

            json_interna_cadena.append(
                self.set_type_html_conf(
                    _type=False, val=round(
                        saldo_actual, 2))
            )

            json['totales']['venta'] += round(venta.venta, 2)
            json['totales']['premio'] += round(venta.premio, 2)
            json['totales']['comision'] += round(venta.comision, 2)
            json['totales']['regalia'] += round(venta.regalia, 2)
            json['totales']['saldo'] += round(venta.saldo_comer, 2)
            json['totales']['operador'] += round(venta.saldo_oper, 2)
            json['totales']['depositos'] += round(depositos, 2)
            json['totales']['pagos'] += round(pagos, 2)
            json['totales']['ajustes'] += round(ajustes, 2)
            json['totales']['cargos'] += round(cargos, 2)

            json_cadena.append(json_interna_cadena)

            i += 1

        json['detalle'] = json_cadena

        if json['detalle']:

            if self.data['personalizado']:
                footer = [
                    'Total',
                    '',
                    '',
                    '',
                    json['totales']['venta'],
                    json['totales']['premio'],
                    json['totales']['comision'],
                    json['totales']['regalia'],
                    json['totales']['saldo'],
                    json['totales']['operador'],
                    json['totales']['depositos'],
                    json['totales']['pagos'],
                    json['totales']['ajustes'],
                    json['totales']['cargos'],
                    '',
                ]
            else:
                footer = [
                    'Total',
                    '',
                    '',
                    json['totales']['venta'],
                    json['totales']['premio'],
                    json['totales']['comision'],
                    json['totales']['regalia'],
                    json['totales']['saldo'],
                    json['totales']['operador'],
                    json['totales']['depositos'],
                    json['totales']['pagos'],
                    json['totales']['ajustes'],
                    json['totales']['cargos'],
                    '',
                ]

            json_detail = []
            for detail in json['detalle']:
                detalle = {}
                detalle['pertenece'] = detail
                json_detail.append(detalle)

            detalle = copy.deepcopy(json_detail[:])
            i = 0
            for obj in detalle[:]:
                if obj['pertenece'][2]['val'] == 0 and obj[
                        'pertenece'][3]['val'] == 0:
                    detalle.remove(obj)
                else:
                    i += 1
                    obj['pertenece'][0]['val'] = i

            var_cache = {
                'titulo': 'Reporte - {0}'.format(self.data['verbose']),
                'fecha': self.data['dia_trabajo'].dia.fecha.strftime('%d-%m-%Y'),
                'titles': json['titles'],
                'content': detalle,
                'footer': footer,
                'comercializador': self.object_comercializadora.get_object().nombre,
                'template_name': 'admin_finanzas/resumen_administrativo/ventas-resumen-administrativo_print.html',
            }

            import re
            if self.object_sistema_juego is not None:
                sistema = self.object_sistema_juego.get_lower_ascci()
            else:
                sistema = 'todo'

            json['cache_key'] = re.sub(
                '--',
                '-',
                '{0}-{1}-{2}-generate-{3}'.format(
                    sistema,
                    var_cache['fecha'],
                    now().strftime('%Y-%m-%d-%H-%M'),
                    self.object_user
                )
            )

            cache.set(
                json['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )

        return json

    def set_type_html_conf(self, _type, val, not_number=True, add_class=''):
        item = {}
        item['html'] = _type
        item['class'] = ' ' if _type else 'text-align-right '
        item['class'] += ' ' if not_number else ' text-align-right '
        if _type is False:
            if val < 0:
                item['class'] += ' link-red'
        item['val'] = val

        item['class'] += add_class
        return item


class VentasResumenAdministrativoPersonalizado(VentasResumenAdministrativo):

    def get_context_data(self, **kwargs):
        self.data = super(
            VentasResumenAdministrativo,
            self).get_context_data(
            **kwargs)

        self.data['importar_saldo'] = True
        self.data['personalizado'] = True
        self.data['tabuladores'] = '12'
        self.data['dia_trabajo'] = self.object_comercializadora.get_dia_trabajo()
        self.data['verbose'] = 'Resumen Administrativo Personalizado'
        self.data['next_url'] = 'admin_finanzas_resumenadministrativo_personalizado'
        if self.data['dia_trabajo']:
            self.data['consulta'] = self.resumen()

        return self.data

    def get_queryset(self):
        queryset = self.object_comercializadora.comercializadora_set.all()

        queryset = queryset.order_by(
            'operadora__nombre',
            'bloque__nombre',
            'banca__nombre',
            'distribuidor__nombre',
            'agencia__nombre',
            'taquilla__taquilla',
        )
        return queryset


class VentasResumenAdministrativoImport(MyViewBase, TemplateView):
    template_name = ''

    def dispatch(self, request, *args, **kwargs):
        super(VentasResumenAdministrativoImport, self).dispatch(
            request, *args, **kwargs
        )

        process = self.object_comercializadora.process_import()

        if process:
            messages.info(
                request,
                'Saldos importados con exíto'
            )
        else:
            messages.warning(
                self.request,
                'Esta acción no a podido completarse, aun hay venta sin procesar.'
            )

        if not request.REQUEST.get('next_url'):
            return HttpResponseRedirect(
                '/reportes/comercializadoras/resumen-administrativo/'
            )
        else:
            return HttpResponseRedirect(
                reverse(request.REQUEST.get('next_url'))
            )


class VentasResumenAdministrativoByComercializadora(MyViewBase, DetailView):
    template_name = 'admin_finanzas/resumen_administrativo/' + \
                    'ventas-resumen-administrativo-by-comercializadora.html'

    pk_url_kwarg = 'comercializadora'

    def get_queryset(self):
        return self.object_comercializadora.get_offspring_level1().filter(
            resumen_personalizado=False
        ) | self.object_comercializadora.comercializadora_set.all()

    def get_context_data(self, **kwargs):
        self.data = super(
            VentasResumenAdministrativoByComercializadora,
            self
        ).get_context_data(**kwargs)

        self.resumen()
        object_comer = self.object_comercializadora.get_object()

        self.data['titles'] = []
        self.data['titles'].append({'text': 'N°', 'width': '5%'})
        self.data['titles'].append({'text': 'Fecha', 'width': '7%'})
        self.data['titles'].append({'text': 'Dia', 'width': '7%'})
        self.data['titles'].append({'text': 'Saldo Anterior', 'width': '7%'})
        self.data['titles'].append({'text': 'Venta', 'width': '7%'})
        self.data['titles'].append({'text': 'Premio', 'width': '7%'})
        self.data['titles'].append(
            {'text': '% ' + self.object.get_object().get_verbose_name(), 'width': '7%'})
        self.data['titles'].append({'text': 'Servicios', 'width': '7%'})
        self.data['titles'].append({'text': 'Saldo', 'width': '7%'})
        self.data['titles'].append(
            {'text': object_comer.get_verbose_name(), 'width': '7%'})
        self.data['titles'].append({'text': 'Deposito', 'width': '7%'})
        self.data['titles'].append({'text': 'Pago', 'width': '7%'})
        self.data['titles'].append({'text': 'Ajustes', 'width': '7%'})
        self.data['titles'].append({'text': 'Cargos', 'width': '7%'})
        self.data['titles'].append({'text': 'Saldo Actual', 'width': '7%'})

        if self.data['detalle']:

            footer = [
                ' ',
                ' ',
                ' ',
                ' ',
                self.data['objects_sum']['venta__sum'],
                self.data['objects_sum']['premio__sum'],
                self.data['objects_sum']['comision__sum'],
                self.data['objects_sum']['regalia__sum'],
                self.data['objects_sum']['saldo_comer__sum'],
                self.data['objects_sum']['saldo_oper__sum'],
                self.data['objects_sum']['deposito__sum'],
                self.data['objects_sum']['pago__sum'],
                self.data['objects_sum']['ajuste__sum'],
                self.data['objects_sum']['cargo__sum'],
                '',
            ]

            var_cache = {
                'titulo': 'Resumen Administrativo Detalle',
                'fecha': '',
                'titles': self.data['titles'],
                'content': self.data['detalle'],
                'footer': footer,
                'comercializador': self.object_comercializadora.get_object().nombre,
                'template_name': 'admin_finanzas/resumen_administrativo/ventas-resumen-administrativo_print.html',
            }

            import re
            if self.object_sistema_juego is not None:
                sistema = self.object_sistema_juego.get_lower_ascci()
            else:
                sistema = 'todo'

            self.data['cache_key'] = re.sub(
                '--',
                '-',
                '{0}-{1}-{2}-generate-{3}'.format(
                    sistema,
                    var_cache['fecha'],
                    now().strftime('%Y-%m-%d-%H-%M'),
                    self.object_user
                )
            )

            cache.set(
                self.data['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )

        return self.data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def resumen(self):
        self.data['comercializadora'] = self.object
        self.data['by_comercializadora'] = self.object.get_object() \
            .get_dimension_arco_comercializadora()

        dia_trabajo = self.object_comercializadora.get_dia_trabajo()
        self.data['objects'] = ResumenAdministrativo.objects.filter(
            dia__fecha__lt=dia_trabajo.dia.fecha,
            comercializacion=self.data['by_comercializadora']
        ).order_by('-dia__fecha')

        fecha = []
        if self.request.method == 'POST':
            self.data['form'] = FilterMesesForm(
                self.request.POST,
                **self.get_form_kwargs()
            )
            if self.data['form'].is_valid():
                fecha = self.data['form'].cleaned_data.get(
                    'filter_fecha').split('-')
        else:
            self.data['form'] = FilterMesesForm(**self.get_form_kwargs())

        self.data['form'].inicializar_fechas(
            list(self.data['objects'].values_list('dia__fecha', flat=True))
        )

        if len(fecha) == 0:
            if len(self.data['form'].fields['filter_fecha'].choices) > 0:
                fecha = self.data['form'].fields[
                    'filter_fecha'].choices[0][0].split('-')

        self.data['detalle'] = []

        if len(fecha) == 2:
            self.data['objects'] = self.data['objects'].filter(
                dia__fecha__year=fecha[0],
                dia__fecha__month=fecha[1]
            ).order_by('dia__fecha')

            self.data['objects_sum'] = self.data['objects'].aggregate(
                Sum('venta'),
                Sum('premio'),
                Sum('comision'),
                Sum('regalia'),
                Sum('participacion'),
                Sum('saldo_comer'),
                Sum('saldo_oper'),
                Sum('deposito'),
                Sum('pago'),
                Sum('ajuste'),
                Sum('cargo'),
            )

            self.data['objects_sum']['venta__sum'] = round(
                self.data['objects_sum']['venta__sum'], 2)
            self.data['objects_sum']['premio__sum'] = round(
                self.data['objects_sum']['premio__sum'], 2)
            self.data['objects_sum']['comision__sum'] = round(
                self.data['objects_sum']['comision__sum'], 2)
            self.data['objects_sum']['regalia__sum'] = round(
                self.data['objects_sum']['regalia__sum'], 2)
            self.data['objects_sum']['participacion__sum'] = round(
                self.data['objects_sum']['participacion__sum'], 2)
            self.data['objects_sum']['saldo_comer__sum'] = round(
                self.data['objects_sum']['saldo_comer__sum'], 2)
            self.data['objects_sum']['saldo_oper__sum'] = round(
                self.data['objects_sum']['saldo_oper__sum'], 2)
            self.data['objects_sum']['deposito__sum'] = round(
                self.data['objects_sum']['deposito__sum'], 2)
            self.data['objects_sum']['pago__sum'] = round(
                self.data['objects_sum']['pago__sum'], 2)
            self.data['objects_sum']['ajuste__sum'] = round(
                self.data['objects_sum']['ajuste__sum'], 2)
            self.data['objects_sum']['cargo__sum'] = round(
                self.data['objects_sum']['cargo__sum'], 2)

            i = 0
            for obj in self.data['objects']:
                json_cadena = {}
                json_interna_cadena = []
                i += 1
                json_interna_cadena.append(
                    self.set_type_html_conf(_type=True, val=i)
                )

                texto = defaultfilters.date(
                    obj.dia.fecha, 'd-m-y').capitalize()
                json_interna_cadena.append(
                    self.set_type_html_conf(_type=True, val=texto)
                )

                texto = defaultfilters.date(obj.dia.fecha, 'l').capitalize()
                json_interna_cadena.append(
                    self.set_type_html_conf(_type=True, val=texto)
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            obj.saldo_anterior, 2))
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(obj.venta, 2))
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(obj.premio, 2),
                        add_class=' link-red ' if obj.premio > 0 else ' '
                    )
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            obj.comision, 2))
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            obj.regalia, 2))
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            obj.saldo_comer, 2))
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            obj.saldo_oper, 2))
                )

                add_class = ''
                if obj.deposito < 0:
                    add_class = ' link-red '
                elif obj.deposito > 0:
                    add_class = ' link-blue '

                texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                    add_class,
                    reverse(
                        'admin_finanzas_resumenadministrativo_movimientos_list',
                        kwargs={
                            'movimiento': 'depositos',
                            'comercializadora': self.object.pk,
                            'year': fecha[0],
                            'month': fecha[1],
                            'day': obj.dia.fecha.strftime('%d')
                        }
                    ),
                    intcomma(
                        round(
                            obj.deposito,
                            2)) if obj.deposito != 0 else 0
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=True, val=texto, not_number=False)
                )

                add_class = ''
                if obj.pago < 0:
                    add_class = ' link-red '
                elif obj.pago > 0:
                    add_class = ' link-blue '

                texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                    add_class,
                    reverse(
                        'admin_finanzas_resumenadministrativo_movimientos_list',
                        kwargs={
                            'movimiento': 'pagos',
                            'comercializadora': self.object.pk,
                            'year': fecha[0],
                            'month': fecha[1],
                            'day': obj.dia.fecha.strftime('%d')
                        }
                    ),
                    intcomma(round(obj.pago, 2)) if obj.pago != 0 else 0
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=True, val=texto, not_number=False)
                )
                add_class = ''
                if obj.ajuste < 0:
                    add_class = ' link-red '
                elif obj.ajuste > 0:
                    add_class = ' link-blue '

                texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                    add_class,
                    reverse(
                        'admin_finanzas_resumenadministrativo_movimientos_list',
                        kwargs={
                            'movimiento': 'ajustes',
                            'comercializadora': self.object.pk,
                            'year': fecha[0],
                            'month': fecha[1],
                            'day': obj.dia.fecha.strftime('%d')
                        }
                    ),
                    intcomma(round(obj.ajuste, 2)) if obj.ajuste != 0 else 0
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=True, val=texto, not_number=False)
                )

                add_class = ''
                if obj.cargo < 0:
                    add_class = ' link-red '
                elif obj.cargo > 0:
                    add_class = ' link-blue '

                texto = '<a class="link-no-color {0}" href="{1}">{2}</a>'.format(
                    add_class,
                    reverse(
                        'admin_finanzas_resumenadministrativo_movimientos_list',
                        kwargs={
                            'movimiento': 'cargos',
                            'comercializadora': self.object.pk,
                            'year': fecha[0],
                            'month': fecha[1],
                            'day': obj.dia.fecha.strftime('%d')
                        }
                    ),
                    intcomma(round(obj.cargo, 2)) if obj.cargo != 0 else 0
                )

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=True, val=texto, not_number=False)
                )
                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            obj.get_saldo_actual(), 2))
                )

                json_cadena['pertenece'] = json_interna_cadena
                self.data['detalle'].append(json_cadena)

        else:
            self.data['objects'] = []
        self.data['fecha'] = fecha

    def set_type_html_conf(self, _type, val, not_number=True, add_class=''):
        item = {}
        item['html'] = _type
        item['class'] = ' ' if _type else 'text-align-right '
        item['class'] += ' ' if not_number else ' text-align-right '
        if _type is False:
            if val < 0:
                item['class'] += ' link-red'
        item['val'] = val

        item['class'] += add_class
        return item


class VentasHojaDeBancoByComercializadora(
        VentasResumenAdministrativoByComercializadora):
    template_name = 'admin_finanzas/resumen_administrativo' + \
                    '/ventas-hoja-banco-by-comercializadora.html'

    def get_context_data(self, **kwargs):
        self.data = super(
            VentasHojaDeBancoByComercializadora,
            self
        ).get_context_data(**kwargs)

        self.resumen_by_movimientos()

        return self.data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def resumen_by_movimientos(self):
        self.data['detalle_resumen'] = {}
        i = 1
        for _object in self.data['objects']:
            _object.new_diccionario()
            json_movimientos = {}
            json_movimientos['detalle'] = []
            saldo_anterior = _object.saldo_anterior
            saldo_actual = saldo_anterior
            for movimiento in Movimiento.objects.filter(
                comercializadora_id=self.object.pk,
                dia=_object.dia
            ).order_by('created_at'):
                json_interno = {}
                codename = movimiento.tipo.codename.split('_')
                json_interno[codename[0] + '_' +
                             codename[1]] = movimiento.monto
                json_interno['saldo_anterior'] = saldo_anterior
                saldo_actual += movimiento.monto
                json_interno['saldo_actual'] = saldo_actual
                saldo_anterior = saldo_actual
                json_interno['count'] = i
                json_movimientos['detalle'].append(json_interno)
                i += 1
            json_movimientos['count'] = i

            json_movimientos['saldo_anterior'] = saldo_anterior

            _object.set_diccionario('movimientos', json_movimientos)
            i += 1


class MovimientosForComercializadoraToFecha(MyViewBase, TemplateView):
    template_name = 'admin_finanzas/resumen_administrativo/' + \
                    'movimientos-for-comercializadora-to-fecha.html'
    tipo = {
        'depositos': {
            'codenames': ('tipo_deposito', ''),
            'verbose': 'Dep.',
            'label': 'Depositos'
        },
        'pagos': {
            'codenames': ('tipo_pago', ''),
            'verbose': 'Pag.',
            'label': 'Pagos'
        },
        'ajustes': {
            'codenames': ('tipo_ajuste_cobrar', 'tipo_ajuste_pagar'),
            'verbose': 'Ajus.',
            'label': 'Ajustes'
        },
        'cargos': {
            'codenames': ('', ''),
            'verbose': 'Carg.',
            'label': 'Cargos'
        },
    }

    def get_context_data(self, **kwargs):
        self.data = super(
            MovimientosForComercializadoraToFecha,
            self
        ).get_context_data(**kwargs)

        self.resumen()

        return self.data

    def resumen(self):
        try:
            self.data['by_comercializadora'] = Comercializadora.objects.get(
                pk=self.kwargs.get('comercializadora')
            )

            self.data['objects'] = Movimiento.objects.filter(
                dia__fecha__lt=self.object_comercializadora.get_dia_trabajo().dia.fecha,
                comercializadora_id=self.data['by_comercializadora'].pk
            )
            tipo_codename = self.tipo.get(self.kwargs.get('movimiento'))

            if tipo_codename is None:
                raise Http404

            self.data['objects'] = self.data['objects'].filter(
                tipo__codename__in=tipo_codename['codenames']
            )

            anho = self.kwargs.get('year')
            mes = self.kwargs.get('month')
            dia = self.kwargs.get('day')

            self.data['fecha'] = ''

            if dia != '00':
                self.data['fecha'] += dia + ' de '
                self.data['objects'] = self.data['objects'].filter(
                    dia__fecha__day=dia
                )

            self.data['objects'] = self.data['objects'].filter(
                dia__fecha__year=anho,
                dia__fecha__month=mes
            )

            self.data['fecha'] += now().strptime(mes, '%m') \
                .strftime('%B').capitalize() + ' de ' + anho

            self.data['tipo'] = tipo_codename
            self.data['objects'] = self.data['objects'].order_by('dia__fecha')
            self.data['objects_sum'] = self.data[
                'objects'].aggregate(Sum('monto'))

        except Exception:
            raise Http404
