# -*- coding: utf-8 -*-
from decimal import Decimal

from admin_finanzas.forms import MovimientoFilterForm, MovimientoForm
from admin_finanzas.models import Comercializadora, EstatoCuenta, Movimiento
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView


class MovimientoView(MyViewBase):
    model = Movimiento
    form_class = MovimientoForm

    def get_queryset(self):
        movimientos = Movimiento.objects.filter(
            cuenta__comercializadora=self.object_comercializadora,
        )

        if hasattr(self, "tipo"):
            movimientos = movimientos.filter(
                tipo__codename__in=self.tipo,
            )
        return movimientos.order_by("-created_at")

    def get_context_data(self, **kwargs):
        context = super(MovimientoView, self).get_context_data(**kwargs)

        if hasattr(self, "verbose_movimiento"):
            context["verbose_movimiento"] = self.verbose_movimiento
            context["beneficiario"] = self.beneficiario
        context["objects_list"] = self.get_queryset()

        if "comercializadora" in self.kwargs:
            comercializadora = Comercializadora.objects.get(
                pk=self.kwargs.get("comercializadora")
            )
            context["form"].fields["comercializadora"].initial = comercializadora

        return context

    def dispatch(self, request, *args, **kwargs):
        """
        Inicializa los objetos de la clase, apenas se invoca la vista
        """
        if not kwargs["object_comercializadora"].get_dia_trabajo():
            messages.warning(request, "Primero debe definir una fecha de trabajo")
            return HttpResponseRedirect(reverse("admin_finanzas_diatrabajo_update"))
        else:
            return super(MovimientoView, self).dispatch(request, *args, **kwargs)


class CreateViewMovimiento(MovimientoView, CreateView):

    def get_success_url_force(self):
        return reverse(
            self.object.get_url_tipo()
        )


class MovimientosDetailView(MovimientoView, DetailView):
    pass


class MovimientoDepositoView(CreateViewMovimiento):
    tipo = ("tipo_deposito", "")
    beneficiario = ("A favor del cliente", "")
    verbose_movimiento = "Deposito"


class MovimientoPagoView(CreateViewMovimiento):
    tipo = ("tipo_pago", "")
    beneficiario = ("A favor nuestro", "")
    verbose_movimiento = "Pago"


class MovimientoAjusteView(CreateViewMovimiento):
    tipo = ("tipo_ajuste_cobrar", "tipo_ajuste_pagar")
    beneficiario = ("A favor nuestro", "A favor del cliente")
    verbose_movimiento = "Ajuste"


class MovimientoDeleteView(MovimientoView, DeleteView):
    model = Movimiento

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object_comercializadora.get_dia_trabajo().dia.pk == self.object.dia.pk:
            return super(MovimientoDeleteView, self).post(self, request, *args, **kwargs)
        else:
            messages.warning(
                self.request,
                "¡Error! El " + str(self.object.tipo) + " no se puede eliminar, "
                "ya que la fecha de registro no coincide con la fecha de trabajo actual!"
            )
            return super(MovimientoDeleteView, self).get(self, request, *args, **kwargs)

    def get_success_url_force(self):
        return reverse(
            self.object.get_url_tipo()
        )


class MovimientosListView(MovimientoView, ListView):
    filter_form = None
    form_class = MovimientoFilterForm

    def get_filter_form(self):
        """
        Retorna el formulario de la instancia,
        de ya estar inicializado devuelve el que esta en memoria
        """
        if self.filter_form is None:
            self.filter_form = self.form_class(
                self.request.REQUEST,
                **self.get_form_kwargs()
            )

        return self.filter_form

    def get_queryset(self):
        """
        Es este get_queryset se hace el respectivo filtro de usuarios
        dependiendo de los parametros recibidos y la comercializadora
        iniciada.
        """
        movimientos = Movimiento.objects.filter(
            cuenta__comercializadora=self.object_comercializadora
        )

        self.saldo_anterior = 0
        if self.get_filter_form().is_valid():
            self.cuenta = self.get_filter_form().cleaned_data.get("filter_cuenta")
            self.fecha = self.get_filter_form().cleaned_data.get("filter_fecha").split("-")

            if self.cuenta:
                try:
                    self.saldo_anterior = EstatoCuenta.objects.get(
                        cuenta=self.cuenta,
                        dia__fecha__year=self.fecha[0],
                        dia__fecha__month=self.fecha[1]
                    ).saldo
                except EstatoCuenta.DoesNotExist:
                    pass

                movimientos = movimientos.filter(
                    cuenta=self.cuenta,
                    dia__fecha__year=self.fecha[0],
                    dia__fecha__month=self.fecha[1]
                )
            else:
                movimientos = movimientos.filter(
                    dia__fecha__year=self.fecha[0],
                    dia__fecha__month=self.fecha[1]
                )
        else:
            movimientos = movimientos.none()

        return movimientos

    def get_context_data(self, **kwargs):
        context = super(MovimientosListView, self).get_context_data(**kwargs)

        context["totales"] = self.procesar_data(context["objects_list"])

        return context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def procesar_data(self, movimientos):
        totales = {}
        totales["saldo_anterior"] = self.saldo_anterior
        copia_saldo_anterior = totales["saldo_anterior"]
        totales["total"] = Decimal()

        for movimiento in movimientos:
            totales["total"] += movimiento.monto

            copia_saldo_anterior += movimiento.monto
            movimiento.saldo_calculado = copia_saldo_anterior

        totales["saldo_actual"] = copia_saldo_anterior
        return totales
