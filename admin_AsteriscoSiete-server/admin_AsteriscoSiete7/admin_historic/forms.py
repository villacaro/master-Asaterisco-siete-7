# -*- coding: utf-8 -*-

from admin_historic.models import MODULES_VERBOSE
from admin_lib.util_forms import WidgetCustomizeForms
from django import forms
from django.utils.timezone import now


class FechasAndModulosForm(WidgetCustomizeForms, forms.Form):

    tipo = forms.ChoiceField(
        choices=MODULES_VERBOSE,
        required=True,
        label='Seleccione un modulo'
    )

    fecha_inicio = forms.CharField(
        max_length=10,
        label="Desde ",
        required=True
    )
    fecha_fin = forms.CharField(
        max_length=10,
        label="Hasta ",
        required=True
    )

    def __init__(self, *args, **kwargs):
        super(FechasAndModulosForm, self).__init__(*args, **kwargs)

        self.fields["fecha_inicio"].initial = now().strftime("%Y-%m-%d")
        self.fields["fecha_fin"].initial = self.fields["fecha_inicio"].initial
