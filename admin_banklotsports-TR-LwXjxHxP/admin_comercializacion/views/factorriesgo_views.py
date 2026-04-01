# -*- coding: utf-8 -*-
from admin_comercializacion.forms import FactorRiesgoForm, FactorRiesgoRowForm
from admin_comercializacion.models import EventNotificationCadena, FactorRiesgo, types_notification_cadena
from admin_comercializacion.task import AsyncProcessInvokeMethod
from admin_comercializacion.views.agencias_views import AgenciasListView
from admin_comercializacion.views.bancas_views import BancasListView
from admin_comercializacion.views.bloques_views import BloquesListView
from admin_comercializacion.views.distribuidores_views import DistribuidoresListView
from admin_finanzas.models import Comercializadora
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_icons import Icons
from admin_lib.util_views import MyViewBase
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.forms.formsets import formset_factory
from django.http import HttpResponseRedirect
from django.views.generic import DetailView, TemplateView


class FactorRiesgoView(MyViewBase):
    model = FactorRiesgo


class FactorRiesgoDetailView(FactorRiesgoView, DetailView):
    pass


class FactorRiesgoUpdateView(FactorRiesgoView, TemplateView):
    model = Comercializadora
    template_name = 'admin_comercializacion/factorriesgo/factorriesgo_form.html'
    filter_form = None

    def get_object(self):
        try:
            self.object = self.model.objects.get(pk=self.kwargs.get('pk'))
            return self.object
        except self.model.DoesNotExist:
            from django.http import Http404
            raise Http404

    def get_success_url_force(self):
        return reverse(
            'admin_comercializacion_{0}_factorriesgo_list'.format(
                self.object.get_object().get_class_name()
            )
        )

    def get_success_url_filter_form(self):
        return '?{0}={1}'.format(
            self.object.get_object().prefix_filter,
            self.object.get_object().pk
        )

    def get_context_data(self, **kwargs):
        '''
        Obtiene el context data
        '''
        context = super(FactorRiesgoUpdateView, self).get_context_data(**kwargs)
        context['object'] = self.object

        return context

    def get_form(self):
        # Obetenemos el view y lo ponemos en el form para poder acceder a los
        # atributos
        FactorRiesgoRowForm.object_comer = self.get_object()
        return formset_factory(
            FactorRiesgoRowForm,
            formset=FactorRiesgoForm,
        )

    def get_filter_form(self):
        '''
        Retorna el formulario de la instancia,
        de ya estar inicializado devuelve el que esta en memoria
        '''
        if self.filter_form is None:
            form = self.get_form()
            if self.request.method == 'POST':
                self.filter_form = form(self.request.POST,)
            else:
                initial = []
                for factor in self.object.get_factores_riesgo().factores:
                    initial.append(
                        {
                            'rango_inicial': factor[0],
                            'rango_final': factor[1],
                            'porcentaje': factor[2],
                        }
                    )

                self.filter_form = form(initial=initial)

        return self.filter_form

    def post(self, request, *args, **kwargs):
        formset = self.get_filter_form()

        if formset.is_valid():
            factores = []
            for form in formset.forms:
                if form.cleaned_data.get('rango_inicial'):
                    factores.append(
                        [
                            form.cleaned_data['rango_inicial'],
                            form.cleaned_data['rango_final'],
                            form.cleaned_data['porcentaje'],
                        ]
                    )

            FactorRiesgo.objects.update_or_create(
                comercializadora_id=self.object.id,
                defaults={
                    'factores': factores,
                }
            )

            # Fragmento de codigo, envia la notificacion de cadena de comercializacion
            # ########################################################################
            kwargs_notificacion = {
                'data_origin': types_notification_cadena['factor_riesgo'][0],
                'data': factores,
            }

            kwargs_notificacion[
                self.object.get_object().prefix_filter
            ] = self.object.get_object().pk

            EventNotificationCadena.objects.create(
                **kwargs_notificacion
            )
            # ########################################################################

            ##########################################################################
            kwargs_async = {
                'session_id': '{0}'.format(self.object_session.pk),
                'parametros': {
                    'comercializadora': self.object.id,
                },
            }

            # Invocando proceso asyncrono que ejecutará la función
            AsyncProcessInvokeMethod.func_delay(
                FactorRiesgoUpdateView.delete_factores,
                kwargs_async
            )

            return HttpResponseRedirect(
                self.get_success_url()
            )
        else:
            return self.get(request, *args, **kwargs)

    def delete_factores(kwargs):
        comercializadora = Comercializadora.objects.only('id').get(
            pk=kwargs.get('comercializadora'))

        cont = 0
        childs = comercializadora.get_offspring().values_list('id', flat=True)
        for child in childs:
            factores_comer = FactorRiesgo.objects.only('id').filter(comercializadora_id=child)
            key = 'factorriesgo_{0}'.format(child)
            cache.delete(key)
            for factor_comer in factores_comer:
                cont += 1
                factor_comer.audit_save = False
                factor_comer.delete()

        return ['{0} comercializadora(s) gestionada(s)'.format(cont)]


class FactorRiesgoListView(MyViewBase):
    template_name = 'admin_comercializacion/factorriesgo/factorriesgo_list.html'


class BloquesFactorRiesgoListView(FactorRiesgoListView, BloquesListView):

    def get_context_data(self, **kwargs):
        context = super(BloquesFactorRiesgoListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Bloques'
        context['model'] = 'Bloques'
        return context


class BancasFactorRiesgoListView(FactorRiesgoListView, BancasListView):

    def get_context_data(self, **kwargs):
        context = super(BancasFactorRiesgoListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Bancas'
        context['model'] = 'Bancas'
        return context


class DistribuidoresFactorRiesgoListView(FactorRiesgoListView, DistribuidoresListView):

    def get_context_data(self, **kwargs):
        context = super(DistribuidoresFactorRiesgoListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Distribuidores'
        context['model'] = 'Distribuidores'
        return context


class AgenciasFactorRiesgoListView(FactorRiesgoListView, AgenciasListView):

    def get_context_data(self, **kwargs):
        context = super(AgenciasFactorRiesgoListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Centros de apuesta'
        context['model'] = 'Agencias'
        return context


class FactorRiesgoDatatableView(MyViewBase, BaseDatatableView):
    # Orden del filtro
    order_columns = ['nombre']
    # Patron de busqueda
    filter_search = 'nombre'

    opcions_url = [
        'admin_comercializacion_factorriesgo_detail$' + Icons.detail,
        'admin_comercializacion_factorriesgo_update$' + Icons.update,
    ]

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            factor = item.get_comercializadora().get_factores_riesgo()
            json_data.append([
                (x + 1 + acarreo),
                item.nombre,
                "<span class='right'>{0}</span>".format(
                    len(factor.factores)
                ),
                "<i title='{0}' class='icon-clock'><i>{1}".format(
                    factor.updated_at,
                    naturaltime(factor.updated_at)
                ),
                self.get_opcions(pk=item.get_comercializadora().id)
            ])
        return json_data


class BloquesFactorRiesgoDatatableView(FactorRiesgoDatatableView, BloquesFactorRiesgoListView):
    pass


class BancasFactorRiesgoDatatableView(FactorRiesgoDatatableView, BancasFactorRiesgoListView):
    pass


class DistribuidoresFactorRiesgoDatatableView(FactorRiesgoDatatableView, DistribuidoresFactorRiesgoListView):
    pass


class AgenciasFactorRiesgoDatatableView(FactorRiesgoDatatableView, AgenciasFactorRiesgoListView):
    pass
