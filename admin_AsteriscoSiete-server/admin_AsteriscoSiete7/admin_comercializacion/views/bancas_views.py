# -*- coding: utf-8 -*-
from admin_comercializacion.forms import BancaForm
from admin_comercializacion.models import Bancas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase, MyViewBaseDeleteView, MyViewBaseDetailView
from django.urls import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View


class BancasView(MyViewBase):
    model = Bancas
    form_class = BancaForm

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return self.model.objects.filter(
            bloque__operadora=self.object_comercializadora.get_object()
        )

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return self.model.objects.filter(
            bloque=self.object_comercializadora.get_object()
        )

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return self.model.objects.filter(
            id=self.object_comercializadora.get_object().pk
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
            return '?bloque={0}&banca={1}'.format(self.object.bloque_id, self.object.pk)
        else:
            return '?banca={0}'.format(self.object.pk)


class BancasCreateView(BancasView, CreateView):

    def get_success_url_filter_form(self):
        if self.object.get_using_porcentajes():
            return '?ccadena={0}'.format(self.object.get_comercializadora().pk)
        else:
            app = self.object.__module__.split('.')[0]
            model = self.object.__class__.__name__.lower()
            return '?ccadena={0}&next={1}'.format(
                self.object.get_comercializadora().pk,
                reverse('{0}_{1}_list'.format(app, model)),
            )
            return super(BancasCreateView, self).get_success_url_filter_form()

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        if self.object.get_using_porcentajes():
            return reverse(
                'admin_comercializacion_porcentajes_update',
                kwargs={
                    'type': self.object.get_class_name(),
                    'pk': self.object.pk,
                }
            )
        else:
            return reverse(
                'admin_users_users_create'
            )

        return None


class BancasDeleteView(BancasView, MyViewBaseDeleteView):
    pass


class BancasDetailView(BancasView, MyViewBaseDetailView):
    pass


class BancasListView(BancasView, ListView):

    filter_form = None
    form_class = FilterCadenaComercializacionForm

    def get_queryset(self):
        bancas = super(BancasListView, self).get_queryset()
        if self.get_filter_form().is_valid():

            bloque = self.get_filter_form().cleaned_data.get('bloque')
            banca = self.get_filter_form().cleaned_data.get('banca')

            if self.request.REQUEST:
                if banca:
                    bancas = bancas.filter(pk=banca.pk)
                elif bloque:
                    bancas = bancas.filter(bloque=bloque)
            else:
                bancas = Bancas.objects.none()

        else:
            bancas = Bancas.objects.none()

        bancas = bancas.select_related('bloque', 'status')
        return bancas


class BancasUpdateView(BancasView, UpdateView):
    pass


class BancasListbyBloqueAjax(View):

    def dispatch(self, request, *args, **kwargs):
        bancas = Bancas.objects.filter(
            bloque_id=request.REQUEST.get('bloque')
        )

        if request.REQUEST.get('resultados'):
            bancas = bancas.filter(
                Q(is_resultados=True) | Q(is_sistema_juego=True)
            )

        return HttpResponse(
            content=JsonDumps(
                list(
                    bancas.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )


class BancasDatatableView(BancasListView, BaseDatatableView):
    # Modelo de la lista
    model = Bancas
    # Orden del filtro
    order_columns = ['nombre']
    # Fields de busqueda
    filter_search = 'nombre'

    opcions_url = [
        'admin_comercializacion_' + model.prefix_filter_plural + '_detail$' + Icons.detail,
        'admin_comercializacion_' + model.prefix_filter_plural + '_update$' + Icons.update,
        'admin_comercializacion_' + model.prefix_filter_plural + '_delete$' + Icons.delete,
    ]

    def get_initial_queryset(self):
        qs = self.get_queryset().values('pk', 'nombre', 'bloque__nombre', 'status__name')
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            json_data.append([
                (x + 1 + acarreo),
                item.get('nombre'),
                item.get('bloque__nombre'),
                item.get('status__name'),
                self.get_opcions(item.get('pk'))
            ])
        return json_data
