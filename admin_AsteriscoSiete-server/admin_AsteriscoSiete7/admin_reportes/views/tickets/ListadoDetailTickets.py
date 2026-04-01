# -*- coding: utf-8 -*-

from admin_apuestas.models import Tickets
from admin_lib.util_views import MyViewBase
from django.views.generic import DetailView


class VentasDetalleTickets(MyViewBase, DetailView):
    model = Tickets
    template_name = "admin_reportes/tickets/tickets_detail.html"

    def get_queryset(self):
        """
        Define el queryset inicial
        """
        if self.object_user.profile.codename == "userprofile_master":
            return Tickets.objects.all()
        else:
            kwargs = {}
            object_comer = self.object_comercializadora.get_object()
            kwargs[
                "user__taquilla__agencia" + object_comer.get_prefix_kwargs_by_level_agencia()
            ] = object_comer.pk

            return Tickets.objects.filter(**kwargs)
