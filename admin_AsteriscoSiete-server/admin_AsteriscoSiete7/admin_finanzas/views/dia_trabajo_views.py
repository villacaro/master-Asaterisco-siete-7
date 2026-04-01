# -*- coding: utf-8 -*-

from admin_finanzas.forms import DiaTrabajoForm
from admin_finanzas.models import Dia, DiaTrabajo
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


class DiaTrabajoView(MyViewBase, FormView):
    template_name = 'admin_finanzas/diatrabajo/dia_trabajo_form.html'
    form_class = DiaTrabajoForm

    def form_valid(self, form):

        dia = Dia.objects.get_or_create(
            fecha=form.cleaned_data.get('fecha')
        )[0]

        dia_trabajo_new = DiaTrabajo.objects.get_or_create(
            dia=dia,
            comercializadora=self.object_comercializadora
        )[0]

        dia_trabajo_old = self.object_comercializadora.get_dia_trabajo()

        if dia_trabajo_old:
            dia_trabajo_old.actual = False
            dia_trabajo_old.procesado = False
            dia_trabajo_old.save(update_fields=['actual', 'procesado'])

        querryset = self.object_comercializadora.diatrabajo_set.filter(actual=True)
        if querryset.exists():
            # por si algun dia quedo hechando vaina
            querryset.update(actual=False)

        dia_trabajo_new.actual = True
        dia_trabajo_new.procesado = False
        dia_trabajo_new.save(update_fields=['actual', 'procesado'])

        messages.info(self.request, 'Dia de trabajo cambiado con exíto')
        self.object_comercializadora.cache_clear()

        return HttpResponseRedirect(reverse('admin_finanzas_resumenadministrativo_general'))


class CerrarDiaTrabajoView(MyViewBase, TemplateView):

    template_name = 'admin_finanzas/diatrabajo/dia_trabajo_form.html'
    cerrar_dia_error = False

    def get_context_data(self, **kwargs):
        context = super(CerrarDiaTrabajoView, self).get_context_data(**kwargs)

        # este atributo indica en la plantilla que es cierre de dia
        context['object'] = True

        context['cerrar_dia_error'] = self.cerrar_dia_error

        return context

    def post(self, request, *args, **kwargs):
        process = self.object_comercializadora.process_close_day()
        if process:
            messages.success(
                self.request, 'Dia de trabajo cerrado con éxito'
            )
            return HttpResponseRedirect(
                reverse('admin_finanzas_resumenadministrativo_general')
            )
        else:
            self.cerrar_dia_error = True
            return self.get(request, *args, **kwargs)
