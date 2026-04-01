# -*- coding: utf-8 -*-
from admin_juego.forms import JugadorTipoForm
from admin_juego.models import JugadorTipo
from admin_lib.util_forms import FilterDeporteForm
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class JugadorTipoView(MyViewBase):
    model = JugadorTipo
    form_class = JugadorTipoForm

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return "?deporte={0}".format(self.object.deporte.pk)


class JugadorTipoCreateView(JugadorTipoView, CreateView):
    pass


class JugadorTipoDeleteView(JugadorTipoView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class JugadorTipoDetailView(JugadorTipoView, DetailView):
    pass


class JugadorTipoListView(JugadorTipoView, ListView):
    filter_form = None
    form_class = FilterDeporteForm

    def get_queryset(self):
        if self.get_filter_form().is_valid():
            deporte = self.get_filter_form().cleaned_data.get("deporte")
            torneos = JugadorTipo.objects.filter(deporte=deporte)
        else:
            torneos = JugadorTipo.objects.none()
        return torneos


class JugadorTipoUpdateView(JugadorTipoView, UpdateView):
    pass


class JugadorTipoListbyDeporteAjax(View):

    def dispatch(self, request, *args, **kwargs):

        jugadores_tipo = JugadorTipo.objects.filter(
            deporte_id=request.REQUEST.get('deporte')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    jugadores_tipo.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )
