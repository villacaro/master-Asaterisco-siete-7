# -*- coding: utf-8 -*-
from admin_finanzas.forms import CuentaForm
from admin_finanzas.models import Cuenta
from admin_lib.util_views import MyViewBase
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class CuentaView(MyViewBase):
    model = Cuenta
    form_class = CuentaForm
    search_dia_trabajo = True

    def get_queryset(self):
        return Cuenta.objects.filter(
            comercializadora=self.object_comercializadora
        )


class CuentaCreateView(CuentaView, CreateView):
    pass


class CuentaDeleteView(CuentaView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class CuentaDetailView(CuentaView, DetailView):
    pass


class CuentaListView(CuentaView, ListView):
    pass


class CuentaUpdateView(CuentaView, UpdateView):
    pass
