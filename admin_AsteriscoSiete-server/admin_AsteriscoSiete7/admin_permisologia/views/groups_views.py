# -*- coding: utf-8 -*-
from admin_lib.util_views import MyViewBase
from admin_permisologia.forms import GroupsForm
from admin_permisologia.models import Groups
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView


class GroupsView(MyViewBase):
    model = Groups
    form_class = GroupsForm

    def get_queryset(self):
        """
        Se prefiltran los grupos a los cuales tiene acceso el usuario
        """
        return self.object_user.get_query_set_groups(
            self.object_comercializadora
        )


class GroupsCreateView(GroupsView, CreateView):
    pass


class GroupsDeleteView(GroupsView, DeleteView):
    relate_delete = True


class GroupsDetailView(GroupsView, DetailView):
    pass


class GroupsListView(GroupsView, ListView):
    pass


class GroupsUpdateView(GroupsView, UpdateView):
    pass
