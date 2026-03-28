# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_banklotsports.settings import CACHES_CONF_TIME, FORMAT_STR_DATE
from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Operadoras
from admin_finanzas.models import Configuracion, Movimiento, ResumenAdministrativo
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import now
from django.views.generic import TemplateView


class CuentasBase(MyViewBase, TemplateView):

    template_name = 'admin_finanzas/cuentas_operaciones/cuentas_base.html'
    template_name_pdf = 'admin_finanzas/cuentas_operaciones/cuentas_base_print.html'

    def get_context_data(self, **kwargs):
        context = super(CuentasBase, self).get_context_data(**kwargs)
        context['consulta'] = self.procesar()

        # True es por cobrar, False es por pagar
        context['band_cobrar'] = self.band_cobrar
        context['verbose_proceso'] = self.verbose_proceso
        context['conf_tipo'] = self.conf_tipo

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def apply_filter_cadena(self):
        if self.request.POST.get('agencia'):
            return Agencias.objects.get(pk=self.request.POST.get('agencia'))
        elif self.request.POST.get('distribuidor'):
            return Distribuidores.objects.get(pk=self.request.POST.get('distribuidor'))
        elif self.request.POST.get('banca'):
            return Bancas.objects.get(pk=self.request.POST.get('banca'))
        elif self.request.POST.get('bloque'):
            return Bloques.objects.get(pk=self.request.POST.get('bloque'))
        elif self.request.POST.get('operadora'):
            return Operadoras.objects.get(pk=self.request.POST.get('operadora'))
        else:
            return self.object_comercializadora.get_object()

    def procesar(self):
        object_comer = self.apply_filter_cadena()
        comer = object_comer.get_comercializadora()
        comercializadora_ini = self.object_comercializadora.get_object()
        json = {}

        json['titles'] = []
        json['titles'].append({'text': 'N°', 'width': '5%'})

        json['footer'] = []
        json['footer'].append('Total')
        json['footer'].append('')

        verbose_name = 'Comercializadora'
        add_tipo = False
        comercializadoras = []
        if self.request.REQUEST.get('comer_asociada'):
            json['titles'].append({'text': 'Tipo', 'width': '10%'})
            json['footer'].append('')
            add_tipo = True
            # obtiene las comercializadoras asociadas al usuario
            comercializadoras = self.object_user.comercializadora.all()
            json['expandido'] = True
        else:
            # obtiene las comercializadoras asociadas a el ente filtrado
            comercializadoras = comer.get_offspring_level1()
            if object_comer.get_offspring().exists():
                verbose_name = object_comer.get_offspring()[0].get_verbose_name_plural()

        if add_tipo is False:
            _object = object_comer.get_origen()
            texto = None
            if _object:
                if comercializadora_ini.nivel <= _object.nivel:
                    texto = '<a href="#" class="no-link" onclick="{0}"><i class="{1}">Atrás</i></a>'.format(
                            "NavegacionComercializacion({0},'{1}')".format(
                                _object.pk,
                                _object.prefix_filter,
                            ),
                            'icon-keyboard-backspace'
                    )
                    json['atras'] = texto

        json['titles'].append({'text': verbose_name, 'width': '20%'})
        json['titles'].append({'text': self.verbose_proceso, 'width': '35%'})

        json_cadena = []

        json['totales'] = {}
        json['totales']['saldo_actual'] = Decimal()

        json['dia_trabajo'] = self.object_comercializadora.get_dia_trabajo()
        dia = json['dia_trabajo'].dia
        i = 1

        dia_comer = comer.get_dia_trabajo()
        if dia_comer is None:
            messages.warning(
                self.request,
                'La comercializadora {0} no tiene fecha de trabajo'.format(
                    object_comer,
                )
            )
        else:
            if dia_comer.dia.fecha < dia.fecha:
                messages.warning(
                    self.request,
                    'La fecha de trabajo {1} de la comercializadora {0} es anterior a la actual'.format(
                        object_comer,
                        dia_comer.dia.fecha.strftime(FORMAT_STR_DATE)
                    )
                )

        for comercializadora in comercializadoras:
            _object = comercializadora.get_object()

            if comercializadora_ini.nivel >= _object.nivel:
                continue

            if comercializadora.saldo_fecha:
                if comercializadora.saldo_fecha > dia.fecha:
                    # si tiene saldo inicial pero es mayor al dia de trabajo actual
                    continue
            else:
                continue

            try:
                venta = ResumenAdministrativo.objects.get(
                    dia=dia,
                    comercializacion=_object.get_dimension_arco_comercializadora()
                )
            except ResumenAdministrativo.DoesNotExist:
                continue

            json_interna_cadena = {}
            json_interna_cadena['pertenece'] = []
            json_interna_cadena['pertenece'].append(
                self.set_type_html_conf(
                    _type=True,
                    val=i
                )
            )

            if add_tipo:
                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=True,
                        val=_object.get_verbose_name()
                    )
                )
                texto = _object
            else:

                if _object.prefix_filter != 'taquilla':
                    texto = '<a href="#" class="link" onclick="{0}">{1}</a>'.format(
                        "NavegacionComercializacion({0},'{1}')".format(
                            _object.pk,
                            _object.prefix_filter
                        ),
                        _object
                    )

                else:
                    texto = _object.taquilla

            json_interna_cadena['pertenece'].append(
                self.set_type_html_conf(_type=True, val=texto)
            )

            movimientos = Movimiento.objects.filter(
                dia=dia,
                comercializadora_id=comercializadora.pk
            )

            resultado = movimientos.filter(tipo__codename='tipo_deposito')
            depositos = resultado.aggregate(Sum('monto'))['monto__sum']
            depositos = Decimal() if depositos is None else depositos

            resultado = movimientos.filter(tipo__codename='tipo_pago')
            pagos = resultado.aggregate(Sum('monto'))['monto__sum']
            pagos = Decimal() if pagos is None else pagos

            resultado = movimientos.filter(
                tipo__codename__in=('tipo_ajuste_cobrar', 'tipo_ajuste_pagar')
            )
            ajustes = resultado.aggregate(Sum('monto'))['monto__sum']
            ajustes = Decimal() if ajustes is None else ajustes

            cargos = venta.cargo

            saldo_actual = round(venta.saldo_anterior + venta.saldo_oper +
                                 depositos + pagos + ajustes - cargos, 2)

            if saldo_actual < 0:
                if self.band_cobrar:
                    continue
            elif saldo_actual > 0:
                if self.band_cobrar is False:
                    continue
            else:
                continue

            try:
                conf = Configuracion.objects.get(
                    comercializadora=comercializadora,
                    tipo=self.conf_tipo,
                )

                valor = saldo_actual
                if valor < 0:
                    valor = valor * -1

                if conf.min > valor:
                    continue

            except Configuracion.DoesNotExist:
                pass

            json_interna_cadena['pertenece'].append(
                self.set_type_html_conf(
                    _type=False,
                    val=saldo_actual,
                    add_url=comercializadora.pk
                )
            )

            json['totales']['saldo_actual'] += saldo_actual
            json_cadena.append(json_interna_cadena)
            i += 1

        json['content'] = json_cadena
        json['footer'].append(
            round(json['totales']['saldo_actual'], 2)
        )

        if json['content']:
            var_cache = {
                'titulo': 'Reporte - Cuentas {0}'.format(self.verbose_proceso),
                'fecha': dia.fecha.strftime('%d-%m-%Y'),
                'titles': json['titles'],
                'content': json['content'],
                'footer': json['footer'],
                'comercializador': self.object_comercializadora.get_object().nombre,
                'template_name': self.template_name_pdf,
            }

            json['cache_key'] = '{0}_{1}_generate_{2}'.format(
                var_cache['fecha'],
                now().strftime('%Y-%m-%d-%H-%M'),
                self.object_user
            )

            cache.set(
                json['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['cuentas_cobrar_pagar']
            )

        return json

    def set_type_html_conf(self, val, _type=False, align=True, add_class='', add_url=None):
        item = {}
        item['html'] = _type
        item['class'] = ' ' if _type is True or align is False else 'text-align-right '
        item['val'] = val
        item['class'] += add_class
        item['add_url'] = add_url
        return item


class CuentasPorCobrarView(CuentasBase):
    verbose_proceso = 'Por cobrar'
    band_cobrar = True
    conf_tipo = Configuracion.TIPO_PAGAR


class CuentasPorPagarView(CuentasBase):
    verbose_proceso = 'Por pagar'
    band_cobrar = False
    conf_tipo = Configuracion.TIPO_COBRAR


class ConfiguracionPorPagarCobrarView(MyViewBase, TemplateView):
    template_name = 'admin_finanzas/cuentas_operaciones/configuracion_base.html'
    save = False

    def get_context_data(self, **kwargs):
        context = super(ConfiguracionPorPagarCobrarView, self).get_context_data(**kwargs)

        if self.request.REQUEST.get('tipo_configuracion'):
            self.conf_tipo = self.request.REQUEST.get('tipo_configuracion')
        else:
            self.conf_tipo = Configuracion.TIPO_COBRAR

        context['consulta'] = self.procesar()
        context['filter'] = self.filter
        context['tipo_configuracion'] = self.conf_tipo
        context['click'] = self.request.REQUEST.get('click')
        return context

    def post(self, request, *args, **kwargs):
        if request.POST.get('_save'):
            self.save = True
        return self.get(request, *args, **kwargs)

    def apply_filter_cadena(self):
        self.filter = {}
        _object = None
        if self.request.POST.get('agencia'):
            _object = Agencias.objects.get(pk=self.request.POST.get('agencia'))
        elif self.request.POST.get('distribuidor'):
            _object = Distribuidores.objects.get(pk=self.request.POST.get('distribuidor'))
        elif self.request.POST.get('banca'):
            _object = Bancas.objects.get(pk=self.request.POST.get('banca'))
        elif self.request.POST.get('bloque'):
            _object = Bloques.objects.get(pk=self.request.POST.get('bloque'))
        elif self.request.POST.get('operadora'):
            _object = Operadoras.objects.get(pk=self.request.POST.get('operadora'))

        if _object:
            self.filter = {
                'id_comer': 'id_{0}'.format(_object.prefix_filter),
                'name_comer': '{0}'.format(_object.prefix_filter),
                'value_comer': self.request.POST.get('{0}'.format(_object.prefix_filter)),
            }
            return _object
        else:
            return self.object_comercializadora.get_object()

    def procesar(self):
        object_comer = self.apply_filter_cadena()
        comer = object_comer.get_comercializadora()
        json = {}

        json['titles'] = []
        json['titles'].append({'text': 'N°', 'width': '5%'})

        verbose_name = 'Comercializadora'
        add_tipo = False
        comercializadoras = []
        if self.request.REQUEST.get('comer_asociada'):
            json['titles'].append({'text': 'Tipo', 'width': '10%'})
            add_tipo = True
            # obtiene las comercializadoras asociadas al usuario
            comercializadoras = self.object_user.comercializadora.all()
            json['expandido'] = True
        else:
            # obtiene las comercializadoras asociadas a el ente filtrado
            comercializadoras = comer.get_offspring_level1()
            if object_comer.get_offspring().exists():
                verbose_name = object_comer.get_offspring()[0].get_verbose_name_plural()

        comercializadora_ini = self.object_comercializadora.get_object()
        if self.request.REQUEST.get('click'):
            click = int(self.request.REQUEST.get('click'))
        else:
            click = 0

        json_cadena = []
        i = 1
        count_updates = 0

        if click == 0 and add_tipo is False:
            _object = object_comer.get_origen()
            texto = None
            if _object:
                if comercializadora_ini.nivel <= _object.nivel:
                    texto = '<a href="#" class="no-link" onclick="{0}"><i class="{1}">Atrás</i></a>'.format(
                            "NavegacionComercializacion({0},'{1}')".format(
                                _object.pk,
                                _object.prefix_filter,
                            ),
                            'icon-keyboard-backspace',
                    )
                    json['atras'] = texto

        json['titles'].append({'text': verbose_name, 'width': '20%'})
        json['titles'].append({'text': 'Mínimo', 'width': '35%'})
        json['titles'].append({'text': 'Máximo', 'width': '35%'})
        json['titles'].append({'text': 'Opción', 'width': '35%'})

        dia = self.object_comercializadora.get_dia_trabajo().dia
        for comercializadora in comercializadoras:

            if click != 0:
                if click != comercializadora.pk:
                    continue

            _object = comercializadora.get_object()

            if comercializadora_ini.nivel >= _object.nivel:
                continue

            try:
                venta = ResumenAdministrativo.objects.get(
                    dia=dia,
                    comercializacion=_object.get_dimension_arco_comercializadora()
                )
            except ResumenAdministrativo.DoesNotExist:
                continue

            json_interna_cadena = {}
            json_interna_cadena['pertenece'] = []
            json_interna_cadena['pertenece'].append(
                self.set_type_html_conf(
                    _type=True,
                    val=i
                )
            )

            if add_tipo:
                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=True,
                        val=_object.get_verbose_name()
                    )
                )
                texto = _object
            else:
                if click == 0:
                    if _object.prefix_filter != 'taquilla':
                        texto = '<a href="#" class="link" onclick="{0}">{1}</a>'.format(
                            "NavegacionComercializacion({0},'{1}')".format(
                                _object.pk,
                                _object.prefix_filter
                            ),
                            _object
                        )
                    else:
                        texto = '{0}'.format(_object)
                else:
                    texto = '{0}'.format(_object)

            json_interna_cadena['pertenece'].append(
                self.set_type_html_conf(_type=True, val=texto)
            )

            conf = Configuracion.objects.update_or_create(
                comercializadora=comercializadora,
                tipo=self.conf_tipo,
                defaults={}
            )[0]

            movimientos = Movimiento.objects.filter(
                dia=dia,
                comercializadora_id=comercializadora.pk
            )

            resultado = movimientos.filter(tipo__codename='tipo_deposito')
            depositos = resultado.aggregate(Sum('monto'))['monto__sum']
            depositos = Decimal() if depositos is None else depositos

            resultado = movimientos.filter(tipo__codename='tipo_pago')
            pagos = resultado.aggregate(Sum('monto'))['monto__sum']
            pagos = Decimal() if pagos is None else pagos

            resultado = movimientos.filter(
                tipo__codename__in=('tipo_ajuste_cobrar', 'tipo_ajuste_pagar')
            )
            ajustes = resultado.aggregate(Sum('monto'))['monto__sum']
            ajustes = Decimal() if ajustes is None else ajustes

            cargos = venta.cargo

            saldo_actual = round(venta.saldo_anterior + venta.saldo_oper +
                                 depositos + pagos + ajustes - cargos, 2)
            if click == 0:
                if conf.updated_at.date() != now().date() or conf.max == 0:
                    if self.conf_tipo == Configuracion.TIPO_COBRAR:
                        if saldo_actual < 0:
                            conf.max = saldo_actual * -1
                        else:
                            conf.max = 0
                        conf.save(update_fields=['max', 'updated_at'])
                    elif self.conf_tipo == Configuracion.TIPO_PAGAR:
                        if saldo_actual > 0:
                            conf.max = saldo_actual
                        else:
                            conf.max = 0
                        conf.save(update_fields=['max', 'updated_at'])

            if self.save:
                min = self.request.POST.get('min_{0}'.format(comercializadora.pk))
                if min is not None:
                    min = min.replace(',', '.')
                    fields = ['updated_at', ]
                    min = round(float(min), 2)
                    if min != conf.min:
                        conf.min = min
                        fields.append('min')
                        count_updates += 1

                    max = round(
                        float(
                            self.request.POST.get(
                                'max_{0}'.format(
                                    comercializadora.pk)).replace(
                                ',',
                                '.')),
                        2)
                    if max != conf.max:
                        conf.max = max
                        fields.append('max')
                        count_updates += 1

                    if len(fields) > 1:
                        conf.save(update_fields=fields)
            if click == 0:
                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=False,
                        val=round(conf.min, 2)
                    )
                )

                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=False,
                        val=round(conf.max, 2)
                    )
                )

                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=True,
                        val='<button type="submit" value="{0}" name="click"><i class="{1}"></i></button>'.format(
                            comercializadora.pk,
                            'icon-edit2',
                        )
                    )
                )
            else:
                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=True,
                        val="<input id='id_{1}' name='{1}' class='{2}' min='0' value='{0}' pattern='{3}'/>".format(
                            '{0}'.format(round(conf.min, 2)).replace('.', ','),
                            'min_{0}'.format(comercializadora.pk),
                            'min all',
                            '[0-9]+[,]?[0-9]*',
                        )
                    )
                )

                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=True,
                        val="<input id='id_{1}' name='{1}' class='{2}' min='0' value='{0}' pattern='{3}'/>".format(
                            '{0}'.format(round(conf.max, 2)).replace('.', ','),
                            'max_{0}'.format(comercializadora.pk),
                            'max all',
                            '[0-9]+[,]?[0-9]*',
                        )
                    )
                )

                json_interna_cadena['pertenece'].append(
                    self.set_type_html_conf(
                        _type=True,
                        val='<button class="{1}" type="submit" value="_save" name="_save">Guardar</button>'.format(
                            "{0}".format(comercializadora.pk),
                            'btn btn-success',
                        )
                    )
                )

            json_cadena.append(json_interna_cadena)
            i += 1

        json['content'] = json_cadena

        if self.save:
            messages.success(
                self.request,
                'Configuración guardada con éxito!'
            )

        return json

    def set_type_html_conf(self, val, _type=False, align=True, add_class=''):
        item = {}
        item['html'] = _type
        item['class'] = ' ' if _type is True or align is False else 'text-align-right '
        item['val'] = val
        item['class'] += add_class
        return item
