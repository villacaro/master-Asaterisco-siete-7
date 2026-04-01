# -*- coding: utf-8 -*-
from admin_juego.forms import GruposJuegoForm
from admin_juego.models import ModalidadJuego, ModalidadGrupo, ModalidadPeriodo, GruposApuesta
from admin_lib.util_forms import FilterDeporteForm
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class GruposJuegoView(MyViewBase):
    model = GruposApuesta
    form_class = GruposJuegoForm

    def get_success_url_filter_form(self):
        return "?deporte={0}".format(
            self.object.temporada.torneo.deporte.pk
        )


class GruposJuegoCreateView(GruposJuegoView, CreateView):

    def form_valid(self, form):
        form.instance.save()
        for equipo in self.request.POST.getlist("equipo_grupo"):
            ModalidadGrupo.objects.create(
                grupo=form.instance,
                equipo=ModalidadJuego.objects.get(
                    pk=equipo
                )
            )
        return super(GruposJuegoCreateView, self).form_valid(form)


class GruposJuegoDeleteView(GruposJuegoView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class GruposJuegoDetailView(GruposJuegoView, DetailView):
    pass


class GruposJuegoListView(GruposJuegoView, ListView):
    filter_form = None
    form_class = FilterDeporteForm

    def get_queryset(self):
        if self.get_filter_form().is_valid():
            deporte = self.get_filter_form().cleaned_data.get("deporte")
            gruposjuego = GruposApuesta.objects.filter(
                temporada__torneo__deporte=deporte,
            )
        else:
            gruposjuego = GruposApuesta.objects.none()
        return gruposjuego


class GruposJuegoUpdateView(GruposJuegoView, UpdateView):

    def get_context_data(self, **kwargs):
        context = super(GruposJuegoUpdateView, self).get_context_data(**kwargs)
        grupo = self.object

        equipos = ModalidadPeriodo.objects.filter(
            temporada=grupo.temporada
        )

        equipos_array = []
        for equipo in equipos:
            equipos_array_interno = {}
            equipos_array_interno["pk"] = equipo.equipo.pk
            equipos_array_interno["nombre"] = equipo.equipo.nombre
            equipos_array_interno["logo"] = equipo.equipo.logo
            if grupo.equiposgrupos_set.filter(equipo=equipo.equipo).exists():
                equipos_array_interno["check"] = "checked"
            else:
                equipos_array_interno["check"] = ""

            equipos_array.append(equipos_array_interno)

        context["equipos"] = equipos_array
        return context

    def form_valid(self, form):
        form.instance.save()
        equipos_grupo_new = []
        for equipo in self.request.POST.getlist("equipo_grupo"):
            equipos_grupo = ModalidadGrupo.objects.get_or_create(
                grupo=form.instance,
                equipo=ModalidadJuego.objects.get(pk=equipo)
            )[0]
            equipos_grupo_new.append(equipos_grupo.pk)

        for equipo_grupo_old in ModalidadGrupo.objects.filter(
            grupo=form.instance
        ).exclude(
            pk__in=equipos_grupo_new
        ):
            equipo_grupo_old.delete()

        return super(GruposJuegoUpdateView, self).form_valid(form)


class GruposJuegoListbyTemporadaAjax(View):

    def dispatch(self, request, *args, **kwargs):

        temporada = request.REQUEST.get('temporada')

        grupos = GruposApuesta.objects.filter(
            temporada_id=temporada
        )

        return HttpResponse(
            content=JsonDumps(
                list(
                    grupos.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )
