# -*- coding: utf-8 -*-
from admin_juego.forms import TemporadasForm
from admin_juego.models import Temporadas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterTemporadaForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class TemporadasView(MyViewBase):
    model = Temporadas
    form_class = TemporadasForm

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return "?deporte={0}&torneo={1}&temporada={2}".format(
            self.object.torneo.deporte.pk,
            self.object.torneo.pk,
            self.object.pk
        )


class TemporadasCreateView(TemporadasView, CreateView):
    pass


class TemporadasDeleteView(TemporadasView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class TemporadasDetailView(TemporadasView, DetailView):
    pass


class TemporadasListView(TemporadasView, ListView):
    filter_form = None
    form_class = FilterTemporadaForm

    def get_next_url_filter_form(self):
        parameters = "?deporte={0}&torneo={1}&temporada={2}".format(
            self.request.GET.get("deporte"),
            self.request.GET.get("torneo"),
            self.request.GET.get("temporada"),
        )
        return "?next=" + reverse("admin_juego_temporadas_list") + parameters

    def get_queryset(self):
        if self.get_filter_form().is_valid():
            temporadas = Temporadas.objects.all().select_related(
                'torneo__deporte',
                'status'
            )

            deporte = self.get_filter_form().cleaned_data.get("deporte")
            torneo = self.get_filter_form().cleaned_data.get("torneo")
            temporada = self.get_filter_form().cleaned_data.get("temporada")

            if temporada:
                temporadas = temporadas.filter(
                    pk=temporada.pk
                )
            elif torneo:
                temporadas = temporadas.filter(
                    torneo_id=torneo.pk
                )
            elif deporte:
                temporadas = temporadas.filter(
                    torneo__deporte_id=deporte.pk,
                )

            return temporadas.filter(
                fechafin__gte=now().date(),
            )
        else:
            temporadas = Temporadas.objects.none()
            return temporadas


class TemporadasUpdateView(TemporadasView, UpdateView):
    pass


class TemporadasListbyTorneoAjax(View):

    def dispatch(self, request, *args, **kwargs):

        temporadas = Temporadas.objects.filter(
            torneo_id=request.REQUEST['liga'],
            fechafin__gte=now().date(),
            status__codename="status_habilitado",
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    temporadas.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )


class TemporadasListbyDeporteAjax(View):

    def dispatch(self, request, *args, **kwargs):

        temporadas = Temporadas.objects.filter(
            torneo__deporte_id=request.REQUEST['deporte'],
        )

        temp = []
        for temporada in temporadas:
            json = {}
            json["pk"] = temporada.id
            json["nombre"] = "{0} - {1}".format(
                temporada.torneo.nombre,
                temporada.nombre
            )
            temp.append(json)
        return HttpResponse(
            content=JsonDumps(
                temp
            ),
            content_type='application/json'
        )


class TemporadasDatatableView(TemporadasListView, BaseDatatableView):
    model = Temporadas
    order_columns = ['nombre']
    # Fields de busqueda
    filter_search = 'nombre'

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
            mes = item.fechaini.strftime("%B")
            json_data.append([
                (x + 1 + acarreo),
                "<span class='tag tag-blue'>{0}</span><span class='tag'>\
                <a class='link' href='{1}'>{2}</a></span>".format(
                    item.torneo,
                    item.get_absolute_url(),
                    item.nombre
                ),
                '{0.day} de {1} de {0.year}'.format(item.fechaini, mes),
                "<span class='tag tag-green'>{0}</span>".format(
                    item.torneo.deporte.nombre
                ),
                item.status.name,
                self.get_opcions(item.pk)
            ])
        return json_data
