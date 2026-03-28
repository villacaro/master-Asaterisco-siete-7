# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_apuestas.models import Tickets
from admin_juego.models import Modalidades_Grupos
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_views import MyViewBase
from admin_reportes.forms import (
    FilterDeportesForm, FilterFechasTimeForm, FilterModalidadesForm, FilterTicketsStatusForm,
    FilterTicketsTiposAndStatusForm,
)
from admin_soporte.forms import BuscarTicketForm
from admin_status.models import Status
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.urlresolvers import reverse
from django.db.models import Q, Sum
from django.utils.timezone import now
from django.views.generic import TemplateView


class ListadoTickets(MyViewBase, TemplateView):
    template_name = 'admin_soporte/tickets/gestion/listadodetickets.html'

    def get_context_data(self, **kwargs):
        context = super(ListadoTickets, self).get_context_data(**kwargs)

        context['form_cadena'] = FilterCadenaComercializacionForm(
            **self.get_form_kwargs()
        )
        context['form_deportes'] = FilterDeportesForm()
        context['form_modalidad'] = FilterModalidadesForm()
        context['form_fecha'] = FilterFechasTimeForm()
        context['form_tipos'] = FilterTicketsTiposAndStatusForm()
        context['form_status'] = FilterTicketsStatusForm()
        context['form_ticket_byid'] = BuscarTicketForm()

        return context


class FilterListadoTickets(object):

    def __init__(self, request, object_comercializadora, object_user):
        super(FilterListadoTickets, self).__init__()
        self.request = request
        self.object_comercializadora = object_comercializadora
        self.object_user = object_user

    def set_filter(self, qs):

        if self.request.GET.get('fecha_inicio'):
            fecha_ini = self.request.GET.get('fecha_inicio')
            fecha_fin = self.request.GET.get('fecha_fin')
        else:
            hoy = strFecha(now())
            fecha_ini = hoy.getFecha() + hora_cero
            fecha_fin = hoy.getFecha() + hora_23

        if self.request.GET.get('code_ticket'):
            qs = qs.filter(pk=self.request.GET.get('code_ticket'))
        else:
            qs = qs.filter(fecha__range=(fecha_ini, fecha_fin))

        # Filtros por juegos
        kwargs = {}
        prefix = 'ticketsdetail__jugada__encuentros_modalidad__encuentro'
        if self.request.GET.get('encuentro'):
            kwargs[prefix + '_id'] = self.request.GET.get('encuentro')
        elif self.request.GET.get('temporada'):
            kwargs[
                prefix +
                '__jornada__temporadas_id'] = self.request.GET.get('temporada')
        elif self.request.GET.get('deporte'):
            kwargs[
                prefix + '__jornada__temporadas__torneo__deporte_id'
            ] = self.request.GET.get('deporte')

        # filtros de modalidades condiciones etc
        prefix = 'ticketsdetail__jugada'
        if self.request.GET.get('condicion'):
            kwargs[prefix + '_id'] = self.request.GET.get('condicion')
        elif self.request.GET.get('modalidad'):
            if self.request.GET.get('grupo_modalidad'):
                grupo_modalidad = Modalidades_Grupos.objects.get(
                    modalidad_id=self.request.GET.get('modalidad'),
                    grupo_id=self.request.GET.get('grupo_modalidad')
                )
                kwargs[prefix + '__encuentros_modalidad__modalidad_grupo'] = grupo_modalidad

                if self.request.GET.get('encuentro'):
                    kwargs[prefix + '__encuentros_modalidad__encuentro_id'] = self.request.GET.get('encuentro')
            else:
                kwargs[prefix + '_condicion__modalidad_id'] = self.request.GET.get('modalidad')

        elif self.request.GET.get('grupo_modalidad'):
            kwargs[prefix + '__encuentros_modalidad__modalidad_grupo'] = self.request.GET.get('grupo_modalidad')

            if self.request.GET.get('encuentro'):
                kwargs[prefix + '__encuentros_modalidad__modalidad_grupo__grupo_id'] = self.request.GET.get(
                    'encuentro'
                )

        # Filtros por cadena de comercializacion
        prefix = 'user__taquilla__agencia'
        if self.request.GET.get('agencia'):
            kwargs[prefix + '_id'] = self.request.GET.get('agencia')

        elif self.request.GET.get('distribuidor'):
            kwargs[
                prefix +
                '__distribuidores_id'] = self.request.GET.get('distribuidor')

        elif self.request.GET.get('banca'):
            kwargs[
                prefix +
                '__distribuidores__banca_id'] = self.request.GET.get('banca')

        elif self.request.GET.get('bloque'):

            kwargs[
                prefix +
                '__distribuidores__banca__bloque_id'] = self.request.GET.get('bloque')
        elif self.request.GET.get('operadora'):
            kwargs[
                prefix + '__distribuidores__banca__bloque__operadora_id'
            ] = self.request.GET.get('operadora')
        else:
            if self.object_user.profile.codename == 'userprofile_master':
                pass
            else:
                object_comer = self.object_comercializadora.get_object()
                kwargs[
                    prefix + object_comer.get_prefix_kwargs_by_level_agencia()
                ] = object_comer.pk

        # Filtros individuales
        prefix = 'user__taquilla__agencia'
        if self.request.GET.get('tipos_ticket'):
            kwargs['ticket_type_id'] = self.request.GET.get('tipos_ticket')

        if self.request.GET.get('status_ticket'):
            kwargs['status_id'] = self.request.GET.get('status_ticket')

        if self.request.GET.get('status_ticket_content'):
            kwargs['ticketstatus__status_id'] = self.request.GET.get(
                'status_ticket_content')

        if kwargs:
            qs = qs.filter(
                **kwargs
            )

        return qs.order_by('pk').distinct()


