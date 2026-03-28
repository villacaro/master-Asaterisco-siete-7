# -*- coding: utf-8 -*-
from admin_finanzas.forms import ComercializadoraSaldoInicialForm, ComercializadoraSaldoInicialRegisterForm
from admin_finanzas.models import Comercializadora
from admin_lib.util_views import MyViewBase
from django.core.urlresolvers import reverse
from django.views.generic import ListView, UpdateView
from django.views.generic.edit import FormView


class ComercializadoraView(MyViewBase):
    model = Comercializadora
    form_class = ComercializadoraSaldoInicialForm

    def get_template_names(self):
        tpl = super(ComercializadoraView, self).get_template_names()[0]
        self.template_name = tpl.replace('comercializadora', 'saldoinicial')
        return [self.template_name]

    def get_queryset(self):
        if self.object_comercializadora:
            queryset = self.object_comercializadora.get_offspring_level1() | \
                Comercializadora.objects.filter(
                    resumen_personalizado_comer_id=self.object_comercializadora.pk
            )

            return queryset.order_by(
                'operadora__nombre',
                'bloque__nombre',
                'banca__nombre',
                'distribuidor__nombre',
                'agencia__nombre',
            )
        else:
            return Comercializadora.objects.none()


class ComercializadoraListView(ComercializadoraView, ListView):
    pass


class ComercializadoraResetView(ComercializadoraView, UpdateView):

    def get(self, request, *args, **kwargs):
        from django.contrib import messages
        from django.http import HttpResponseRedirect
        _object = self.get_object()
        _object.reiniciar()
        messages.info(
            request,
            '¡El saldo inicial de la Comercializadora {0} a sido reiniciado con éxito!'.format(
                _object
            )
        )
        return HttpResponseRedirect(reverse('admin_finanzas_saldoinicial_list'))


class ComercializadoraUpdateView(ComercializadoraView, UpdateView):
    proceso = 'process_comercializadora_saldo_inicial_update'

    def form_valid(self, form):
        dia_trabajo = self.object_comercializadora.get_dia_trabajo()

        try:
            error = False
            if self.object.saldo_fecha != dia_trabajo.dia.fecha:
                form._errors['saldo_fecha'] = 'Solo es posible editar un saldo inicial ' \
                                              'con la misma fecha de trabajo actual'
                error = True
            elif self.object.saldo_fecha < dia_trabajo.dia.fecha:
                form._errors['saldo_fecha'] = 'Solo se puede colocar un saldo inicial con'  \
                                              'fecha mayor o igual al dia de trabajo actual'
                error = True
        except Exception:
            error = True
            form._errors['saldo_fecha'] = 'Primero debe configurar su fecha de trabajo'

        if error:
            return super(ComercializadoraUpdateView, self).form_invalid(form)
        else:
            return super(ComercializadoraUpdateView, self).form_valid(form)

    def get_success_url_force(self):
        return reverse(
            'admin_finanzas_saldoinicial_list'
        )


class ComercializadoraRegisterView(ComercializadoraView, FormView):
    form_class = ComercializadoraSaldoInicialRegisterForm
    template_name = 'admin_finanzas/saldoinicial/saldoinicial_form.html'

    def form_valid(self, form):
        self.object = form.cleaned_data.get('comercializadora')
        self.object.saldo_inicial = form.cleaned_data.get('saldo_inicial')
        self.object.saldo_fecha = form.cleaned_data.get('saldo_fecha')
        self.object.resumen_personalizado = True
        self.object.resumen_personalizado_comer = self.object_comercializadora

        self.object.save(update_fields=[
            'saldo_inicial',
            'saldo_fecha',
            'resumen_personalizado',
            'resumen_personalizado_comer',
            'updated_at',
        ]
        )

        self.object.set_saldo_inicial()
        return super(ComercializadoraRegisterView, self).form_valid(form)

    def get_success_url_force(self):
        return reverse(
            'admin_finanzas_saldoinicial_list'
        )
