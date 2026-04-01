# -*- coding: utf-8 -*-
from admin_asterisco7.settings import FORMAT_STR_DATETIME
from admin_comercializacion.forms import TaquillaForm, UpdateTaquillaForm
from admin_comercializacion.models import Taquillas
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class TaquillasView(MyViewBase):
    model = Taquillas

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return Taquillas.objects.filter(
            agencia__distribuidores__banca__bloque__operadora=self.object_comercializadora.get_object()
        )

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return Taquillas.objects.filter(
            agencia__distribuidores__banca__bloque=self.object_comercializadora.get_object()
        )

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """
        return Taquillas.objects.filter(
            agencia__distribuidores__banca=self.object_comercializadora.get_object()
        )

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        return Taquillas.objects.filter(
            agencia__distribuidores=self.object_comercializadora.get_object()
        )

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una agencia
        """
        return Taquillas.objects.filter(
            agencia__distribuidores=self.object_comercializadora.get_object()
        )

    def get_queryset(self):
        """
        Define el queryset inicial
        """
        return self.set_execute_function_by_profile(
            **{
                'prefix': 'filter',
                'instance': self
            }
        )

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        if self.get_profile().codename == 'userprofile_operadora':
            return '?bloque={0}&banca={1}&distribuidor={2}&agencia={3}'.format(
                self.object.agencia.distribuidores.banca.bloque_id,
                self.object.agencia.distribuidores.banca_id,
                self.object.agencia.distribuidores_id,
                self.object.agencia_id,
            )
        elif self.get_profile().codename == 'userprofile_bloque':
            return '?banca={0}&distribuidor={1}&agencia={2}'.format(
                self.object.agencia.distribuidores.banca_id,
                self.object.agencia.distribuidores_id,
                self.object.agencia_id,
            )
        elif self.get_profile().codename == 'userprofile_banca':
            return '?distribuidor={0}&agencia={1}'.format(
                self.object.agencia.distribuidores_id,
                self.object.agencia_id,
            )
        elif self.get_profile().codename == 'userprofile_agencia':
            return '?distribuidor={0}&agencia={1}'.format(
                self.object.agencia.distribuidores_id,
                self.object.agencia_id,
            )
        else:
            return ''


class TaquillasCreateView(TaquillasView, CreateView):
    form_class = TaquillaForm


class TaquillasDeleteView(TaquillasView, DeleteView):

    def delete(self, request, *args, **kwargs):
        app = self.model().__module__.split('.')[0]
        model = self.model().__class__.__name__.lower()

        self.object = self.get_object()
        concat_delete = '_delete_{0}'.format(now().strftime(FORMAT_STR_DATETIME))
        taquilla = self.object.taquilla
        self.object.taquilla += concat_delete
        self.object.save()

        user = self.object.get_user()
        user.user += concat_delete
        user.save()

        self.object.set_new_status('status_eliminado')

        if isinstance(self.model()._meta.verbose_name, str):
            verbose = self.model()._meta.verbose_name
        else:
            verbose = model

        messages.warning(
            self.request,
            '¡Enhorabuena! {0} {1} '
            'Esta siendo eliminada, esto solo llevara unos segundos!'.format(
                verbose,
                taquilla
            )
        )

        return HttpResponseRedirect(
            reverse('{0}_{1}_list'.format(app, model)) + self.get_success_url_filter_form()
        )


class TaquillasDetailView(TaquillasView, DetailView):
    pass


class TaquillasListView(TaquillasView, ListView):
    filter_form = None
    form_class = FilterCadenaComercializacionForm
    template_name = 'admin_comercializacion/taquillas/taquillas_list.html'

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        self.verbose_title_suc = 'Bancas'
        return self.object_comercializadora.get_object().bloques_set.all()

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        self.verbose_title_suc = 'Distribuidores'
        return self.object_comercializadora.get_object().bancas_set.all()

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """
        self.verbose_title_suc = 'Centros de apuesta'
        return self.object_comercializadora.get_object().distribuidores_set.all()

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        self.verbose_title_suc = 'Taquillas'
        return self.object_comercializadora.get_object().agencias_set.all()

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una agencia
        """
        self.verbose_title_suc = 'Taquillas'
        return self.object_comercializadora.get_object().taquillas_set.all()

    def get_queryset(self):

        queryset = Taquillas.objects.none()
        if self.get_filter_form().is_valid():

            bloque = self.get_filter_form().cleaned_data.get('bloque')
            banca = self.get_filter_form().cleaned_data.get('banca')
            distribuidor = self.get_filter_form().cleaned_data.get('distribuidor')
            agencia = self.get_filter_form().cleaned_data.get('agencia')

            if self.request.REQUEST:
                if agencia:
                    queryset = Taquillas.objects.filter(agencia_id=agencia.pk)
                    self.verbose_title_suc = 'Taquillas'
                elif distribuidor:
                    queryset = distribuidor.agencias_set.all()
                    self.verbose_title_suc = 'Taquillas'
                elif banca:
                    queryset = banca.distribuidores_set.all()
                    self.verbose_title_suc = 'Centros de apuesta'
                elif bloque:
                    queryset = bloque.bancas_set.all()
                    self.verbose_title_suc = 'Distribuidores'
                else:
                    queryset = self.set_execute_function_by_profile(
                        **{
                            'prefix': 'filter',
                            'instance': self
                        }
                    )
        return queryset

    def get_context_data(self, **kwargs):
        context = super(TaquillasListView, self).get_context_data(**kwargs)
        if hasattr(self, 'verbose_title_suc'):
            context['verbose_title_suc'] = self.verbose_title_suc
        return context


class TaquillasUpdateView(TaquillasView, UpdateView):
    form_class = UpdateTaquillaForm
