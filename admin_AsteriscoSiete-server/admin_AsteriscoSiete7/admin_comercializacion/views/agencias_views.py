# -*- coding: utf-8 -*-
from admin_comercializacion.forms import AgenciaForm
from admin_comercializacion.models import Agencias, Bancas, Operadoras
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase, MyViewBaseDeleteView, MyViewBaseDetailView
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View


class AgenciasView(MyViewBase):
    model = Agencias
    form_class = AgenciaForm

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return Agencias.objects.filter(
            distribuidores__banca__bloque__operadora=self.object_comercializadora.get_object()
        )

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return Agencias.objects.filter(
            distribuidores__banca__bloque=self.object_comercializadora.get_object()
        )

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un banca
        """
        return Agencias.objects.filter(
            distribuidores__banca=self.object_comercializadora.get_object()
        )

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        return Agencias.objects.filter(
            distribuidores=self.object_comercializadora.get_object()
        )

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        return Agencias.objects.filter(
            pk=self.object_comercializadora.get_object().pk
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
                self.object.distribuidores.banca.bloque_id,
                self.object.distribuidores.banca_id,
                self.object.distribuidores_id,
                self.object.pk,
            )
        elif self.get_profile().codename == 'userprofile_bloque':
            return '?banca={0}&distribuidor={1}&agencia={2}'.format(
                self.object.distribuidores.banca_id,
                self.object.distribuidores_id,
                self.object.pk,
            )
        elif self.get_profile().codename == 'userprofile_banca':
            return '?distribuidor={0}&agencia={1}'.format(
                self.object.distribuidores_id,
                self.object.pk,
            )
        else:
            return '?agencia={0}'.format(self.object.pk)


class AgenciasCreateView(AgenciasView, CreateView):

    def get_success_url_filter_form(self):
        if not self.object.distribuidores.banca.modelo_negocio ==\
                Bancas.modelo_negocio_codenames["codename_negocio_alquiler"]:
            return "?ccadena={0}".format(self.object.get_comercializadora().pk)
        else:
            app = self.object.__module__.split(".")[0]
            model = self.object.__class__.__name__.lower()
            return "?ccadena={0}&next={1}".format(
                self.object.get_comercializadora().pk,
                reverse("{0}_{1}_list".format(app, model)),
            )
            return super(AgenciasCreateView, self).get_success_url_filter_form()

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        if not self.object.distribuidores.banca.modelo_negocio ==\
                Bancas.modelo_negocio_codenames["codename_negocio_alquiler"]:
            from django.urls import reverse
            return reverse(
                'admin_comercializacion_porcentajes_update',
                kwargs={
                    'type': self.object.get_class_name(),
                    'pk': self.object.pk,
                }
            )

        return None


class AgenciasDeleteView(AgenciasView, MyViewBaseDeleteView):
    pass


class AgenciasDetailView(AgenciasView, MyViewBaseDetailView):
    pass


class AgenciasListView(AgenciasView, ListView):
    filter_form = None
    form_class = FilterCadenaComercializacionForm

    def get_queryset(self):
        agencias = super(AgenciasListView, self).get_queryset()
        if self.get_filter_form().is_valid():

            operadora = self.get_filter_form().cleaned_data.get('operadora')
            bloque = self.get_filter_form().cleaned_data.get('bloque')
            banca = self.get_filter_form().cleaned_data.get('banca')
            distribuidor = self.get_filter_form().cleaned_data.get('distribuidor')
            agencia = self.get_filter_form().cleaned_data.get('agencia')

            if self.request.REQUEST:
                if agencia:
                    agencias = agencias.filter(pk=agencia.pk)
                elif distribuidor:
                    agencias = agencias.filter(distribuidores=distribuidor)
                elif banca:
                    agencias = agencias.filter(distribuidores__banca=banca)
                elif bloque:
                    agencias = agencias.filter(distribuidores__banca__bloque=bloque)
                elif operadora:
                    agencias = agencias.filter(distribuidores__banca__bloque__operadora=operadora)
            else:
                agencias = Agencias.objects.none()

        else:
            agencias = Agencias.objects.none()

        agencias = agencias.select_related('distribuidores', 'status')
        return agencias


class AgenciasUpdateView(AgenciasView, UpdateView):
    pass


class AgenciasListbyBloquesAjax(View):

    def dispatch(self, request, *args, **kwargs):
        agencias = Agencias.objects.filter(
            distribuidores__banca__bloque_id=request.REQUEST.get('bloque')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    agencias.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )


class AgenciasListbyBancasAjax(View):

    def dispatch(self, request, *args, **kwargs):
        agencias = Agencias.objects.filter(
            distribuidores__banca_id=request.REQUEST.get('banca')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    agencias.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )


class AgenciasListbyDistribuidoresAjax(View):

    def dispatch(self, request, *args, **kwargs):
        agencias = Agencias.objects.filter(
            distribuidores_id=request.REQUEST.get('distribuidor')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    agencias.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )


class AgenciasListAjax(View):

    def dispatch(self, request, *args, **kwargs):
        agencias = Agencias.objects.filter(
            pk=request.REQUEST.get('pk')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    agencias.values(
                        'pk',
                        'num_taquillas',
                    )
                )
            ),
            content_type='application/json'
        )


class AgenciasMonitorView(AgenciasListView):

    template_name = 'admin_comercializacion/agencias/monitor_list.html'

    def filter_userprofile_master(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return Operadoras.objects.all()

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return self.object_comercializadora.get_object().bloques_set.all()

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return self.object_comercializadora.get_object().bancas_set.all()

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """
        return self.object_comercializadora.get_object().distribuidores_set.all()

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        return self.object_comercializadora.get_object().agencias_set.all()

    def get_queryset(self):

        queryset = Agencias.objects.none()
        if self.get_filter_form().is_valid():

            operadora = self.get_filter_form().cleaned_data.get('operadora')
            bloque = self.get_filter_form().cleaned_data.get('bloque')
            banca = self.get_filter_form().cleaned_data.get('banca')
            distribuidor = self.get_filter_form().cleaned_data.get('distribuidor')
            agencia = self.get_filter_form().cleaned_data.get('agencia')

            if self.request.REQUEST:
                if agencia:
                    queryset = Agencias.objects.filter(pk=agencia.pk)
                elif distribuidor:
                    queryset = distribuidor.agencias_set.all()
                elif banca:
                    queryset = banca.distribuidores_set.all()
                elif bloque:
                    queryset = bloque.bancas_set.all()
                elif operadora:
                    queryset = operadora.bloques_set.all()
                else:
                    queryset = self.set_execute_function_by_profile(
                        **{
                            'prefix': 'filter',
                            'instance': self
                        }
                    )
        return queryset


class AgenciasDatatableView(AgenciasListView, BaseDatatableView):
    # Modelo de la lista
    model = Agencias
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
            codigo = item.codigo
            if codigo:
                nombre = codigo + '-' + item.nombre
            else:
                nombre = item.nombre
            json_data.append([
                (x + 1 + acarreo),
                nombre,
                item.distribuidores.nombre,
                item.status.name,
                item.taquillas_set.all().count(),
                '<i title=' + str(item.get_ultima_conexion()) + ' class="icon-clock"><i>' +
                naturaltime(item.get_ultima_conexion()),
                self.get_opcions(item.pk)
            ])
        return json_data
