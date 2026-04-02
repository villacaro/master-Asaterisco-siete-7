# -*- coding: utf-8 -*-

from datetime import date, timedelta
from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME
from admin_historic import auditoria
from admin_lib.util_fechas import Funs, hora_23, hora_cero, strFecha
from admin_lib.util_models import ProtectDelete
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import AbstractBaseUser
from django.core.cache import cache
from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField

choices_frecuencia_monto_alquiler = [
    ['frecuencia_semanal', 'Alquiler semanal'],
    ['frecuencia_quincenal', 'Alquiler quincenal'],
    ['frecuencia_mensual', 'Alquiler mensual'],
]

choices_frecuencia_queda = [
    ['frecuencia_semanal', 'Queda semanal'],
    ['frecuencia_quincenal', 'Queda quincenal'],
    ['frecuencia_mensual', 'Queda mensual'],
]

choices_factor_riesgo = [
    [1, 'Activado'],
    [0, 'Desactivado'],
]

choices_cancel_ticket = [
    [0, 'No'],
    [1, 'Si'],
]


class AgenciaDataDefault(models.Model):

    """AgenciaDataDefault: Datos por defecto para las agencias.

    Campos definidos:
        montomin(decimal): nomto minito por ticket

        montomax(decimal): monto maximo por ticket

        montomax_ganancia(decimal): monto maximo de ganancia

        cantidad_apuesta_max(entero): numero maximo de apuestas por ticket

        cantidad_apuesta_min(entero): numero minimo de apuestas por ticket

        tiempoexpiracion(entero): tiempo de expiracion de los tickets en dias,
            ejemplo : 2 = 2 dias

        parley_machos_max(entero): numero maximo de machos por ticket
        parley_machos_min(entero): munero minimo de machos por ticket

        parley_hembras_max(entero): numero maximo de hembras por ticket
        parley_hembras_min(entero): munero minimo de hembras por ticket

        parley_empates_max(entero): numero maximo de empates por ticket

        parley_clonados_maxima_ganancia(decimal): maxima ganancia por agencia
            al dia de tickets clonados o repetidos

        everyone(booleano): bandera que indica si el registro esta activado
            para todos

        monto_alquiler(decimal): monto de alquiler

        frecuencia_monto_alquiler(string): codename de la frecuencia del modo
            alquiler, en caso de estar activo

        factor_riesgo(entero): entero que me indica que el factro de riesgo esta
            habilitado cuando es 1, en caso de ser 0 es desactivado

        frecuencia_queda(string): codename de la frecuencia del modelo de negocio
            queda

        created_at y updated_at: registros de creacion y actualizacion.
    """

    montomin = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto minimo (*)',
        help_text='Ingrese el monto minimo por ticket'
    )
    montomax = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto maximo (*)',
        help_text='Ingrese el monto maximo por ticket'
    )
    montomax_ganancia = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto maximo ganancia (*)',
        help_text='Ingrese el monto maximo de ganancia por ticket'
    )
    cantidad_apuesta_max = models.IntegerField(
        verbose_name='Cantidad maxima de apuesta (*)',
        help_text='Ingrese la cantidad maxima de apuestas por ticket'
    )
    cantidad_apuesta_min = models.IntegerField(
        verbose_name='Cantidad minima de apuesta (*)',
        help_text='Ingrese la cantidad minima de apuestas por ticket'
    )
    tiempoexpiracion = models.IntegerField(
        verbose_name='Tiempo de expiracion (*)',
        help_text='Ingrese el tiempo de expiracion de los tickets en dias, ejemplo: 2 = 2 dias'
    )
    parley_machos_max = models.IntegerField(
        verbose_name='Parley: cantidad maxima de machos (*)',
        help_text='Ingrese la cantidad maxima de machos por ticket'
    )
    parley_machos_min = models.IntegerField(
        verbose_name='Parley: cantidad minima de machos (*)',
        help_text='Ingrese la cantidad minima de machos por ticket'
    )
    parley_hembras_max = models.IntegerField(
        verbose_name='Parley: cantidad maxima de hembras (*)',
        help_text='Ingrese la cantidad maxima de hembras por ticket'
    )
    parley_hembras_min = models.IntegerField(
        verbose_name='Parley: cantidad minima de hembras (*)',
        help_text='Ingrese la cantidad minima de hembras por ticket'
    )
    parley_hembras_min = models.IntegerField(
        verbose_name='Parley: cantidad minima de hembras (*)',
        help_text='Ingrese la cantidad minima de hembras por ticket'
    )
    parley_empates_max = models.IntegerField(
        verbose_name='Parley: Cantidad mÃ¡xima de apuesta a empate por ticket',
        help_text='Parley: Indique la cantidad mÃ¡xima permitida de apuestas a empate en un ticket'
    )
    parley_clonados_maxima_ganancia = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Parley: cantidad maxima de ganancia para tickets clonados (*)',
        help_text='Ingrese la cantidad maxima de ganancia para tickets clonados'
    )
    monto_alquiler = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Monto de alquiler por taquilla(*)',
        help_text='Ingrese el monto por alquier de taquilla'
    )
    frecuencia_monto_alquiler = models.CharField(
        choices=choices_frecuencia_monto_alquiler,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Frecuencia de cobro de monto de alquiler (*)',
        help_text='Seleccione la frecuencia de cobro de monto de alquiler'
    )
    factor_riesgo = models.IntegerField(
        verbose_name='Factor de riesgo (*)',
        default=1,
        choices=choices_factor_riesgo,
        help_text='Seleccione una opcion de factor de riesgo',
    )
    frecuencia_queda = models.CharField(
        choices=choices_frecuencia_queda,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Frecuencia de corte de la queda (*)',
        help_text='Seleccione la frecuencia de corte para la queda'
    )
    ticket_titulo = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Ticket: Titulo del ticket (*)',
        help_text='Ingrese el titulo del ticket'
    )
    ticket_pie = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Ticket: Pie del ticket (*)',
        help_text='Ingrese el pie del ticket'
    )
    everyone = models.BooleanField(
        default=False,
        verbose_name='Â¿Para todos? ',
        help_text='En caso de estar activada esta opcion todas las agencias aplicaran esta '
                  'configuracion'
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
        verbose_name = ('Data por defecto de una agencias')
        verbose_name_plural = ('Data por defecto de las agencias')
        ordering = ['created_at', ]

    def __str__(self):
        return '{0}'.format(self.pk)

    def save(self, *args, **kwargs):
        super(AgenciaDataDefault, self).save(*args, **kwargs)
        self.cache_clear()

    def cache_clear(self):
        cache.delete('AgenciaDataDefault_everyone')

    @staticmethod
    def get_everyone():
        everyone = cache.get('AgenciaDataDefault_everyone')
        if everyone is None:
            try:
                everyone = AgenciaDataDefault.objects.get(
                    everyone=True
                )
            except AgenciaDataDefault.DoesNotExist:
                everyone = False
            cache.set(
                'AgenciaDataDefault_everyone',
                everyone,
                CACHES_CONF_TIME['registros_db']['everyone']
            )
        return everyone


class TaquillaDataDefault(models.Model):

    """TaquillaDataDefault: Datos por defecto para las taquillas.

    Campos definidos:

        user_name(string): prefijo de usuario por defecto para las taquillas

        passwd(string): passwd en texto plano por defecto para las taquillas

        created_at y updated_at: registros de creacion y actualizacion.
    """
    user_name = models.CharField(
        max_length=160,
        verbose_name='Prefijo de usuario (*)',
        help_text='Ingrese el prefijo de usuarios por defecto para las taquillas'
    )
    passwd = models.CharField(
        max_length=160,
        verbose_name='ContraseÃ±a (*)',
        help_text='Ingrese la contraseÃ±a por defecto para las taquillas'
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
        verbose_name = ('Data por defecto de una taquilla')
        verbose_name_plural = ('Data por defecto de las taquillas')
        ordering = ['user_name', ]

    def __str__(self):
        return '{0}'.format(self.pk)


class TicketsDataDefault(models.Model):

    """TicketsDataDefault: Datos por defecto para los tickets.

    Campos definidos:

        titulo1(string): primer titulo de pagina para la impresion de los tickets

        titulo2(string): segundo titulo de pagina para la impresion de los tickets

        titulo3(string): tercer titulo de pagina para la impresion de los tickets

        pie1(string): primer pie de pagina para la impresion de los tickets

        pie2(string): segundo pie de pagina para la impresion de los tickets

        pie3(string): tercer pie de pagina para la impresion de los tickets

        passwd(string): passwd en texto plano por defecto para las taquillas

        everyone(booleano): bandera que indica si el registro esta activado
            para todos

        created_at y updated_at: registros de creacion y actualizacion.
    """
    titulo1 = models.CharField(
        max_length=160,
        verbose_name='Primer titulo de pagina (*)',
        help_text='Ingrese el primer titulo de pagina para impresion de tickets'
    )
    titulo2 = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Segundo titulo de pagina ',
        help_text='Ingrese el segundo titulo de pagina para impresion de tickets'
    )
    titulo3 = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Tercer titulo de pagina ',
        help_text='Ingrese el tercer titulo de pagina para impresion de tickets'
    )
    pie1 = models.CharField(
        max_length=160,
        verbose_name='Primer pie de pagina (*)',
        help_text='Ingrese el primer pie de pagina para impresion de tickets'
    )
    pie2 = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Segundo pie de pagina ',
        help_text='Ingrese el segundo pie de pagina para impresion de tickets'
    )
    pie3 = models.CharField(
        max_length=160,
        null=True,
        blank=True,
        verbose_name='Tercer pie de pagina ',
        help_text='Ingrese el tercer pie de pagina para impresion de tickets'
    )
    everyone = models.BooleanField(
        default=False,
        verbose_name='Â¿Para todos? (*)',
        help_text='En caso de estar activada esta opcion todas los tickets se'
                  ' imprimiran con esta configuracion'
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
        verbose_name = ('Data por defecto de impresion')
        verbose_name_plural = ('Data por defecto para la impresion')
        ordering = ['titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3']

    def __str__(self):
        return '{0}'.format(self.pk)

    def save(self, *args, **kwargs):
        super(TicketsDataDefault, self).save(*args, **kwargs)
        self.cache_clear()

    def cache_clear(self):
        cache.delete('TicketsDataDefault_everyone_obj')
        cache.delete('TicketsDataDefault_everyone_json')

    @staticmethod
    def get_everyone():
        everyone = cache.get('TicketsDataDefault_everyone_obj')
        if not everyone:
            try:
                everyone = TicketsDataDefault.objects.get(
                    everyone=True
                )
            except TicketsDataDefault.DoesNotExist:
                everyone = None
            cache.set(
                'TicketsDataDefault_everyone_obj',
                everyone,
                CACHES_CONF_TIME['registros_db']['everyone']
            )
        return everyone

    @staticmethod
    def get_everyone_json(agencia):
        try:
            everyone = TicketsDataDefault.objects.get(
                everyone=True
            )
            json = {
                "footer": {
                    "foot1": agencia.get_preference_value_by_codename('preference_foot')
                    if agencia.get_preference_value_by_codename('preference_foot')
                    else everyone.pie1,
                    "foot2": everyone.pie2,
                    "foot3": everyone.pie3,
                },
                "heads": {
                    "head1": '',
                    "head2": agencia.get_preference_value_by_codename('preference_title')
                    if agencia.get_preference_value_by_codename('preference_title')
                    else everyone.titulo2,
                    "head3": everyone.titulo3
                }
            }
        except TicketsDataDefault.DoesNotExist:
            json = {
                "footer": {
                    "foot1": agencia.get_preference_value_by_codename('preference_foot')
                    if agencia.get_preference_value_by_codename('preference_foot')
                    else '',
                    "foot2": '',
                    "foot3": '',
                },
                "heads": {
                    "head1": '',
                    "head2": agencia.get_preference_value_by_codename('preference_title')
                    if agencia.get_preference_value_by_codename('preference_title')
                    else '',
                    "head3": '',
                }
            }
        return json


class DataDefault(models.Model):

    """DataDefault: Datos por defecto para la cadena.

    Campos definidos:

        user_type(foreing): tipo de cadena al que hace referencia la data

        cupo(decimal): cupo de venta diario por comercializadora

        porcentaje_comision(decimal): porcentaje de la comision

        porcentaje_regalia(decimal): porcentaje de regalia

        porcentaje_participacion(decimal): porcentaje de parcicipacion

        porcentaje_queda(decimal): porcentaje de queda

        porcentaje_maximo(decimal): porcentaje maximo

        monto_alquiler(decimal): monto de alquiler por taquilla

        frecuencia_monto_alquiler(string): codename de la frecuencia del modo
            alquiler, en cado de estar activo

        factor_riesgo(entero): entero que me indica que el factro de riesgo esta
            habilitado cuando es 1, en caso de ser 0 es desactivado

        frecuencia_queda(string): codename de la frecuencia del modelo de negocio
            quedalquiler, en cado de estar activo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    user_type = models.ForeignKey(
        'admin_permisologia.Permissions',  # Perfil/tipo de cadena (Permissions es el equivalente de Profile)
        on_delete=models.CASCADE,
    )
    cupo = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        verbose_name='Cupo de venta (*)',
        help_text='Ingrese el cupo maximo de venta diaria por tipo comercializadora'
    )
    porcentaje_comision = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Porcentaje de comision (*)',
        help_text='Ingrese el porcentaje de comision por tipo de comercializadora'
    )
    porcentaje_regalia = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Porcentaje de servicios (*)',
        help_text='Ingrese el porcentaje de servicios por tipo de comercializadora'
    )
    porcentaje_participacion = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Porcentaje de participacion (*)',
        help_text='Ingrese el porcentaje de participacion por tipo de comercializadora'
    )
    porcentaje_queda = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Porcentaje de queda (*)',
        help_text='Ingrese el porcentaje de queda por tipo de comercializadora'
    )
    porcentaje_maximo = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Porcentaje de maximo (*)',
        help_text='Ingrese el porcentaje de maximo por tipo de comercializadora'
    )
    monto_alquiler = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Monto de alquiler por taquilla(*)',
        help_text='Ingrese el monto por alquier de taquilla'
    )
    frecuencia_monto_alquiler = models.CharField(
        choices=choices_frecuencia_monto_alquiler,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Frecuencia de cobro de monto de alquiler (*)',
        help_text='Seleccione la frecuencia de cobro de monto de alquiler'
    )
    factor_riesgo = models.IntegerField(
        verbose_name='Factor de riesgo (*)',
        default=1,
        choices=choices_factor_riesgo,
        help_text='Seleccione una opcion de factor de riesgo',
    )
    frecuencia_queda = models.CharField(
        choices=choices_frecuencia_queda,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Frecuencia de corte de la queda (*)',
        help_text='Seleccione la frecuencia de corte para la queda'
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
        verbose_name = ('Data por defecto por comercializadora')
        verbose_name_plural = ('Data por defecto para las comercializadoras')
        ordering = ['user_type', ]

    def __str__(self):
        return '{0}'.format(self.pk)


class TipoPorcentajes(models.Model):

    """TipoPorcentajes: Tipos de porcentajes.

    Campos definidos:

        nombre(string): nombre del tipo porcentaje

        codename(string): texto en codigo del tipo de porcentaje

        orden(entero): orden del tipo de porcentaje

        bloque(booleano): indica si el porcentaje es por bloque

        banca(booleano): indica si el porcentaje es por banca

        distribuidor(booleano): indica si el porcentaje es por distribuidor

        agencia(booleano): indica si el porcentaje es por agencia

        taquilla(booleano): indica si el porcentaje es por taquilla

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre (*)',
        help_text='Ingrese el nombre del tipo de porcentaje'
    )
    codename = models.CharField(
        max_length=100,
        verbose_name='Codename (*)',
        help_text='Ingrese el codename del tipo de porcentaje'
    )
    orden = models.IntegerField(
        default=0,
        verbose_name='Orden (*)',
        help_text='Ingrese el orden del tipo de porcentaje'
    )
    bloque = models.BooleanField(
        default=False,
        verbose_name='Â¿Tipo de porcentaje por bloque? ',
        help_text='Seleccione solo en caso de que el porcentaje sea por bloque'
    )
    banca = models.BooleanField(
        default=False,
        verbose_name='Â¿Tipo de porcentaje por banca? ',
        help_text='Seleccione solo en caso de que el porcentaje sea por banca'
    )
    distribuidor = models.BooleanField(
        default=False,
        verbose_name='Â¿Tipo de porcentaje por distribuidor? ',
        help_text='Seleccione solo en caso de que el porcentaje sea por distribuidor'
    )
    agencia = models.BooleanField(
        default=False,
        verbose_name='Â¿Tipo de porcentaje por agencia? ',
        help_text='Seleccione solo en caso de que el porcentaje sea por agencia'
    )
    taquilla = models.BooleanField(
        default=False,
        verbose_name='Â¿Tipo de porcentaje por taquilla? ',
        help_text='Seleccione solo en caso de que el porcentaje sea por taquilla'
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
        verbose_name = ('Tipo de porcentaje')
        verbose_name_plural = ('Tipos de porcentajes')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}'.format(self.nombre)


