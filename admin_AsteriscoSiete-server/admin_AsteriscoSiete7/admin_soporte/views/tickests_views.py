# -*- coding: utf-8 -*-

from admin_apuestas.models import Tickets, TicketsDetail
from admin_apuestas.task import (
    AsyncProcesarTickets_Soporte_Manual_anular, AsyncProcesarTickets_Soporte_Manual_desanular,
)
from admin_datamart.task import AsyncGestion_rest_MontoPremio
from admin_finanzas.task import AsyncProcesarTicket
from admin_lib.util_views import MyViewBase
from admin_soporte.forms import BuscarTicketForm
from admin_status.models import Status
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import DetailView
from django.views.generic.edit import FormView


class BuscarTicket(MyViewBase, FormView):
    template_name = 'admin_soporte/tickets/gestion/buscar.html'
    form_class = BuscarTicketForm

    def form_valid(self, form):
        """
        Al ser valido el formulario, se envia al detalle del ticket
        en cuestion
        """

        return HttpResponseRedirect(
            reverse(
                'admin_soporte_DetalleTicket_url',
                kwargs={'pk': form.cleaned_data.get('code_ticket')}
            )
        )


class DetalleTicket(MyViewBase, DetailView):
    model = Tickets
    template_name = 'admin_soporte/tickets/gestion/detalle.html'

    def filter_userprofile_master(self, **kwargs):
        """
        Puesto que es el master accede a todo, devuelve el mismo queryset
        """
        return kwargs['tickets']

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return kwargs['tickets'].filter(
            user__taquilla__agencia__distribuidores__banca__bloque__operadora=self.object_comercializadora.get_object()
        )

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return kwargs['tickets'].filter(
            user__taquilla__agencia__distribuidores__banca__bloque=self.object_comercializadora.get_object()
        )

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """
        return kwargs['tickets'].filter(
            user__taquilla__agencia__distribuidores__banca=self.object_comercializadora.get_object()
        )

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        return kwargs['tickets'].filter(
            user__taquilla__agencia__distribuidores=self.object_comercializadora.get_object()
        )

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una agencia
        """
        return kwargs['tickets'].filter(
            user__taquilla__agencia=self.object_comercializadora.get_object()
        )

    def get_queryset(self):
        """
        Es este get_queryset se hace el respectivo filtro
        para verificar que el ticket pertenesca a la cadena que lo solicita
        """
        tickets = super(DetalleTicket, self).get_queryset()

        return self.set_execute_function_by_profile(
            **{
                'tickets': tickets,
                'prefix': 'filter',
                'instance': self
            }
        )

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(DetalleTicket, self).get_context_data(**kwargs)
        context['master'] = self.get_profile().codename == 'userprofile_master'
        if context['master']:
            context['status_filter'] = Status.objects.filter(
                codename__in=[
                    'status_procesandoganador',
                    'status_procesadoperdedor',
                    'status_anulado'
                ]
            )
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if request.POST.get('accion') == 'anular':
            invalid = False
            if self.get_profile().codename != 'userprofile_master':
                invalid = self.object.ticketsdetail_set.filter(
                    jugada__encuentros_modalidad__encuentro__horacierre__lt=now()
                ).exists()

            if invalid is False:
                if self.object.get_status().codename in [
                        'status_anulado', 'status_anulado_automatico']:
                    tarea = AsyncProcesarTickets_Soporte_Manual_desanular()
                else:
                    tarea = AsyncProcesarTickets_Soporte_Manual_anular()

                resp = tarea.run(*(), **{'ticket': self.object.pk, })

                for sms in resp:
                    messages.info(request, sms)
            else:
                messages.error(
                    request,
                    'Una vez comenzado algún encuentro relacionado con el '
                    'ticket no puede gestionarse de forma manual.'
                )
        elif request.POST.get('accion') == 'procesar' and self.get_profile().codename == 'userprofile_master':
            new_status = request.POST.get('ticket_status_new')
            if new_status:
                new_status = Status.objects.get(pk=new_status)
                if self.object.status.codename == 'status_ganado_frio':
                    if new_status.codename == 'status_anulado':
                        tarea = AsyncProcesarTickets_Soporte_Manual_anular()
                        resp = tarea.run(*(), **{'ticket': self.object.pk, })
                        for sms in resp:
                            messages.info(request, sms)
                    else:
                        if new_status.codename == 'status_procesandoganador':
                            pass
                        elif new_status.codename == 'status_procesadoperdedor':
                            tarea = AsyncGestion_rest_MontoPremio()
                            tarea.delay(*(), **{'ticket': self.object.pk, })
                        messages.info(
                            request,
                            'Ticket procesado, status old => {}, new status => {}'.format(
                                self.object.status, new_status
                            )
                        )
                        self.object.set_new_status(new_status)
                else:
                    messages.error(
                        request,
                        'Solo puede cambiarse un ticket en estatus frío.'
                    )
            else:
                recalculo = False
                for data in request.POST.getlist('status_new'):
                    if data:
                        data = data.split('-')
                        jugada = TicketsDetail.objects.get(pk=data[0])

                        # Si antes era anulado se recalcula
                        if jugada.status.codename == 'status_anulado':
                            recalculo = True

                        jugada.set_new_status(Status.objects.get(pk=data[1]))

                        # Si despues fue anulado se recalcula
                        if jugada.status.codename == 'status_anulado':
                            recalculo = True

                tarea = AsyncProcesarTicket()
                message = tarea.run(
                    *(),
                    **{
                        'ticket': self.object.pk,
                        'recalculo': recalculo
                    }
                )
                messages.info(
                    request,
                    'Ticket procesado, resultado => {0}'.format(message)
                )
        # Consultamos el ticket nuevamente, para obtener el status
        # terminal
        self.object = Tickets.objects.get(pk=self.object.pk)
        return self.get(request, *args, **kwargs)
