# -*- coding: utf-8 -*-
from admin_comercializacion.forms import OperadoraForm
from admin_comercializacion.models import Operadoras
from admin_lib.util_views import MyViewBase
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class OperadorasView(MyViewBase):
    model = Operadoras
    form_class = OperadoraForm


class OperadorasCreateView(OperadorasView, CreateView):
    pass


class OperadorasDeleteView(OperadorasView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class OperadorasDetailView(OperadorasView, DetailView):
    pass


class OperadorasListView(OperadorasView, ListView):
    pass


class OperadorasUpdateView(OperadorasView, UpdateView):
    pass
