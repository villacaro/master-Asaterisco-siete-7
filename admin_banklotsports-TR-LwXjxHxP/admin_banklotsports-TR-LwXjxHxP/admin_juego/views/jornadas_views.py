# -*- coding: utf-8 -*-
from admin_juego.forms import JornadasForm
from admin_juego.models import Jornadas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterTorneoForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class JornadasView(MyViewBase):
    model = Jornadas
    form_class = JornadasForm

    def get_queryset(self):
        """
        Queryset inicial validando el sistema de juego
        """
        return Jornadas.objects.filter(
            sistema=self.object_sistema_juego
        )

    def get_success_url_filter_form(self):
        return "?deporte={0}".format(
            self.object.temporadas.torneo.deporte.pk
        )


class JornadasCreateView(JornadasView, CreateView):
    pass


class JornadasDeleteView(JornadasView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class JornadasDetailView(JornadasView, DetailView):
    pass


class JornadasListView(JornadasView, ListView):
    filter_form = None
    form_class = FilterTorneoForm

    def get_next_url_filter_form(self):
        parameters = "?deporte={0}&torneo={1}".format(
            self.request.GET.get("deporte"),
            self.request.GET.get("torneo"),
        )
        return "?next=" + reverse("admin_juego_jornadas_list") + parameters

    def get_queryset(self):
        jornadas = super(JornadasListView, self).get_queryset()
        if self.get_filter_form().is_valid():
            deporte = self.get_filter_form().cleaned_data.get("deporte")
            torneo = self.get_filter_form().cleaned_data.get("torneo")
            if torneo is not None and torneo != 0:
                jornadas = jornadas.filter(
                    temporadas__torneo=torneo,
                )
            elif deporte != 0:
                jornadas = jornadas.filter(
                    temporadas__torneo__deporte=deporte,
                )
        else:
            jornadas = Jornadas.objects.none()
        return jornadas


class JornadasUpdateView(JornadasView, UpdateView):
    pass


class JornadasListbyTemporadaAjax(View):

    def dispatch(self, request, *args, **kwargs):

        if "object_session" in kwargs:
            self.object_sistema_juego = kwargs.pop("object_sistema_juego")
        else:
            self.object_sistema_juego = None

        temporada = request.REQUEST.get('temporada')

        jornadas = self.get_jornadas(
            temporada
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    jornadas.values(
                        "pk",
                        "jornada"
                    )
                )
            ),
            content_type='application/json'
        )

    def get_jornadas(self, temporada):
        """
        Devuelve las jornadas dado una temporada
        """
        return Jornadas.objects.filter(
            temporadas_id=temporada,
            sistema=self.object_sistema_juego,
            fechafin__gte=now().date(),
            status__codename="status_habilitado",
        )


class JornadasDatatableView(JornadasListView, BaseDatatableView):
    model = Jornadas
    order_columns = ['jornada']
    # Fields de busqueda
    filter_search = "jornada"
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
            tipo = ""
            if item.parley:
                tipo += "<span class='tag tag-block tag-yellow'>Parley</span>"

            if item.quiniela:
                tipo += "<span class='tag tag-block tag-yellow'>Quiniela</span>"

            if item.apuestasimple:
                tipo += "<span class='tag tag-block tag-yellow'>Apuesta simple</span>"

            json_data.append([
                (x + 1 + acarreo),
                "<a class='link' href={0}>{1}</a>".format(
                    item.get_absolute_url(),
                    item.jornada
                ),
                "<span class='tag tag-block tag-blue'>{0} \
                </span><span class=tag tag-block'>{1}</span>".format(
                    item.temporadas.torneo,
                    item.temporadas
                ),
                "{:%d-%m-%Y}".format(item.fechaini),
                tipo,
                "<span class='tag tag-green'>{0}</span>".format(
                    item.temporadas.torneo.deporte
                ),
                item.status.name,
                self.get_opcions(item.pk)
            ])
        return json_data
