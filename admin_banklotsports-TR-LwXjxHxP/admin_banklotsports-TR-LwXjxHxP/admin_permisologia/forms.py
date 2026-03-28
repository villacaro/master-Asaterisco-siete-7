# -*- coding: utf-8 -*-

from admin_lib.util_forms import WidgetCustomizeForms
from admin_permisologia.models import Groups
from django import forms


class GroupsForm(WidgetCustomizeForms, forms.ModelForm):
    """
    Formulario para gestionar grupos de usuarios
    """

    class Meta:
        model = Groups
        fields = '__all__'

        widgets = {
            'permissions': forms.widgets.CheckboxSelectMultiple()
        }

    def __init__(self, *args, **kwargs):
        super(GroupsForm, self).__init__(*args, **kwargs)
        self.fields["permissions"].queryset = self.view.object_user.get_query_set_permissions(
            comercializadora=self.view.object_comercializadora
        )
