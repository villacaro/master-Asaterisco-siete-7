# -*- coding: utf-8 -*-
from admin_comercializacion.forms import UpdatePorcentajeForm
from admin_comercializacion.models import Bancas, Porcentajes, TipoPorcentajes
from admin_comercializacion.task import AsyncProcessInvokeMethod
from admin_comercializacion.views.agencias_views import AgenciasListView
from admin_comercializacion.views.bancas_views import BancasListView
from admin_comercializacion.views.bloques_views import BloquesListView
from admin_comercializacion.views.distribuidores_views import DistribuidoresListView
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_icons import Icons
from admin_lib.util_views import MyViewBase
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.urlresolvers import reverse
from django.utils.timezone import now
from django.views.generic.edit import FormView


class PorcentajesListView(MyViewBase):
    template_name = 'admin_comercializacion/porcentajes/porcentajes_list.html'

    def get_context_data(self, **kwargs):
        '''
        Obtiene el context data
        '''
        context = super(PorcentajesListView, self).get_context_data(**kwargs)
        kwargs = {}
        kwargs[self.model().prefix_filter] = True
        context['tipos_porcentajes'] = TipoPorcentajes.objects.filter(
            **kwargs
        ).order_by('orden')

        return context


class BloquesPorcentajesListView(PorcentajesListView, BloquesListView):

    def get_context_data(self, **kwargs):
        context = super(BloquesPorcentajesListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Bloques'
        context['model'] = 'Bloques'
        return context


class BancasPorcentajesListView(PorcentajesListView, BancasListView):

    def get_queryset(self):

        bancas = super(BancasPorcentajesListView, self).get_queryset()

        form = self.get_filter_form()
        kwargs = {
            'modelo_negocio': Bancas.modelo_negocio_codenames['codename_negocio_alquiler']
        }
        if 'banca' in form.fields:
            form.fields['banca'].queryset = form.fields['banca'].queryset.exclude(**kwargs)

        self.filter_form = form

        return bancas.exclude(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(BancasPorcentajesListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Bancas'
        context['model'] = 'Bancas'
        return context


class DistribuidoresPorcentajesListView(PorcentajesListView, DistribuidoresListView):

    def get_queryset(self):

        distribuidores = super(DistribuidoresPorcentajesListView, self).get_queryset()

        form = self.get_filter_form()
        kwargs = {
            'modelo_negocio': Bancas.modelo_negocio_codenames['codename_negocio_alquiler']
        }
        if 'banca' in form.fields:
            form.fields['banca'].queryset = form.fields['banca'].queryset.exclude(**kwargs)

        kwargs['banca__modelo_negocio'] = kwargs.pop('modelo_negocio')

        if 'distribuidor' in form.fields:
            form.fields['distribuidor'].queryset = form.fields['distribuidor'].queryset.exclude(
                **kwargs
            )

        self.filter_form = form

        return distribuidores.exclude(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(DistribuidoresPorcentajesListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Distribuidores'
        context['model'] = 'Distribuidores'
        return context


class AgenciasPorcentajesListView(PorcentajesListView, AgenciasListView):

    def get_queryset(self):

        agencias = super(AgenciasPorcentajesListView, self).get_queryset()

        form = self.get_filter_form()
        kwargs = {
            'modelo_negocio': Bancas.modelo_negocio_codenames['codename_negocio_alquiler']
        }
        if 'banca' in form.fields:
            form.fields['banca'].queryset = form.fields['banca'].queryset.exclude(**kwargs)

        kwargs['banca__modelo_negocio'] = kwargs.pop('modelo_negocio')

        if 'distribuidor' in form.fields:
            form.fields['distribuidor'].queryset = form.fields['distribuidor'].queryset.exclude(
                **kwargs
            )

        kwargs['distribuidores__banca__modelo_negocio'] = kwargs.pop('banca__modelo_negocio')

        if 'agencia' in form.fields:
            form.fields['agencia'].queryset = form.fields['agencia'].queryset.exclude(
                **kwargs
            )

        self.filter_form = form

        return agencias.exclude(**kwargs)

    def get_context_data(self, **kwargs):
        context = super(AgenciasPorcentajesListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Centros de apuesta'
        context['model'] = 'Agencias'
        return context


class PorcentajesFunctionsView(object):

    def create_form(
        self,
        context,
        object_,
        sucesor,
        bloques,
        bancas,
        distribuidores,
        agencias
    ):

        form_list = []
        firts_column = []
        ptype = object_.get_class_name()
        for x, porcentaje in enumerate(self.get_porcentajes_types()):
            column = []
            column.append(str(porcentaje.nombre))
            if ptype != 'bloques':  # Maximo para todos excepto el bloque
                if x == 0:
                    firts_column.append('Maximo')

                column.append(
                    {
                        'perc': context['form']['max_' + str(porcentaje.codename)]
                    }
                )

            if bloques is not None:
                object_comer = bloques[0].get_object()
                if (
                    self.object_comercializadora.get_type().content_type <
                    object_comer.get_type().content_type
                ):
                    if x == 0:
                        firts_column.append(
                            '<span title="{0}""> {0} </span>'.format(
                                object_comer.get_verbose_name()
                            )
                        )
                    column.append(
                        {
                            'perc': context['form'][object_comer.prefix_filter_plural + '_' + str(porcentaje.codename)]
                        }
                    )
            if bancas is not None:
                object_comer = bancas[0].get_object()
                if (
                    self.object_comercializadora.get_type().content_type <
                    object_comer.get_type().content_type
                ):
                    if x == 0:
                        firts_column.append(
                            '<span title="{0}"> {0} </span>'.format(
                                object_comer.get_verbose_name()
                            )
                        )
                    relacion = None
                    if porcentaje.codename == 'porcentaje_comision':
                        relacion = context['form'][object_comer.prefix_filter_plural +
                                                   '_' + str(porcentaje.codename) + '_relacion']
                    if ptype == 'bancas':
                        column.append(
                            {
                                'perc': context['form'][
                                    object_comer.prefix_filter_plural + '_' + str(porcentaje.codename)
                                ],
                                'rel': relacion
                            }
                        )
                    else:
                        column.append(
                            {
                                'perc': context['form'][
                                    object_comer.prefix_filter_plural + '_' + str(porcentaje.codename)
                                ]
                            }
                        )
            if distribuidores is not None:
                object_comer = distribuidores[0].get_object()
                if (
                    self.object_comercializadora.get_type().content_type <
                    object_comer.get_type().content_type
                ):
                    if x == 0:
                        firts_column.append(
                            '<span title="{0}"> {0} </span>'.format(
                                object_comer.get_verbose_name()
                            )
                        )
                    relacion = None
                    if porcentaje.codename == 'porcentaje_comision':
                        relacion = context['form'][object_comer.prefix_filter_plural +
                                                   '_' + str(porcentaje.codename) + '_relacion']
                    if ptype == 'distribuidores':
                        column.append(
                            {
                                'perc': context['form'][
                                    object_comer.prefix_filter_plural + '_' + str(porcentaje.codename)
                                ],
                                'rel': relacion
                            }
                        )
                    else:
                        column.append(
                            {
                                'perc': context['form'][
                                    object_comer.prefix_filter_plural + '_' + str(porcentaje.codename)
                                ]
                            }
                        )
            if agencias is not None:
                object_comer = agencias[0].get_object()
                if (
                    self.object_comercializadora.get_type().content_type <
                    object_comer.get_type().content_type
                ):
                    if x == 0:
                        firts_column.append(
                            '<span title="{0}"> {0} </span>'.format(
                                object_comer.get_verbose_name()
                            )
                        )
                    column.append(
                        {
                            'perc': context['form'][object_comer.prefix_filter_plural + '_' + str(porcentaje.codename)]
                        }
                    )

            form_list.append(column)

        context['firts_column'] = firts_column
        context['form_list'] = form_list
        return context

    def get_porcentajes_types(self):
        return TipoPorcentajes.objects.all().order_by('orden')

    @staticmethod
    def get_porcentajes(object_, tipo):
        return object_.get_queryset_porcentajes().filter(tipo=tipo)

    @staticmethod
    def get_last_porcentaje(object_, tipo):
        percs = PorcentajesFunctionsView.get_porcentajes(object_, tipo)
        if percs.exists():
            return percs[0]
        return None

    @staticmethod
    def get_diferencia(object_, tipo, field, maximo):
        ptype = object_.get_class_name()
        if ptype == 'bancas':
            if PorcentajesFunctionsView.get_porcentajes(object_.bloque, tipo).exists():
                old = PorcentajesFunctionsView.get_porcentajes(object_.bloque, tipo)[0]
                return float(old.porcentaje_maximo) - float(field)
        if ptype == 'distribuidores':
            if PorcentajesFunctionsView.get_porcentajes(object_.banca, tipo).exists():
                old = PorcentajesFunctionsView.get_porcentajes(object_.banca, tipo)[0]
                return float(old.porcentaje_maximo) - float(old.bloque_porc) - float(field)
        if ptype == 'agencias':
            if PorcentajesFunctionsView.get_porcentajes(object_.distribuidores, tipo).exists():
                old = PorcentajesFunctionsView.get_porcentajes(object_.distribuidores, tipo)[0]
                return float(old.porcentaje_maximo) - float(old.bloque_porc) - \
                    float(old.banca_porc) - float(field)

    def get_maximo(self, object_, tipo, maximo):
        ptype = object_.get_class_name()
        if ptype == 'bloques':
            if self.get_porcentajes(object_, tipo).exists():
                old = self.get_porcentajes(object_, tipo)[0]
                return round(old.porcentaje_maximo, 2)
        if ptype == 'bancas':
            if self.get_porcentajes(object_.bloque, tipo).exists():
                old = self.get_porcentajes(object_.bloque, tipo)[0]
                return round(old.porcentaje_maximo, 2)
        if ptype == 'distribuidores':
            if self.get_porcentajes(object_.banca, tipo).exists():
                old = self.get_porcentajes(object_.banca, tipo)[0]
                return round(maximo - old.bloque_porc, 2)
        if ptype == 'agencias':
            if self.get_porcentajes(object_.distribuidores, tipo).exists():
                old = self.get_porcentajes(object_.distribuidores, tipo)[0]
                return round(maximo - old.bloque_porc - old.banca_porc, 2)

    def edit_porcentajes(self, object_, tipo, field):
        if object_.get_class_name() == 'bloques':
            objects = object_.bancas_set.all()
        elif object_.get_class_name() == 'bancas':
            objects = object_.distribuidores_set.all()
        elif object_.get_class_name() == 'distribuidores':
            objects = object_.agencias_set.all()
        elif object_.get_class_name() == 'agencias':
            objects = None

        if self.get_porcentajes(object_, tipo).exists():
            object_porc = self.get_porcentajes(object_, tipo)[0]
            maximo = object_porc.porcentaje_maximo
            bloque_porc = object_porc.bloque_porc
            banca_porc = object_porc.banca_porc
        if objects is not None:
            for obj in objects:
                old = None
                diferencia = 0
                porcentaje_ganancia = 0
                if self.get_porcentajes(obj, tipo).exists():
                    old = self.get_porcentajes(obj, tipo)[0]
                    old.fecha_fin = now()
                    old.save(update_fields=['fecha_fin'])
                if old:
                    diferencia = round((float(field) - float(old.porcentaje_ganancia)), 4)
                    porcentaje_ganancia = old.porcentaje_ganancia
                if object_.get_class_name() == 'bloques':
                    Porcentajes.objects.create(
                        fecha_inicio=now(),
                        porcentaje_ganancia=0,
                        banca=obj,
                        tipo=tipo,
                        porcentaje_maximo=field,
                        bloque_porc=field
                    )
                    self.edit_porcentajes(obj, tipo, 0)
                elif object_.get_class_name() == 'bancas':
                    Porcentajes.objects.create(
                        fecha_inicio=now(),
                        porcentaje_ganancia=0,
                        distribuidor=obj,
                        tipo=tipo,
                        porcentaje_maximo=maximo,
                        bloque_porc=bloque_porc,
                        banca_porc=field
                    )
                    self.edit_porcentajes(obj, tipo, 0)
                elif object_.get_class_name() == 'distribuidores':
                    distribuidor_porc_new = field
                    if diferencia > 0:
                        distribuidor_porc_new = round(diferencia, 4)
                    Porcentajes.objects.create(
                        fecha_inicio=now(),
                        porcentaje_ganancia=porcentaje_ganancia,
                        agencia=obj,
                        tipo=tipo,
                        porcentaje_maximo=maximo,
                        bloque_porc=bloque_porc,
                        banca_porc=banca_porc,
                        distribuidor_porc=distribuidor_porc_new
                    )


class PorcentajesFormView(MyViewBase, PorcentajesFunctionsView, FormView):
    form_class = UpdatePorcentajeForm
    template_name = 'admin_comercializacion/porcentajes/porcentajes_form.html'
    model = Porcentajes

    def get_model(self):
        try:
            from django.db.models import get_app
            return getattr(
                get_app('admin_comercializacion'),
                self.kwargs.get('type').capitalize()
            )
        except Exception:
            from django.http import Http404
            raise Http404

    def get_object(self):
        try:
            model = self.get_model()
            return model.objects.get(
                pk=self.kwargs.get('pk')
            )

        except Exception:
            from django.http import Http404
            raise Http404

    @staticmethod
    def get_object_by_type(type, pk):
        try:
            from django.db.models import get_app
            model = getattr(
                get_app('admin_comercializacion'),
                type.capitalize()
            )
            return model.objects.get(
                pk=pk
            )

        except Exception:
            from django.http import Http404
            raise Http404

    def get_success_url_force(self):
        if self.request.GET.get('ccadena'):
            return reverse(
                'admin_users_users_create'
            )

        return reverse(
            'admin_comercializacion_{0}_porcentajes_list'.format(
                self.object.get_class_name()
            )
        )

    def get_success_url_filter_form(self):
        '''
        Devuelve los filtros equivalentes
        '''
        if self.request.GET.get('ccadena'):
            app = self.object.__module__.split('.')[0]
            model = self.object.__class__.__name__.lower()

            if model != 'agencias':
                return '?ccadena={0}&next={1}'.format(
                    self.object.get_comercializadora().pk,
                    reverse('{0}_{1}_list'.format(app, model))
                )
            else:
                return '?ccadena={0}&next={1}'.format(
                    self.object.get_comercializadora().pk,
                    reverse(
                        '{0}_{1}_detail'.format(app, model),
                        kwargs={'pk': self.object.pk}
                    )
                )

        return '?{0}={1}'.format(
            self.object.prefix_filter,
            self.object.pk
        )

    def get_context_data(self, **kwargs):
        context = super(PorcentajesFormView, self).get_context_data(**kwargs)

        # Saco el tipo de cadena
        context['object'] = self.object = self.get_object()
        ptype = self.object.get_class_name()
        if ptype == 'bloques':
            bloques = Porcentajes.objects.filter(
                bloque=self.object,
                fecha_fin=None
            ).order_by('tipo__orden')
            bancas = None
            distribuidores = None
            agencias = None
            sucesor = bloques
        elif ptype == 'bancas':
            bancas = Porcentajes.objects.filter(
                banca=self.object,
                fecha_fin=None
            ).order_by('tipo__orden')
            bloques = Porcentajes.objects.filter(
                bloque=self.object.bloque,
                fecha_fin=None
            ).order_by('tipo__orden')
            distribuidores = None
            agencias = None
            sucesor = bancas
        elif ptype == 'distribuidores':
            bloques = Porcentajes.objects.filter(
                bloque=self.object.banca.bloque,
                fecha_fin=None
            ).order_by('tipo__orden')
            bancas = Porcentajes.objects.filter(
                banca=self.object.banca,
                fecha_fin=None
            ).order_by('tipo__orden')
            distribuidores = Porcentajes.objects.filter(
                distribuidor=self.object,
                fecha_fin=None
            ).order_by('tipo__orden')
            agencias = None
            sucesor = distribuidores
        elif ptype == 'agencias':
            bloques = Porcentajes.objects.filter(
                bloque=self.object.distribuidores.banca.bloque,
                fecha_fin=None
            ).order_by('tipo__orden')
            bancas = Porcentajes.objects.filter(
                banca=self.object.distribuidores.banca,
                fecha_fin=None
            ).order_by('tipo__orden')
            distribuidores = Porcentajes.objects.filter(
                distribuidor=self.object.distribuidores,
                fecha_fin=None
            ).order_by('tipo__orden')
            agencias = Porcentajes.objects.filter(
                agencia=self.object,
                fecha_fin=None
            ).order_by('tipo__orden')
            sucesor = agencias

        context = self.create_form(
            context,
            self.object,
            sucesor,
            bloques,
            bancas,
            distribuidores,
            agencias
        )

        return context

    @staticmethod
    def set_bloques_perc(object_, field, old, perc_type, parent_perc, relacion=True):
        porcentaje = None
        if old is None:
            porcentaje = Porcentajes.objects.create(
                fecha_inicio=now(),
                porcentaje_ganancia=field,
                bloque=object_,
                tipo=perc_type,
                porcentaje_maximo=field
            )
        else:
            if field != old.porcentaje_ganancia:
                old.fecha_fin = now()
                old.audit_save = False

                old.save(update_fields=['fecha_fin'])
                porcentaje = Porcentajes.objects.create(
                    fecha_inicio=now(),
                    porcentaje_ganancia=field,
                    bloque=object_,
                    tipo=perc_type,
                    porcentaje_maximo=field
                )
        # Recorro todas las agencias de ese distribuidor
        bancas = object_.bancas_set.all()
        for banca in bancas:
            old = PorcentajesFormView.get_last_porcentaje(banca, perc_type)
            if old is not None:
                PorcentajesFormView.set_bancas_perc(
                    banca,
                    old.porcentaje_ganancia,
                    old,
                    perc_type,
                    porcentaje)

    @staticmethod
    def set_bancas_perc(object_, field, old, perc_type, parent_perc, relacion=True):
        diferencia = PorcentajesFormView.get_diferencia(object_, perc_type, field, 0)
        porcentaje = None
        if old is None:
            porcentaje = Porcentajes.objects.create(
                fecha_inicio=now(),
                porcentaje_ganancia=field,
                banca=object_,
                tipo=perc_type,
                porcentaje_maximo=parent_perc.porcentaje_maximo,
                bloque_porc=diferencia,
                relacion=relacion
            )
        else:
            if field != old.porcentaje_ganancia or diferencia != old.bloque_porc or relacion is not True:
                # Si la diferencia es negativa eso quiere decir que es menor
                if diferencia < 0:
                    field = float(field) + float(diferencia)
                    diferencia = 0
                old.fecha_fin = now()
                old.audit_save = False

                old.save(update_fields=['fecha_fin'])
                porcentaje = Porcentajes.objects.create(
                    fecha_inicio=now(),
                    porcentaje_ganancia=field,
                    banca=object_,
                    tipo=perc_type,
                    porcentaje_maximo=parent_perc.porcentaje_maximo,
                    bloque_porc=diferencia,
                    relacion=relacion
                )
        # Recorro todas las agencias de ese distribuidor
        distribuidores = object_.distribuidores_set.all()
        for dist in distribuidores:
            old = PorcentajesFormView.get_last_porcentaje(dist, perc_type)
            if old is not None:
                PorcentajesFormView.set_distribuidores_perc(
                    dist,
                    old.porcentaje_ganancia,
                    old,
                    perc_type,
                    porcentaje)

    @staticmethod
    def set_distribuidores_perc(object_, field, old, perc_type, parent_perc, relacion=True):
        diferencia = PorcentajesFormView.get_diferencia(object_, perc_type, field, 0)
        porcentaje = None
        if old is None:
            porcentaje = Porcentajes.objects.create(
                fecha_inicio=now(),
                porcentaje_ganancia=field,
                distribuidor=object_,
                tipo=perc_type,
                porcentaje_maximo=parent_perc.porcentaje_maximo,
                bloque_porc=parent_perc.bloque_porc,
                banca_porc=diferencia,
                relacion=relacion
            )
        else:
            if field != old.porcentaje_ganancia or diferencia != old.banca_porc or relacion is not True:
                # Si la diferencia es negativa eso quiere decir que es menor
                if diferencia < 0:
                    field = float(field) + float(diferencia)
                    diferencia = 0
                old.fecha_fin = now()
                old.audit_save = False
                old.save(update_fields=['fecha_fin'])
                porcentaje = Porcentajes.objects.create(
                    fecha_inicio=now(),
                    porcentaje_ganancia=field,
                    distribuidor=object_,
                    tipo=perc_type,
                    porcentaje_maximo=parent_perc.porcentaje_maximo,
                    bloque_porc=parent_perc.bloque_porc,
                    banca_porc=diferencia,
                    relacion=relacion
                )
        # Recorro todas las agencias de ese distribuidor
        agencias = object_.agencias_set.all()
        for agencia in agencias:
            old = PorcentajesFormView.get_last_porcentaje(agencia, perc_type)
            if old is not None:
                PorcentajesFormView.set_agencias_perc(
                    agencia,
                    old.porcentaje_ganancia,
                    old,
                    perc_type,
                    porcentaje
                )

    @staticmethod
    def set_agencias_perc(object_, field, old, perc_type, parent_perc, relacion=True):
        diferencia = PorcentajesFormView.get_diferencia(object_, perc_type, field, 0)
        if old is None:
            Porcentajes.objects.create(
                fecha_inicio=now(),
                porcentaje_ganancia=field,
                agencia=object_,
                tipo=perc_type,
                porcentaje_maximo=parent_perc.porcentaje_maximo,
                bloque_porc=parent_perc.bloque_porc,
                banca_porc=parent_perc.banca_porc,
                distribuidor_porc=diferencia
            )
        else:
            if field != old.porcentaje_ganancia \
                    or diferencia != old.distribuidor_porc:
                # Si la diferencia es negativa eso quiere decir que es menor
                if diferencia < 0:
                    field = float(field) + float(diferencia)
                    diferencia = 0
                old.fecha_fin = now()

                old.audit_save = False
                old.save(update_fields=['fecha_fin'])
                Porcentajes.objects.create(
                    fecha_inicio=now(),
                    porcentaje_ganancia=field,
                    agencia=object_,
                    tipo=perc_type,
                    porcentaje_maximo=parent_perc.porcentaje_maximo,
                    bloque_porc=parent_perc.bloque_porc,
                    banca_porc=parent_perc.banca_porc,
                    distribuidor_porc=diferencia
                )

    def form_valid(self, form):
        self.object = self.get_object()
        comer_type = self.object.get_class_name()
        enrro = False
        porcentajes_types = self.get_porcentajes_types()
        # Tipo de porcentajes
        for x, perc_type in enumerate(porcentajes_types):
            field = round((form.cleaned_data['{0}_{1}'.format(comer_type, perc_type.codename)] / 100), 4)
            relacion = True
            if perc_type.codename == 'porcentaje_comision' \
                    and (self.object.get_class_name() == 'bancas' or self.object.get_class_name() == 'distribuidores'):
                relacion = form.cleaned_data['{0}_{1}_relacion'.format(comer_type, perc_type.codename)]
            old = PorcentajesFormView.get_last_porcentaje(self.object, perc_type)

            if old:
                if field == old.porcentaje_ganancia \
                        and relacion == old.relacion:
                    # Si es el mismo porcentaje no se verifica nada
                    # y se continua con el proximo
                    continue

                maximo = old.porcentaje_maximo

                if field > self.get_maximo(self.object, perc_type, maximo) and comer_type != 'bloques':
                    enrro = True

                    form._errors = 'El porcentaje no puede ser mayor al del nivel superior'

            if not enrro:
                kwargs_async = {
                    'session_id': '{0}'.format(self.object_session.pk),
                    'parametros': {
                        'object': self.get_object().pk,
                        'type': self.object.get_class_name(),
                        'field': field,
                        'perc_type': perc_type.codename,
                        'relacion': relacion
                    }
                }
                AsyncProcessInvokeMethod.func_delay(
                    PorcentajesFormView.savePorcentajes,
                    kwargs_async
                )

        if enrro:
            return super(PorcentajesFormView, self).form_invalid(form)
        return super(PorcentajesFormView, self).form_valid(form)

    @staticmethod
    def savePorcentajes(kwargs):
        perc_type = TipoPorcentajes.objects.get(codename=kwargs.get('perc_type'))
        object_ = PorcentajesFormView.get_object_by_type(kwargs.get('type'), kwargs.get('object'))
        parent_perc = PorcentajesFormView.get_last_porcentaje(object_.get_origen(), perc_type)
        old = PorcentajesFormView.get_last_porcentaje(object_, perc_type)
        function = getattr(PorcentajesFormView, 'set_{0}_perc'.format(object_.get_class_name()))
        function(
            object_,
            float(kwargs.get('field')),
            old,
            perc_type,
            parent_perc,
            relacion=kwargs.get('relacion'))


class PorcentajesDatatableView(MyViewBase, BaseDatatableView):
    # Orden del filtro
    order_columns = ['nombre']
    # Patron de busqueda
    filter_search = 'nombre'

    opcions_url = ['admin_comercializacion_porcentajes_update$' + Icons.update]

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            array = [(x + 1 + acarreo), item.nombre]
            for porcentaje in item.get_queryset_porcentajes():
                html = ''
                html += '<span title="Actualizado ' + str(naturaltime(porcentaje.updated_at)) + '" class="right">'
                html += str(intcomma(porcentaje.get_porcentaje())) + '%'
                html += '</span>'
                array.append(html)
            array.append(self.get_opcions(pk=item.pk, tipo=self.request.GET.get('cadena').lower()))
            json_data.append(array)
        return json_data


class BloquesPorcentajesDatatableView(PorcentajesDatatableView, BloquesPorcentajesListView):
    pass


class BancasPorcentajesDatatableView(PorcentajesDatatableView, BancasPorcentajesListView):
    pass


class DistribuidoresPorcentajesDatatableView(PorcentajesDatatableView, DistribuidoresPorcentajesListView):
    pass


class AgenciasPorcentajesDatatableView(PorcentajesDatatableView, AgenciasPorcentajesListView):
    pass
