# -*- coding: utf-8 -*-
from admin_juego.forms import DeportesForm
from admin_juego.models import Deportes
from admin_lib.util_views import MyViewBase
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class DeportesView(MyViewBase):
    model = Deportes
    form_class = DeportesForm


class DeportesCreateView(DeportesView, CreateView):
    pass


class DeportesDeleteView(DeportesView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class DeportesDetailView(DeportesView, DetailView):
    pass


class DeportesListView(DeportesView, ListView):
    pass


class DeportesUpdateView(DeportesView, UpdateView):
    pass
