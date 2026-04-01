# -*- coding: utf-8 -*-
from decimal import Decimal

from admin_banklotsports.settings import CACHES_CONF_TIME
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from django.core.cache import cache
from django.db import models
from django.utils.timezone import now


class TicketsType(models.Model):
    """TicketsType: Tipos de tickets

    Campos definidos:
        nombre(string): nombre del tipo de ticket

        codename(string): codigo del tipo de ticket, ejemplo: type_parley

        descripcion(string): descripcion formal del tipo de ticket

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=100
    )
    codename = models.CharField(
        max_length=160,
        unique=True,
        db_index=True,
    )
    descripcion = models.CharField(
        max_length=200
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Tipo de apuesta para un ticket')
        verbose_name_plural = ('Tipos de apuestas para los tickes')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}'.format(self.nombre)

    def save(self, *args, **kwargs):
        super(TicketsType, self).save(*args, **kwargs)
        cache.delete('type_bet_{0}'.format(self.codename))

    @staticmethod
    def get_type_bet_by_codename(codename):
        type_bet = cache.get('type_bet_{0}'.format(codename))
        if not type_bet:
            type_bet = TicketsType.objects.get(
                codename=codename
            )
            cache.set(
                'type_bet_{0}'.format(codename),
                type_bet,
                CACHES_CONF_TIME['registros_db']['type_bet']
            )
        return type_bet


class Tickets(models.Model):
    """Tickets: Tickets

    Campos definidos:

        key(string): llave usada al momento de cobrar los tickets,
            este solo se pagara si dicha llave coincide

        user(foreign): usuario de taquilla relacionado, el cual genera el ticket

        ticket_type(foreign): tipo de ticket

        monto(decimal): monto apostado en el ticket

        monto_premio(decimal): monto de posible premio

        monto_ganancia(decimal): monto de ganancia del tickets, en caso de que sea ganador

        puntaje_calculado(entero): puntaje acumulado por el ticket, solo para quiniela

        created_at y updated_at: registros de creacion y actualizacion.
    """
    key = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'admin_comercializacion.UsuariosTaquilla'
    )
    ticket_type = models.ForeignKey(
        'TicketsType'
    )
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    monto_premio = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    monto_ganancia = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )
    fecha = models.DateTimeField(
        db_index=True,
    )
    puntaje_calculado = models.IntegerField(
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        'admin_status.Status',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pks_jugadas = models.CharField(
        max_length=300,
        default='',
        db_index=True,
    )

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Ticket')
        verbose_name_plural = ('Tickets')

    def __str__(self):
        """
        Devuelve el string que lo representa
        """
        return '{0}'.format(self.pk)

    @staticmethod
    def get_ticket_low(pk):
        # Esta cache no se invalida, simplemente expira
        ticket_low = cache.get('ticket_low_{0}'.format(pk))
        if not ticket_low:
            ticket_low = Tickets.objects.select_related('user').only(
                'user__taquilla',
                'fecha',
                'monto',
            ).get(pk=pk)
            cache.set(
                'ticket_low_{0}'.format(pk),
                ticket_low,
                CACHES_CONF_TIME['registros_db']['tickets']
            )
        return ticket_low

    def get_calcular_premio(self, recalculo=False):

        items = self.ticketsdetail_set.all()

        if self.ticket_type.codename == 'type_parley':
            ganancia_new = 1
            for item in items:
                if item.get_status().codename not in [
                        'status_anulado', 'status_anulado_automatico']:
                    ganancia_new = ganancia_new * float(
                        self.convert_americano_europeo(
                            item.logro_apostado
                        )
                    )

            if ganancia_new != 1:
                ganancia_new = round(
                    float(ganancia_new) * float(self.monto),
                    2
                )
            else:
                ganancia_new = self.monto

            self.monto_premio = ganancia_new
            if not recalculo:
                self.monto_ganancia = self.monto_premio

            # self.set_factor_riesgo()
            self.save(update_fields=['monto_premio', 'monto_ganancia'])

        else:
            """
            Auditar los demas tipos tickets
            """
            pass
        return self.monto_premio

    def convert_americano_europeo(self, logro):
        if logro < 0:
            return float(float(-(100 - float(logro))) / float(logro))
        elif logro > 0:
            return float(float((100 + float(logro))) / 100)
        else:
            return logro

    def set_factor_riesgo(self, save=True):
        """
        Aqui se aplican todas las rutinas para aplicar el factor de riesgo
        """
        agencia = self.user.taquilla.agencia
        if agencia.factor_riesgo:

            comercializadora = agencia.get_comercializadora()

            for regla in comercializadora.factorriesgo.factores:
                # 0 es el rango inicial
                # 1 es el rango final
                # 2 es el porcentaje a aplicar
                if self.monto >= regla[0] and self.monto <= regla[1]:
                    porcentaje_riesgo = float(regla[2] / 100)
                    self.monto_premio = round(
                        float(self.monto_premio) -
                        (float(self.monto_premio) * porcentaje_riesgo),
                        0
                    )

                    self.monto_ganancia = round(
                        float(self.monto_ganancia) -
                        (float(self.monto_ganancia) * porcentaje_riesgo),
                        0
                    )

                    self.save(update_fields=['monto_premio', 'monto_ganancia'])
                    break

    @models.permalink
    def get_absolute_url(self):
        return ('admin_reportes_tickets_detail', (), {'pk': self.pk})

    @models.permalink
    def get_absolute_url_soporte(self):
        return ('admin_soporte_DetalleTicket_url', (), {'pk': self.pk})

    def get_pk(self):
        """
        Devuelve el pk en forma de string
        """
        return '{0}'.format(self.pk)

    def set_new_status(self, status, initial=False):
        """
        Crea un nuevo status para el item del ticket en cuestion,
        y procese a cerrar los status anteriores
        """
        if not self.status_id:
            self.status = status
            self.save(update_fields=['status', 'updated_at'])
        else:
            if self.status.pk != status.pk:
                self.status = status
                self.save(update_fields=['status', 'updated_at'])

        if not initial:
            self.ticketstatus_set.all().filter(
                enddate=None
            ).update(
                enddate=now()
            )

        TicketStatus.objects.create(
            ticket=self,
            startdate=now(),
            status=status
        )

    def get_new_status(self):
        """
        Devuelve el status del item del ticket,
        verificando posibles errores, en caso de que no tenga,
        o tenga varios devuelve un estatus que corresponda
        """
        if self.status is None:
            status_filter = self.ticketstatus_set.all().filter(enddate=None)
            count_status = status_filter.count()
            if count_status == 0:
                old_status_exist = self.ticketstatus_set.all().order_by('-startdate')
                if old_status_exist.exists():
                    # entra cuando por algun motivo no hay ningun status activo,
                    # se pone el ultimo como activo nuevamente
                    ultimo_status = old_status_exist[0]
                    ultimo_status.enddate = None
                    ultimo_status.save()
                else:
                    # si por algun motivo el ticket no tiene status, se crea
                    from admin_status.models import Status
                    ultimo_status = TicketStatus.objects.create(
                        ticket=self,
                        startdate=now(),
                        status=Status.get_status_by_codename(
                            codename='status_ticketpendiente'
                        ),
                    )
            elif count_status == 1:
                ultimo_status = status_filter[0]
            elif count_status >= 2:
                # puede pasar que queden 2 status activos,
                # cierra los viejos y devuelve el mas nuevo
                status_filter = status_filter.order_by('-startdate')
                for obj in status_filter[1:]:
                    obj.enddate = now()
                    obj.save(update_fields=['enddate'])
                ultimo_status = status_filter[0]

            self.status = ultimo_status.status
            self.updated_at = ultimo_status.startdate
            self.save(update_fields=['status', 'updated_at'])
        return self

    def get_status(self):
        """
        Devuelve el status acual del item del ticke
        """
        return self.get_new_status().status

    def get_status_all(self):
        """
        Devuelve todos los status asociados al item del ticket
        """
        return self.ticketstatus_set.all().order_by('startdate')

    def get_status_change(self):
        """
        Devuelve un string particular para saber que tipo de gestion se le aplica al ticket
        """
        if self.get_status().codename in [
                'status_anulado', 'status_anulado_automatico']:
            return 'Desanular'
        else:
            return 'Anular'

    def get_status_update(self):
        """
        Devuelve la fecha de inicio del ultimo status asociado
        """
        return self.get_new_status().updated_at

    def get_monto_premio(self):
        """
        Dependiendo del status del ticket devuelve el monto del premio,
        de no ser ganador devuelve 0
        """
        codename = self.get_status().codename
        if (codename == 'status_procesandoganador' or
                codename == 'status_pagado' or
                codename == 'status_ganado_frio'):
            return self.monto_premio
        else:
            return Decimal(str('0.00'))

    def get_clonados(self):
        if self.pks_jugadas:
            fecha = strFecha(self.fecha)
            return Tickets.objects.filter(
                user__taquilla__agencia_id=self.user.taquilla.agencia_id,
                fecha__range=(
                    fecha.getFecha() + hora_cero,
                    fecha.getFecha() + hora_23,
                ),
                pks_jugadas=self.pks_jugadas,
            ).exclude(pk=self.pk)
        else:
            return Tickets.objects.none()

    def get_clonados_exists(self):
        """
        Devuelve un icono en cado de existir tickets clonados
        """
        count = self.get_clonados().count()

        if count:
            clonados = '{0} ticket(s) clonado(s)'.format(count)
        else:
            clonados = ''

        return clonados

    def get_clonados_exists_and_ref(self):
        """
        Devuelve los pks de todos los tickets clonados, es decir con las mismas jugadas
        """
        return self.get_clonados()

    def get_verbose_column_type(self):
        if self.ticket_type.codename == 'type_quiniela':
            return 'Puntajes'
        else:
            return 'Logros'


class TicketsDetail(models.Model):
    """TicketsDetail: Detalle de los tickets

    Campos definidos:
        jugada(foreign): jugada a la cual pertenece el item

        ticket(foreign): ticket al cual pertenece dicho item

        monto(decimal): monto de apuesta por item

        logro_apostado(entero): logro americano al cual se aposto
            al momento de registrar el ticket

        modalidad_ref(string): referencia de la modalidad a la cual
            se aposto al momento de registrar el ticket

        condicion_ref(string): referencia de la condicion a la cual
            se aposto al momento de registrar el ticket

        puntaje_calculado(entero): puntaje calculado en base a su estatus

        puntaje_apostado(entero): goles o puntaje q hace referencia a la apuesta

        created_at y updated_at: registros de creacion y actualizacion.
    """
    jugada = models.ForeignKey(
        'admin_juego.Jugadas'
    )
    ticket = models.ForeignKey(
        'Tickets'
    )
    monto = models.DecimalField(
        max_digits=30,
        decimal_places=16,
    )
    logro_apostado = models.IntegerField(
        null=True,
        blank=True
    )
    puntaje_calculado = models.IntegerField(
        null=True,
        blank=True
    )
    puntaje_apostado = models.IntegerField(
        null=True,
        blank=True
    )
    modalidad_ref = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    condicion_ref = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        'admin_status.Status',
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    def __str__(self):
        """
        Retorna el string que lo representa
        """
        return '{0}'.format(self.pk)

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Detalle de ticket')
        verbose_name_plural = ('Detalle de tickets')
        ordering = ['created_at', ]

    def get_pk(self):
        """
        Devuelve el pk del objeto en string
        """
        return '{0}'.format(self.pk)

    def set_new_status(self, status, initial=False):
        """
        Crea un nuevo status para el item del ticket en cuestion,
        y procese a cerrar los status anteriores
        """
        if not self.status_id:
            self.status = status
            self.save(update_fields=['status', 'updated_at'])
        else:
            if self.status.pk != status.pk:
                self.status = status
                self.save(update_fields=['status', 'updated_at'])

        if not initial:
            self.ticketsdetailstatus_set.all().filter(
                enddate=None
            ).update(
                enddate=now()
            )
        TicketsDetailStatus.objects.create(
            detalle_ticket=self,
            startdate=now(),
            status=status
        )

    def get_new_status(self):
        """
        Devuelve el status del item del ticket,
        verificando posibles errores, en caso de que no tenga,
        o tenga varios devuelve un estatus que corresponda
        """
        if self.status is None:
            status_filter = self.ticketsdetailstatus_set.all().filter(enddate=None)
            count_status = status_filter.count()
            if count_status == 0:
                old_status_exist = self.ticketsdetailstatus_set.all().order_by('-startdate')
                if old_status_exist.exists():
                    # entra cuando por algun motivo no hay ningun status activo,
                    # se pone el ultimo como activo nuevamente
                    ultimo_status = old_status_exist[0]
                    ultimo_status.enddate = None
                    ultimo_status.save(update_fields=['enddate'])
                else:
                    # si por algun motivo el item del ticket no tiene status,
                    # se crea el status inicial
                    from admin_status.models import Status
                    ultimo_status = TicketsDetailStatus.objects.create(
                        detalle_ticket=self,
                        startdate=now(),
                        status=Status.get_status_by_codename(
                            codename='status_ticketpendiente'
                        ),
                    )
            elif count_status == 1:
                # normalmente entra aqui, ya que deberia aver un solo status
                ultimo_status = status_filter[0]
            elif count_status >= 2:
                # puede pasar que queden 2 status activos,
                # cierra los viejos y devuelve el mas nuevo
                status_filter = status_filter.order_by('-startdate')
                for obj in status_filter[1:]:
                    obj.enddate = now()
                    obj.save(update_fields=['enddate'])
                ultimo_status = status_filter[0]

            self.status = ultimo_status.status
            self.updated_at = ultimo_status.startdate
            self.save(update_fields=['status', 'updated_at'])
        return self

    def get_status(self):
        """
        Devuelve el status acual del item del ticke
        """
        return self.get_new_status().status

    def get_status_all(self):
        """
        Devuelve todos los status asociados al item del ticket
        """
        return self.ticketsdetailstatus_set.all()

    def get_valor_column_type(self):
        if self.ticket.ticket_type.codename == 'type_quiniela':
            return self.puntaje_apostado
        else:
            return self.logro_apostado


class TicketStatus(models.Model):
    """TicketStatus: Detalle de los estatus de los tickets

    Campos definidos:
        startdate(datetime): fecha y hora de inicio del status

        enddate(datetime): fecha y hora del cierre del status

        status(foreign): estatus al que hace referencia el registro

        ticket(foreign): ticket al cual hace referencia el registro

        created_at y updated_at: registros de creacion y actualizacion.
    """
    startdate = models.DateTimeField(
    )
    enddate = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        'admin_status.Status'
    )
    ticket = models.ForeignKey(
        'Tickets'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Estatus de un ticket')
        verbose_name_plural = ('Estatus de los tickets')
        ordering = ['startdate', ]


class TicketsDetailStatus(models.Model):
    """TicketsDetailStatus: Detalle de los estatus de los items de los tickets

    Campos definidos:
        startdate(datetime): fecha y hora de inicio del status

        enddate(datetime): fecha y hora del cierre del status

        status(foreign): estatus al que hace referencia el registro

        detalle_ticket(foreign): item de detalle de ticket al que hace
            referencia el registro

        created_at y updated_at: registros de creacion y actualizacion.
    """
    startdate = models.DateTimeField(
    )
    enddate = models.DateTimeField(
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        'admin_status.Status'
    )
    detalle_ticket = models.ForeignKey(
        'TicketsDetail'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Estatus de un item de un ticket')
        verbose_name_plural = ('Estatus de los items de los tickets')
        ordering = ['startdate', ]