class ListadoTicketsAjax(BaseDatatableView):
    model = Tickets
    order_columns = [
        'pk',
        'user__taquilla__agencia__distribuidores__banca__nombre',
        'user__taquilla__agencia__nombre',
        'fecha',
        'pk',
        'ticketsdetail__ticket',
        'monto',
        'monto_ganancia',
        'monto_premio',
        'status'
    ]

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            status = ''
            if item.get_status().codename == 'status_procesandoganador':
                status = 'tag-green'
            elif item.get_status().codename == 'status_pagado':
                status = 'tag-blue'
            elif item.get_status().codename == 'status_ticketpendiente':
                status = 'tag-orange'
            elif item.get_status().codename == 'status_procesandose':
                status = 'tag-yellow'
            else:
                status = 'tag-red'

            taquilla = item.user.get_taquilla()
            agencia = taquilla.get_origen()
            distribuidor = agencia.get_origen()
            banca = distribuidor.get_origen()

            clonados = item.get_clonados_exists()
            icon = ''
            if clonados:
                icon = '<i class="icon-new"></i>'

            json_data.append([
                (x + 1 + acarreo),
                banca.nombre,
                '{0} ({1})'.format(agencia, taquilla),
                '{0}'.format(item.fecha.strftime('%I:%M %p - %d %b')),
                '<a class="link" href="{0}" title="{3}">{1}{2}</a>'.format(
                    reverse(
                        'admin_soporte_DetalleTicket_url',
                        kwargs={'pk': item.pk}
                    ),
                    icon,
                    item.pk,
                    clonados
                ),
                item.ticketsdetail_set.count(),
                intcomma(item.monto),
                intcomma(item.monto_ganancia),
                intcomma(item.get_monto_premio()),
                '<span class="tag2 {0}">{1}</span>'.format(
                    status, item.get_status())
            ])
        return json_data

    def prepare_footeresults(self, qs):

        json_data = []
        ticket = qs
        qs_ganador = ticket.filter(
            status__codename='status_procesandoganador'
        )

        qs_pagado = ticket.filter(
            status__codename='status_pagado'
        )

        qs_frio = ticket.filter(
            status__codename='status_ganado_frio'
        )

        data = Status.objects.filter(
            content_type=8
        ).exclude(
            codename__in=['status_anulado', 'status_anulado_automatico']
        )

        data_choices = []
        for obj in data:
            data_choices.append(obj.pk)

        qs_venta = ticket.filter(
            status__pk__in=data_choices
        )

        total_tickets = qs.exclude(
            status__codename__in=[
                'status_anulado',
                'status_anulado_automatico']
        ).count()

        qs_premio = qs_ganador | qs_pagado | qs_frio

        if not (self.request.GET.get('status_ticket_content') or self.request.GET.get(
                'encuentro') or self.request.GET.get('temporada') or self.request.GET.get('deporte')):
            total_venta = qs_venta.aggregate(Sum('monto'))['monto__sum']
            if not total_venta:
                total_venta = Decimal(0)

            total_premio_ref = qs_venta.aggregate(Sum('monto_premio'))[
                'monto_premio__sum']
            if not total_premio_ref:
                total_premio_ref = Decimal(0)

            total_premio = qs_premio.aggregate(Sum('monto_premio'))[
                'monto_premio__sum']
            if not total_premio:
                total_premio = Decimal(0)
        else:
            total_venta = Decimal(0)
            total_premio_ref = Decimal(0)
            for venta in qs_venta:
                total_venta += venta.monto
                total_premio_ref += venta.monto_premio

            total_premio = Decimal(0)
            for premio in qs_premio:
                total_premio += premio.monto_premio

        if total_tickets:
            total_media = total_venta / total_tickets
        else:
            total_media = 0

        json_data.append(
            [
                intcomma(total_venta),
                intcomma(total_premio),
                intcomma(total_premio_ref),
                round(total_media, 2),
                qs.count()
            ]
        )
        return json_data

    def filter_queryset(self, qs):

        qs_params = None
        search = self.request.GET.get('sSearch', None)
        if search:
            q = Q(pk=search)
            qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)

        filters = FilterListadoTickets(
            self.request,
            self.object_comercializadora,
            self.object_user
        )

        qs = filters.set_filter(qs)

        qs = qs.select_related(
            'user',
            'status',
        )

        return qs
