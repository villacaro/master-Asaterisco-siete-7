from decimal import Decimal

from admin_banklotsports.settings import CACHES_CONF_TIME
from admin_finanzas.forms import FilterMesesSuperiorForm
from admin_finanzas.models import Movimiento, ResumenAdministrativo
from admin_lib.util_views import MyViewBase
from django.core.cache import cache
from django.db.models import Sum
from django.template import defaultfilters
from django.utils.timezone import now
from django.views.generic import TemplateView


class CuadreNivelSuperior(MyViewBase, TemplateView):

    template_name = 'admin_reportes/cuadres/cuadre_nivel_superior.html'

    def get_context_data(self, **kwargs):
        self.data = super(CuadreNivelSuperior, self).get_context_data(**kwargs)

        self.comer_origen = self.object_comercializadora.resumen_personalizado_comer
        if not self.comer_origen:
            self.comer_origen = self.object_comercializadora.get_origen()

        self.origen = self.comer_origen.get_object()
        self.object_comercializadora_object = self.object_comercializadora.get_object()

        #####################################################################
        self.data['titles'] = []
        self.data['titles'].append({'text': 'N°', 'width': '3%'})
        self.data['titles'].append({'text': 'Fecha', 'width': '12%'})
        self.data['titles'].append({'text': 'Dia', 'width': '7%'})
        self.data['titles'].append({'text': 'Saldo Anterior', 'width': '7%'})
        self.data['titles'].append({'text': 'Venta', 'width': '7%'})
        self.data['titles'].append({'text': 'Premio', 'width': '7%'})
        self.data['titles'].append(
            {'text': '% ' + self.object_comercializadora_object.get_verbose_name(), 'width': '7%'})
        self.data['titles'].append({'text': 'Regalía', 'width': '7%'})
        self.data['titles'].append({'text': 'Saldo', 'width': '7%'})
        self.data['titles'].append(
            {'text': self.origen.get_verbose_name(), 'width': '7%'})
        self.data['titles'].append({'text': 'Deposito', 'width': '5%'})
        self.data['titles'].append({'text': 'Pago', 'width': '5%'})
        self.data['titles'].append({'text': 'Ajustes', 'width': '5%'})
        self.data['titles'].append({'text': 'Cargos', 'width': '5%'})
        self.data['titles'].append({'text': 'Saldo Actual', 'width': '7%'})
        #####################################################################

        self.resumen()

        return self.data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def resumen(self):
        self.data['comercializadora'] = self.data[
            'object'] = self.object_comercializadora
        self.data['by_comercializadora'] = self.object_comercializadora_object \
            .get_dimension_arco_comercializadora()

        self.data['objects'] = ResumenAdministrativo.objects.filter(
            comercializacion=self.data['by_comercializadora']
        ).order_by('-dia__fecha')

        fecha = []
        kwargs = self.get_form_kwargs()
        kwargs['fechas'] = list(
            self.data['objects'].values_list(
                'dia__fecha', flat=True))
        if self.request.method == 'POST':

            self.data['form'] = FilterMesesSuperiorForm(
                self.request.POST,
                **kwargs
            )
            if self.data['form'].is_valid():
                fecha = self.data['form'].cleaned_data.get(
                    'filter_fecha').split('-')
        else:
            self.data['form'] = FilterMesesSuperiorForm(**kwargs)

        self.data['detalle'] = []

        if len(fecha) == 0:
            if len(self.data['form'].fields['filter_fecha'].choices) > 0:
                fecha = self.data['form'].fields[
                    'filter_fecha'].choices[0][0].split('-')

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
                Sum('saldo_anterior'),
                Sum('saldo_actual')
            )

            i = 0

            fecha_origen = self.comer_origen.get_dia_trabajo()

            if fecha_origen:
                fecha_origen = fecha_origen.dia.fecha

            for obj in self.data['objects']:

                depositos = obj.deposito
                pagos = obj.pago
                ajustes = obj.ajuste
                cargos = obj.cargo
                saldo_actual = obj.saldo_actual

                if fecha_origen < obj.dia.fecha:
                    continue
                elif fecha_origen == obj.dia.fecha:
                    movimientos = Movimiento.objects.filter(
                        dia=obj.dia,
                        comercializadora_id=self.object_comercializadora.pk
                    )

                    depositos = movimientos.filter(
                        tipo__codename='tipo_deposito'
                    ).aggregate(Sum('monto'))['monto__sum']
                    depositos = Decimal() if depositos is None else depositos

                    pagos = movimientos.filter(
                        tipo__codename='tipo_pago'
                    ).aggregate(Sum('monto'))['monto__sum']
                    pagos = Decimal() if pagos is None else pagos

                    ajustes = movimientos.filter(
                        tipo__codename__in=(
                            'tipo_ajuste_cobrar', 'tipo_ajuste_pagar')
                    ).aggregate(Sum('monto'))['monto__sum']
                    ajustes = Decimal() if ajustes is None else ajustes

                    saldo_actual = obj.saldo_anterior + obj.saldo_oper + \
                        depositos + pagos + ajustes - cargos

                    self.data['objects_sum']['deposito__sum'] += depositos
                    self.data['objects_sum']['pago__sum'] += pagos
                    self.data['objects_sum']['ajuste__sum'] += ajustes
                    self.data['objects_sum'][
                        'saldo_actual__sum'] += saldo_actual

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
                if depositos < 0:
                    add_class = ' link-red '
                elif depositos > 0:
                    add_class = ' link-blue '

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False,
                        val=round(depositos, 2),
                        add_class=add_class
                    )
                )

                add_class = ''
                if pagos < 0:
                    add_class = ' link-red '
                elif pagos > 0:
                    add_class = ' link-blue '

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False,
                        val=round(pagos, 2),
                        add_class=add_class
                    )
                )
                add_class = ''
                if ajustes < 0:
                    add_class = ' link-red '
                elif ajustes > 0:
                    add_class = ' link-blue '

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False,
                        val=round(ajustes, 2),
                        add_class=add_class
                    )
                )

                add_class = ''
                if cargos < 0:
                    add_class = ' link-red '
                elif cargos > 0:
                    add_class = ' link-blue '

                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False,
                        val=round(cargos, 2),
                        add_class=add_class
                    )
                )
                json_interna_cadena.append(
                    self.set_type_html_conf(
                        _type=False, val=round(
                            saldo_actual, 2))
                )

                json_cadena['pertenece'] = json_interna_cadena

                self.data['detalle'].append(json_cadena)

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
            self.data['objects_sum']['saldo_anterior__sum'] = round(
                self.data['objects_sum']['saldo_anterior__sum'], 2)
            self.data['objects_sum']['saldo_actual__sum'] = round(
                self.data['objects_sum']['saldo_actual__sum'], 2)

        else:
            self.data['objects'] = []

        if self.data['detalle']:

            footer = [
                'Total',
                ' ',
                ' ',
                self.data['objects_sum']['saldo_anterior__sum'],
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
                self.data['objects_sum']['saldo_actual__sum']
            ]

            var_cache = {
                'titulo': 'Reporte - Cuadre Nivel Superior',
                'fecha': fecha[0] + '/' + fecha[1],
                'titles': self.data['titles'],
                'content': self.data['detalle'],
                'footer': footer,
                'comercializador': self.object_comercializadora.get_object().nombre,
                'template_name': 'admin_reportes/cuadres/cuadres-print.html',
            }

            self.data['cache_key'] = '{0}-{1}-generate-{2}'.format(
                var_cache['fecha'],
                now().strftime('%Y-%m-%d-%H-%M'),
                self.object_user
            )

            cache.set(
                self.data['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )

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
