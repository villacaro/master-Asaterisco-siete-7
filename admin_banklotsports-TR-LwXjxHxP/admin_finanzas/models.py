# -*- coding: utf-8 -*-
from datetime import timedelta
from decimal import Decimal

from admin_banklotsports.settings import CACHES_CONF_TIME, FORMAT_STR_DATE_REPORTS
from admin_historic import auditoria
from admin_lib.util_funtions import get_decimal_is_not_none
from django.core.cache import cache
from django.db import models
from django.db.models import Sum
from django.utils.timezone import now


class Banco(models.Model):
    """Banco: Bancos

    Campos definidos:
        nombre(string): nombre del banco

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre (*)'
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
        verbose_name = ('Banco')
        verbose_name_plural = ('Bancos')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class TipoCuenta(models.Model):
    """TipoCuenta: Tipos de cuentas

    Campos definidos:
        nombre(string): nombre del banco
        codigo(string): codigo del tipo de cuenta:
            C.A (cuenta de ahorro)
            C.C (Cuenta corriente)
            C.E (Efectivo)

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre (*)'
    )
    codigo = models.CharField(
        max_length=10,
        verbose_name='Codigo (*)'
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
        verbose_name = ('Tipo de cuenta')
        verbose_name_plural = ('Tipos de cuenta')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class TipoMovimiento(models.Model):
    """TipoMovimiento: Tipos de movimientos

    Campos definidos:
        nombre(string): nombre del banco
        codename(string): codename en string de los distintos tipos de movimientos:
            tipo_deposito (deposito)
            tipo_pago (pago)
            tipo_ajuste_cobrar (ajuste para cobrar)
            tipo_ajuste_pagar (ajuste para pagar)

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=50,
        verbose_name='Nombre (*)'
    )
    codename = models.CharField(
        max_length=100,
        verbose_name='Código (*)'
    )
    description = models.CharField(
        max_length=100,
        verbose_name='Descripción (*)'
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
        verbose_name = ('Tipo de movimiento')
        verbose_name_plural = ('Tipos de movimientos')
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class ComercializadoraManager(models.Manager):

    def get_comercializadora(self, object=None):
        kwargs = {}
        kwargs[object.prefix_filter] = object
        return Comercializadora.objects.get(
            **kwargs
        )

    def get_or_cretate_comercializadora(self, object=None):
        kwargs = {}
        kwargs[object.prefix_filter] = object
        return Comercializadora.objects.get_or_create(
            **kwargs
        )[0]

    def get(self, *args, **kwargs):
        comercializadora = None

        if len(kwargs) == 1 and kwargs.get('pk'):
            comercializadora = cache.get(
                '{0}_{1}'.format('comercializadora', kwargs.get('pk'))
            )
            if not comercializadora:
                comercializadora = super(ComercializadoraManager, self).get(*args, **kwargs)
                cache.set(
                    '{0}_{1}'.format('comercializadora', kwargs.get('pk')),
                    comercializadora,
                    CACHES_CONF_TIME['registros_db']['comercializacion'],
                )
            return comercializadora
        else:
            return super(ComercializadoraManager, self).get(*args, **kwargs)


class Comercializadora(models.Model):
    """Comercializadora: Comercializadora

    Campos definidos:
        operadora(foreing): operadora a la cual pertenece el cupo
        bloque(foreing): bloque a la cual pertenece el cupo
        banca(foreing): banca a la cual pertenece el cupo
        distribuidor(foreing): distribuidor a la cual pertenece el cupo
        agencia(foreing): agencia a la cual pertenece el cupo
        taquilla(foreing): taquilla a la cual pertenece el cupo

        Los campos: operadora, bloque, banca, distribuidor, agencia y taquilla forman
            un arco

        saldo_inicial(decimal): contiene el saldo inicial con el que comienza la cadena
        saldo_fecha(date): contiene la fecha en la que se asigna el saldo inicial

        created_at y updated_at: registros de creacion y actualizacion.

    """

    operadora = models.ForeignKey(
        'admin_comercializacion.Operadoras',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Operadora'
    )
    bloque = models.ForeignKey(
        'admin_comercializacion.Bloques',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Bloque'
    )
    banca = models.ForeignKey(
        'admin_comercializacion.Bancas',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Banca'
    )
    distribuidor = models.ForeignKey(
        'admin_comercializacion.Distribuidores',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Distribuidor'
    )
    agencia = models.ForeignKey(
        'admin_comercializacion.Agencias',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Agencia'
    )
    taquilla = models.ForeignKey(
        'admin_comercializacion.Taquillas',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Taquilla'
    )
    saldo_inicial = models.DecimalField(
        null=True,
        blank=True,
        max_digits=15,
        decimal_places=2,
        default=0.0,
        verbose_name='Saldo inicial (*)',
        help_text='Introduzca el saldo inicial de la comercializadora'
    )
    saldo_fecha = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fecha de saldo inicial (*)',
        help_text='Introduzca la fecha del saldo inicial de la comercializadora'
    )
    resumen_personalizado = models.BooleanField(
        default=False,
        verbose_name='Resumen personalizado',
        help_text='En caso de estar activada esta opcion la comercializadora sera gestionada '
        'solo desde resumen personalizado.'
    )
    resumen_personalizado_comer = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    objects = ComercializadoraManager()

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    object_relate = None
    name_cache = 'object_comer'
    audit_exclude = ('resumen_personalizado_comer',)

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Comercializadora')
        verbose_name_plural = ('Comercializadoras')
        ordering = [
            'operadora',
            'bloque',
            'banca',
            'distribuidor',
            'agencia',
            'taquilla'
        ]

    def __str__(self):
        object = self.get_object()
        return '{0} | {1}'.format(
            object._meta.verbose_name,
            object
        )

    def save(self, *args, **kwargs):
        super(Comercializadora, self).save(*args, **kwargs)
        self.cache_clear()
        self.get_object().cache_clear()

    def cache_clear(self):
        cache.delete('{0}_{1}'.format(self.name_cache, self.pk))
        cache.delete('{0}_{1}'.format('comercializadora', self.pk))
        cache.delete('{0}_{1}'.format('dia_trabajo', self.pk))
        cache.delete('{0}_{1}'.format('sistemalogros_', self.pk))
        cache.delete('{0}_{1}'.format('sistemaresultados_', self.pk))
        cache.delete('{0}_{1}'.format('sistemajuego_', self.pk))

    def reiniciar(self):
        """
        Reinicia el saldo incial
        """
        self.saldo_inicial = 0.0
        self.saldo_fecha = now()
        self.resumen_personalizado = False
        self.resumen_personalizado_comer = None
        self.save(update_fields=[
            'saldo_inicial',
            'saldo_fecha',
            'resumen_personalizado',
            'resumen_personalizado_comer',
            'updated_at'
        ]
        )
        self.set_saldo_inicial()

    def set_saldo_inicial(self):
        """
        Asigna el saldo incial
        """

        resumen = ResumenAdministrativo.objects.get_or_create(
            comercializacion=self.get_object().get_dimension_arco_comercializadora(),
            dia=Dia.objects.get_or_create(fecha=self.saldo_fecha)[0]
        )[0]

        resumen.saldo_anterior += Decimal(self.saldo_inicial)
        resumen.save(update_fields=['saldo_anterior'])
        self.save(update_fields=['saldo_inicial', 'saldo_fecha', 'updated_at'])

    def get_object(self):
        """
        Retorna el obteto de la cadena correspondiente
        """
        self.object_relate = cache.get('{0}_{1}'.format(self.name_cache, self.pk))
        if not self.object_relate:
            if self.operadora_id:
                self.object_relate = self.operadora
            elif self.bloque_id:
                self.object_relate = self.bloque
            elif self.banca_id:
                self.object_relate = self.banca
            elif self.distribuidor_id:
                self.object_relate = self.distribuidor
            elif self.agencia_id:
                self.object_relate = self.agencia
            elif self.taquilla_id:
                self.object_relate = self.taquilla
            cache.set(
                '{0}_{1}'.format(self.name_cache, self.pk),
                self.object_relate,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return self.object_relate

    def get_status(self):
        """
        Retorna el obteto de la cadena correspondiente
        """
        key_cache = 'status_comer_{0}_{1}'.format(
            self.get_object().prefix_filter,
            self.get_object().pk
        )

        status = cache.get(key_cache)
        if not status:
            status = self.get_object().status
            cache.set(
                key_cache,
                status,
                CACHES_CONF_TIME['registros_db']['user'],
            )
        return status

    def get_object_id(self):
        """
        Retorna el obteto de la cadena correspondiente
        """
        if self.operadora_id:
            return self.operadora_id
        elif self.bloque_id:
            return self.bloque_id
        elif self.banca_id:
            return self.banca_id
        elif self.distribuidor_id:
            return self.distribuidor_id
        elif self.agencia_id:
            return self.agencia_id
        elif self.taquilla_id:
            return self.taquilla_id

    def get_origen(self):
        origen = self.get_object().get_origen()
        if origen:
            return origen.get_comercializadora()
        else:
            return None

    def get_exclude_resumen_personalizado_kwargs(self):

        kwargs = {}
        if self.operadora_id:
            kwargs['bloque__operadora_id'] = self.operadora_id
            kwargs['banca__bloque__operadora_id'] = self.operadora_id
            kwargs['distribuidor__banca__bloque__operadora_id'] = self.operadora_id
            kwargs['agencia__distribuidores__banca__bloque__operadora_id'] = self.operadora_id

        elif self.bloque_id:
            kwargs['banca__bloque_id'] = self.bloque_id
            kwargs['distribuidor__banca__bloque_id'] = self.bloque_id
            kwargs['agencia__distribuidores__banca__bloque_id'] = self.bloque_id

        elif self.banca_id:
            kwargs['distribuidor__banca_id'] = self.banca_id
            kwargs['agencia__distribuidores__banca_id'] = self.banca_id

            # Se exluye el bloque al cual pertenece
            kwargs['bloque_id'] = self.banca.bloque_id

        elif self.distribuidor_id:
            kwargs['agencia__distribuidores_id'] = self.distribuidor_id

            # Se exluye el bloque y banca al cual pertenece
            kwargs['bloque_id'] = self.distribuidor.banca.bloque_id
            kwargs['banca_id'] = self.distribuidor.banca_id

        elif self.agencia_id:

            # Se exluye el bloque, banca y distribuidor al cual pertenece
            kwargs['bloque_id'] = self.agencia.distribuidores.banca.bloque_id
            kwargs['banca_id'] = self.agencia.distribuidores.banca_id
            kwargs['distribuidor_id'] = self.agencia.distribuidores_id

        return kwargs

    def get_offspring(self, profile=None):
        if not profile:
            codename = self.get_object().user_type_codename
        else:
            codename = profile.codename
        from admin_status.models import Status
        status_eliminado = Status.get_status_by_codename('status_eliminado')
        queryset = Comercializadora.objects.none()
        if self.operadora_id:
            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
            ]:
                queryset |= Comercializadora.objects.filter(
                    bloque__operadora_id=self.operadora_id
                ).exclude(
                    bloque__status_id=status_eliminado.pk
                )

            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
            ]:
                queryset |= Comercializadora.objects.filter(
                    banca__bloque__operadora_id=self.operadora_id
                ).exclude(
                    banca__status_id=status_eliminado.pk
                )

            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
            ]:
                queryset |= Comercializadora.objects.filter(
                    distribuidor__banca__bloque__operadora_id=self.operadora_id
                ).exclude(
                    distribuidor__status_id=status_eliminado.pk
                )

            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
                'userprofile_agencia',
            ]:
                queryset |= Comercializadora.objects.filter(
                    agencia__distribuidores__banca__bloque__operadora_id=self.operadora_id
                ).exclude(
                    agencia__status_id=status_eliminado.pk
                )
        elif self.bloque_id:
            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
            ]:
                queryset |= Comercializadora.objects.filter(
                    banca__bloque_id=self.bloque_id
                ).exclude(
                    banca__status_id=status_eliminado.pk
                )

            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
            ]:
                queryset |= Comercializadora.objects.filter(
                    distribuidor__banca__bloque_id=self.bloque_id
                ).exclude(
                    distribuidor__status_id=status_eliminado.pk
                )

            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
                'userprofile_agencia',
            ]:
                queryset |= Comercializadora.objects.filter(
                    agencia__distribuidores__banca__bloque_id=self.bloque_id
                ).exclude(
                    agencia__status_id=status_eliminado.pk
                )
        elif self.banca_id:
            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
            ]:
                queryset |= Comercializadora.objects.filter(
                    distribuidor__banca_id=self.banca_id
                ).exclude(
                    distribuidor__status_id=status_eliminado.pk
                )

            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
                'userprofile_agencia',
            ]:
                queryset |= Comercializadora.objects.filter(
                    agencia__distribuidores__banca_id=self.banca_id
                ).exclude(
                    agencia__status_id=status_eliminado.pk
                )
        elif self.distribuidor_id:
            if codename in [
                'userprofile_operadora',
                'userprofile_bloque',
                'userprofile_banca',
                'userprofile_distribuidor',
                'userprofile_agencia',
            ]:
                queryset |= Comercializadora.objects.filter(
                    agencia__distribuidores_id=self.distribuidor_id
                ).exclude(
                    agencia__status_id=status_eliminado.pk
                )
        elif self.agencia_id:
            queryset = Comercializadora.objects.none()

        return queryset

    def get_offspring_level1(self, exclude_delete=True):
        queryset = Comercializadora.objects.none()
        from admin_status.models import Status
        status_eliminado = Status.get_status_by_codename('status_eliminado')
        if self.operadora_id:
            queryset = Comercializadora.objects.filter(
                bloque__operadora_id=self.operadora_id
            )
        elif self.bloque_id:
            queryset = Comercializadora.objects.filter(
                banca__bloque_id=self.bloque_id
            )
        elif self.banca_id:
            queryset = Comercializadora.objects.filter(
                distribuidor__banca_id=self.banca_id
            )
        elif self.distribuidor_id:
            queryset = Comercializadora.objects.filter(
                agencia__distribuidores_id=self.distribuidor_id
            )
        elif self.agencia_id:
            queryset = Comercializadora.objects.filter(
                taquilla__agencia_id=self.agencia_id
            )
        elif self.taquilla_id:
            queryset = Comercializadora.objects.none()

        if exclude_delete:
            if self.operadora_id:
                queryset = queryset.exclude(
                    bloque__status_id=status_eliminado.pk
                )
            elif self.bloque_id:
                queryset = queryset.exclude(
                    banca__status_id=status_eliminado.pk
                )
            elif self.banca_id:
                queryset = queryset.exclude(
                    distribuidor__status_id=status_eliminado.pk
                )
            elif self.distribuidor_id:
                queryset = queryset.exclude(
                    agencia__status_id=status_eliminado.pk
                )
            elif self.agencia_id:
                queryset = queryset.exclude(
                    taquilla__usuariostaquilla__status_id=status_eliminado.pk
                )

        return queryset

    def get_offspring_level1_by_profile(self, profile):
        codename = profile.codename

        queryset = Comercializadora.objects.none()
        if self.operadora_id:
            if codename == 'userprofile_operadora':
                queryset = Comercializadora.objects.filter(
                    operadora_id=self.operadora_id
                )
            elif codename == 'userprofile_bloque':
                queryset = Comercializadora.objects.filter(
                    bloque__operadora_id=self.operadora_id
                )
            elif codename == 'userprofile_banca':
                queryset = Comercializadora.objects.filter(
                    banca__bloque__operadora_id=self.operadora_id
                )
            elif codename == 'userprofile_distribuidor':
                queryset = Comercializadora.objects.filter(
                    distribuidor__banca__bloque__operadora_id=self.operadora_id
                )
            elif codename == 'userprofile_agencia':
                queryset = Comercializadora.objects.filter(
                    agencia__distribuidores__banca__bloque__operadora_id=self.operadora_id
                )

        elif self.bloque_id:
            if codename == 'userprofile_bloque':
                queryset = Comercializadora.objects.filter(
                    bloque_id=self.bloque_id
                )
            elif codename == 'userprofile_banca':
                queryset = Comercializadora.objects.filter(
                    banca__bloque_id=self.bloque_id
                )
            elif codename == 'userprofile_distribuidor':
                queryset = Comercializadora.objects.filter(
                    distribuidor__banca__bloque_id=self.bloque_id
                )
            elif codename == 'userprofile_agencia':
                queryset = Comercializadora.objects.filter(
                    agencia__distribuidores__banca__bloque_id=self.bloque_id
                )
        elif self.banca_id:
            if codename == 'userprofile_banca':
                queryset = Comercializadora.objects.filter(
                    banca_id=self.banca_id
                )
            elif codename == 'userprofile_distribuidor':
                queryset = Comercializadora.objects.filter(
                    distribuidor__banca_id=self.banca_id
                )
            elif codename == 'userprofile_agencia':
                queryset = Comercializadora.objects.filter(
                    agencia__distribuidores__banca_id=self.banca_id
                )
        elif self.distribuidor_id:
            if codename == 'userprofile_distribuidor':
                queryset = Comercializadora.objects.filter(
                    distribuidor_id=self.distribuidor_id
                )
            elif codename == 'userprofile_agencia':
                queryset = Comercializadora.objects.filter(
                    agencia__distribuidores_id=self.distribuidor_id
                )
        elif self.agencia_id:
            if codename == 'userprofile_agencia':
                queryset = Comercializadora.objects.filter(
                    agencia_id=self.agencia_id
                )

        from admin_status.models import Status
        status_eliminado = Status.get_status_by_codename('status_eliminado').pk
        queryset = queryset\
            .exclude(bloque__status_id=status_eliminado)\
            .exclude(banca__status_id=status_eliminado)\
            .exclude(distribuidor__status_id=status_eliminado)\
            .exclude(agencia__status_id=status_eliminado)

        return queryset

    def get_offspring_taquillas(self):
        if self.operadora:
            queryset = Comercializadora.objects.filter(
                taquilla__agencia__distribuidores__banca__bloque__operadora_id=self.operadora.pk
            )
        elif self.bloque:
            queryset = Comercializadora.objects.filter(
                taquilla__agencia__distribuidores__banca__bloque_id=self.bloque.pk
            )
        elif self.banca:
            queryset = Comercializadora.objects.filter(
                taquilla__agencia__distribuidores__banca_id=self.banca.pk
            )
        elif self.distribuidor:
            queryset = Comercializadora.objects.filter(
                taquilla__agencia__distribuidores_id=self.banca.pk
            )
        elif self.agencia:
            queryset = Comercializadora.objects.filter(
                taquilla__agencia_id=self.agencia.pk
            )
        elif self.taquilla:
            queryset = Comercializadora.objects.none()

        return queryset

    def get_type(self):
        return self.get_object().get_type()

    def get_type_codename(self):
        return self.get_object().user_type_codename

    def get_dia_trabajo(self):
        dia_trabajo = cache.get('{0}_{1}'.format('dia_trabajo', self.pk))
        if not dia_trabajo:
            try:
                dia_trabajo = self.diatrabajo_set.select_related('dia').get(actual=True)
                cache.set(
                    '{0}_{1}'.format('dia_trabajo', self.pk),
                    dia_trabajo,
                    CACHES_CONF_TIME['registros_db']['dia_trabajo']
                )
            except Exception:
                pass
        return dia_trabajo

    def get_or_create_dia_trabajo(self):
        self.cache_clear()
        return DiaTrabajo.objects.get_dia_de_trabajo_actual(
            self
        )

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.get_object().__module__.split('.')[0],
            self.get_object().__class__.__name__.lower(),
            self.get_object_id()
        )

    def get_porcentaje(self, codename, fecha=None):
        from admin_datamart.task import ObtenerPorcentaje
        if not fecha:
            dia_trabajo = self.get_dia_trabajo()
            fecha = dia_trabajo.dia.fecha
        return ObtenerPorcentaje(
            codename=codename,
            cadena=self.get_object(),
            fecha=fecha
        )

    def process_import(self, force_anulado=False, import_all=True):
        """
            Realiza los procesos necesarios que implican importar saldos en
            el dia de trabajo actual
        """

        dia_trabajo = self.get_dia_trabajo()
        comercializadora_object = self.get_object()

        if comercializadora_object.get_exists_get_tickets_is_day_unprocessed(
            fecha=dia_trabajo.dia.fecha
        ):
            if not force_anulado:
                return False
            else:
                from admin_apuestas.task import AsyncProcesarTickets_Soporte_Manual_anular
                for ticket in comercializadora_object.get_tickets_is_day_unprocessed(
                    fecha=dia_trabajo.dia.fecha
                ):
                    resp = AsyncProcesarTickets_Soporte_Manual_anular()
                    resp.run(
                        *(),
                        **{
                            'ticket': ticket.pk,
                        }
                    )

        queryset = self.get_offspring_level1().filter(
            resumen_personalizado=False
        )
        if import_all:
            queryset |= self.comercializadora_set.all()

        for comercializadora in queryset:

            if not comercializadora.saldo_fecha:
                # si aun no tiene saldo inicial
                continue
            elif comercializadora.saldo_fecha > dia_trabajo.dia.fecha:
                # si tiene saldo inicial pero es mayor al dia de trabajo actual
                continue

            comercializadora_object = comercializadora.get_object()
            dimencion_comer = comercializadora_object.get_dimension_arco_comercializadora()

            venta, create = ResumenAdministrativo.objects.get_or_create(
                dia=dia_trabajo.dia,
                comercializacion=dimencion_comer
            )

            from admin_datamart.models import Hecho5_ComisionesCadena
            try:
                data_procesada = Hecho5_ComisionesCadena.objects.get(
                    tiempo__fecha=dia_trabajo.dia.fecha,
                    comercializacion=dimencion_comer
                )

                venta.venta = data_procesada.venta
                venta.premio = data_procesada.premio
                venta.comision = data_procesada.comision
                venta.regalia = data_procesada.regalia
                venta.participacion = data_procesada.participacion
                venta.saldo_bruto = data_procesada.saldo_bruto
                venta.queda = data_procesada.queda_ref
                venta.saldo_comer = data_procesada.saldo_comer
                venta.saldo_oper = data_procesada.saldo_oper

                if comercializadora_object.get_frecuencia_queda_is_corte_day(
                    dia_trabajo.dia.fecha + timedelta(days=1)
                ):

                    ventas_hecho = Hecho5_ComisionesCadena.objects.filter(
                        tiempo__fecha__range=comercializadora_object
                        .get_frecuencia_queda_is_range_corte(
                            dia_trabajo.dia.fecha
                        ),
                        comercializacion=dimencion_comer
                    )
                    queda = get_decimal_is_not_none(
                        ventas_hecho.aggregate(
                            Sum('queda_ref'),
                        )['queda_ref__sum']
                    )

                    if queda > 0:

                        venta.cargo = queda - (
                            queda * comercializadora.get_porcentaje(
                                codename='porcentaje_participacion',
                                fecha=dia_trabajo.dia.fecha
                            )
                        )

                venta.save()
            except Hecho5_ComisionesCadena.DoesNotExist:
                pass
        dia_trabajo.procesado = True
        dia_trabajo.save(update_fields=['procesado'])
        self.cache_clear()
        return True

    def process_close_day(self, import_add=False):
        """
            Realiza los procesos necesarios que implican cerrar un dia de trabajo
        """

        dia_trabajo_old = self.get_dia_trabajo()

        if not dia_trabajo_old:
            return False
        elif not dia_trabajo_old.procesado:
            if import_add:
                import_success = self.process_import()
                if import_success is False:
                    return False
            else:
                return False

        dia = dia_trabajo_old.dia
        dia_new = Dia.objects.get_or_create(
            fecha=dia.fecha + timedelta(days=1)
        )[0]
        dia_trabajo_new = DiaTrabajo.objects.get_or_create(
            dia=dia_new,
            comercializadora=self
        )[0]

        for comercializadora in self.get_offspring_level1():
            comercializadora_object = comercializadora.get_object()
            dimencion_comer = comercializadora_object.get_dimension_arco_comercializadora()
            venta = ResumenAdministrativo.objects.get_or_create(
                dia=dia,
                comercializacion=dimencion_comer
            )[0]

            if not comercializadora.saldo_fecha:
                # si aun no tiene saldo inicial
                continue
            elif comercializadora.saldo_fecha > dia_trabajo_new.dia.fecha:
                # si tiene saldo inicial pero es mayor al dia de trabajo actual
                continue

            movimientos = Movimiento.objects.filter(
                dia=dia,
                comercializadora_id=comercializadora.pk
            )

            resultado = movimientos.filter(
                tipo__codename='tipo_deposito'
            )

            depositos = resultado.aggregate(Sum('monto'))['monto__sum']
            depositos = Decimal() if not depositos else depositos
            venta.deposito = depositos

            resultado = movimientos.filter(
                tipo__codename='tipo_pago'
            )
            pagos = resultado.aggregate(Sum('monto'))['monto__sum']
            pagos = Decimal() if not pagos else pagos
            venta.pago = pagos

            resultado = movimientos.filter(
                tipo__codename__in=('tipo_ajuste_cobrar', 'tipo_ajuste_pagar')
            )
            ajustes = resultado.aggregate(Sum('monto'))['monto__sum']
            ajustes = Decimal() if not ajustes else ajustes
            venta.ajuste = ajustes

            venta.saldo_actual = venta.saldo_anterior + venta.saldo_oper \
                + depositos + pagos + ajustes - venta.cargo

            venta.save(update_fields=['saldo_actual', 'deposito', 'pago', 'ajuste'])

            venta_new = ResumenAdministrativo.objects.get_or_create(
                dia=dia_new,
                comercializacion=dimencion_comer
            )[0]
            venta_new.saldo_anterior = venta.saldo_actual
            venta_new.save(update_fields=['saldo_anterior'])

        # vefiricar si cambiamos de mes
        if dia.fecha.strftime('%m') != dia_new.fecha.strftime('%m'):

            from admin_finanzas.task import AsyncGenerarEstadosDeCuenta
            AsyncGenerarEstadosDeCuenta().delay(
                *(),
                **{
                    'comercializadora': self.pk,
                    'dia_old': dia.fecha.strftime(FORMAT_STR_DATE_REPORTS),
                    'dia_new': dia_new.fecha.strftime(FORMAT_STR_DATE_REPORTS),
                }
            )

        dia_trabajo_new.actual = True
        dia_trabajo_new.procesado = False
        dia_trabajo_old.actual = False
        dia_trabajo_new.save(update_fields=['actual', 'procesado'])
        dia_trabajo_old.save(update_fields=['actual'])
        self.cache_clear()
        return True

    def get_preference_parent(self, codename):
        preference_comer = None
        origen = self.get_object().get_origen()
        while origen and origen.user_type_codename != 'userprofile_operadora':
            preference_comer = origen.get_preference(codename)
            if preference_comer:
                break
            else:
                origen = origen.get_origen()
        return preference_comer

    def create_or_update_preference(self, typepreference, value, distribute):
        '''
            Retornara el antiguo valor
        '''
        from admin_comercializacion.models import Preferences, DefaultPreferences
        try:
            # Si existe lo actualiza
            preference = Preferences.objects.get(
                comercializacion_id=self.id,
                typepreference_id=typepreference.id
            )
            old_value = preference.value
            preference.value = value
            preference.distribute = distribute
            preference.save(update_fields=['value', 'distribute'])

            # Si existe cache, se borra
            key = 'preference_{0}_{1}'.format(
                self.id,
                typepreference.codename
            )
            cache.delete(key)
        except Preferences.DoesNotExist:
            # Si no existe lo crea
            preference = Preferences(
                comercializacion_id=self.id,
                typepreference_id=typepreference.id,
                value=value,
                distribute=distribute
            )
            preference.save()
            old_value = DefaultPreferences.objects.get(
                typepreference=typepreference,
                default=True,
            ).value
        return old_value

    def get_factores_riesgo(self):
        """
            Función que retorna el factor riesgo asociado a la comercializadora.
            Primero se consulta de la cache, si no existe se consulta directamente en la tabla.
            De no existir un factor de riesgo directo busca el del padre(comercializadora) mas cercano.
        """
        from admin_comercializacion.models import FactorRiesgo

        # Se consulta cache
        key = 'factorriesgo_{0}'.format(self.id)
        factor = cache.get(key)
        if not factor:
            try:
                factor = FactorRiesgo.objects.get(comercializadora=self)
                # Se guarda en cache
                cache.set(key, factor, CACHES_CONF_TIME['registros_db']['comercializacion'])
            except FactorRiesgo.DoesNotExist:
                factor = None
                origen = self.get_origen()
                while origen and origen.get_object().user_type_codename != 'userprofile_operadora':
                    factor = origen.get_factores_riesgo()
                    if factor:
                        break
                    else:
                        origen = origen.get_origen()
        if not factor:
            factor = []
        return factor

    def get_permissions_sales(self, deporte_id, grupo_id=None, modalidad_id=None, breaking=False):
        """
            Función que retorna las restricciones de venta por deporte asociado a la comercializadora.
            Primero se consulta de la cache, si no existe se consulta directamente en la tabla.
            De no existir esa restriccion directa busca el del padre(comercializadora) mas cercano.
            Si no consigue la restriccion se retorna None
        """
        from admin_permisologia.models import PermissionsSales
        # Se busca la restriccion de cache
        if breaking is False:
            key = 'permissionssales_{0}_{1}_{2}_{3}'.format(
                self.id, deporte_id, grupo_id, modalidad_id,)
            restriction = cache.get(key)
        else:
            restriction = None
        if not restriction:
            restriction = None
            kwargs = {}
            kwargs['comercializadora_id'] = self.id
            kwargs['deporte_id'] = deporte_id
            if modalidad_id:
                kwargs['modalidad_id'] = modalidad_id
            else:
                kwargs['modalidad__isnull'] = True

            if grupo_id:
                kwargs['grupo_id'] = grupo_id
            else:
                kwargs['grupo__isnull'] = True

            try:
                restriction = PermissionsSales.objects.get(**kwargs)
                restriction.parent = False
                if restriction.breaking is True and breaking is False:
                    return None
                elif restriction.breaking is False and breaking is True:
                    return None
                # Se guarda
                if breaking is False:
                    key = 'permissionssales_{0}_{1}_{2}_{3}'.format(
                        self.id, deporte_id, grupo_id, modalidad_id,)
                    cache.set(key, restriction, CACHES_CONF_TIME['registros_db']['comercializacion'])
            except PermissionsSales.DoesNotExist:
                origen = self.get_origen()
                while origen and origen.get_object().user_type_codename != 'userprofile_operadora':
                    restriction = origen.get_permissions_sales(deporte_id, grupo_id, modalidad_id)
                    if restriction:
                        restriction.parent = True
                        break
                    else:
                        origen = origen.get_origen()
        return restriction

    def get_permissions_sales_restrictions(self, deporte_id):
        """
            Función que retorna las restricciones de venta (modalidades) por deporte asociado
            a la comercializadora.
            Primero se consulta de la cache, si no existe se consulta directamente en la tabla.
            De no existir esa restriccion directa busca el del padre(comercializadora) mas cercano.
            Si no consigue la restriccion se retorna None
        """
        from admin_permisologia.models import PermissionsSalesRestrictions
        # Se busca la restriccion de cache
        key = 'permissionssalesrestrictions_{0}_{1}'.format(self.id, deporte_id)
        restriction = cache.get(key)
        if not restriction:
            try:
                restriction = PermissionsSalesRestrictions.objects.get(
                    comercializadora_id=self.id, deporte_id=deporte_id)
                cache.set(key, restriction, CACHES_CONF_TIME['registros_db']['comercializacion'])
            except PermissionsSalesRestrictions.DoesNotExist:
                origen = self.get_origen()
                while origen and origen.get_object().user_type_codename != 'userprofile_operadora':
                    restriction = origen.get_permissions_sales_restrictions(deporte_id)
                    if restriction:
                        break
                    else:
                        origen = origen.get_origen()
        return restriction

    def get_restrictions_ventas(self):
        """
            Retorna las restricciones de ventas de la comercializadora.
            Se retorna un arreglo con las restricciones de deporte, grupo o modalidad
        """
        from admin_permisologia.models import PermissionsSales
        kwargs = {}
        kwargs['comercializadora_id'] = self.id
        query = PermissionsSales.objects.filter(**kwargs)
        origen = self.get_origen()
        while origen and origen.get_object().user_type_codename != 'userprofile_operadora':
            kwargs['comercializadora_id'] = origen.id
            query |= PermissionsSales.objects.filter(**kwargs)
            origen = origen.get_origen()

        breaking_true = query.filter(breaking=True).values(
            'deporte_id', 'grupo_id', 'modalidad_id')

        query = query.filter(breaking=False)
        for breaking in breaking_true:
            query = query.exclude(**breaking)

        if query:
            return query
        else:
            return PermissionsSales.objects.none()


class Configuracion(models.Model):
    """Configuracion: Configuracion

    Campos definidos:
        comercializadora(foreing): comercializadora a la que pertenece la configuracion


        created_at y updated_at: registros de creacion y actualizacion.

    """
    comercializadora = models.ForeignKey(
        'Comercializadora',
        editable=False
    )
    TIPO_PAGAR = 'pc'
    TIPO_COBRAR = 'pp'
    CHOICES_TIPO = (
        (TIPO_PAGAR, 'Por cobrar'),
        (TIPO_COBRAR, 'Por pagar')
    )
    tipo = models.CharField(
        choices=CHOICES_TIPO,
        max_length=2,
    )
    min = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )
    max = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
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
        unique_together = ('comercializadora', 'tipo')
        verbose_name = ('Configuracion comercializadora')
        verbose_name_plural = ('Configuraciones de las comercializadoras')

    def __str__(self):
        return 'Configuración {0}, min: {1}, max: {2}'.format(self.get_tipo_display(), self.min, self.max)

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.comercializadora.get_object().__module__.split('.')[0],
            self.comercializadora.get_object().__class__.__name__.lower(),
            self.comercializadora.get_object_id()
        )


class Cuenta(models.Model):
    """Cuenta: Cuenta

    Campos definidos:
        comercializadora(foreing): comercializadora a la que pertenece la cuenta

        banco(foreing): banco al que pertenece la cuenta

        tipocuenta(foreing): tipo de cuenta

        numero(string): numero de cuenta bancaria

        description(string): description de la cuenta bancaria

        created_at y updated_at: registros de creacion y actualizacion.

    """
    comercializadora = models.ForeignKey(
        'Comercializadora',
        null=True,
        blank=True,
        editable=False,
        verbose_name='Comercializadora '
    )
    banco = models.ForeignKey(
        'Banco',
        verbose_name='Banco (*)',
        help_text='Seleccione un banco'
    )
    tipocuenta = models.ForeignKey(
        'TipoCuenta',
        verbose_name='Tipo de cuenta (*)'
    )
    numero = models.CharField(
        max_length=20,
        verbose_name='Numero de cuenta (*)'
    )
    description = models.CharField(
        max_length=100,
        verbose_name='Descripción (*)'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    audit_exclude = ('updated_at', )

    class Meta:
        db_tablespace = 'ts_finance'
        verbose_name = ('Cuenta bancaria')
        verbose_name_plural = ('Cuentas bancarias')

    def __str__(self):
        return self.description + ' ' + self.numero[:4]

    @models.permalink
    def get_absolute_url(self):
        return ('admin_finanzas_cuenta_detail', (), {'pk': self.pk})

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.comercializadora.get_object().__module__.split('.')[0],
            self.comercializadora.get_object().__class__.__name__.lower(),
            self.comercializadora.get_object_id()
        )


class Dia(models.Model):
    """Cuenta: Cuenta

    Campos definidos:
        fecha(date): fecha del dia
        created_at y updated_at: registros de creacion y actualizacion.

    """
    fecha = models.DateField(
        unique=True,
        verbose_name='Fecha '
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
        verbose_name = ('Dias')
        verbose_name_plural = ('Dias')

    def __str__(self):
        return '{0}'.format(self.fecha)


class EstatoCuenta(models.Model):
    """EstatoCuenta: Estado de cuenta

    Campos definidos:
        dia(foreing): dia que se proceso el estado de cuenta

        cuenta(foreing): cuenta que se esta procesando

        saldo(foreing): saldo acumulado

        created_at y updated_at: registros de creacion y actualizacion.

    """
    dia = models.ForeignKey(
        'Dia',
        verbose_name='Día'
    )
    cuenta = models.ForeignKey(
        'Cuenta',
        verbose_name='Cuenta'
    )
    saldo = models.DecimalField(
        max_digits=15,
        default=0.0,
        decimal_places=2,
        verbose_name='Saldo'
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
        verbose_name = ('Estado de cuenta')
        verbose_name_plural = ('Estados de cuenta')

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.cuenta.__module__.split('.')[0],
            self.cuenta.__class__.__name__.lower(),
            self.cuenta_id
        )


class DiaTrabajoManager(models.Manager):

    def get_dia_de_trabajo_actual(self, comercializadora):
        try:
            return self.get(
                actual=True,
                comercializadora=comercializadora
            )
        except DiaTrabajo.DoesNotExist:
            return self.create(
                dia=Dia.objects.get_or_create(fecha=comercializadora.created_at.date())[0],
                comercializadora=comercializadora
            )


class DiaTrabajo(models.Model):
    """DiaTrabajo: Dia de trabajo

    Campos definidos:
        comercializadora(foreing): comercializadora a la cual pertenece el dia de trabajo

        dia(foreing): dia que se proceso el estado de cuenta

        proceso(booleano): bandera que me indica si el dia de trabajo ya fue procesado

        actual(booleano): bandera que me indica si es dia de trabajo es el actual

        created_at y updated_at: registros de creacion y actualizacion.

    """
    comercializadora = models.ForeignKey(
        'Comercializadora',
        verbose_name='Comercializadora'
    )
    dia = models.ForeignKey(
        'Dia',
        verbose_name='Día'
    )
    procesado = models.BooleanField(
        default=False,
        verbose_name='Procesado'
    )
    actual = models.BooleanField(
        default=True,
        verbose_name='Actual'
    )

    objects = DiaTrabajoManager()

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
        verbose_name = ('Dia de trabajo')
        verbose_name_plural = ('Dia de trabajos')

    def __str__(self):
        return 'Dia de trabajo: {0}'.format(self.dia)

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.comercializadora.get_object().__module__.split('.')[0],
            self.comercializadora.get_object().__class__.__name__.lower(),
            self.comercializadora.get_object_id()
        )


class Movimiento(models.Model):
    """Movimiento: Movimientos bancarios

    Campos definidos:
        user(foreing): usuario que proceso el movimiento

        dia(foreing): dia que se proceso el movimiento

        comercializadora(foreing): comercializadora a la que pertenece el movimiento

        cuenta(foreing): cuenta a la que pertenece el movimiento
        tipo(foreing): tipo de movimiento
        numero(string): numero de referencia del movimiento

        fecha(date): fecha del movimiento
        observacion(string): alguna observacion del movimeinto

        comprobante(imagen): imagen de comprobante opcional para gestionar movimientos

        created_at y updated_at: registros de creacion y actualizacion.

    """
    user = models.ForeignKey(
        'admin_users.Users',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name='Usuario ',
    )
    dia = models.ForeignKey(
        'Dia',
        verbose_name='Día ',
    )
    comercializadora = models.ForeignKey(
        'Comercializadora',
        verbose_name='Comercializadora (*)'
    )
    cuenta = models.ForeignKey(
        'Cuenta',
        verbose_name='Cuenta (*)'
    )
    tipo = models.ForeignKey(
        'TipoMovimiento',
        verbose_name='Tipo de movimiento'
    )
    numero = models.CharField(
        max_length=5,
        null=True,
        blank=True,
        verbose_name='Número referencia (*)'
    )
    monto = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto (*)'
    )
    fecha = models.DateField(
        help_text='Fecha del movimiento',
        verbose_name='Fecha (*)',
    )
    observacion = models.CharField(
        max_length=200,
        verbose_name='Observación (*)'
    )
    comprobante = models.ImageField(
        upload_to='movimientos',
        blank=True,
        null=True,
        verbose_name='Comprobante ',
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
        verbose_name = ('Movimiento bancario')
        verbose_name_plural = ('Movimientos bancarios')

    def __str__(self):
        return '{0} de {1} por {2}'.format(
            self.tipo,
            self.comercializadora,
            self.monto if self.monto > 0 else self.monto * -1
        )

    def get_url_tipo(self):
        return 'admin_finanzas_operaciones_' + self.tipo.codename.split('_')[1] + '_list'

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.cuenta.__module__.split('.')[0],
            self.cuenta.__class__.__name__.lower(),
            self.cuenta_id
        )

    def save(self, *args, **kwargs):
        super(Movimiento, self).save(*args, **kwargs)
        self.update_hecho9(operacion='+')

    def delete(self, *args, **kwargs):
        self.update_hecho9(operacion='-')
        super(Movimiento, self).delete(*args, **kwargs)

    def update_hecho9(self, operacion):
        from admin_datamart.task import InitDimensiones
        dimensiones = InitDimensiones()
        if self.comercializadora.operadora is None:
            arcocomercializacion = self.comercializadora.get_object() \
                .get_dimension_arco_comercializadora()

            fecha = self.dia.fecha.strftime(FORMAT_STR_DATE_REPORTS)
            # Se consulta o crea el registro del hecho9
            hecho9 = dimensiones.get_hecho9_ventas_saldo_cadena(
                fecha,
                arcocomercializacion
            )

            if self.tipo.codename == 'tipo_deposito':
                if operacion == '+':
                    hecho9.depositos += self.monto
                else:
                    hecho9.depositos -= self.monto

            elif self.tipo.codename == 'tipo_pago':
                if operacion == '+':
                    hecho9.pagos += self.monto
                else:
                    hecho9.pagos -= self.monto

            elif (self.tipo.codename == 'tipo_ajuste_pagar' or
                  self.tipo.codename == 'tipo_ajuste_cobrar'):
                if operacion == '+':
                    hecho9.ajustes += self.monto
                else:
                    hecho9.ajustes -= self.monto

            from admin_datamart.models import Hecho9_VentasSaldosCadena
            hecho9_anterior = Hecho9_VentasSaldosCadena.objects.filter(
                comercializacion=arcocomercializacion
            ).order_by('-tiempo__fecha')

            subtotal = hecho9.depositos + hecho9.pagos + hecho9.ajustes

            if hecho9_anterior.count() >= 2:
                hecho9.saldo_anterior = hecho9_anterior[1].saldo_actual
            else:
                hecho9.saldo_anterior = 0
            hecho9.saldo_actual = hecho9.saldo_anterior + subtotal
            hecho9.save()


class ResumenAdministrativo(models.Model):
    """ResumenAdministrativo: Resumen administrativo diario

    Campos definidos:
        dia(foreing): dia que se proceso el movimiento

        comercializadora(foreing): comercializadora a la que pertenece el movimiento

        venta(decimal): venta del dia
        premios(decimal): premios del dia
        regalia(decimal): regalia del dia
        queda(decimal): queda del dia
        participacion(decimal): participacion del dia
        saldo_bruto(decimal): saldo_bruto del dia
        saldo_comer(decimal): saldo_comer del dia
        saldo_oper(decimal): saldo_oper del dia

        depositos(decimal): depositos del dia
        pagos(decimal): pagos del dia
        ajustes(decimal): ajustes del dia
        cargo(decimal): cargos efectuados

        saldo_anterior(decimal): saldo anterio
        saldo_actual(decimal): saldo actual

        created_at y updated_at: registros de creacion y actualizacion.

    """
    dia = models.ForeignKey(
        'Dia'
    )
    comercializacion = models.ForeignKey(
        'admin_datamart.DimensionArcoComercializacion'
    )

    venta = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    premio = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )

    comision = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    regalia = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    queda = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    participacion = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )

    saldo_bruto = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    saldo_comer = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    saldo_oper = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )

    deposito = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    pago = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    ajuste = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    cargo = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )

    saldo_anterior = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
    )
    saldo_actual = models.DecimalField(
        null=True, max_digits=30, decimal_places=16, default=0
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
        verbose_name = ('Resumen administrativo')
        verbose_name_plural = ('Resumenes administrativos')

    def new_diccionario(self):
        self.dicc = {}

    def set_diccionario(self, key, value):
        self.dicc[key] = value

    def get_diccionario(self):
        return self.dicc

    def get_saldo_actual(self):
        if self.saldo_actual == 0:
            return self.saldo_anterior + self.saldo_oper + \
                self.deposito + self.pago + self.ajuste - self.cargo
        else:
            return self.saldo_actual

# =============================================================
# =============================================================
# ====================Modelos auditados========================


auditoria.register(
    Cuenta,
    Comercializadora,
    EstatoCuenta,
    DiaTrabajo,
    Movimiento
)
# =============================================================
# =============================================================
# =============================================================
