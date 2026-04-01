# -*- coding: utf-8 -*-
from admin_comercializacion.forms import CuposForm
from admin_comercializacion.models import Cupos
from admin_comercializacion.views.agencias_views import AgenciasListView
from admin_comercializacion.views.bancas_views import BancasListView
from admin_comercializacion.views.bloques_views import BloquesListView
from admin_comercializacion.views.distribuidores_views import DistribuidoresListView
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_icons import Icons
from admin_lib.util_views import MyViewBase
from django.contrib.humanize.templatetags.humanize import intcomma, naturaltime
from django.core.urlresolvers import reverse
from django.views.generic import DetailView, UpdateView


class CuposView(MyViewBase):
    model = Cupos
    form_class = CuposForm

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """

        cupos = Cupos.objects.filter(
            bloque__operadora=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            banca__bloque__operadora=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            distribuidor__banca__bloque__operadora=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            agencia__distribuidores__banca__bloque__operadora=self.object_comercializadora.get_object()
        )
        return cupos

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        cupos = Cupos.objects.filter(
            bloque=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            banca__bloque=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            distribuidor__banca__bloque=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            agencia__distribuidores__banca__bloque=self.object_comercializadora.get_object()
        )

        return cupos

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un banca
        """
        cupos = Cupos.objects.filter(
            banca=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            distribuidor__banca=self.object_comercializadora.get_object()
        )

        cupos |= Cupos.objects.filter(
            agencia__distribuidores__banca=self.object_comercializadora.get_object()
        )

        return cupos

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        cupos = Cupos.objects.filter(
            agencia__distribuidores=self.object_comercializadora.get_object()
        )

        return cupos

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        cupos = Cupos.objects.none()
        return cupos

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


class CuposDetailView(CuposView, DetailView):
    pass


class CuposUpdateView(CuposView, UpdateView):

    def get_success_url_force(self):
        return reverse(
            'admin_comercializacion_{0}_cupos_list'.format(
                self.object.get_object().get_class_name()
            )
        )

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return '?{0}={1}'.format(
            self.object.get_object().prefix_filter,
            self.object.get_object().pk
        )

    def get_object(self):
        object = super(CuposUpdateView, self).get_object()
        if not object.fecha_fin:
            return object
        else:
            from django.http import Http404
            raise Http404


class CuposListView(MyViewBase):
    template_name = 'admin_comercializacion/cupos/cupos_list.html'


class BloquesCuposListView(CuposListView, BloquesListView):

    def get_context_data(self, **kwargs):
        context = super(BloquesCuposListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Bloques'
        context['model'] = 'Bloques'
        return context


class BancasCuposListView(CuposListView, BancasListView):

    def get_context_data(self, **kwargs):
        context = super(BancasCuposListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Bancas'
        context['model'] = 'Bancas'
        return context


class DistribuidoresCuposListView(CuposListView, DistribuidoresListView):

    def get_context_data(self, **kwargs):
        context = super(DistribuidoresCuposListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Distribuidores'
        context['model'] = 'Distribuidores'
        return context


class AgenciasCuposListView(CuposListView, AgenciasListView):

    def get_context_data(self, **kwargs):
        context = super(AgenciasCuposListView, self).get_context_data(**kwargs)
        context['cadena'] = 'Centros de apuesta'
        context['model'] = 'Agencias'
        return context


class CuposDatatableView(MyViewBase, BaseDatatableView):
    # Orden del filtro
    order_columns = ['nombre']
    # Patron de busqueda
    filter_search = 'nombre'

    opcions_url = [
        'admin_comercializacion_cupos_detail$' + Icons.detail,
        'admin_comercializacion_cupos_update$' + Icons.update,
    ]

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            cupo = item.get_cupo()
            if cupo.monto_premio:
                monto_premio = str(intcomma(cupo.monto_premio)) + ' Bs.'
            else:
                monto_premio = 'No asignado'

            json_data.append([
                (x + 1 + acarreo),
                item.nombre,
                "<span class='right'>{0} Bs.</span>".format(intcomma(cupo.monto_diario)),
                "<span class='right'>{0}</span>".format(monto_premio),
                "<i title='{0}' class='icon-clock'><i>{1}".format(
                    cupo.fecha_inicio,
                    naturaltime(cupo.fecha_inicio)
                ),
                self.get_opcions(pk=cupo.pk)
            ])
        return json_data


class BloquesCuposDatatableView(CuposDatatableView, BloquesCuposListView):
    pass


class BancasCuposDatatableView(CuposDatatableView, BancasCuposListView):
    pass


class DistribuidoresCuposDatatableView(CuposDatatableView, DistribuidoresCuposListView):
    pass


class AgenciasCuposDatatableView(CuposDatatableView, AgenciasCuposListView):
    pass