class BaseModelCadena(ProtectDelete, models.Model):
    """BaseModelCadena: datos basicos de modelo para la cadena de comercializacion

    Hereda de proteccion contra eliminacion

    Campos definidos:

        nombre(string): nombre de la cadena

        resumen_automatic(booleano): indica si el resumen administrativo
            se gestionan de forma automÃ¡tica.

        telefono(string): telefono de la cadena

        rif(string): rif de la cadena

        email(email): correo de la cadena

        direccion(foreing): direccion de la cadena

        status(foreing): estatus de la cadena

        created_at y updated_at: registros de creacion y actualizacion.
    """

    nombre = models.CharField(
        max_length=100,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre',
    )
    resumen_automatic = models.BooleanField(
        default=False,
        verbose_name='Cierre administrativo AutomÃ¡tico',
        help_text='Seleccione este campo solo si desea que el resumen administrativo se'
                  ' gestione de forma automÃ¡tica, importacion de saldos y cierre de dias.'
    )
    telefono = models.CharField(
        max_length=12,
        verbose_name='NÃºmero TelefÃ³nico ',
        help_text='Ingrese el nÃºmero telefÃ³nico',
        null=True,
        blank=True
    )
    rif = models.CharField(
        max_length=15,
        verbose_name='Rif ',
        help_text='Ingrese el rif',
        null=True,
        blank=True
    )
    email = models.EmailField(
        max_length=254,
        # unique=True,
        # se quita el unique, ya que un banquero puede tener n agencias con un
        # mismo correo
        null=True,
        blank=True,
        verbose_name='Correo electrÃ³nico ',
        help_text='Ingrese el correo electrÃ³nico'
    )
    direccion = models.ForeignKey(
        'admin_profiles.Direcciones',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.PositiveIntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('updated_at', 'pk_clone')

    class Meta:
        abstract = True
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}'.format(self.nombre)

    def save(self, *args, **kwargs):
        if not self.nombre.isupper() and self.nombre.find('_delete_') < 0:
            self.nombre = self.nombre.upper()
        super(BaseModelCadena, self).save(*args, **kwargs)

        self.cache_clear()

    def get_cupo(self):
        """
        Devuelve el cupo activo del objeto actual
        """
        if not self.cupos_set.filter(fecha_fin=None).exists():
            self.create_data_global()

        cupos = self.cupos_set.filter(fecha_fin=None)
        if cupos.count() == 1:
            return cupos[0]
        else:
            cupos = cupos.order_by('-updated_at')
            cupo = cupos[0]
            for obj in cupos[1:]:
                obj.fecha_fin = now()
                obj.save(update_fields=['fecha_fin'])
            return cupo

    def get_queryset_porcentajes(self):
        """
        Retorna todos los porcentajes
        """
        return self.porcentajes_set.filter(
            fecha_fin=None
        ).order_by('tipo__orden').select_related('tipo')

    def get_queryset_preferencias(self):
        """
        Retorna todas las preferencias
        """
        from admin_comercializacion.views.preferencias_views import validate_model_bussiness
        preferencias = []
        preferences = TypePreferences.objects.all().order_by('group__order', 'order')
        preferences = validate_model_bussiness(self, preferences)

        for preference in preferences:
            preferencia = {}
            preferencia['nombre'] = preference.name
            preferencia['valor'] = self.get_preference_value_by_codename(preference.codename)
            preferencias.append(preferencia)

        return preferencias

    def get_queryset_preferencias_serialize(self):
        """
        Retorna todas las preferencias
        """
        from admin_comercializacion.views.preferencias_views import validate_model_bussiness
        preferencias = []
        preferences = TypePreferences.objects.filter(
            profile__codename=self.user_type_codename)
        preferences = validate_model_bussiness(self, preferences)

        for preference in preferences:
            preferencia = {}
            preferencia['codename'] = preference.codename
            array = self.get_preference_by_codename(preference.codename)
            preferencia['value'] = array[0]
            preferencia['distribute'] = array[1]
            preferencias.append(preferencia)

        return preferencias

    def create_data_global(self):
        """
        Crea la data global necesaria de cada cadena
        """
        try:
            # ===========================================#
            # Buscando data global
            # ===========================================#

            data_detault = DataDefault.objects.get(
                user_type__codename=self.user_type_codename
            )

            # ===========================================#
            # Asignando cupos
            # ===========================================#
            kwargs = {}
            kwargs[self.user_type_codename.split('_')[1]] = self
            kwargs['fecha_fin'] = None
            if Cupos.objects.filter(
                **kwargs
            ).count() != 1:

                Cupos.objects.filter(**kwargs).update(fecha_fin=now())
                del kwargs['fecha_fin']

                kwargs['monto_diario'] = data_detault.cupo
                kwargs['fecha_inicio'] = now()
                Cupos.objects.create(
                    **kwargs
                )

            # ===========================================#
            # Asignando porcentajes
            # ===========================================#
            kwargs = {}
            prefix_poc = self.user_type_codename.split('_')[1]
            kwargs[prefix_poc] = self
            kwargs['fecha_fin'] = None
            if (
                    Porcentajes.objects.filter(**kwargs).count() !=
                    TipoPorcentajes.objects.all().count()):
                tipos = TipoPorcentajes.objects.all()
                for t in tipos:
                    kwargs = {}
                    kwargs[prefix_poc] = self
                    kwargs['fecha_fin'] = None
                    kwargs['tipo__codename'] = t.codename
                    if Porcentajes.objects.filter(**kwargs).count() == 1:
                        continue
                    else:
                        Porcentajes.objects.filter(**kwargs).update(
                            fecha_fin=now()
                        )
                        del kwargs['tipo__codename']
                        del kwargs['fecha_fin']

                    if t.codename == 'porcentaje_regalia':
                        porcentaje = data_detault.porcentaje_regalia
                    elif t.codename == 'porcentaje_comision':
                        porcentaje = data_detault.porcentaje_comision
                    elif t.codename == 'porcentaje_participacion':
                        porcentaje = data_detault.porcentaje_participacion
                    elif t.codename == 'porcentaje_queda':
                        porcentaje = data_detault.porcentaje_queda

                    maximo = data_detault.porcentaje_maximo

                    kwargs['porcentaje_ganancia'] = porcentaje
                    kwargs['porcentaje_maximo'] = maximo
                    kwargs['fecha_inicio'] = now()
                    kwargs['tipo'] = t

                    porcentaje = Porcentajes(
                        **kwargs
                    )
                    porcentaje.audit_save = False
                    porcentaje.save()

                    if self.prefix_filter not in [
                            'operadora', 'bloque', 'taquilla']:

                        origen = self.get_origen()
                        kwargs_origen = {}
                        kwargs_origen[origen.prefix_filter] = origen
                        kwargs_origen['tipo'] = t
                        kwargs_origen['fecha_fin'] = None

                        if Porcentajes.objects.filter(
                                **kwargs_origen).exists():
                            origen_porcentaje = Porcentajes.objects.get(
                                **kwargs_origen
                            )

                            porcentaje.porcentaje_maximo = origen_porcentaje.porcentaje_maximo

                            if self.prefix_filter == 'agencia':
                                porcentaje.distribuidor_porc = origen_porcentaje \
                                    .porcentaje_ganancia
                                porcentaje.banca_porc = origen_porcentaje.banca_porc
                                porcentaje.bloque_porc = origen_porcentaje.bloque_porc
                            elif self.prefix_filter == 'distribuidor':
                                porcentaje.banca_porc = origen_porcentaje.porcentaje_ganancia
                                porcentaje.bloque_porc = origen_porcentaje.bloque_porc
                            elif self.prefix_filter == 'banca':
                                porcentaje.bloque_porc = origen_porcentaje.porcentaje_ganancia

                            porcentaje.save()

        except DataDefault.DoesNotExist:
            pass

        # ===========================================#
        # Verificando preferencias distribuidas
        # ===========================================#
        if self.prefix_filter == 'agencia':
            preferences = Preferences.objects.filter(
                comercializacion_id=self.distribuidores.get_comercializadora().id,
                distribute=True
            )
            if preferences:
                childs = self.distribuidores.get_comercializadora().get_offspring()
                for preference in preferences:
                    if preference.value:
                        rate = Decimal(round(float(preference.value) / len(childs), 2))
                        for child in childs:
                            child.create_or_update_preference(
                                preference.typepreference,
                                rate,
                                True
                            )
        # ===========================================#
        # Asignando datos de finanzas
        # ===========================================#
        from admin_finanzas.models import Cuenta, Dia
        from admin_finanzas.models import Banco, TipoCuenta

        # Creacion de la comercializadora
        self.create_comercializadora_and_dimension()
        comercializadora = self.get_comercializadora()

        # Creacion del dia
        dia = Dia.objects.get_or_create(fecha=self.created_at.date())[0]
        dia_trabajo = comercializadora.get_or_create_dia_trabajo()

        if dia_trabajo:
            if comercializadora.saldo_fecha is None:
                comercializadora.saldo_inicial = 0
                comercializadora.saldo_fecha = dia.fecha
                comercializadora.audit_save = False
                comercializadora.save(
                    update_fields=['saldo_inicial', 'saldo_fecha']
                )
                comercializadora.set_saldo_inicial()
        try:
            """
            # Agregando al usuario la comercializadora
            # que acaba de crear
            """
            from crequest.middleware import CrequestMiddleware
            request = CrequestMiddleware.get_request()
            if request:
                from admin_principal.security import Security
                security = Security()
                try:
                    user = security.get_user(request)
                    user.audit_save = False
                    user.comercializadora.add(comercializadora)
                    user.cache_clear()
                except Exception:
                    pass
        except Exception:
            pass

        # Creacion de la cuenta efectivo
        banco = Banco.objects.get_or_create(
            nombre='Efectivo'
        )[0]

        tipocuenta = TipoCuenta.objects.get_or_create(
            nombre='Cuenta Efectivo',
            codigo='C.E'
        )[0]

        Cuenta.objects.update_or_create(
            comercializadora=comercializadora,
            banco=banco,
            tipocuenta=tipocuenta,
            numero='0000',
            defaults={
                'description': 'Efectivo',
            }
        )

        # ===========================================#
        # Creacion de factor de riesgo
        # ===========================================#
        if self.prefix_filter == 'bloque':
            if not FactorRiesgo.objects.filter(comercializadora=comercializadora).exists():
                factor = FactorRiesgo(
                    comercializadora=comercializadora,
                    factores=[]
                )
                factor.audit_save = False
                factor.save()


