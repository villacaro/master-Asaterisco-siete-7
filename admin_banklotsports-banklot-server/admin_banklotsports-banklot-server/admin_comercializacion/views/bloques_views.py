# -*- coding: utf-8 -*-
from admin_comercializacion.forms import BloqueForm
from admin_comercializacion.models import Bloques
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase, MyViewBaseDeleteView, MyViewBaseDetailView
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView, View


class BloquesView(MyViewBase):
    model = Bloques
    form_class = BloqueForm

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return self.model.objects.filter(
            operadora_id=self.object_comercializadora.get_object().pk
        )

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return self.model.objects.filter(
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
        ).order_by('nombre')


class BloquesCreateView(BloquesView, CreateView):

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        return reverse(
            'admin_comercializacion_porcentajes_update',
            kwargs={
                'type': self.object.get_class_name(),
                'pk': self.object.pk,
            }
        )

    def get_success_url_filter_form(self):
        return '?ccadena={0}'.format(self.object.get_comercializadora().pk)


class BloquesDeleteView(BloquesView, MyViewBaseDeleteView):
    pass


class BloquesDetailView(BloquesView, MyViewBaseDetailView):
    pass


class BloquesListView(BloquesView, ListView):

    def get_queryset(self):
        bloques = super(BloquesListView, self).get_queryset()
        bloques = bloques.select_related('operadora', 'status')
        return bloques


class BloquesUpdateView(BloquesView, UpdateView):
    pass


class BloquesListbyOperadoraAjax(View):

    def dispatch(self, request, *args, **kwargs):
        bloques = Bloques.objects.filter(
            operadora_id=request.REQUEST.get('operadora')
        )

        if request.REQUEST.get('resultados'):
            bloques = bloques.filter(
                Q(is_resultados=True) | Q(is_sistema_juego=True)
            )

        return HttpResponse(
            content=JsonDumps(
                list(
                    bloques.values(
                        'pk',
                        'nombre',
                    )
                )
            ),
            content_type='application/json'
        )
