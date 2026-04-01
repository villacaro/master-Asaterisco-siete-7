# -*- coding: utf-8 -*-
from admin_asterisco7.settings import MEDIA_URL
from admin_juego.forms import TorneosForm
from admin_juego.models import TipoProducto
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterTorneoForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class TorneosView(MyViewBase):
    model = TipoProducto
    form_class = TorneosForm

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return "?deporte={0}&torneo={1}".format(
            self.object.deporte.pk,
            self.object.pk
        )


class TorneosCreateView(TorneosView, CreateView):
    pass


class TorneosDeleteView(TorneosView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class TorneosDetailView(TorneosView, DetailView):
    pass


class TorneosListView(TorneosView, ListView):
    filter_form = None
    form_class = FilterTorneoForm

    def get_next_url_filter_form(self):
        parameters = "?deporte={0}&torneo={1}".format(
            self.request.GET.get("deporte"),
            self.request.GET.get("torneo"),
        )
        return "?next=" + reverse("admin_juego_torneos_list") + parameters

    def get_queryset(self):
        if self.get_filter_form().is_valid():

            torneos = TipoProducto.objects.select_related('deporte').all()

            deporte = self.get_filter_form().cleaned_data.get('deporte')
            torneo = self.get_filter_form().cleaned_data.get('torneo')

            if torneo:
                torneos = torneos.filter(pk=torneo.pk)
            elif deporte:
                torneos = torneos.filter(deporte=deporte)

        else:
            torneos = TipoProducto.objects.none()
        return torneos


class TorneosUpdateView(TorneosView, UpdateView):
    pass


class TorneosListbyDeporteAjax(View):

    def dispatch(self, request, *args, **kwargs):
        deporte = request.REQUEST.get("deporte")
        if deporte != '':
            torneos = TipoProducto.objects.filter(
                deporte_id=request.REQUEST.get("deporte")
            )
        else:
            torneos = TipoProducto.objects.all()

        if request.REQUEST.get("por_jornadas", False):
            torneos = torneos.filter(
                por_jornadas=request.REQUEST.get("por_jornadas")
            )

        if request.REQUEST.get("por_grupos", False):
            torneos = torneos.filter(
                por_grupos=request.REQUEST.get("por_grupos"),
            )

        return HttpResponse(
            content=JsonDumps(
                list(
                    torneos.values(
                        "pk",
                        "nombre",
                        "logo"
                    )
                )
            ),
            content_type='application/json'
        )


class TorneoGetAjax(View):

    def dispatch(self, request, *args, **kwargs):

        torneos = TipoProducto.objects.filter(
            pk=request.REQUEST.get('pk')
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    torneos.values(
                        "por_jornadas",
                        "por_grupos"
                    )
                )
            ),
            content_type='application/json'
        )


class TorneosDatatableView(TorneosListView, BaseDatatableView):
    model = TipoProducto
    order_columns = ['nombre']
    # Fields de busqueda
    filter_search = "nombre"
    opcions_url = []

    def get_initial_queryset(self):
        self.opcions_url = [
            "admin_juego_" + self.model.prefix_filter_plural + "_detail$" + Icons.detail,
            "admin_juego_" + self.model.prefix_filter_plural + "_update$" + Icons.update +
            "$" + self.get_next_url_filter_form(),
            "admin_juego_" + self.model.prefix_filter_plural + "_delete$" + Icons.delete,
        ]
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            json_data.append([
                (x + 1 + acarreo),
                "<a class='link' href={0}>{1}</a>".format(
                    item.get_absolute_url(),
                    item.nombre
                ),
                "<img src='{0}' width='35' height='auto'>".format(
                    MEDIA_URL + str(item.logo)
                ) if item.logo else "Sin imagen",
                "<img src='{0}'  height='30px'>".format(
                    MEDIA_URL + str(item.fondoweb)
                ) if item.fondoweb else "Sin fondo",
                "<span class='tag tag-green'>{0}</span>".format(
                    item.deporte.nombre
                ),
                self.get_opcions(item.pk)
            ])
        return json_data