class BaseGenericProcessManager(models.Manager):

    def get_queryset(self):
        try:
            return super(BaseGenericProcessManager, self).get_queryset().exclude(
                status__codename='status_eliminado'
            )
        except Exception:
            try:
                return super(BaseGenericProcessManager, self).get_queryset().exclude(
                    usuariostaquilla__status__codename='status_eliminado'
                )
            except Exception:
                return super(BaseGenericProcessManager, self).get_queryset()

    def get(self, *args, **kwargs):
        if len(kwargs) == 1 and kwargs.get('pk'):
            cadena = cache.get(
                '{0}_{1}'.format(self.model.prefix_filter, kwargs.get('pk'))
            )
            if not cadena:
                cadena = super(
                    BaseGenericProcessManager, self).get(
                    *args, **kwargs)
                cache.set(
                    '{0}_{1}'.format(
                        self.model.prefix_filter, kwargs.get('pk')),
                    cadena,
                    CACHES_CONF_TIME['registros_db']['comercializacion'],
                )
            return cadena
        else:
            return super(BaseGenericProcessManager, self).get(*args, **kwargs)


PK_STATUS_ELIMINADO = None


class BaseGenericProcess(models.Model):
    """BaseGenericProcess: Base generica de procesos

    Definida para escribir funciones base que pueden ser implementadas en un principio
        por sus clase hijas

    """

    class Meta:
        abstract = True

    objects = BaseGenericProcessManager()

    def __str__(self):
        # Este metodo se sobreescribe en agencia en taquilla
        nombre = self.nombre
        if not self.activo():
            nombre = nombre.split('_delete_')
            return '<span id="{1}" class="cadena-delete no-pd">{0}</span>'.format(
                nombre[0],
                self.prefix_filter + '_' + str(self.pk)
            )
        else:
            return '{0}'.format(nombre)

    def save(self, *args, **kwargs):
        super(BaseGenericProcess, self).save(*args, **kwargs)
        self.cache_clear()

    def activo(self):
        global PK_STATUS_ELIMINADO
        if not PK_STATUS_ELIMINADO:
            from admin_status.models import Status
            PK_STATUS_ELIMINADO = Status.get_status_by_codename(
                codename='status_eliminado'
            ).pk
        return self.status_id != PK_STATUS_ELIMINADO

    def cache_clear(self):
        key_cache = '{0}_{1}'.format(
            self.prefix_filter,
            self.pk
        )
        cache.delete('{0}'.format(key_cache))
        cache.delete('status_comer_{0}'.format(key_cache))
        cache.delete('comer_{0}'.format(key_cache))
        cache.delete('cadena_{0}'.format(key_cache))
        self.get_comercializadora().cache_clear()

    def get_kwargs_by_taquillasessions(self):
        """
        Este metodo debe implementarse en las clases hijas,
        devuelve un kwargs para usar en filtros desde la tabla
        taquillasessions
        """
        raise NotImplementedError()

    def get_querryset_taquillasessions(self):
        kwargs = self.get_kwargs_by_taquillasessions()
        kwargs['updated_at__gte'] = now() - timedelta(minutes=5)
        from admin_historic.models import TaquillaSessionsDetail
        return TaquillaSessionsDetail.objects.only('pk').filter(**kwargs)

    def get_querryset_taquilla_connections(self):
        kwargs = {}
        kwargs['connection_at__gte'] = now() - timedelta(minutes=5)

        if self.prefix_filter != 'master':
            kwargs[self.prefix_filter + '_id'] = self.pk
        from admin_historic.models import HechoConnectionsComer
        return HechoConnectionsComer.objects.filter(
            **kwargs
        )

    def get_distribuidores_count(self):
        kwargs = {}
        count = 0
        if self.prefix_filter != 'distribuidor' and self.prefix_filter != 'agencia':
            kwargs['{}_id'.format(self.prefix_filter)] = self.pk
            from admin_datamart.models import DimensionComercializacion
            count = DimensionComercializacion.objects.filter(
                **kwargs
            ).distinct(
                'distribuidor_id'
            ).count()
        return count

    def get_agencias_conectadas(self):
        """
        Retorna el numero de agencias de un querryset ya filtrado
        """
        return self.get_querryset_taquilla_connections().distinct(
            'agencia_id'
        ).count()

    def get_taquillas_conectadas(self):
        """
        Retorna el numero de taquillas de un querryset ya filtrado
        """
        return self.get_querryset_taquilla_connections().count()

    def get_class_name(self):
        return str(self.__class__.__name__).lower()

    def get_verbose_name(self):
        return self._meta.verbose_name

    def get_verbose_name_plural(self):
        return self._meta.verbose_name_plural

    # get_absolute_url compatible con Django 3.1+ (sin @models.permalink)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        url_name = 'admin_comercializacion_{0}_detail'.format(self.get_class_name())
        try:
            return reverse(url_name, kwargs={'pk': self.pk})
        except NoReverseMatch:
            # Fallback al admin de Django si la URL de detalle no existe
            app  = self._meta.app_label
            name = self._meta.model_name
            try:
                return reverse('admin:{0}_{1}_change'.format(app, name), args=[self.pk])
            except NoReverseMatch:
                return '/admin/'

    def create_comercializadora_and_dimension(self):
        from admin_finanzas.models import Comercializadora
        kwargs = {}

        kwargs[self.prefix_filter] = self

        comer, create = Comercializadora.objects.get_or_create(
            **kwargs
        )
        if create:
            comer.saldo_inicial = None
            comer.saldo_fecha = None
            comer.audit_save = False
            comer.save(update_fields=['saldo_inicial', 'saldo_fecha'])

        from admin_datamart.models import DimensionArcoComercializacion
        kwargs = {}
        kwargs[self.prefix_filter + '_id'] = self.pk
        if self.prefix_filter == 'operadora':
            kwargs['bloque_id'] = None

        else:
            origen = self.get_origen()
            kwargs[origen.prefix_filter + '_id'] = origen.pk

        DimensionArcoComercializacion.objects.get_or_create(
            **kwargs
        )

    def get_comercializadora(self):
        comercializadora = cache.get(
            'comer_{0}_{1}'.format(
                self.prefix_filter, self.pk))
        if not comercializadora:
            from admin_finanzas.models import Comercializadora
            kwargs = {}
            kwargs[self.prefix_filter] = self
            comercializadora = Comercializadora.objects.get_or_create(
                **kwargs
            )[0]
            cache.set(
                'comer_{0}_{1}'.format(self.prefix_filter, self.pk),
                comercializadora,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )

        return comercializadora

    def get_dimension_arco_comercializadora(self):
        dimensionarcocomercializadora = cache.get(
            'comer_arco_dime_{0}_{1}'.format(self.prefix_filter, self.pk)
        )

        if not dimensionarcocomercializadora:
            from admin_datamart.models import DimensionArcoComercializacion
            kwargs = {}
            kwargs[self.prefix_filter + '_id'] = self.pk
            if self.prefix_filter == 'operadora':
                # los porcentajes hacia operadora nunca se
                # calcular
                # por lo tanto todo lo de la operadora es su hijo
                kwargs['bloque_id__isnull'] = True
            else:
                origen = self.get_origen()
                kwargs[origen.prefix_filter + '_id'] = origen.pk
            dimensionarcocomercializadora = DimensionArcoComercializacion.objects.get_or_create(
                **kwargs
            )[0]
            # Es una dimension, nunca se invalida
            cache.set(
                'comer_arco_dime_{0}_{1}'.format(self.prefix_filter, self.pk),
                dimensionarcocomercializadora,
                0
            )

        return dimensionarcocomercializadora

    def get_kwargs_dimension_arco_comercializadora(self):
        kwargs = {}
        kwargs['comercializacion__' + self.prefix_filter + '_id'] = self.pk
        if self.prefix_filter == 'operadora':
            # los porcentajes hacia operadora nunca se
            # calcular
            # por lo tanto todo lo de la operadora es su hijo
            kwargs['comercializacion__bloque_id__isnull'] = False
        else:
            origen = self.get_origen()
            kwargs[
                'comercializacion__' +
                origen.prefix_filter +
                '_id'] = origen.pk

        return kwargs

    def get_kwargs_hijos_dimension_arco_comercializadora(self):
        kwargs = {}
        kwargs['comercializacion__' + self.prefix_filter + '_id'] = self.pk
        if self.status.codename != 'status_eliminado':
            if not self.get_offspring().exists():
                if self.prefix_filter == 'operadora':
                    kwargs['comercializacion__bloque_id'] = None
                else:
                    origen = self.get_origen()
                    kwargs[
                        'comercializacion__' +
                        origen.prefix_filter +
                        '_id'] = origen.pk
            else:
                kwargs[
                    'comercializacion__' +
                    self.get_offspring()[0].prefix_filter + '_id__isnull'
                ] = False
        else:
            kwargs[
                'comercializacion__' + self.get_comercializadora().get_offspring_level1(
                    exclude_delete=False
                )[0].get_object().prefix_filter + '_id__isnull'
            ] = False
        return kwargs

    def get_kwargs_hijos_agencia_dimension_arco_comercializadora(self):
        kwargs = {}
        kwargs['comercializacion__agencia_id__isnull'] = False
        kwargs['comercializacion__distribuidor_id__in'] = []
        if self.prefix_filter in ['operadora', 'bloque', 'banca']:
            kwargs['comercializacion__distribuidor_id__in'] = list(self.get_distribuidores_filter()
                                                                   .values_list('pk', flat=True))
        elif self.prefix_filter == 'distribuidor':
            kwargs['comercializacion__distribuidor_id__in'].append(self.pk)
        elif self.prefix_filter == 'agencia':
            origen = self.get_origen()
            kwargs[
                'comercializacion__' +
                origen.prefix_filter +
                '_id'] = origen.pk
            kwargs['comercializacion__agencia_id'] = self.pk
            kwargs.pop('comercializacion__distribuidor_id__in')
            kwargs.pop('comercializacion__agencia_id__isnull')
        return kwargs

    def get_kwargs_dimension_comercializadora(self):
        kwargs = {}
        kwargs['comercializacion__' + self.prefix_filter + '_id'] = self.pk
        return kwargs

    def get_prefix_kwargs_by_level_taquilla(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '__agencia' + self.get_prefix_kwargs_by_level_agencia()

    def get_prefix_kwargs_by_level_tickets(self):
        """
        Retorna un prefix, para hacer un queryset desde cualquier nivel de la cadena a tickes
        """
        return 'user__taquilla' + self.get_prefix_kwargs_by_level_taquilla()

    def get_type(self):
        from admin_users.models import UserProfile
        return UserProfile.get_profile_by_codename(
            codename=self.user_type_codename)

    def get_frecuencia_queda(self):
        """
        Obtiene el tipo de frecuencia relacionada a la comercializadora
        de la instanca actual
        """
        return self.get_preference_value_by_codename('preference_queda_frequency')

    def get_frecuencia_queda_display(self):
        """
        Obtiene el tipo de frecuencia relacionada a la comercializadora
        de ls instanca actual
        """
        frecuencia_queda = self.get_frecuencia_queda()
        for display in choices_frecuencia_queda:
            if frecuencia_queda == display[0]:
                return display[1]
        return ''

    def get_is_apply_porcentaje(self, codename):
        """
        Retorna un True en caso de que apliquen porcentajes del codename recibido,
        en caso contrario retorna False
        """
        kwargs_porcentaje = {
            'tipo__codename': codename,
            'fecha_fin': None,
        }
        kwargs_porcentaje[self.prefix_filter] = self
        porcentaje = Porcentajes.objects.filter(
            **kwargs_porcentaje
        )

        if porcentaje.exists():
            if porcentaje[0].porcentaje_ganancia <= 0:
                return False
            else:
                return True
        return False

    def get_is_apply_queda(self):
        if self.nivel == 1:
            return True
        else:
            return self.get_is_apply_porcentaje(
                'porcentaje_queda'
            )

    def get_is_apply_participacion(self):
        if self.nivel == 1:
            return True
        else:
            return self.get_is_apply_porcentaje(
                'porcentaje_participacion'
            )

    def get_is_apply_regalia(self):
        if self.nivel == 1:
            return True
        else:
            return self.get_is_apply_porcentaje(
                'porcentaje_regalia'
            )

    def get_is_apply_comision(self):
        if self.nivel == 1:
            return True
        else:
            return self.get_is_apply_porcentaje(
                'porcentaje_comision'
            )

    def get_day_queda_is_corte_previous(self, fecha=None, frecuencia=None):
        """
        Calcula la ultima fecha de corte
        """
        if not fecha:
            fecha = now()

        if not frecuencia:
            frecuencia = self.get_frecuencia_queda()

        if frecuencia == 'frecuencia_semanal':
            if fecha.weekday() == 0:
                # Es dia lunes
                return fecha
            else:
                return fecha - timedelta(days=fecha.weekday())

        elif frecuencia == 'frecuencia_quincenal':
            if fecha.day == 1:
                # primero del mes
                return fecha
            elif fecha.day == 16:
                # 16 del mes
                return fecha
            elif fecha.day < 16:
                # estoy en la primera quincena
                return fecha - timedelta(days=fecha.day - 1)
            elif fecha.day > 16:
                # estoy en la segunda quincena
                return fecha - timedelta(days=(fecha.day - 16))

        elif frecuencia == 'frecuencia_mensual':
            if fecha.day == 1:
                # primero del mes
                return fecha
            else:
                return fecha - timedelta(days=fecha.day - 1)

    def get_day_queda_is_corte_next(self, fecha=None, frecuencia=None):
        """
        Calcula la proxima fecha de corte
        """
        if not fecha:
            fecha = now()

        if not frecuencia:
            frecuencia = self.get_frecuencia_queda()

        if frecuencia == 'frecuencia_semanal':
            if fecha.weekday() == 0:
                # Es dia lunes
                return fecha + timedelta(days=7)
            else:
                return fecha + timedelta(days=7 - fecha.weekday())

        elif frecuencia == 'frecuencia_quincenal':
            if fecha.day == 1:
                # primero del mes
                return fecha + timedelta(days=15)
            elif fecha.day == 16:
                # 16 del mes
                return (fecha - timedelta(days=15)) + relativedelta(months=1)
            elif fecha.day < 16:
                # estoy en la primera quincena
                return (fecha - timedelta(days=fecha.day - 1)) + \
                    timedelta(days=15)
            elif fecha.day > 16:
                # estoy en la segunda quincena
                return (fecha - timedelta(days=fecha.day - 1)) + \
                    relativedelta(months=1)

        elif frecuencia == 'frecuencia_mensual':
            if fecha.day == 1:
                # primero del mes
                return fecha + relativedelta(months=1)
            else:
                return (fecha - timedelta(days=fecha.day - 1)) + \
                    relativedelta(months=1)

    def get_frecuencia_queda_is_range_corte(self, fecha):
        """
        En caso de ser dia de corte para la comercializadora actual,
        retorna un true, en caso contrario, retorna false,
        en ambos casos retorna un dict con el rango de fecha habilitado
        desde la fecha actual
        """
        ini_queda = self.get_day_queda_is_corte_previous(fecha)
        fin_queda = self.get_day_queda_is_corte_next(fecha) - timedelta(days=1)
        return ini_queda, fin_queda

    def get_frecuencia_queda_is_corte_day_early(self, fecha):
        """
        Eso me permite ver el dia de corte por anticipado, util para el reporte de la queda
        cuando se quiere mostrar el corte semanal el dia domingo por ejemplo
        """
        return self.get_frecuencia_queda_is_corte_day(
            fecha + timedelta(days=1)
        )

    def get_frecuencia_queda_is_corte_day(self, fecha):
        """
        En caso de ser dia de corte para la comercializadora actual,
        retorna un true, en caso contrario, retorna false,
        en ambos casos retorna un dict con el rango de fecha habilitado
        desde la fecha actual
        """
        frecuencia = self.get_frecuencia_queda()
        band = False
        if frecuencia == 'frecuencia_semanal':
            if fecha.weekday() == 0:
                # Es dia lunes, osea corte de la semana
                band = True
        elif frecuencia == 'frecuencia_quincenal':
            if fecha.day == 1:
                band = True
            elif fecha.day == 16:
                band = True
        elif frecuencia == 'frecuencia_mensual':
            if fecha.day == 1:
                # primer dia del mes
                band = True
        return band

    def get_queda_by_range(self, init_date, final_date):
        """
        Retorna un booleano de acuerdo a un rango de fechas, si este rango coindice
        con la frecuencia retorna 'True', de lo contrario retorna 'False'
        """
        show_queda = False
        ini = strFecha(init_date)
        if self.prefix_filter != 'operadora':
            # Contamos los dÃ­as
            dias = (final_date - init_date).days
            frecuencia = self.get_frecuencia_queda()
            show_queda = False
            if frecuencia == 'frecuencia_semanal':
                if dias == 6:
                    week = list(Funs.get_week_by_date(init_date))
                    if init_date == week[0]:
                        show_queda = True
            elif frecuencia == 'frecuencia_quincenal':
                if dias == 14:
                    quincena = list(Funs.get_quincena_by_date(final_date))
                    if str(ini.getFecha()) == str(quincena[0]):
                        show_queda = True
            elif frecuencia == 'frecuencia_mensual':
                if dias == (Funs.get_month_days(init_date)[1] - 1):
                    if date(init_date.year, init_date.month,
                            init_date.day) == Funs.first_day_of_month(init_date):
                        show_queda = True

        return show_queda

    def get_tickets_is_day(self, fecha=now(), fecha_fin=None):
        hoy = strFecha(fecha).getFecha()
        if not fecha_fin:
            fecha_ini = hoy + hora_cero
            fecha_fin = hoy + hora_23
        else:
            fecha_ini = hoy + hora_cero
            fecha_fin = strFecha(fecha_fin).getFecha() + hora_23
        kwargs = {
            'fecha__range': (fecha_ini, fecha_fin)
        }
        kwargs[self.get_prefix_kwargs_by_level_tickets()] = self.pk
        from admin_apuestas.models import Tickets
        return Tickets.objects.filter(
            **kwargs
        )

    def get_tickets_is_day_unprocessed(self, fecha=now(), fecha_fin=None):
        from admin_status.models import Status
        pk_pediente = Status.get_status_by_codename(
            'status_ticketpendiente').pk
        pk_procesandose = Status.get_status_by_codename(
            'status_procesandose').pk
        return self.get_tickets_is_day(fecha, fecha_fin).filter(
            status_id__in=[pk_pediente, pk_procesandose]
        )

    def get_count_get_tickets_is_day_unprocessed(
            self, fecha=now(), fecha_fin=None):
        return self.get_tickets_is_day_unprocessed(fecha, fecha_fin).count()

    def get_exists_get_tickets_is_day_unprocessed(
            self, fecha=now(), fecha_fin=None):
        return self.get_tickets_is_day_unprocessed(fecha, fecha_fin).exists()

    def get_preference(self, codename):
        """
            Funcion que retorna la preferencia asociada,
            si no tiene la preferencia retorna None
        """
        key = 'preference_{0}_{1}'.format(
            self.get_comercializadora().id,
            codename
        )
        preference_comer = cache.get(key)
        if not preference_comer:
            try:
                preference_comer = Preferences.objects.get(
                    comercializacion_id=self.get_comercializadora().id,
                    typepreference__codename=codename
                )
                cache.set(
                    key,
                    preference_comer,
                    CACHES_CONF_TIME['registros_db']['comercializacion']
                )
            except Preferences.DoesNotExist:
                preference_comer = None
        return preference_comer

    def get_preference_value_by_codename(self, codename):
        from admin_comercializacion.models import Preferences, DefaultPreferences
        key = 'preference_{0}_{1}'.format(self.get_comercializadora().id, codename)

        preference_comer = cache.get(key)
        if not preference_comer:
            key = 'preference_value_{0}_{1}'.format(self.get_comercializadora().id, codename)
            value = cache.get(key)
            if not value:
                comercializadora = self.get_comercializadora()

                get_default = True
                try:
                    preference_comer = Preferences.objects.only('value').get(
                        comercializacion_id=comercializadora.id,
                        typepreference__codename=codename
                    )
                except Preferences.DoesNotExist:
                    preference_comer = None

                if preference_comer:
                    if preference_comer.value:
                        get_default = False
                        value = preference_comer.value

                if get_default:
                    if self.user_type_codename != 'userprofile_bloque':
                        preference_parent = comercializadora.get_preference_parent(codename)
                        if preference_parent:
                            if preference_parent.value:
                                get_default = False
                                value = preference_parent.value

                if get_default:
                    default = DefaultPreferences.objects.only('value').get(
                        typepreference__codename=codename, default=True
                    )
                    value = default.value

                # Guardar en cache el valor
                cache.set(key, value, CACHES_CONF_TIME['registros_db']['comercializacion'])
        else:
            value = preference_comer.value
        return value

    def get_preference_by_codename(self, codename):
        from admin_comercializacion.models import Preferences, DefaultPreferences
        key = 'preference_{0}_{1}'.format(self.get_comercializadora().id, codename)
        preference_comer = cache.get(key)
        if not preference_comer:
            comercializadora = self.get_comercializadora()
            get_default = True
            try:
                preference_comer = Preferences.objects.only('value').get(
                    comercializacion_id=comercializadora.id,
                    typepreference__codename=codename
                )
            except Preferences.DoesNotExist:
                preference_comer = None

            if preference_comer:
                if preference_comer.value:
                    get_default = False
                    array = [preference_comer.value, preference_comer.distribute]

            if get_default:
                if self.user_type_codename != 'userprofile_bloque':
                    preference_parent = comercializadora.get_preference_parent(codename)
                    if preference_parent:
                        if preference_parent.value:
                            get_default = False
                            array = [preference_parent.value, preference_parent.distribute]

            if get_default:
                default = DefaultPreferences.objects.only('value').get(
                    typepreference__codename=codename, default=True
                )
                array = [default.value, False]
        else:
            array = [preference_comer.value, preference_comer.distribute]
        return array

    def get_restrictions_modalidades(self):
        from admin_juego.models import TipoProducto

        comercializadora = self.get_comercializadora()
        deportes = TipoProducto.objects.all().values_list('id', flat=True)

        restrictions = {}
        for deporte in deportes:
            restriction = comercializadora.get_permissions_sales_restrictions(deporte)
            if restriction:
                restrictions[str(deporte)] = restriction.restrictions

        return restrictions


class Master(object):
    """Master: Este es el papÃ¡ de los helados :)
    no se representa en base de datos

    Se hereda de los datos basicos de cadena
    """
    nivel = 1
    pk = '0'
    prefix_filter = 'master'
    prefix_filter_plural = 'masters'
    status = 'Activo'
    user_type_codename = 'userprofile_master'
    nombre = 'Master'
    resumen_automatic = False

    def __str__(self):
        return self.nombre

    def get_object(self):
        return self

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        return None

    def get_offspring(self):
        """
        Retorna los hijos del objeto actual
        """
        return Operadoras.objects.all()

    def get_offspring_ventas(self, ventas):
        """
        Retorna los hijos del objeto actual para los reportes
        """
        from admin_finanzas.models import Comercializadora
        kwargs_filter = {}
        ids = list(
            ventas.distinct('comercializacion__operadora_id').values_list(
                'comercializacion__operadora_id',
                flat=True))
        kwargs_filter['operadora_id__in'] = ids
        return Comercializadora.objects.filter(
            **kwargs_filter).order_by('operadora__nombre')

    def get_kwargs_hijos_dimension_arco_comercializadora(self):
        kwargs = {
            'comercializacion__operadora_id__isnull': False,
            'comercializacion__bloque_id__isnull': False
        }
        return kwargs

    def get_kwargs_dimension_comercializadora(self):
        kwargs = {
            'comercializacion__operadora_id__isnull': False,
        }
        return kwargs

    def get_kwargs_dimension_arco_comercializadora(self):
        kwargs = {
            'comercializacion__operadora_id__isnull': False,
        }
        return kwargs

    def get_is_apply_queda(self):
        return True

    def get_is_apply_participacion(self):
        return True

    def get_is_apply_regalia(self):
        return True

    def get_is_apply_comision(self):
        return True

    def get_type(self):
        from admin_users.models import UserProfile
        return UserProfile.get_profile_by_codename(
            codename=self.user_type_codename)

    def get_type_codename(self):
        return self.user_type_codename

    def get_verbose_name(self):
        return 'Master'

    def get_verbose_name_plural(self):
        return 'Masters'

    def get_tickets_is_day(self, fecha=now(), fecha_fin=None):
        hoy = strFecha(fecha).getFecha()
        if not fecha_fin:
            fecha_ini = hoy + hora_cero
            fecha_fin = hoy + hora_23
        else:
            fecha_ini = hoy + hora_cero
            fecha_fin = strFecha(fecha_fin).getFecha() + hora_23
        kwargs = {
            'fecha__range': (fecha_ini, fecha_fin)
        }
        from admin_apuestas.models import Tickets
        return Tickets.objects.filter(
            **kwargs
        )

    def get_tickets_is_day_unprocessed(self, fecha=now(), fecha_fin=None):
        from admin_status.models import Status
        pk_pediente = Status.get_status_by_codename(
            'status_ticketpendiente').pk
        pk_procesandose = Status.get_status_by_codename(
            'status_procesandose').pk
        return self.get_tickets_is_day(fecha, fecha_fin).filter(
            status_id__in=[pk_pediente, pk_procesandose]
        )

    def get_count_get_tickets_is_day_unprocessed(
            self, fecha=now(), fecha_fin=None):
        return self.get_tickets_is_day_unprocessed(fecha, fecha_fin).count()

    def get_exists_get_tickets_is_day_unprocessed(
            self, fecha=now(), fecha_fin=None):
        return self.get_tickets_is_day_unprocessed(fecha, fecha_fin).exists()


class Operadoras(BaseGenericProcess, BaseModelCadena):
    """Operadoras: Operadoras.

    Se hereda de los datos basicos de cadena
    """
    nivel = 1
    prefix_filter = 'operadora'
    prefix_filter_plural = 'operadoras'

    user_type_codename = 'userprofile_operadora'

    class Meta:
        unique_together = ('nombre',)
        verbose_name = ('Operadora')
        verbose_name_plural = ('Operadoras')

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        return None

    def get_offspring(self):
        """
        Retorna los hijos del objeto actual
        """
        return self.bloques_set.all().order_by('nombre')

    def get_offspring_ventas(self, ventas):
        """
        Retorna los hijos del objeto actual para los reportes
        """
        from admin_finanzas.models import Comercializadora

        kwargs_filter = {}
        ids = list(ventas.distinct(
            'comercializacion__bloque_id'
        ).values_list('comercializacion__bloque_id', flat=True))
        kwargs_filter['bloque_id__in'] = ids
        return Comercializadora.objects.filter(
            **kwargs_filter).order_by('bloque__nombre')

    def get_distribuidores_filter(self):
        """
        Devuelve los distribuidores pertenecientes a la operadora
        """
        return Distribuidores.objects.filter(
            banca__bloque__operadora_id=self.pk)

    def get_kwargs_by_taquillasessions(self):
        kwargs = {}
        kwargs[
            'session__user__taquilla__agencia__distribuidores__banca__bloque__operadora_id'] = self.pk
        return kwargs

    def get_prefix_kwargs_by_level_agencia(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '__distribuidores__banca__bloque__operadora_id'

    def get_kwargs_by_agencia(self):
        """
        Devuelve el kwargs para consulta en reportes de agencias
        """
        kwargs = {}
        kwargs['distribuidores__banca__bloque__operadora_id'] = self.pk
        return kwargs

    def get_prefix_kwargs_offspring_all(self, prefix=''):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        kwargs = {}
        kwargs[
            prefix +
            '__agencia__distribuidores__banca__bloque__operadora_id'] = self.pk
        kwargs[prefix + '__distribuidor__banca__bloque__operadora_id'] = self.pk
        kwargs[prefix + '__banca__bloque__operadora_id'] = self.pk
        kwargs[prefix + '__bloque__operadora_id'] = self.pk
        return kwargs


class BaseGenericModeloJuego(models.Model):
    """BaseGenericModeloJuego: Base generica para modelos de negocio de juego

    Definida para definir propiedades compartidas entre una multibanca y una banca

    Campos definidos:

        is_sistema_juego(booleano): bandera que me indica si tiene un sistema de juego
            propio asociado

        is_logros(booleano): bandera que me indica si administa logros (agrega o edita),
            partiendo de encuentros base, cargados por el dueÃ±o del sistema principal

        is_resultados(booleano): bandera que me indica si administa resultados, partiendo
            de encuentros base, cargados por el dueÃ±o del sistema principal

        permissions_create_user(booleano): bandera que indica si tiene permiso de crear
            usuarios de su mismo nivel

    """

    is_sistema_juego = models.BooleanField(
        default=False,
        verbose_name='Â¿Administra su propio sistema de juego? ',
        help_text='Seleccione este campo solo si desea que la comercializadora tenga su propio'
                  ' sistema de juego'
    )

    is_logros = models.BooleanField(
        default=False,
        verbose_name='Â¿Administra sus propios logros? ',
        help_text='Seleccione este campo solo si desea que la comercializadora administe sus propios'
                  ' logros'
    )

    is_resultados = models.BooleanField(
        default=False,
        verbose_name='Â¿Administra sus propios resultados? ',
        help_text='Seleccione este campo solo si desea que la comercializadora administe su propios'
                  ' resultados'
    )

    permissions_create_user = models.BooleanField(
        default=False,
        verbose_name='Â¿Tiene permisos de crear usuarios de su mismo nivel? ',
        help_text='Seleccione este campo solo si desea que la comercializadora pueda crear'
                  ' mas usuarios de su mismo nivel'
    )

    class Meta:
        abstract = True

    def save_sistema_juego(self):
        from admin_juego.models import SistemaJuego

        comercializadora = self.get_comercializadora()

        if not SistemaJuego.objects.filter(
            comercializadora=comercializadora
        ).exists():
            sistema = SistemaJuego.objects.create(
                comercializadora=comercializadora,
                nombre=self.nombre
            )
        else:
            sistema = comercializadora.sistemajuego

        sistema.is_resultados = self.is_resultados
        sistema.save(update_fields=['is_resultados'])


class Bloques(BaseGenericProcess, BaseModelCadena, BaseGenericModeloJuego):
    """Bloques: Bloque

    Se hereda de los datos basicos de cadena, basicos de procesos y genericos
    para modelos de negocio.

    Campos definidos:

        tipo(booleano): bandera que me indica si es un bloque dedicado a la
            venta web

        operadora(foreing): operadora a la cual pertenece el bloque

    """
    nivel = 2
    prefix_filter = 'bloque'
    prefix_filter_plural = 'bloques'
    user_type_codename = 'userprofile_bloque'

    tipo = models.BooleanField(
        default=False,
        verbose_name='Â¿Para venta web? ',
        help_text='En caso de ser un bloque para venta en la web, seleccione este campo'
    )
    operadora = models.ForeignKey(
        'admin_comercializacion.Operadoras',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('nombre', 'operadora')
        verbose_name = ('Multi Banca')
        verbose_name_plural = ('Multi Bancas')

    def get_kwargs_by_taquillasessions(self):
        kwargs = {}
        kwargs[
            'session__user__taquilla__agencia__distribuidores__banca__bloque_id'] = self.pk
        return kwargs

    def get_kwargs_by_agencia(self):
        """
        Devuelve el kwargs para consulta en reportes de agencias
        """
        kwargs = {}
        kwargs['distribuidores__banca__bloque_id'] = self.pk
        return kwargs

    def get_prefix_kwargs_by_level_agencia(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '__distribuidores__banca__bloque_id'

    def get_offspring(self):
        """
        Retorna los hijos del objeto actual
        """
        return self.bancas_set.all().order_by('nombre')

    def get_offspring_ventas(self, ventas):
        """
        Retorna los hijos del objeto actual para los reportes
        """
        from admin_finanzas.models import Comercializadora

        kwargs_filter = {}
        ids = list(ventas.distinct(
            'comercializacion__banca_id'
        ).values_list('comercializacion__banca_id', flat=True))
        kwargs_filter['banca_id__in'] = ids

        return Comercializadora.objects.filter(
            **kwargs_filter).order_by('banca__nombre')

    def get_distribuidores_filter(self):
        """
        Devuelve los distribuidores pertenecientes al bloque
        """
        return Distribuidores.objects.filter(banca__bloque_id=self.pk)

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        key = 'cadena_{0}_{1}'.format(
            'userprofile_operadora',
            self.pk
        )
        origen = cache.get(key)
        if not origen:
            origen = self.operadora
            cache.set(
                key,
                origen,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return origen

    def get_prefix_kwargs_offspring_all(self, prefix=''):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        kwargs = {}
        kwargs[prefix + '__agencia__distribuidores__banca__bloque_id'] = self.pk
        kwargs[prefix + '__distribuidor__banca__bloque_id'] = self.pk
        kwargs[prefix + '__banca__bloque_id'] = self.pk
        return kwargs


class Bancas(BaseGenericProcess, BaseModelCadena, BaseGenericModeloJuego):
    """Bancas: Bancoas

    Se hereda de los datos basicos de cadena, basicos de procesos y genericos
    para modelos de negocio.

    Campos definidos:

        modelo_negocio(entero): entero tipo choice que indica el modelo de negocio

        bloque(foreing): bloque a la cual pertenece la banca

    """
    nivel = 3
    prefix_filter = 'banca'
    prefix_filter_plural = 'bancas'
    user_type_codename = 'userprofile_banca'

    bloque = models.ForeignKey(
        'admin_comercializacion.Bloques',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    modelo_negocio_codenames = {
        'codename_negocio_porcentajes': 1,
        'codename_negocio_alquiler': 2,
    }
    choices_modelo_negocio = [
        [1, 'Porcentajes'],
        [2, 'Alquiler']
    ]
    modelo_negocio = models.IntegerField(
        verbose_name='Modelo de negocio (*)',
        choices=choices_modelo_negocio,
        default=1,
        help_text='Seleccione el modelo de negocio'
    )

    class Meta:
        unique_together = ('nombre', 'bloque', )
        verbose_name = ('Banca')
        verbose_name_plural = ('Bancas')

    def get_kwargs_by_taquillasessions(self):
        kwargs = {}
        kwargs['session__user__taquilla__agencia__distribuidores__banca_id'] = self.pk
        return kwargs

    def get_kwargs_by_agencia(self):
        """
        Devuelve el kwargs para consulta en reportes de agencias
        """
        kwargs = {}
        kwargs['distribuidores__banca_id'] = self.pk
        return kwargs

    def get_prefix_kwargs_by_level_agencia(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '__distribuidores__banca_id'

    def get_offspring(self):
        """
        Retorna los hijos del objeto actual
        """
        return self.distribuidores_set.all().order_by('nombre')

    def get_offspring_ventas(self, ventas):
        """
        Retorna los hijos del objeto actual para los reportes
        """
        from admin_finanzas.models import Comercializadora

        kwargs_filter = {}
        ids = list(ventas.distinct(
            'comercializacion__distribuidor_id'
        ).values_list('comercializacion__distribuidor_id', flat=True))
        kwargs_filter['distribuidor_id__in'] = ids

        return Comercializadora.objects.filter(
            **kwargs_filter).order_by('distribuidor__nombre')

    def get_distribuidores_filter(self):
        """
        Devuelve los distribuidores pertenecientes a la banca
        """
        return Distribuidores.objects.filter(banca_id=self.pk)

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        key = 'cadena_{0}_{1}'.format(
            'userprofile_bloque',
            self.pk
        )
        origen = cache.get(key)
        if not origen:
            origen = self.bloque
            cache.set(
                key,
                origen,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return origen

    def get_prefix_kwargs_offspring_all(self, prefix=''):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        kwargs = {}
        kwargs[prefix + '__agencia__distribuidores__banca_id'] = self.pk
        kwargs[prefix + '__distribuidor__banca_id'] = self.pk
        return kwargs

    def get_using_porcentajes(self):
        return self.modelo_negocio_codenames[
            'codename_negocio_porcentajes'] == self.modelo_negocio


class Distribuidores(BaseGenericProcess, BaseModelCadena):
    """Distribuidores: Distribuidores

    Se hereda de los datos basicos de cadena y basicos de procesos

    Campos definidos:

        banca(foreing): banca a la cual pertenece el distribuidor
    """
    nivel = 4
    prefix_filter = 'distribuidor'
    prefix_filter_plural = 'distribuidores'
    user_type_codename = 'userprofile_distribuidor'

    banca = models.ForeignKey(
        'admin_comercializacion.Bancas',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    class Meta:
        unique_together = ('nombre', 'banca', )
        verbose_name = ('Distribuidor')
        verbose_name_plural = ('Distribuidores')

    def get_kwargs_by_taquillasessions(self):
        kwargs = {}
        kwargs['session__user__taquilla__agencia__distribuidores_id'] = self.pk
        return kwargs

    def get_prefix_kwargs_by_level_agencia(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '__distribuidores_id'

    def get_kwargs_by_agencia(self):
        """
        Devuelve el kwargs para consulta en reportes de agencias
        """
        kwargs = {}
        kwargs['distribuidores_id'] = self.pk
        return kwargs

    def get_offspring(self):
        """
        Retorna los hijos del objeto actual
        """
        return self.agencias_set.all().order_by('nombre')

    def get_offspring_ventas(self, ventas):
        """
        Retorna los hijos del objeto actual para los reportes
        """
        from admin_finanzas.models import Comercializadora

        kwargs_filter = {}
        ids = list(ventas.distinct(
            'comercializacion__agencia_id'
        ).values_list('comercializacion__agencia_id', flat=True))
        kwargs_filter['agencia_id__in'] = ids

        return Comercializadora.objects.filter(
            **kwargs_filter).order_by('agencia__nombre')

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        key = 'cadena_{0}_{1}'.format(
            'userprofile_banca',
            self.pk
        )
        origen = cache.get(key)
        if not origen:
            origen = self.banca
            cache.set(
                key,
                origen,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return origen

    def get_prefix_kwargs_offspring_all(self, prefix=''):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        kwargs = {}
        kwargs[prefix + '__agencia__distribuidores_id'] = self.pk
        return kwargs

    def get_using_porcentajes(self):
        return self.banca.modelo_negocio_codenames[
            'codename_negocio_porcentajes'] == self.banca.modelo_negocio


class Agencias(BaseGenericProcess, BaseModelCadena):
    """Agencias: Agencias

    Se hereda de los datos basicos de cadena y basicos de procesos

    Campos definidos:

        distribuidores(foreing): distribuidor a la cual pertenece la agencia

        num_taquillas(entero): contador de numero de taquillas para la
            agencia

        codigo (string): codigo personalizado para agencias

        montomin(decimal): nomto minito por ticket

        montomax(decimal): monto maximo por ticket

        montomax_ganancia(decimal): monto maximo de ganancia

        cantidad_apuesta_max(entero): numero maximo de apuestas por ticket

        cantidad_apuesta_min(entero): numero minimo de apuestas por ticket

        tiempoexpiracion(entero): tiempo de expiracion de los tickets en dias,
            ejemplo : 2 = 2 dias

        parley_machos_max(entero): numero maximo de machos por ticket
        parley_machos_min(entero): munero minimo de machos por ticket

        parley_hembras_max(entero): numero maximo de hembras por ticket
        parley_hembras_min(entero): munero minimo de hembras por ticket

        parley_empates_max(entero): numero maximo de empates por ticket

        parley_clonados_maxima_ganancia(decimal): maxima ganancia por agencia
            al dia de tickets clonados o repetidos

        monto_alquiler(decimal): monto de alquiler de las taquillas,
            es caso de estar defino es aplicable a todas sus taquillas

        frecuencia_monto_alquiler(string): codename de la frecuencia del modo
            alquiler, en cado de estar activo

        frecuencia_queda(string): codename de la frecuencia del modelo de negocio
            queda

        factor_riesgo(entero): entero que me indica que el factro de riesgo esta
            habilitado cuando es 1, en caso de ser 0 es desactivado

        ticket_titulo y ticket_pie: campo personalizados para impresion de tickets


    """
    nivel = 5
    prefix_filter = 'agencia'
    prefix_filter_plural = 'agencias'
    user_type_codename = 'userprofile_agencia'

    distribuidores = models.ForeignKey(
        'admin_comercializacion.Distribuidores',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    num_taquillas = models.IntegerField(
        verbose_name='NÃºmero de taquillas (*)',
        help_text='Seleccione el numero de taquillas a crear automÃ¡ticamente para la agencia'
    )
    codigo = models.CharField(
        null=True,
        blank=True,
        max_length=30,
        verbose_name='CÃ³digo ',
        help_text='Introduzca un cÃ³digo de centro de apuesta',
        db_index=True,
    )
    ##
    montomin = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto mÃ­nimo de apuesta ',
        help_text='Seleccione el monto mÃ­nimo de apuesta'
    )
    montomax = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto mÃ¡ximo de apuesta ',
        help_text='Seleccione el monto mÃ¡ximo de apuesta'
    )
    montomax_ganancia = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto mÃ¡ximo de ganancia ',
        help_text='Seleccione el monto mÃ¡ximo de ganancia'
    )
    cantidad_apuesta_max = models.IntegerField(
        null=True,
        verbose_name='Cantidad mÃ¡xima de combinaciones ',
        help_text='Seleccione la cantidad mÃ¡xima de combinaciones'
    )
    cantidad_apuesta_min = models.IntegerField(
        null=True,
        verbose_name='Cantidad minima de combinaciones ',
        help_text='Seleccione la cantidad minima de combinaciones'
    )
    tiempoexpiracion = models.IntegerField(
        null=True,
        verbose_name='DÃ­as de expiraciÃ³n del los tickets ',
        help_text='Seleccione la cantidad de dÃ­as de expiraciÃ³n para los tickets'
    )
    parley_machos_max = models.IntegerField(
        null=True,
        verbose_name='Parley: MÃ¡ximo de apuestas a un macho por ticket',
        help_text='Parley: Seleccione el numero mÃ¡ximo de apuesta a un macho en un ticket'
    )
    parley_machos_min = models.IntegerField(
        null=True,
        verbose_name='Parley: MÃ­nimo de apuestas a un macho por ticket',
        help_text='Parley: Seleccione el numero mÃ­nimo de apuesta a un macho en un ticket'
    )
    parley_hembras_max = models.IntegerField(
        null=True,
        verbose_name='Parley: MÃ¡ximo de apuestas a una hembra por ticket',
        help_text='Parley: Seleccione el numero mÃ¡ximo de apuesta a una en un ticket'
    )
    parley_hembras_min = models.IntegerField(
        null=True,
        verbose_name='Parley: MÃ­nimo de apuestas a un hembra por ticket',
        help_text='Parley: Seleccione el numero mÃ­nimo de apuesta a una hembra en un ticket'
    )
    parley_hembras_min = models.IntegerField(
        null=True,
        verbose_name='Parley: cantidad minima de hembras (*)',
        help_text='Ingrese la cantidad minima de hembras por ticket'
    )
    parley_empates_max = models.IntegerField(
        null=True,
        verbose_name='Parley: Cantidad mÃ¡xima de apuesta a empate por ticket',
        help_text='Parley: Indique la cantidad mÃ¡xima permitida de apuestas a empate en un ticket'
    )
    parley_clonados_maxima_ganancia = models.DecimalField(
        null=True,
        max_digits=15,
        decimal_places=2,
        verbose_name='Parley: Monto mÃ¡ximo de ganancia para combinaciones repetidas en tickets',
        help_text='Parley: Seleccione el monto mÃ¡ximo para la ganancia de apuestas con '
                  'combinaciones repetidas en los tickets'
    )
    monto_alquiler = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=None,
        null=True,
        blank=True,
        verbose_name='Monto de alquiler por taquilla (*)',
        help_text='Ingrese el monto por alquier de taquilla'
    )

    frecuencia_monto_alquiler = models.CharField(
        choices=choices_frecuencia_monto_alquiler,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Frecuencia de cobro de monto de alquiler (*)',
        help_text='Seleccione la frecuencia de cobro de monto de alquiler'
    )
    factor_riesgo = models.IntegerField(
        null=True,
        verbose_name='Factor de riesgo (*)',
        default=1,
        choices=choices_factor_riesgo,
        help_text='Seleccione una opcion de factor de riesgo',
    )

    frecuencia_queda = models.CharField(
        choices=choices_frecuencia_queda,
        null=True,
        blank=True,
        max_length=30,
        verbose_name='Frecuencia de corte de la queda (*)',
        help_text='Seleccione la frecuencia de corte para la queda'
    )

    ticket_titulo = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Ticket: Titulo del ticket (*)',
        help_text='Ingrese el titulo del ticket'
    )

    ticket_pie = models.CharField(
        null=True,
        blank=True,
        max_length=100,
        verbose_name='Ticket: Pie del ticket (*)',
        help_text='Ingrese el pie del ticket'
    )

    class Meta:
        unique_together = ('nombre', 'distribuidores', )
        verbose_name = ('Centro de apuesta')
        verbose_name_plural = ('Centros de apuesta')

    def __str__(self):
        if self.codigo:
            nombre = self.codigo + '-' + self.nombre
        else:
            nombre = self.nombre

        if not self.activo():
            nombre = nombre.split('_delete_')[0]
            return '<span id="{1}" class="cadena-delete no-pd">{0}</span>'.format(
                nombre[0],
                self.prefix_filter + '_' + str(self.pk)
            )
        else:
            return '{0}'.format(nombre)

    def get_kwargs_by_taquillasessions(self):
        kwargs = {}
        kwargs['session__user__taquilla__agencia_id'] = self.pk
        return kwargs

    def get_kwargs_by_agencia(self):
        """
        Devuelve el kwargs para consulta en reportes de agencias
        """
        kwargs = {}
        kwargs['id'] = self.pk
        return kwargs

    def get_prefix_kwargs_by_level_agencia(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '_id'

    def get_offspring(self):
        """
        Retorna los hijos del objeto actual
        """
        return self.taquillas_set.all().order_by('taquilla')

    def get_offspring_ventas(self, ventas):
        """
        Retorna los hijos del objeto actual para los reportes
        """
        from admin_finanzas.models import Comercializadora

        kwargs_filter = {}
        ids = list(ventas.distinct(
            'comercializacion__taquilla_id'
        ).values_list('comercializacion__taquilla_id', flat=True))
        kwargs_filter['taquilla_id__in'] = ids

        return Comercializadora.objects.filter(
            **kwargs_filter).order_by('taquilla__taquilla')

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        key = 'cadena_{0}_{1}'.format(
            'userprofile_distribuidor',
            self.pk
        )
        origen = cache.get(key)
        if not origen:
            origen = self.distribuidores
            cache.set(
                key,
                origen,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return origen

    def get_ultima_conexion(self):
        self._connection_at = getattr(self, '_connection_at', None)

        if not self._connection_at:
            from admin_historic.models import HechoConnectionsComer
            ultima_conexion = HechoConnectionsComer.objects.only('connection_at').filter(
                agencia_id=self.pk
            ).order_by('-connection_at')

            try:
                self._connection_at = ultima_conexion[0].connection_at
            except Exception:
                self._connection_at = 'Nunca'
            return self._connection_at
        else:
            return self._connection_at

    def get_prefix_kwargs_offspring_all(self, prefix=''):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return None

    def check_taquilla_master(self):
        """
        Devuelve un booleano que define si la agencia tiene una taquilla master
        """
        taquilla_master = self.taquillas_set.filter(is_taquilla_master=True)
        if taquilla_master:
            return taquilla_master[0]
        else:
            return False


class Taquillas(ProtectDelete, BaseGenericProcess, models.Model):
    """Taquillas: Taquillas

    Se hereda de la clase basica de ProtectDelete

    Campos definidos:

        taquilla(string): nombre de la taquilla

        serial(string): serial de la taquilla, generalmente el serial del pc

        agencia(foreing): agencia a la cual pertenece la taquilla

        monto_alquiler(decimal): monto de alquiler por taquilla

        created_at y updated_at: registros de creacion y actualizacion.

    """

    nivel = 6
    prefix_filter = 'taquilla'
    prefix_filter_plural = 'taquillas'

    taquilla = models.CharField(
        max_length=100,
        verbose_name='Nombre de la taquilla (*)',
        help_text='Ingrese el nombre de la taquilla'
    )
    serial = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Serial (*)',
        help_text='Ingrese el serial de la taquilla'
    )
    agencia = models.ForeignKey(
        'admin_comercializacion.Agencias',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    monto_alquiler = models.DecimalField(
        max_digits=15,
        decimal_places=5,
        default=0.00000,
        verbose_name='Monto de alquiler por taquilla (*)',
        help_text='Ingrese el monto por alquier de taquilla'
    )
    modo_alquiler = models.BooleanField(
        default=False,
        verbose_name='Â¿Modo de alquiler activo? ',
        help_text='si este campo esta activo, esta taquilla pasa a modo alquiler',
        editable=False
    )
    is_taquilla_master = models.BooleanField(
        default=True,
        verbose_name='Taquilla master ',
        help_text='Si este campo esta activo, se crea la taquilla con todos los permisos',
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.PositiveIntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('updated_at', 'pk_clone')

    class Meta:
        unique_together = ('taquilla', 'agencia', )
        verbose_name = ('Taquilla')
        verbose_name_plural = ('Taquillas')

    def __str__(self):
        return self.taquilla

    def save(self, *args, **kwargs):
        super(Taquillas, self).save(*args, **kwargs)
        cache.delete(
            'cadena_{0}_{1}'.format(
                'taquilla',
                self.pk,
            )
        )

    def get_prefix_kwargs_by_level_taquilla(self):
        """
        Devuelve un prefijo de kwargs para consulta en reportes
        """
        return '_id'

    def get_origen(self):
        """
        Retorna el origen de la instanca
        """
        key = 'cadena_{0}_{1}'.format(
            'userprofile_agencia',
            self.pk
        )
        origen = cache.get(key)
        if not origen:
            origen = self.agencia
            cache.set(
                key,
                origen,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return origen

    def get_user(self):
        return self.usuariostaquilla

    def get_passwd(self):
        return self.get_user().get_passwd()

    def get_status(self):
        return self.get_user().get_status()

    def set_new_status(self, codename):
        return self.get_user().set_new_status(codename)

    def get_ultima_conexion(self):
        return self.get_user().get_ultima_conexion()

    def update_serial(self, client_srl):
        self.serial = client_srl
        self.save(update_fields=['serial', 'updated_at'])

    # get_absolute_url compatible con Django 3.1+ (sin @models.permalink)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_comercializacion_taquillas_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            try:
                return reverse('admin:admin_comercializacion_taquillas_change', args=[self.pk])
            except NoReverseMatch:
                return '/admin/'

    def get_values_cadena_notificacions(self):
        values = cache.get('values_cadena_notificacions_{0}'.format(self.pk))
        if not values:
            values = {
                'taquilla': self.pk,
                'agencia': self.agencia_id,
                'distribuidor': self.agencia.distribuidores_id,
                'banca': self.agencia.distribuidores.banca_id,
                'bloque': self.agencia.distribuidores.banca.bloque_id,
            }
            cache.set(
                'values_cadena_notificacions_{0}'.format(self.pk),
                values,
                CACHES_CONF_TIME['registros_db']['everyone']
            )
        return values

    def get_filters_taquilla(self):
        """
        Retorna un json con los filtros que se pueden consultar en la taquilla,
        dependiendo si es una taquilla master o no
        """
        json = {'filter_taquilla': 'Taquilla'}
        if self.is_taquilla_master:
            json['filter_agencia'] = 'Centro de apuesta'
        return json


class UsuariosTaquilla(ProtectDelete, AbstractBaseUser):
    """UsuariosTaquilla: Usuarios por taquilla

    Se hereda de la clase basica de ProtectDelete y AbstractBaseUser

    Campos definidos en la clase AbstractBaseUser
        password: es el password
        last_login: fecha en la que se realizo el ultimo login

    Campos definidos:
        user(string): usuario de la taquilla

        serial(string): serial de la taquilla, generalmente el serial del pc

        agencia(foreing): agencia a la cual pertenece la taquilla

        created_at y updated_at: registros de creacion y actualizacion.

    """
    user = models.CharField(
        max_length=200,
        verbose_name='Usuario (*)',
        help_text='Ingrese un usuario',
        db_index=True,
    )
    nombre = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='Nombre (*)',
        help_text='Ingrese un nombre para el usuario'
    )
    taquilla = models.ForeignKey(
        'admin_comercializacion.Taquillas',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    pub_key_client = models.CharField(max_length=1000, default='', editable=False)
    pub_key = models.CharField(max_length=1000, default='', editable=False)
    priv_key = models.CharField(max_length=1000, default='', editable=False)
    keys_date = models.DateTimeField(null=True, editable=False)
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.PositiveIntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('updated_at', 'pk_clone')

    class Meta:
        unique_together = ('user', 'taquilla', )
        verbose_name = ('Usuario de taquilla')
        verbose_name_plural = ('Usuarios de taquillas')

    def __str__(self):
        return self.user

    def get_taquilla(self):
        """
        Retorna la taquilla desde la cache
        """
        key = 'cadena_{0}_{1}'.format(
            'taquilla',
            self.taquilla_id
        )
        origen = cache.get(key)
        if not origen:
            origen = self.taquilla
            cache.set(
                key,
                origen,
                CACHES_CONF_TIME['registros_db']['comercializacion']
            )
        return origen

    def get_agencia(self):
        return self.get_taquilla().get_origen()

    def get_distribuidor(self):
        return self.get_agencia().get_origen()

    def get_banca(self):
        return self.get_distribuidor().get_origen()

    def get_bloque(self):
        return self.get_banca().get_origen()

    def get_operadora(self):
        return self.get_bloque().get_origen()

    def get_passwd(self):
        user = self
        try:
            default = TaquillaDataDefault.objects.all()
            if default.exists():
                default = default[0]
                if user.check_password(default.passwd):
                    return 'por default: ' + default.passwd
                else:
                    return 'ya fue cambiada'
        except Exception:
            pass

        return ''

    def get_taquilla_status_details(self):
        from admin_status.models import Status, TaquillaStatusDetail
        status = self.taquillastatusdetail_set.filter(
            enddate=None
        )
        if status.exists():
            return status[0]
        else:

            detail_status = TaquillaStatusDetail.objects.create(
                usuariotaquilla=self,
                startdate=now(),
                status=Status.get_status_by_codename(
                    codename='status_instalacion')
            )

            return detail_status

    def set_new_status(self, codename):
        self.get_taquilla_status_details().close_status_to(codename)

    def get_status(self):
        if not self.status:
            self.status = self.get_taquilla_status_details().status
            self.save(update_fields=['admin_status.Status'])
        return self.status

    def get_ultima_conexion(self):
        from admin_historic.models import HechoConnectionsComer
        try:
            return HechoConnectionsComer.objects.only('connection_at').get(
                taquilla_id=self.taquilla_id
            ).connection_at
        except HechoConnectionsComer.DoesNotExist:
            return 'Nunca'

    def get_class_name(self):
        return str(self.__class__.__name__).lower()

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.taquilla.__module__.split('.')[0],
            self.taquilla.__class__.__name__.lower(),
            self.taquilla_id
        )


class Cupos(ProtectDelete, models.Model):
    """Cupos: Cupos para la cadena

    Campos definidos:
        fecha_inicio(datetime): fecha de inicio del cupo

        fecha_fin(string): fecha de fin del cupo

        monto_diario(decimal): monto diario de apuestas

        operadora(foreing): operadora a la cual pertenece el cupo
        bloque(foreing): bloque a la cual pertenece el cupo
        banca(foreing): banca a la cual pertenece el cupo
        distribuidor(foreing): distribuidor a la cual pertenece el cupo
        agencia(foreing): agencia a la cual pertenece el cupo

        Los campos: operadora, bloque, banca, distribuidor y agencia forman
            un arco

        created_at y updated_at: registros de creacion y actualizacion.

    """
    not_delete = True
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha de inicio (*)',
        help_text='Ingrese la fecha de inicio ',
        auto_now_add=True,
    )
    fecha_fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de fin ',
        help_text='Ingrese la fecha de fin '
    )
    monto_diario = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0.0,
        verbose_name='Monto diario de venta (*)',
        help_text='Ingrese el monto diario '
    )
    monto_premio = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name='Monto diario de premio (*)',
        help_text='Ingrese el monto diario de premio ',
        null=True,
        blank=True,
    )
    operadora = models.ForeignKey(
        'admin_comercializacion.Operadoras',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    bloque = models.ForeignKey(
        'admin_comercializacion.Bloques',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    banca = models.ForeignKey(
        'admin_comercializacion.Bancas',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    distribuidor = models.ForeignKey(
        'admin_comercializacion.Distribuidores',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    agencia = models.ForeignKey(
        'admin_comercializacion.Agencias',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
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
        verbose_name = ('Cupo de una comercializadora')
        verbose_name_plural = ('Cupos de las comercializadoras')
        ordering = ['-fecha_inicio']

    def __str__(self):
        return '{0} - {1}'.format(self.get_object(), self.monto_diario)

    def get_object(self):
        """
        Retorna el objeto al cual pertenece el cupo
        """
        if self.operadora_id:
            return self.operadora
        elif self.bloque_id:
            return self.bloque
        elif self.banca_id:
            return self.banca
        elif self.distribuidor_id:
            return self.distribuidor
        elif self.agencia_id:
            return self.agencia
        else:
            raise ValueError('Error: el cupo no tiene objeto relacionado')

    def get_object_id(self):
        """
        Retorna el objeto al cual pertenece el cupo
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
        else:
            raise ValueError('Error: el cupo no tiene objeto relacionado')

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

    # get_absolute_url compatible con Django 3.1+ (sin @models.permalink)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_comercializacion_cupos_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            try:
                return reverse('admin:admin_comercializacion_cupos_change', args=[self.pk])
            except NoReverseMatch:
                return '/admin/'


class Porcentajes(ProtectDelete, models.Model):
    """Porcentajes: Porcentajes para la cadena

    Campos definidos:
        fecha_inicio(datetime): fecha de inicio del porcentaje

        fecha_fin(string): fecha de fin del porcentaje

        tipo(foreing): tipo de porcentaje

        porcentaje_ganancia(decimal): porcentaje de ganancia

        porcentaje_maximo(decimal): porcentaje maximo que puede asignarse
            en la cadena a la que se hace referencia

        Estos campos son los porcentajes que quedan disponibles repartidos
        entre la cadena.
            bloque_porc(decimal)
            banca_porc(decimal)
            distribuidor_porc(decimal)
            agencia_porc(decimal)
            taquilla_porc(decimal)

        operadora(foreing): operadora a la cual pertenece el porcentaje
        bloque(foreing): bloque a la cual pertenece el porcentaje
        banca(foreing): banca a la cual pertenece el porcentaje
        distribuidor(foreing): distribuidor a la cual pertenece el porcentaje
        agencia(foreing): agencia a la cual pertenece el porcentaje
        taquilla(foreing): agencia a la cual pertenece el porcentaje

        Los campos: operadora, bloque, banca, distribuidor, agencia y taquilla forman
            un arco

        created_at y updated_at: registros de creacion y actualizacion.

    """
    not_delete = True
    fecha_inicio = models.DateTimeField(
        verbose_name='Fecha de inicio (*)',
        help_text='Ingrese la fecha de inicio ',
        auto_now_add=True,
    )
    fecha_fin = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Fecha de fin ',
        help_text='Ingrese la fecha de fin '
    )
    tipo = models.ForeignKey(
        'admin_comercializacion.TipoPorcentajes',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    relacion = models.BooleanField(
        default=True,
        verbose_name='RelaciÃ³n ',
    )
    porcentaje_ganancia = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        verbose_name='Porcentaje ganancia ',
    )
    porcentaje_maximo = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        verbose_name='Porcentaje mÃ¡ximo ',
    )
    bloque_porc = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        default=None,
        verbose_name='Bloque porcentaje',
    )
    banca_porc = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        default=None,
        verbose_name='Banca porcentaje',
    )
    distribuidor_porc = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        default=None,
        verbose_name='Distribuidor porcentaje',
    )
    agencia_porc = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        default=None,
        verbose_name='Agencia porcentaje',
    )
    taquilla_porc = models.DecimalField(
        max_digits=15,
        decimal_places=4,
        null=True,
        blank=True,
        default=None,
        verbose_name='Taquilla porcentaje',
    )
    operadora = models.ForeignKey(
        'admin_comercializacion.Operadoras',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    bloque = models.ForeignKey(
        'admin_comercializacion.Bloques',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    banca = models.ForeignKey(
        'admin_comercializacion.Bancas',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    distribuidor = models.ForeignKey(
        'admin_comercializacion.Distribuidores',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    agencia = models.ForeignKey(
        'admin_comercializacion.Agencias',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    taquilla = models.ForeignKey(
        'admin_comercializacion.Taquillas',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    # audit_exclude = ('bloque_porc', 'banca_porc', 'distribuidor_porc', 'agencia_porc', 'taquilla_porc')

    class Meta:
        verbose_name = ('Porcentaje de una comercializadora')
        verbose_name_plural = ('Porcentajes de las comercializadoras')
        ordering = ['-fecha_inicio']

    def get_object(self):
        """
        Retorna el objeto al cual pertenece el porcentaje
        """
        if self.operadora:
            return self.operadora
        elif self.bloque:
            return self.bloque
        elif self.banca:
            return self.banca
        elif self.distribuidor:
            return self.distribuidor
        elif self.agencia:
            return self.agencia
        elif self.taquilla:
            return self.taquilla
        else:
            raise ValueError(
                'Error: el porcentaje no tiene objeto relacionado')

    def get_object_id(self):
        """
        Retorna el objeto al cual pertenece el cupo
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
        else:
            raise ValueError(
                'Error: el porcentaje no tiene objeto relacionado')

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

    # get_absolute_url compatible con Django 3.1+ (sin @models.permalink)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_comercializacion_porcentajes_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            try:
                return reverse('admin:admin_comercializacion_porcentajes_change', args=[self.pk])
            except NoReverseMatch:
                return '/admin/'

    def get_class_name(self):
        return str(self.__class__.__name__).lower()

    def __str__(self):
        return '{0} - {1} - {2}'.format(self.get_object(),
                                        self.tipo, self.porcentaje_ganancia)

    def get_porcentaje(self):
        return round(self.porcentaje_ganancia * 100, 1)

    def get_bloque_porc(self):
        return round(self.bloque_porc * 100, 1)

    def get_banca_porc(self):
        return round(self.banca_porc * 100, 1)

    def get_distribuidor_porc(self):
        return round(self.distribuidor_porc * 100, 1)

    def get_agencia_porc(self):
        return round(self.agencia_porc * 100, 1)

    def get_porcentaje_float(self):
        return self.get_porcentaje()

    def get_porcentaje_maximo(self):
        return round(self.porcentaje_maximo * 100, 1)

    def get_porcentaje_maximo_float(self):
        return self.get_porcentaje_maximo()


class FactorRiesgo(ProtectDelete, models.Model):
    """PreferenciasCadena: Preferencias para la cadena

    Campos definidos:

        data_origin(integer): Campo que guarda el codigo que posee en las notificaciones

        factores(json): arreglo con los rangos y porcentajes a aplicar
            Ejemplo:
            [ [100,200,30], [100,200,30],]
            Donde:
                100 es el rango inicial
                200 es el rango final
                30 es el porcentaje aplicado a dichos rangos

        comercializadora(foreing): comercializadora a la cual pertenece
            el factor de riesgo

        created_at y updated_at: registros de creacion y actualizacion.

    """

    factores = JSONField(
        null=True,
        blank=True,
        verbose_name='Factores',
    )

    comercializadora = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
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
        app_label = 'admin_comercializacion'
        verbose_name = ('Factor de riesgo')
        verbose_name_plural = ('Factores de riesgo')
        ordering = ['-created_at']

    def __str__(self):
        return 'Factor de riesgo | {0}'.format(str(self.comercializadora))

    def save(self, *args, **kwargs):
        super(FactorRiesgo, self).save(*args, **kwargs)
        cache.delete('factorriesgo_{0}'.format(self.comercializadora_id))

    def get_object(self):
        """
        Retorna el objeto al cual pertenece el factor de riesgo
        """
        return self.comercializadora.get_object()

    def get_object_id(self):
        """
        Retorna el objeto al cual pertenece el factor de riesgo
        """
        return self.comercializadora.get_object_id()

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

    def get_class_name(self):
        return str(self.__class__.__name__).lower()


types_notification = {
    'data_type_origin': {
        'deporte': (1, 'TipoProducto'),
        'temporada': (2, 'Fechas'),
        'jornada': (3, 'Fechas'),
        'encuentro': (4, 'Sorteo'),
        'encuentro_modalidad': (5, 'Referencias'),
        'jugada': (6, 'Logros'),
        'grupos_juego': (7, 'Grupos de juego'),
        'deporte_grupo': (8, 'TipoProducto Grupos'),
        'grupo_modalidad': (9, 'Grupos ModalidadJuego'),
    },
}

types_notification_cadena = {
    'preferencia': (1, 'Preferencias'),
    'factor_riesgo': (2, 'Factor de riesgo'),
    'mensajes': (3, 'Mensajes'),
    'permiso_venta': (4, 'Permiso de venta'),
    'permiso_venta_restriccion': (5, 'Permiso de venta (Restriccion)'),
}


class EventNotificationCadena(models.Model):
    """EventNotificationCadena: Notificacion de eventos, por cadena

    Campos definidos:

        bloque, banca, distribuidor, agencia, taquilla(entero): a la
            cual puede pertenecer la Notificacion

        data_origin(integer): Tipo de origen de la data

        data(json): Data correspondiente a la actualizacion

        date_production(datetime): Fecha y hora de envio

    Dichas notificaciones de envian en los modulos respectivos, dependiendo de su tipo
    """

    bloque = models.IntegerField(
        null=True,
        blank=True
    )
    banca = models.IntegerField(
        null=True,
        blank=True
    )
    distribuidor = models.IntegerField(
        null=True,
        blank=True
    )
    agencia = models.IntegerField(
        null=True,
        blank=True
    )

    taquilla = models.IntegerField(
        null=True,
        blank=True
    )

    data_origin = models.IntegerField(
        choices=[
            types_notification_cadena['preferencia'],
            types_notification_cadena['factor_riesgo'],
            types_notification_cadena['mensajes'],
            types_notification_cadena['permiso_venta'],
        ],
        editable=False
    )

    data = JSONField(
        null=True,
        blank=True
    )

    date_production = models.DateTimeField(
        db_index=True,
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = ('Actualizacion por comercializadora')
        verbose_name_plural = ('Actualizaciones por comercializadoras')

    def get_object(self):
        """
        Retorna el objeto al cual pertenece el factor de riesgo
        """
        return self.comercializadora.get_object()

    def __str__(self):
        return 'Notificacion de eventos, por cadena'


"""
//////////////////////////////////////////////////////////////////////////////////////////////
        Nuevos modelos de preferencias
/////////////////////////////////////////////////////////////////////////////////////////////

"""


class GroupPreferences(models.Model):
    """GroupPreferences: Grupo de preferencias

    Campos definidos:

        name(string): Nombre del grupo

        codename(string): Codigo del grupo

        order(entero): Orden del grupo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre (*)',
        help_text='Ingrese el nombre para el grupo de preferencia'
    )

    codename = models.CharField(
        max_length=100,
        verbose_name='Codename (*)',
        help_text='Ingrese el codename para el grupo de preferencia'
    )

    order = models.IntegerField(
        default=1,
        verbose_name='Orden (*)',
        help_text='Ingrese el orden del grupo de preferencia'
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
        verbose_name = ('Grupo de preferencia')
        verbose_name_plural = ('Grupos de preferencias')

    def __str__(self):
        return '{0}'.format(self.name)


class TypePreferences(models.Model):
    """TypePreferences: Tipos de preferencias por comercializadora

    Campos definidos:

        name(string): nombre del tipo preferencia

        codename(string): texto en codigo del tipo de preferencia

        comparison(entero): entero para comparar las preferencias
            en los distintos niveles de la cadena

        order(entero): Orden de la preferencia dentro del grupo

        edit(booleano): Bandera que decide si es una preferencia editable

        distribute(booleano): Bandera que decide si es una preferencia distribuida

        group(foreing): Relacion con GroupPreferences

        profile(many): Relacion muchos a muchos que define los perfiles que pueden editar
        la preferencia

        heredity(booleano): Bandera que indica si una preferencia puede ser o no hereditaria

        created_at y updated_at: registros de creacion y actualizacion.
    """

    OLD_PREFERENCES = {
        'preference_amount_min': 'montomin',
        'preference_amount_max': 'montomax',
        'preference_amount_price_max': 'montomax_ganancia',
        'preference_quantity_combinations_max': 'cantidad_apuesta_max',
        'preference_quantity_combinations_min': 'cantidad_apuesta_min',
        'preference_time_expire_max': 'tiempoexpiracion',
        'preference_quantity_combinations_male_max': 'parley_machos_max',
        'preference_quantity_combinations_male_min': 'parley_machos_min',
        'preference_quantity_combinations_female_max': 'parley_hembras_max',
        'preference_quantity_combinations_female_min': 'parley_hembras_min',
        'preference_amount_price_clone_max': 'parley_clonados_maxima_ganancia',
        'preference_amount_rental': 'monto_alquiler',
        'preference_amount_rental_frequency': 'frecuencia_monto_alquiler',
        'preference_queda_frequency': 'frecuencia_queda',
        'preference_quantity_combinations_draw_max': 'parley_empates_max',
        'preference_title': 'ticket_titulo',
        'preference_foot': 'ticket_pie',
    }

    name = models.CharField(
        max_length=100,
        verbose_name='Nombre (*)',
        help_text='Ingrese el nombre para el tipo de preferencia'
    )

    codename = models.CharField(
        max_length=100,
        verbose_name='Codename (*)',
        help_text='Ingrese el codename para el tipo de preferencia'
    )

    comparison_codenames = {
        'codename_min': 1,
        'codename_max': 2,
        'codename_free': 3,
    }

    choices_comparison = [
        [1, 'Menor'],
        [2, 'Mayor'],
        [3, 'Libre']
    ]

    comparison_type = {
        'codename_int': 1,
        'codename_decimal': 2,
        'codename_string': 3,
    }

    choices_type = [
        [1, 'Entero'],
        [2, 'Decimal'],
        [3, 'String']
    ]

    comparison = models.IntegerField(
        choices=choices_comparison,
        verbose_name='Compraracion nivel (*)',
        help_text='Seleccione la compraracion de nivel'
    )

    type_data = models.IntegerField(
        choices=choices_type,
        verbose_name='Tipo de dato (*)',
        help_text='Seleccione el tipo de dato'
    )

    order = models.IntegerField(
        default=1,
        verbose_name='Orden (*)',
        help_text='Ingrese el orden del tipo de preferencia'
    )

    edit = models.BooleanField(
        default=True,
        verbose_name='Â¿Editable? ',
        help_text='Seleccione si es una preferencia editable'
    )

    distribute = models.BooleanField(
        default=False,
        verbose_name='Â¿Distribuida? ',
        help_text='Seleccione si es una preferencia distribuida'
    )

    group = models.ForeignKey(
        'admin_permisologia.Groups',  # Grupo de permisología que agrupa las preferencias
        on_delete=models.CASCADE,
    )

    profile = models.ManyToManyField(
        'admin_users.UserProfile',
        blank=True,
        symmetrical=False,
        verbose_name='Perfiles de configuracion (*)',
        help_text='Seleccione los perfiles de usuario que editan la preferencia'
    )

    heredity = models.BooleanField(
        default=False,
        verbose_name='Â¿Hereditaria? ',
        help_text='Seleccione si es una preferencia heredada'
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
        verbose_name = ('Tipo de preferencia')
        verbose_name_plural = ('Tipos de preferencias')
        ordering = ['name', ]

    def __str__(self):
        return '{0}'.format(self.name)

    def get_profiles(self):
        return '\n'.join([obj.nombre for obj in self.profile.all()])


class DefaultPreferences(models.Model):
    """DefaultPreferences: Preferencias por defecto

    Campos definidos:

        value(string): Valor asociado al tipo de preferencia

        default(booleano): Bandera que decide si es un valor por defecto

        typepreference(foreing): Relacion con TypePreferences

        created_at y updated_at: registros de creacion y actualizacion.
    """
    value = models.CharField(
        max_length=100,
        verbose_name='Valor (*)',
        help_text='Ingrese el valor de la data'
    )

    default = models.BooleanField(
        default=False,
        verbose_name='Â¿Por defecto?',
        help_text='Seleccione solo si esta es la preferecnia por defecto, para '
                  'el tipo de preferencia asociada y la comercialzadora.'
    )

    typepreference = models.ForeignKey(
        'admin_comercializacion.TypePreferences',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
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
        verbose_name = ('Preferencia por defecto')
        verbose_name_plural = ('Preferencias por defecto')

    def __str__(self):
        return '{0}'.format(self.value)


class Preferences(ProtectDelete, models.Model):
    """Preferences: Preferencias para la cadena

    Campos definidos:
        value(string): Valor de la preferencia

        typepreference(foreing): Relacion con TypePreferences

        comercializacion(foreing): Relacion con Comercializadora

        created_at y updated_at: registros de creacion y actualizacion.
    """
    value = models.CharField(
        max_length=100,
        null=True,
        blank=True,
        verbose_name='Valor'
    )

    typepreference = models.ForeignKey(
        'admin_comercializacion.TypePreferences',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    comercializacion = models.ForeignKey(
        'admin_finanzas.Comercializadora',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    distribute = models.BooleanField(
        default=False,
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
        verbose_name = ('Preferencia de una comercializadora')
        verbose_name_plural = ('Preferencias de las comercializadoras')
        ordering = ['-created_at']

    def __str__(self):
        return 'Preferencia {0} para {1}'.format(
            self.typepreference.name,
            self.comercializacion)

    def get_ref_related_historic(self):
        """
        Retorna una relaciÃ³n de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.comercializacion.get_object().__module__.split('.')[0],
            self.comercializacion.get_object().__class__.__name__.lower(),
            self.comercializacion.get_object_id()
        )

# =============================================================
# =============================================================
# ====================Modelos auditados========================


auditoria.register(
    Operadoras,
    Bloques,
    Bancas,
    Distribuidores,
    Agencias,
    Taquillas,
    UsuariosTaquilla,
    Cupos,
    Porcentajes,
    FactorRiesgo,
    Preferences,
    TypePreferences,
)
# =============================================================
# =============================================================
# =============================================================
