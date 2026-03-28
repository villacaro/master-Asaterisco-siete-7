# -*- coding: utf-8 -*-
from admin_comercializacion.forms import DistribuidorForm
from admin_comercializacion.models import Distribuidores
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase, MyViewBaseDeleteView, MyViewBaseDetailView
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View


class DistribuidoresView(MyViewBase):
    model = Distribuidores
    form_class = DistribuidorForm

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return Distribuidores.objects.filter(
            banca__bloque__operadora=self.object_comercializadora.get_object()
        )

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return Distribuidores.objects.filter(
            banca__bloque=self.object_comercializadora.get_object()
        )

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return Distribuidores.objects.filter(
            pk=self.object_comercializadora.get_object().pk
        )

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return Distribuidores.objects.filter(
            banca=self.object_comercializadora.get_object()
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
            return '?bloque={0}&banca={1}&distribuidor={2}'.format(
                self.object.banca.bloque_id,
                self.object.banca_id,
                self.object.pk
            )
        elif self.get_profile().codename == 'userprofile_bloque':
            return '?banca={0}&distribuidor={1}'.format(
                self.object.banca_id,
                self.object.pk
            )
        else:
            return '?distribuidor={0}'.format(self.object.pk)


class DistribuidoresCreateView(DistribuidoresView, CreateView):

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
            return super(DistribuidoresCreateView, self).get_success_url_filter_form()

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

        return None


class DistribuidoresDeleteView(DistribuidoresView, MyViewBaseDeleteView):
    pass


class DistribuidoresDetailView(DistribuidoresView, MyViewBaseDetailView):
    pass


class DistribuidoresListView(DistribuidoresView, ListView):
    filter_form = None
    form_class = FilterCadenaComercializacionForm

    def get_queryset(self):
        distribuidores = super(DistribuidoresListView, self).get_queryset()
        if self.get_filter_form().is_valid():

            bloque = self.get_filter_form().cleaned_data.get('bloque')
            banca = self.get_filter_form().cleaned_data.get('banca')
            distribuidor = self.get_filter_form().cleaned_data.get('distribuidor')

            if self.request.REQUEST:
                if distribuidor:
                    distribuidores = distribuidores.filter(pk=distribuidor.pk)
                elif banca:
                    distribuidores = distribuidores.filter(banca=banca)
                elif bloque:
                    distribuidores = distribuidores.filter(banca__bloque=bloque)
            else:
                distribuidores = Distribuidores.objects.none()

        else:
            distribuidores = Distribuidores.objects.none()

        distribuidores = distribuidores.select_related('banca', 'status')
        return distribuidores


class DistribuidoresUpdateView(DistribuidoresView, UpdateView):
    pass


class DistribuidoresListbyBloqueAjax(View):

    def dispatch(self, request, *args, **kwargs):
        distribuidores = Distribuidores.objects.filter(
            banca__bloque_id=request.REQUEST.get('bloque')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    distribuidores.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )


class DistribuidoresListbyBancaAjax(View):

    def dispatch(self, request, *args, **kwargs):
        distribuidores = Distribuidores.objects.filter(
            banca_id=request.REQUEST.get('banca')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    distribuidores.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )


class DistribuidoresDatatableView(DistribuidoresListView, BaseDatatableView):
    # Modelo de la lista
    model = Distribuidores
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
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            json_data.append([
                (x + 1 + acarreo),
                item.nombre,
                item.banca.nombre,
                item.status.name,
                self.get_opcions(item.pk)
            ])
        return json_data
