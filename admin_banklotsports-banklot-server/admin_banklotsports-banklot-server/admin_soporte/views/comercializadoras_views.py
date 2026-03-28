# -*- coding: utf-8 -*-

from admin_lib.util_views import MyViewBase
from admin_soporte.forms import ComercializadorasForm
from admin_status.models import Status
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import FormView


class OptionsRestore(MyViewBase, FormView):
    form_class = ComercializadorasForm
    template_name = 'admin_soporte/comercializacion/opciones/restaurar.html'

    def form_valid(self, form):
        """
        Al ser valido el formulario, se procese a ejecutar la rutina para restaurar la
        junto con sus dependencias.
        """

        comercializadora = form.cleaned_data.get('comercializadora').get_object()
        status = Status.get_status_by_codename('status_activo_sin_venta')

        def restore(comercializadora):
            if comercializadora.prefix_filter == 'taquilla':
                comercializadora.taquilla = comercializadora.taquilla.split('_delete_')[0]
                try:
                    comercializadora.save(update_fields=['taquilla', 'updated_at'])
                except IntegrityError:
                    comercializadora.taquilla = comercializadora.taquilla + ' restaurad@'
                    comercializadora.save(update_fields=['taquilla', 'updated_at'])
                comercializadora.set_new_status('status_instalacion')
            else:
                comercializadora.nombre = comercializadora.nombre.split('_delete_')[0]
                comercializadora.status = status
                try:
                    comercializadora.save(update_fields=['nombre', 'status', 'updated_at'])
                except IntegrityError:
                    comercializadora.nombre = comercializadora.nombre + ' restaurad@'
                    comercializadora.save(update_fields=['nombre', 'status', 'updated_at'])

        restore(comercializadora)
        origen = comercializadora.get_origen()
        while origen:
            if origen.status.codename != 'status_eliminado':
                break

            restore(origen)
            origen = origen.get_origen()
            if not origen:
                break

        messages.success(self.request, 'Comercializadora restaurad@ con éxito')
        return HttpResponseRedirect(reverse('admin_soporte_comercializacion_opciones_restaurar'))
