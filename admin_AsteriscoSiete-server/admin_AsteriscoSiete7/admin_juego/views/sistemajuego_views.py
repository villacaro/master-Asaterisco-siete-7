# -*- coding: utf-8 -*-
from admin_juego.forms import SistemaJuegoForm
from admin_juego.models import SistemaJuego
from admin_lib.util_views import MyViewBase
from django.views.generic import DetailView, ListView, UpdateView


class SistemaJuegoView(MyViewBase):
    model = SistemaJuego
    form_class = SistemaJuegoForm

    def get_queryset(self):
        """
        Queryset inicial validando el sistema de juego
        """

        sistemajuego = SistemaJuego.objects.all()

        if not self.object_user.profile.codename == "userprofile_master":
            if self.object_sistema_juego:
                sistemajuego = sistemajuego.filter(
                    pk=self.object_sistema_juego.pk
                )
            else:
                sistemajuego = sistemajuego.none()

        return sistemajuego


class SistemaJuegoDetailView(SistemaJuegoView, DetailView):
    pass


class SistemaJuegoListView(SistemaJuegoView, ListView):

    def get_queryset(self):
        queryset = super(SistemaJuegoListView, self).get_queryset()
        return queryset.only('pk', 'nombre', 'logo', 'notificacion_automatica')


class SistemaJuegoUpdateView(SistemaJuegoView, UpdateView):
    pass
