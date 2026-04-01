# -*- coding: utf-8 -*-
from admin_banklotsports.settings import MEDIA_URL
from admin_juego.forms import JugadorForm
from admin_juego.models import Equipos, Jugador, JugadorTipo
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterDeporteJugadoresForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class JugadorView(MyViewBase):
    model = Jugador
    form_class = JugadorForm

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return "?deporte={0}&tipo={1}&jugador={2}".format(
            self.object.tipo.deporte.pk,
            self.object.tipo.pk,
            self.object.pk,
        )


class JugadorCreateView(JugadorView, CreateView):

    def form_valid(self, form):
        equipos = self.request.POST.getlist("equipo")
        form.instance.save()
        if len(equipos) > 0:
            for i, equipo in enumerate(equipos):
                form.instance.equipos.add(
                    Equipos.objects.get(pk=equipo)
                )

        if self.request.POST["_save"] == "_addanother":

            messages.success(
                self.request,
                "¡Enhorabuena! {0} {1} "
                "ha sido guardado con éxito!".format(
                    self.model().__class__.__name__.lower(),
                    form.instance
                )
            )

            equipos_queryset = Equipos.objects.filter(
                deporte=form.instance.tipo.deporte
            ).order_by('nombre')
            equipos_array = []
            for equipo in equipos_queryset:
                equipo_array = {}
                equipo_array["pk"] = equipo.pk
                equipo_array["nombre"] = equipo.nombre
                equipo_array["logo"] = equipo.logo
                if str(equipo.pk) in equipos:
                    equipo_array["check"] = "checked"
                equipos_array.append(equipo_array)

            form.data["nombre"] = ""
            form.data["lateralidad"] = ""
            return self.render_to_response(self.get_context_data(form=form, equipos=equipos_array))
        else:
            return super(JugadorCreateView, self).form_valid(form)


class JugadorDeleteView(JugadorView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class JugadorDetailView(JugadorView, DetailView):
    pass


class JugadorListView(JugadorView, ListView):
    filter_form = None
    form_class = FilterDeporteJugadoresForm

    def get_next_url_filter_form(self):
        parameters = "?deporte={0}&tipo={1}&equipo={2}&jugador={3}".format(
            self.request.GET.get("deporte"),
            self.request.GET.get("tipo"),
            self.request.GET.get("equipo"),
            self.request.GET.get("jugador"),
        )
        return "?next=" + reverse("admin_juego_jugador_list") + parameters

    def get_queryset(self):
        deporte = self.request.GET.get("deporte")
        tipo = self.request.GET.get("tipo")
        equipo = self.request.GET.get("equipo")
        jugador = self.request.GET.get("jugador")

        if jugador and jugador != "0" and jugador != "None":
            jugadores = Jugador.objects.filter(pk=jugador)
        elif equipo and equipo != "0" and equipo != "None":
            jugadores = Jugador.objects.filter(equipos=equipo)
        elif tipo and tipo != "0" and tipo != "None":
            jugadores = Jugador.objects.filter(tipo=tipo)
            if equipo == "0":
                jugadores = Jugador.objects.filter(equipos__isnull=True)
        elif deporte and deporte != "0" and deporte != "None":
            jugadores = Jugador.objects.filter(tipo__deporte=deporte)
        else:
            jugadores = Jugador.objects.none()
        return jugadores


class JugadorUpdateView(JugadorView, UpdateView):

    def form_valid(self, form):
        # String
        equipos = self.request.POST.getlist("equipo")
        form.instance.save()

        # Enteros
        equipos_old = list(form.instance.equipos.all().values_list("pk", flat=True))

        for equipo in equipos:
            if int(equipo) not in equipos_old:
                form.instance.equipos.add(
                    Equipos.objects.get(pk=equipo)
                )
        for equipo in equipos_old:
            if str(equipo) not in equipos:
                form.instance.equipos.remove(
                    Equipos.objects.get(pk=equipo)
                )

        return super(JugadorUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(JugadorUpdateView, self).get_context_data(**kwargs)

        equipos = Equipos.objects.filter(
            deporte=self.object.tipo.deporte
        ).order_by("nombre")
        equipos_array = []
        for equipo in equipos:
            equipo_array = {}
            equipo_array["pk"] = equipo.pk
            equipo_array["nombre"] = equipo.nombre
            equipo_array["logo"] = equipo.logo
            if self.object.equipos.filter(
                pk=equipo.pk
            ).exists():
                equipo_array["check"] = "checked"
            equipos_array.append(equipo_array)
        context["equipos"] = equipos_array
        return context


class JugadorListbyTipoAjax(View):

    def dispatch(self, request, *args, **kwargs):

        jugadores = Jugador.objects.filter(
            tipo_id=request.GET.get('tipo')
        )

        return HttpResponse(
            content=JsonDumps(
                [
                    {"pk": q.pk, "nombre": q.get_label()}
                    for q in jugadores
                ]
            ),
            content_type='application/json'
        )


class JugadorListbyEquipoAjax(View):

    def dispatch(self, request, *args, **kwargs):

        jugadores = Jugador.objects.filter(
            equipos=request.GET.get('equipo')
        )

        return HttpResponse(
            content=JsonDumps(
                [
                    {"pk": q.pk, "nombre": q.get_label()}
                    for q in jugadores
                ]
            ),
            content_type='application/json'
        )


class JugadorListbyEquipoAndTipoAjax(View):

    def dispatch(self, request, *args, **kwargs):

        if (request.GET.get('equipo') != '0' and request.GET.get('equipo') != '' and
                request.GET.get('tipo') != '0' and request.GET.get('tipo') != ''):
            jugadores = Jugador.objects.filter(
                tipo_id=request.GET.get('tipo'),
                equipos=request.GET.get('equipo')
            )
        elif request.GET.get('tipo') != '0' and request.GET.get('tipo') != '':
            jugadores = Jugador.objects.filter(
                tipo_id=request.GET.get('tipo'),
                equipos__isnull=True
            )
        else:
            jugadores = Jugador.objects.none()

        return HttpResponse(
            content=JsonDumps(
                [
                    {"pk": q.pk, "nombre": q.get_label()}
                    for q in jugadores
                ]
            ),
            content_type='application/json'
        )


class TipoListbyDeporteAjax(View):

    def dispatch(self, request, *args, **kwargs):

        tipos = JugadorTipo.objects.filter(
            deporte_id=request.GET.get('deporte')
        )

        return HttpResponse(
            content=JsonDumps(
                [
                    {"pk": q.pk, "nombre": q.nombre}
                    for q in tipos
                ]
            ),
            content_type='application/json'
        )


class JugadoresDatatableView(JugadorListView, BaseDatatableView):
    model = Jugador
    order_columns = ['nombre']
    # Fields de busqueda
    filter_search = "nombre"

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
            equipos = ""
            for equipo in item.get_equipos_all():
                equipos += "<span class='tag tag-green'>{0}</span>".format(
                    equipo
                )

            foto_text = "Si imagen"
            if item.foto:
                foto_text = '<img src="{0}{1}" width="50" height="50">'.format(
                    MEDIA_URL, item.foto
                )

            json_data.append([
                (x + 1 + acarreo),
                "<a class='link' href='{0}'>({1}) {2}</a>".format(
                    item.get_absolute_url(),
                    item.lateralidad,
                    item.nombre
                ),
                foto_text,
                "<span class='tag tag-green'>{0}</span>".format(
                    item.tipo.nombre
                ),
                "<span class='tag tag-green'>{0}</span>".format(
                    item.tipo.deporte.nombre
                ),
                equipos,
                self.get_opcions(item.pk),
            ])
        return json_data
