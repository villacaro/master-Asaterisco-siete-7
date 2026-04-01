# -*- coding: utf-8 -*-
from datetime import timedelta

from admin_asterisco7.settings import (
    CACHES_CONF_TIME, DEBUG, FORMAT_STR_DATE_2, FORMAT_STR_DATETIME, FORMAT_STR_TIME, MEDIA_URL,
)
from admin_historic import auditoria
from admin_lib.util_models import BaseGenericProcessManagerCache, BaseGenericProcessModelCache, ProtectDelete
from admin_principal.security import Security
from crequest.middleware import CrequestMiddleware
from django.core.cache import cache
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.utils.timezone import now
from jsonfield import JSONField

# â”€â”€â”€ Sistema Asterisco Siete (*7) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
types_notification = {
    'data_type_origin': {
        'preferencias':       (0, 'Preferencias'),
        'deporte':            (1, 'LoterÃ­as'),            # antes: TipoProducto
        'temporada':          (2, 'Tipos de Sorteo'),     # antes: PeriodoSorteo
        'jornada':            (3, 'Horarios de Sorteo'),  # antes: Fechas
        'equipos':            (4, 'Animalitos/Figuras'),  # antes: ModalidadJuego
        'encuentro':          (5, 'Sorteos del dÃ­a'),     # antes: Sorteo
        'encuentro_modalidad':(6, 'Resultados LoterÃ­a'),  # antes: Referencias
        'jugada':             (7, 'Tipos de Jugada'),     # antes: Logros
        'grupos_juego':       (8, 'Grupos de Venta'),     # antes: Grupos de juego
    },
}


class EventNotification(models.Model):
    """EventNotification: Notificacion de eventos - Sistema Asterisco Siete (*7)

    Campos definidos:
        sistema(foreign): sistema de juego al que pertenece la notificacion

        data_origin(entero): entero tipo choices â€” origen del evento:
            0 = Preferencias
            1 = LoterÃ­as            (antes: TipoProducto)
            2 = Tipos de Sorteo     (antes: PeriodoSorteo)
            3 = Horarios de Sorteo  (antes: Fechas)
            4 = Animalitos/Figuras  (antes: ModalidadJuego)
            5 = Sorteos del dÃ­a     (antes: Sorteo)
            6 = Resultados LoterÃ­a  (antes: Referencias)
            7 = Tipos de Jugada     (antes: Logros)
            8 = Grupos de Venta     (antes: Grupos de juego)

        pk_origin(entero): pk del objeto origen
        data(json): json con toda la data del objeto actualizada
        in_production(booleano): indica si ya se estÃ¡ descargando
        date_production(datetime): fecha y hora de puesta en producciÃ³n
    """
    sistema = models.IntegerField(
        db_index=True,
        null=True,
        editable=False
    )

    CHOICES_data_type_origin = [
        (0, 'Preferencias'),
        (1, 'LoterÃ­as'),
        (2, 'Tipos de Sorteo'),
        (3, 'Horarios de Sorteo'),
        (4, 'Animalitos/Figuras'),
        (5, 'Sorteos del dÃ­a'),
        (6, 'Resultados LoterÃ­a'),
        (7, 'Tipos de Jugada'),
        (8, 'Grupos de Venta'),
    ]

    data_origin = models.IntegerField(
        choices=CHOICES_data_type_origin,
        editable=False
    )
    pk_origin = models.IntegerField(
        editable=False
    )
    data = JSONField(
        editable=False
    )
    in_production = models.BooleanField(
        db_index=True,
        default=False,
        editable=False
    )
    date_production = models.DateTimeField(
        db_index=True,
        null=True,
        editable=False,
        # auto_now=True
    )

    class Meta:
        verbose_name = ('Actualizacion')
        verbose_name_plural = ('Actualizaciones')

    def __str__(self):
        return '{0}'.format(self.get_data_origin_display())

    def get_data_keys(self):
        """Retorna pares [etiqueta, valor] para mostrar en el panel de admin.
        Sistema Asterisco Siete (*7).
        """
        if self.data_origin == 0:
            # Preferencias â€” sin campos adicionales por ahora
            pass

        elif self.data_origin == 1:
            # â”€â”€ LoterÃ­as (antes: TipoProducto) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['Nombre LoterÃ­a',    self.data['nombre']],
                ['Logo',              self.data['logo']],
                ['Estado',            self.data.get('admin_status.Status', '-')],
                ['Orden',             self.data['orden']],
                ['LÃ­mite de Venta',   self.data.get('limite_general', '0.00')],
                ['Grupos de Venta',   self.data.get('grupos', '')],
            ]

        elif self.data_origin == 2:
            # â”€â”€ Tipos de Sorteo (antes: PeriodoSorteo) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['Tipo',        self.data['temporada']],
                ['Logo',        self.data['logo']],
                ['ID LoterÃ­a',  self.data['deporte_id']],
            ]

        elif self.data_origin == 3:
            # â”€â”€ Horarios de Sorteo (antes: Fechas) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['Sorteo',          self.data['jornada']],
                ['Hora de Cierre',  self.data.get('hora_cierre', self.data.get('jornada', '-'))],
                ['Valor MÃ­nimo',    self.data.get('valor', '0.00')],
                ['Acumulado/Potazo',self.data.get('acumulado', 'N/A')],
                ['ID Tipo',         self.data.get('liga_id', '-')],
                ['Sistema',         self.data.get('deporte_id', '-')],
            ]

        elif self.data_origin == 4:
            # â”€â”€ Animalitos / Figuras (antes: ModalidadJuego) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['Nombre / Animal',  self.data['nombre']],
                ['NÃºmero',           self.data.get('numero', '-')],
                ['Imagen',           self.data['logo']],
                ['ID LoterÃ­a',       self.data.get('deporte_id', '-')],
            ]

        elif self.data_origin == 5:
            # â”€â”€ Sorteos del dÃ­a (antes: Sorteo) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['Sorteo',              self.data.get('nombre_sorteo', self.data.get('jornada_id', '-'))],
                ['Hora',                self.data['hora']],
                ['Fecha',               self.data['fecha']],
                ['Hora de Cierre',      self.data['hora_cierre']],
                ['Estatus',             self.data['admin_status.Status']],
                ['Grupos de Venta',     self.data['grupo_id']],
                ['ID Tipo de Sorteo',   self.data['jornada_id']],
                ['ID LoterÃ­a',          self.data['deporte_id']],
                ['Sistema',             self.data['sistema']],
            ]

        elif self.data_origin == 6:
            # â”€â”€ Resultados LoterÃ­a (antes: Sorteo modalidad) â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['NÃºmero Ganador',   self.data.get('numero', self.data.get('ref_mod', '-'))],
                ['Signo',            self.data.get('signo', 'N/A')],
                ['Fecha Registro',   self.data.get('fecha_registro', '-')],
                ['ID Sorteo',        self.data.get('encuentro_id', '-')],
                ['ID LoterÃ­a',       self.data.get('deporte_id', '-')],
                ['Sistema',          self.data.get('sistema', '-')],
                ['Origen',           self.data.get('origen', '-')],
            ]

        elif self.data_origin == 7:
            # â”€â”€ Tipos de Jugada (antes: Logros) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            # Triple, Terminal, 4 dÃ­gitos, Animalitos, etc.
            return [
                ['Tipo de Jugada',       self.data.get('tipo_jugada',
                                             self.data.get('pertenece', '-'))],
                ['Multiplicador Pago',   self.data.get('factor_pago',
                                             self.data.get('logro_americano', '-'))],
                ['Monto MÃ¡ximo Apuesta', self.data.get('monto_max_apuesta',
                                             self.data.get('logro_europeo', '-'))],
                ['Signo Requerido',      self.data.get('usa_signo', 'No')],
                ['Referencia',           self.data['ref']],
                ['Origen',               self.data['origen']],
                ['Sistema',              self.data['sistema']],
            ]

        elif self.data_origin == 8:
            # â”€â”€ Grupos de Venta (antes: Grupos de juego) â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
            return [
                ['Nombre',      self.data['nombre']],
                ['Orden',       self.data['orden']],
                ['ID LoterÃ­a',  self.data.get('liga_id', '-')],
                ['Sistema',     self.data.get('deporte_id', '-')],
            ]

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        """URLs de detalle â€” Sistema Asterisco Siete (*7)."""
        if self.data_origin == 0:
            pass
        elif self.data_origin == 1:
            # LoterÃ­as
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse('admin_juego_deportes_detail', kwargs={'pk': self.pk_origin})
            except NoReverseMatch:
                return '/admin/'
        elif self.data_origin == 2:
            # Tipos de Sorteo
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse('admin_juego_temporadas_detail', kwargs={'pk': self.pk_origin})
            except NoReverseMatch:
                return '/admin/'
        elif self.data_origin == 3:
            # Horarios de Sorteo
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse('admin_juego_jornadas_detail', kwargs={'pk': self.pk_origin})
            except NoReverseMatch:
                return '/admin/'
        elif self.data_origin == 4:
            # Animalitos
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse('admin_juego_equipos_detail', kwargs={'pk': self.pk_origin})
            except NoReverseMatch:
                return '/admin/'
        elif self.data_origin == 5:
            # Sorteos del dÃ­a
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse('admin_juego_encuentros_detail', kwargs={'pk': self.pk_origin})
            except NoReverseMatch:
                return '/admin/'
        elif self.data_origin == 8:
            # Grupos de Venta
            from django.urls import reverse, NoReverseMatch
            try:
                return reverse('admin_juego_gruposjuego_detail', kwargs={'pk': self.pk_origin})
            except NoReverseMatch:
                return '/admin/'

    def get_absolute_url_str(self):
        if self.data_origin == 6:
            # Resultado LoterÃ­a â€” redirige al sorteo
            return '/asterisco7/resultado/{0}/ver/#resultado_{1}'.format(
                self.data.get('encuentro_id', self.pk_origin),
                self.pk_origin
            )
        elif self.data_origin == 7:
            # Tipo de Jugada â€” redirige a la asignaciÃ³n de logro existente
            return '/asterisco7/jugada/{0}/ver/#jugada_{1}'.format(
                self.data.get('encuentro_id', self.pk_origin),
                self.pk_origin
            )
        return None


def get_sistema_juego(return_object=False):
    request = CrequestMiddleware.get_request()
    if request is None:
            # si no hay request quiere decir que no se ha ingresado por el panel
            # entonces no se guarda la notificacion, puesto que no hay manera
            # de saber a quien pertenece
        return None

    security = Security()
    try:
        # Si hay poblemas tambien al obtener la session
        # no se guarda la auditoria, puesto que no hay session con que vincular
        if return_object:
            return security.get_sistemaJuego(request)
        else:
            return security.get_sistemaJuego(request).pk
    except Exception:
        return None


class CachinEvent(object):
    """
    Clase generica usada para crear
    las notificaciones de una forma dinamica
    """
    broadcast_automatic = True

    def save(self, *args, **kwargs):
        super(CachinEvent, self).save()
        if self.broadcast_automatic:
            self.broadcast()

    @staticmethod
    def broadcast_manual(json_new, pk, data_origin,
                         sistema=None, day=None, force=False):

        if day:
            if day != now().date() and not DEBUG:
                return False

        if not sistema:
            sistema = get_sistema_juego(return_object=True)

        if sistema:
            if sistema.notificacion_automatica:

                block = cache.get('{0}_{1}'.format('block_event', sistema.pk))
                if block:
                    in_production = False
                else:
                    in_production = True

                date_production = now()
            else:
                in_production = False
                date_production = None
            sistema = sistema.pk
        else:
            # Si no hay sistema no se genera nada
            return False

        try:
            notificacion = EventNotification.objects.get(
                pk_origin=pk,
                data_origin=data_origin,
                sistema=sistema,
            )

            if notificacion.data == json_new and not force:
                """
                Si la data es igual no se envia
                """
                return False

            notificacion.data = json_new
            notificacion.in_production = in_production
            notificacion.date_production = date_production
            notificacion.save(
                update_fields=[
                    'data',
                    'in_production',
                    'date_production'])

        except EventNotification.DoesNotExist:
            EventNotification.objects.update_or_create(
                sistema=sistema,
                data_origin=data_origin,
                pk_origin=pk,
                defaults={
                    'data': json_new,
                    'in_production': in_production,
                    'date_production': date_production,
                }
            )

    def broadcast(self, sistema=None, day=None):
        CachinEvent.broadcast_manual(
            json_new=self.set_cache(cache_standar=False),
            pk=self.pk,
            data_origin=self.name_data_type_origin,
            sistema=sistema,
            day=day,
        )

    def get_cache(self):
        json = cache.get('{0}{1}'.format(self.name_cache, self.pk))
        if not json:
            json = self.set_cache()
        return json

    def get_cache_exists(self):
        json = cache.get('{0}{1}'.format(self.name_cache, self.pk))
        return json


class SistemaJuegoManager(models.Manager):
    """
    Clase Manager del sistema de juego, aqui se definen
    los metodos de busqueda del mismo dado una comercializadora
    """

    def get_sistema_juego_by_comercializadora(self, comercializadora):
        """
        Obtiene y devuelve el sistema de juego asociado a una comercializadora
        """
        sistemajuego = cache.get(
            'sistemajuego_{0}'.format(
                comercializadora.pk))
        if not sistemajuego:
            while True:
                if ((comercializadora.get_type_codename() == 'userprofile_operadora') or
                        (
                            comercializadora.get_type_codename() in ['userprofile_banca', 'userprofile_bloque'] and
                    comercializadora.get_object().is_sistema_juego is True
                )
                ):
                    break
                else:
                    comercializadora = comercializadora.get_origen()
            sistemajuego = comercializadora.sistemajuego
            cache.set(
                'sistemajuego_{0}'.format(comercializadora.pk),
                sistemajuego,
                CACHES_CONF_TIME['registros_db']['session_expire']
            )
        return sistemajuego

    def get_sistema_resultados_by_comercializadora(self, comercializadora):
        """
        Obtiene y devuelve el sistema de juego asociado a una comercializadora
        """
        sistemaresultados = cache.get(
            'sistemaresultados_{0}'.format(
                comercializadora.pk))
        if sistemaresultados is None:
            while comercializadora:
                if ((comercializadora.get_type_codename() == 'userprofile_operadora') or
                        (
                            comercializadora.get_type_codename() in ['userprofile_banca', 'userprofile_bloque'] and
                    (
                                comercializadora.get_object().is_sistema_juego is True or
                                comercializadora.get_object().is_resultados is True
                            )
                )
                ):
                    break
                else:
                    comercializadora = comercializadora.get_origen()

            if not comercializadora:
                sistemaresultados = False
            else:
                sistemaresultados = comercializadora.sistemajuego

            cache.set(
                'sistemaresultados_{0}'.format(comercializadora.pk),
                sistemaresultados,
                CACHES_CONF_TIME['registros_db']['session_expire']
            )
        return sistemaresultados

    def get_sistema_logros_by_comercializadora(self, comercializadora):
        """
        Obtiene y devuelve el sistema de juego asociado a una comercializadora
        """
        sistemalogros = cache.get(
            'sistemalogros_{0}'.format(
                comercializadora.pk))
        if sistemalogros is None:
            while comercializadora:
                if ((comercializadora.get_type_codename() == 'userprofile_operadora') or
                        (
                            comercializadora.get_type_codename() in ['userprofile_banca', 'userprofile_bloque'] and
                    (
                                comercializadora.get_object().is_sistema_juego is True or
                                comercializadora.get_object().is_logros is True
                            )
                )
                ):
                    break
                else:
                    comercializadora = comercializadora.get_origen()

            if not comercializadora:
                sistemalogros = False
            else:
                sistemalogros = comercializadora.sistemajuego
            cache.set(
                'sistemalogros_{0}'.format(comercializadora.pk),
                sistemalogros,
                CACHES_CONF_TIME['registros_db']['session_expire']
            )
        return sistemalogros

    def get(self, *args, **kwargs):
        sistemajuego = None

        key = None
        if len(kwargs) == 1:
            if kwargs.get('pk'):
                key = 'pk'
            elif kwargs.get('comercializadora_id'):
                key = 'comercializadora_id'

        if key:
            sistemajuego = cache.get(
                '{0}_{1}'.format('sistemajuego', kwargs.get(key))
            )
            if not sistemajuego:
                sistemajuego = super(
                    SistemaJuegoManager, self).get(
                    *args, **kwargs)
                cache.set(
                    '{0}_{1}'.format('sistemajuego', kwargs.get(key)),
                    sistemajuego,
                    CACHES_CONF_TIME['registros_db']['sistemajuego'],
                )
            return sistemajuego
        else:
            return super(SistemaJuegoManager, self).get(*args, **kwargs)


class SistemaJuego(models.Model):
    """SistemaJuego: Sistema de juego

    Campos definidos:
        nombre(string): nombre del sistema de juego

        logo(imagen): logo del sistema de juego

        banner(imagen): Banner del sistema de juego

        user(foreign): usuario al cual pertenece el usuario
            este campo esta en des uso, debe eliminarse cuando se termine
            la migracion de data

        comercializadora(foreign one): comercializadora a la cual pertenece el
            sistema de juego, puede ser una operadora o una banca

        is_resultados y is_logros: son banderas usadas para saber que sistemas de juego tienen
            esta opcion adicional, para comercializadoras que no manejan su propio sistema de juego

        created_at y updated_at: registros de creacion y actualizacion.
    """

    nombre = models.CharField(
        max_length=200,
        blank=True,
        null=True
    )
    logo = models.ImageField(
        upload_to='sistema',
        blank=True,
        null=True
    )
    banner = models.ImageField(
        upload_to='sistema',
        blank=True,
        null=True
    )
    comercializadora = models.ForeignKey(
        'admin_finanzas.Comercializadora',
        on_delete=models.CASCADE,
        related_name='sistemas_juego_principal',
        null=True, blank=True,
    )
    is_resultados = models.BooleanField(
        default=False,
        editable=False,
        verbose_name='Â¿Permite cargar resultados?'
    )
    is_logros = models.BooleanField(
        default=False,
        editable=False,
        verbose_name='Â¿Permite cargar logros?'
    )
    CHOICES_NOTIFICACION = (
        (True, 'AutomÃ¡tica'),
        (False, 'Manual'),
    )
    notificacion_automatica = models.BooleanField(
        verbose_name='Tipo de actualizaciÃ³n (*)',
        help_text='Seleccione el tipo de actualizaciÃ³n que desea',
        choices=CHOICES_NOTIFICACION,
        default=False,
    )
    theme = models.ForeignKey(
        'admin_themes.Theme',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    company = models.ForeignKey(
        'admin_finanzas.Comercializadora',
        on_delete=models.CASCADE,
        related_name='sistemas_juego_company',
        null=True, blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    objects = SistemaJuegoManager()

    audit_exclude = ('updated_at', )

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Sistema de juego')
        verbose_name_plural = ('Sistemas de juegos')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}'.format(self.nombre)

    def save(self, *args, **kwargs):
        super(SistemaJuego, self).save(*args, **kwargs)
        self.cache_clear()

    def cache_clear(self):
        cache.delete(
            '{0}_{1}'.format('sistemajuego', self.pk)
        )

    def get_lower_ascci(self):
        """
        Retorna el nombre sel sistema de juego eliminando todos los signos
        de puntuacion
        """
        import re
        return re.sub(r'[^\w]', '-', self.nombre.lower())

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_sistemajuego_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    def get_logo(self):
        return '' if not self.logo else '{0}{1}'.format(MEDIA_URL, self.logo)

    def get_company(self, json=False):
        if self.company_id:
            company = cache.get('{0}_{1}'.format('company', self.company_id))
            if not company:
                company = self.company
                cache.set(
                    '{0}_{1}'.format('company', self.company_id),
                    company,
                    CACHES_CONF_TIME['registros_db']['company']
                )

            if json:
                respond = {
                    'company_name': company.name,
                    'company_logo': ''
                }
                if company.logo:
                    respond['company_logo'] = '{0}{1}'.format(
                        MEDIA_URL, company.logo)
                return respond
            else:
                return company

        if json:
            return {
                'company_name': '',
                'company_logo': ''
            }
        else:
            return None

    def get_theme(self, json=False):

        if self.theme_id:
            theme = cache.get('{0}_{1}'.format('theme', self.theme_id))
            if not theme:
                theme = self.theme
                cache.set(
                    '{0}_{1}'.format('theme', self.theme_id),
                    theme,
                    CACHES_CONF_TIME['registros_db']['theme']
                )

            if json:
                return {
                    'theme_media_url': theme.media_url,
                    'theme_colors': [
                        obj for obj in theme.color_set.all().values(
                            'color', 'color_type'
                        )
                    ]
                }
            else:
                return theme

        else:
            if json:
                return {
                    'theme_media_url': '',
                    'theme_colors': []
                }

        return None


class OperadoraLoteria(CachinEvent, models.Model):
    """OperadoraLoteria: OperadoraLoteria

    Campos definidos:
        nombre(string): nombre del deporte

        logo(imagen): logo del deporte

        orden(entero): numero que indica el orden de impresion de los deportes

        orden_equipos(entero): entero tipo choice que indica el orden de impreseion de los equipos

        count_apuesta(entero): numero de apuestas por encuentro de un mismo deporte,
            Ejemplo: un encuentro de futbol, en caso de esta variable ser 1, solo puedo apostar
            a un logro del mismo encuentro

        fondoweb(imagen): fondo web o baner, para usos graficos

        cantidad(entero): se debe indicar si el deporte es por Sorteo
            de 2 o mas equipos

        cantidad_tiempos(entero): numero que indica la cantidad de tiempos
            de juego, ejemplo en futbol son 2 tiempos normalmente

        runline_positivo(booleano): indica si el runline con referencia y logro positivo
            se permiten para el deporte

        ganador_empate_not_null(booleano): indica al momento de procesar el algotitmo de ganador,
            si detecta un empate no deje anular la jugada, sino la coloca como perdida

        resultado(CharField): referencia de victoria del deporte.(Puntaje o posicion)

        created_at y updated_at: registros de creacion y actualizacion.
    """
    prefix_filter = 'deporte'
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre del deporte'
    )
    logo = models.ImageField(
        upload_to='deportes',
        blank=True,
        null=True,
        verbose_name='Logo ',
        help_text='Ingrese logo del deporte'
    )
    orden = models.IntegerField(
        verbose_name='Orden (*)',
        help_text='Ingrese la numeraciÃ³n de orden'
    )
    CHOICES_ORDEN_EQUIPOS = (
        (1, 'Home/Visitante'),
        (2, 'Visitante/Home'),
    )
    orden_equipos = models.IntegerField(
        verbose_name='Orden de equipos (*)',
        help_text='Seleccione el orden de impresion de logros de los equipos',
        choices=CHOICES_ORDEN_EQUIPOS,
        default=2,
    )
    CHOICES_COUNT_APUESTA = (
        (1, '1 apuesta'),
        (2, '2 apuestas'),
        (3, '3 apuestas'),
        (4, '4 apuestas'),
        (5, '5 apuestas'),
    )
    count_apuesta = models.IntegerField(
        verbose_name='NÃºmero mÃ¡ximo de apuesta por encuentro (*)',
        help_text='Indique el nÃºmero de logros que se deben apostar como mÃ¡ximo por'
        ' cada encuentro',
        choices=CHOICES_COUNT_APUESTA,
        default=5,
    )
    fondoweb = models.ImageField(
        upload_to='deportes/fondos',
        blank=True,
        null=True,
        verbose_name='Fondo ',
        help_text='Ingrese fondo del deporte'
    )
    CHOICES_CANTIDAD_EQUIPOS = (
        (2, '2 participantes'),
        (1, '+2 participantes'),
    )
    cantidad = models.IntegerField(
        verbose_name='Participantes (*)',
        help_text='Seleccione la cantidad de equipos a enfrentarse por encuentro',
        choices=CHOICES_CANTIDAD_EQUIPOS
    )
    cantidad_tiempos = models.IntegerField(
        verbose_name='Cantidad de tiempos por encuentro (*)',
        help_text='Ingrese la cantidad de tiempos por encuentro mayor o igual a 2'
    )
    runline_positivo = models.BooleanField(
        default=False,
        verbose_name='Â¿Desea poder cargar logros con runline y referencia positiva para este  deporte? ',
        help_text='Seleccione este campo solo si esta seguro de permitir '
        'editar el runline sin restriccion de positivos'
    )
    ganador_empate_not_null = models.BooleanField(
        default=False,
        verbose_name='Â¿Al procesar resultados, la modalidad ganador no se anula si detecta un empate? ',
        help_text='Seleccione este campo solo si esta seguro de que el '
        ' algotitmo de resultados no debe poner como anuladas las jugadas '
        ' relacionadas a ganador si hay un empate'
    )

    resultado_codenames = {
        "codename_puntaje": '-',
        "codename_posicion": '+',
    }
    choices_resultado = [
        ['-', "Por puntaje"],
        ['+', "Por posicion"]
    ]
    resultado = models.CharField(
        verbose_name='Modo de ganar (*)',
        choices=choices_resultado,
        default='-',
        max_length=1,
        help_text="Seleccione el modo de ganar en un deporte"
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
        db_tablespace = 'ts_parley'
        verbose_name = ('Deporte')
        verbose_name_plural = ('OperadoraLoteria')
        ordering = ['nombre']

    def __str__(self):
        return '{0}'.format(self.nombre)

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__encuentro__jornada__temporadas__torneo__deporte_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_deportes_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    def get_logo(self):
        return '' if not self.logo else '{0}{1}'.format(MEDIA_URL, self.logo)

    def get_fondo(self):
        return '' if not self.fondoweb else '{0}{1}'.format(
            MEDIA_URL, self.fondoweb)

    def get_filter_orden_equipos(self):
        """
        Devuelve una cadena manejable para aplicar filtros al imprimir los
        equipos de un encuentro
        """
        if self.orden_equipos == 2:
            return '-indice'
        else:
            return 'indice'

    name_cache = 'deporte_json_event'
    name_cache_deporte_grupo = 'deporte_grupo_by_encuentro_json_event'
    name_data_type_origin = types_notification[
        'data_type_origin']['deporte'][0]

    def set_cache(self, cache_standar=True):
        json = {
            'nombre': self.nombre,
            'logo': self.get_logo(),
            'orden': self.orden,
            'fondo': self.get_fondo(),
            'orden_equipos': self.orden_equipos,
            'count_apuesta': self.count_apuesta,
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )
        if cache_standar is False:
            if getattr(self, '_add_grupos', None):
                ModalidadJuego = [
                    {"pk": jugador_tipo["pk"] * -1}
                    for jugador_tipo in self.jugadortipo_set.all().values("pk")
                ]

                grupos = self.deportes_grupos_set.all().order_by("grupo__orden")
                json["grupos"] = []
                if ModalidadJuego:
                    json["grupos"].append(
                        {"pk": -1, "ModalidadJuego": ModalidadJuego}
                    )

                for obj in grupos:
                    grupo = obj.grupo
                    ModalidadJuego = []
                    for modalidad in grupo.modalidades_grupos_set.all() \
                            .order_by("modalidad__orden"):
                        if modalidad.deporte_restriccion.filter(
                            pk=self.pk
                        ).exists():
                            continue
                        else:
                            ModalidadJuego.append(
                                {"pk": modalidad.modalidad_id}
                            )
                    if ModalidadJuego:
                        json["grupos"].append(
                            {"pk": grupo.pk, "ModalidadJuego": ModalidadJuego}
                        )
                # se retorna en string
                json["grupos"] = '{0}'.format(json["grupos"])
        return json

    def save(self, *args, **kwargs):
        self._add_grupos = None
        if not self.pk:
            self._add_grupos = True
        super(OperadoraLoteria, self).save()


class TipoProducto(models.Model):
    prefix_filter = 'torneo'
    prefix_filter_plural = 'TipoProducto'
    """TipoProducto: TipoProducto

    Campos definidos:
        nombre(string): nombre del torneo o liga

        logo(imagen): logo del torneo

        orden(entero): numero que indica el orden de impresion de los deportes

        fondoweb(imagen): fondo web o baner, para usos graficos

        deporte(foreign): deporte al cual pertenece el torneo, ejemplo
            futbol copa mundial

        por_jornadas(booleano): bandera que indica si el torneo se juega
            por Fechas o no

        por_grupos(booleano): bandera que indica si el torneo se juega por grupos
            sirve por ejemplo para defirnir los grupos de un mundial

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre de la liga'
    )
    logo = models.ImageField(
        upload_to='eventos',
        blank=True,
        null=True,
        verbose_name='Logo ',
        help_text='Ingrese logo de la liga'
    )
    fondoweb = models.ImageField(
        upload_to='eventos/fondos',
        blank=True,
        null=True,
        verbose_name='Fondo ',
        help_text='Ingrese fondo de la liga'
    )
    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    por_jornadas = models.BooleanField(
        default=False,
        verbose_name='Liga por Fechas ',
        blank=True,
        help_text='De ser una liga que admite Fechas, seleccione el campo'
    )
    por_grupos = models.BooleanField(
        default=False,
        verbose_name='Liga por grupos ',
        blank=True,
        help_text='De ser una liga que admite grupos, seleccione el campo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('nombre', 'deporte')
        verbose_name = ('Liga')
        verbose_name_plural = ('Ligas')
        ordering = ['nombre', ]

    def __str__(self):
        return self.nombre

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__encuentro__jornada__temporadas__torneo_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_torneos_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    @property
    def has_jornadas(self):
        """
        propiedad que indica si es por Fechas
        """
        return self.por_jornadas

    def get_logo(self):
        return '' if not self.logo else '{0}{1}'.format(MEDIA_URL, self.logo)

    def get_fondo(self):
        return '' if not self.fondoweb else '{0}{1}'.format(
            MEDIA_URL, self.fondoweb)

    @property
    def loteria_display(self):
        """Institución a la que pertenece este tipo de producto."""
        return 'LOTERIA DE COJEDES'


class PeriodoSorteo(CachinEvent, models.Model):
    prefix_filter = 'temporada'
    prefix_filter_plural = 'temporadas'
    """PeriodoSorteo: PeriodoSorteo

    Campos definidos:
        nombre(string): nombre de la temporada

        status(foreign): estatus de la temporada, activa o suspendida
            por ejmplo

        fechaini(date): indica la fecha de inicio de la temporada

        fechafin(date): indica la fecha de fin de la temporada

        torneo(foreign): referencia al torneo que pertenece de x deporte

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=140,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre a la temporada'
    )
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    fechaini = models.DateField(
        verbose_name='Fecha de inicio (*)',
        help_text='Seleccione la fecha de inicio de la temporada'
    )
    fechafin = models.DateField(
        verbose_name='Fecha de fin (*)',
        help_text='Seleccione la fecha de fin de la temporada',
        db_index=True,
    )
    torneo = models.ForeignKey(
        'admin_juego.TipoProducto',
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

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('nombre', 'torneo')
        verbose_name = ('Temporada')
        verbose_name_plural = ('PeriodoSorteo')

    def __str__(self):
        return self.nombre

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__encuentro__jornada__temporadas_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_temporadas_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    name_cache = 'temporada_json_event'
    name_data_type_origin = types_notification[
        'data_type_origin']['temporada'][0]

    broadcast_automatic = False

    def set_cache(self, cache_standar=True):
        json = {
            'temporada': self.nombre,
            'torneo': self.torneo.nombre,
            'logo': self.torneo.get_logo(),
            'fondo': self.torneo.get_fondo(),
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )

        if cache_standar is False:
            json['deporte_id'] = self.torneo.deporte_id
        return json


class ModalidadJuego(BaseGenericProcessModelCache, CachinEvent, models.Model):
    prefix_filter_plural = 'equipos'
    """ModalidadJuego: ModalidadJuego

    Campos definidos:
        nombre(string): nombre del equipo

        logo(imagen): imagen o logo del equipo

        deporte(foreign): deporte al que pertenece dicho equipo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=140,
        verbose_name='Nombre (*)',
        help_text='Ingrese un nombre para el equipo, '
                  'no pueden haber equipos con el mismo nombre en un deporte'
    )
    logo = models.ImageField(
        upload_to='equipos',
        blank=True,
        null=True,
        verbose_name='Logo ',
    )
    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
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

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    prefix_cache_manager = 'model_equipos'
    objects = BaseGenericProcessManagerCache()
    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('nombre', 'deporte')
        verbose_name = ('Equipo')
        verbose_name_plural = ('ModalidadJuego')

    def __str__(self):
        return self.nombre

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__detalle_encuentro__equipos_temporadas__equipo_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_equipos_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    name_cache = 'equipos_json_event'
    name_data_type_origin = types_notification[
        'data_type_origin']['equipos'][0]

    def get_logo(self):
        return '' if not self.logo else '{0}{1}'.format(MEDIA_URL, self.logo)

    def set_cache(self, cache_standar=True):
        json = {
            'nombre': str(self),
            'logo': self.get_logo(),
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )
        if cache_standar is False:
            json['deporte_id'] = self.deporte_id

        return json

    def get_ligas(self):
        return list(ModalidadProducto.objects.filter(
            equipo=self).values_list('liga__nombre', flat=True))


class ModalidadProducto(models.Model):
    """ModalidadProducto: ModalidadJuego por liga

    Campos definidos:
        liga(foreign): torneo al cual pertenece el equipo

        equipo(foreign): equipo asociado a la liga

        created_at y updated_at: registros de creacion y actualizacion.
    """
    liga = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    equipo = models.ForeignKey(
        'admin_juego.ModalidadJuego',  # TODO: revisar modelo destino
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
        db_tablespace = 'ts_parley'
        unique_together = ('equipo', 'liga')
        verbose_name = ('Equipo por liga')
        verbose_name_plural = ('ModalidadJuego por ligas')

    def __str__(self):
        return '{0} | {1}'.format(
            self.liga,
            self.equipo
        )

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.equipo.__module__.split('.')[0],
            self.equipo.__class__.__name__.lower(),
            self.equipo_id
        )


class TipoNumeroSorteo(models.Model):
    """TipoNumeroSorteo: Tipos de jugadores

    Campos definidos:
        nombre(string): nombre del tipo de jugado

        codename(string): codigo del tipo de jugador

        deporte(foreign): deporte al que pertenece dicho tipo de jugador

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=200,
        verbose_name='Tipo de jugador (*)',
        help_text='Ingrese un nombre para el tipo de jugador'
    )
    codename = models.CharField(
        max_length=200,
        editable=False
    )
    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
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

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('nombre', 'deporte')
        verbose_name = ('Tipo de jugador')
        verbose_name_plural = ('Tipos de jugadores')

    def __str__(self):
        return self.nombre

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__detalle_encuentro__jugador__tipo_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_jugadortipo_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'


class NumeroSorteo(models.Model):
    prefix_filter_plural = 'jugador'
    """NumeroSorteo: Jugadores

    Campos definidos:
        nombre(string): nombre del jugado

        tipo(foreign): tipo de jugador al que se hace referencia

        lateralidad(string): lateralidad del jugador

        foto(imagen): imagen del jugador

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=140,
        verbose_name='Nombre (*)',
        help_text='Ingrese un nombre para el jugador'
    )
    tipo = models.ForeignKey(
        'admin_juego.TipoNumeroSorteo',
        on_delete=models.CASCADE,
    )
    choices_lateralidad = (
        ('D', 'Derecho'),
        ('Z', 'Zurzo')
    )
    lateralidad = models.CharField(
        max_length=140,
        choices=choices_lateralidad,
        verbose_name='Lateralidad (*)',
        help_text='Ingrese la lateralidad del jugador'
    )
    foto = models.ImageField(
        upload_to='jugadores',
        blank=True,
        null=True
    )
    equipos = models.ManyToManyField(
        'ModalidadJuego',
        blank=True,
        symmetrical=False,
        verbose_name='Seleccione los equipos (*)',
        help_text='Seleccione los equipos a los que desea asignar el jugador.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('nombre', 'tipo')
        verbose_name = ('NumeroSorteo')
        verbose_name_plural = ('Jugadores')
        ordering = ['nombre', 'lateralidad']

    def __str__(self):
        return '{0}'.format(self.nombre)

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__detalle_encuentro__jugador_id'

    def get_label(self):
        return '({0}) {1}'.format(
            self.lateralidad,
            self.nombre
        )

    def get_equipos_all(self):
        json = []

        for equipo in self.equipos.all():
            json.append(equipo)
        return json

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_jugador_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    def get_display(self):
        return self.get_label()


class ModalidadPeriodo(models.Model):
    """ModalidadPeriodo: ModalidadJuego por temporada

    Campos definidos:
        temporada(foreign): temporada en la que esta un equipo

        equipo(foreign): equipo que esta en una temporada

        created_at y updated_at: registros de creacion y actualizacion.
    """
    temporada = models.ForeignKey(
        'admin_juego.PeriodoSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    equipo = models.ForeignKey(
        'admin_juego.ModalidadJuego',  # TODO: revisar modelo destino
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
        db_tablespace = 'ts_parley'
        unique_together = ('equipo', 'temporada')
        verbose_name = ('Equipo por temporada')
        verbose_name_plural = ('ModalidadJuego por temporadas')

    def __str__(self):
        return '{0} | {1}'.format(self.temporada, self.equipo)

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.temporada.__module__.split('.')[0],
            self.temporada.__class__.__name__.lower(),
            self.temporada_id
        )


class Fechas(CachinEvent, models.Model):
    prefix_filter_plural = 'Fechas'
    """Fechas: Fechas

    Campos definidos:
        jornada(string): nombre de la jornada

        status(foreign): estatus de la jornada

        temporadas(foreign): temporada a la que pertenece la jornada

        fechaini(date): indica la fecha de inicio de la jornada

        fechafin(date): indica la fecha de fin de la jornada

        parley(booleano): bandera que indica si en la jornada se vende
            parlay

        quiniela(booleano): bandera que indica si en la jornada se vende
            quiniela

        apuestasimple(booleano): bandera que indica si en la jornada se vende
            la apuesta simple

        sistema(foreign): sistema de juego al que pertenece la jornada

        count_encuentros(entero): numero de Sorteo que se habilitaran para la jornada,
            Este campo solo es usado cuando la jornada, tiene activa la quiniela,
            buscando validar si la quiniela esta completa o no para sus apuestas.

        monto_inicial(entero): monto en Bs del pote inicial, el acumulado con el
            que comenzara a jugar la quiniela

        valor(entero): Monto en Bs del valor que tendran los tickets, este campo,
            es solo estara activo en las Fechas con quiniela activa,

        created_at y updated_at: registros de creacion y actualizacion.
    """
    jornada = models.CharField(
        max_length=140,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre de la jornada'
    )
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    temporadas = models.ForeignKey(
        'admin_juego.PeriodoSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    fechaini = models.DateField(
        verbose_name='Fecha de inicio (*)',
        help_text='Fecha de inicio de la jornada'
    )
    fechafin = models.DateField(
        verbose_name='Fecha de fin (*)',
        help_text='Fecha de fin de la jornada',
        db_index=True,
    )
    parley = models.BooleanField(
        default=False,
        verbose_name='Permite la venta de parley? ',
        help_text='Seleccione este campo solo si la temporada admite venta de parley'
    )
    quiniela = models.BooleanField(
        default=False,
        verbose_name='Permite la venta de quiniela? ',
        help_text='Seleccione este campo solo si la temporada admite venta de quiniela'
    )
    apuestasimple = models.BooleanField(
        default=False,
        verbose_name='Permite la venta de apuesta simple? ',
        help_text='Seleccione este campo solo si la temporada admite venta de apuesta simple'
    )
    sistema = models.ForeignKey(
        'admin_juego.SistemaJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    count_encuentros = models.IntegerField(
        default=0,
        verbose_name='Cantidad de Sorteo',
        help_text='Ingrese la cantidad de Sorteo a realizar en la jornada, este campo '
        'solo sera util, para las Fechas de quiniela.'
    )
    monto_inicial = models.IntegerField(
        default=0,
        verbose_name='Monto inicial Bs',
        help_text='Ingrese la cantidad de monto inicial, este campo '
        'solo sera util, para las Fechas de quiniela.'
    )
    valor = models.IntegerField(
        default=0,
        verbose_name='Valor por ticket Bs',
        help_text='Ingrese la cantidad del valor en Bs, este campo '
        'solo sera util, para las Fechas de quiniela.'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone', 'count_encuentros', 'monto_inicial', 'valor',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('jornada', 'temporadas', 'sistema')
        verbose_name = ('Jornada')
        verbose_name_plural = ('Fechas')

    def __str__(self):
        return self.jornada

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__encuentro__jornada_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_jornadas_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    @staticmethod
    def get_or_create_or_flush(temporada, sistemajuego):
        """
        Metodo statico que se encarga de gestionar las creacion
        y busqueda de Fechas automaticas cuando son de una liga sin Fechas
        """
        if not temporada.torneo.por_jornadas:
            try:
                return Fechas.objects.get(
                    temporadas=temporada,
                    sistema=sistemajuego,
                )
            except Exception:
                count_jornada = Fechas.objects.filter(
                    temporadas=temporada,
                    sistema=sistemajuego,
                ).count()

                if count_jornada == 0:
                    # No existe por lo tanto se crea
                    return Fechas.objects.create(
                        temporadas=temporada,
                        sistema=sistemajuego,
                        parley=True,
                        fechaini=temporada.fechaini,
                        fechafin=temporada.fechafin,
                        status=temporada.status,
                        jornada=temporada.nombre,

                    )
                else:
                    # Existe mas de 1, se procede a eliminar la mas nueva.
                    Fechas = Fechas.objects.filter(
                        temporadas=temporada,
                        sistema=sistemajuego,
                    ).order_by('created_at')

                    jornada = Fechas[0]
                    for obj in Fechas[1:]:
                        obj.delete()
                    return jornada
        else:
            raise ValueError(
                'Error: Este metodo es exlusivo para jornandas automaticas.')

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.temporadas.__module__.split('.')[0],
            self.temporadas.__class__.__name__.lower(),
            self.temporadas_id
        )

    name_cache = 'jornadas_json_event'
    name_data_type_origin = types_notification[
        'data_type_origin']['jornada'][0]
    broadcast_automatic = False

    def get_parley(self):
        return 1 if self.parley else 0

    def get_quiniela(self):
        return 1 if self.quiniela else 0

    def get_apuesta_simple(self):
        return 1 if self.apuestasimple else 0

    def get_acumulado(self):
        return self.monto_inicial

    def get_acumulado_generate_broadcast(self):
        return self.get_acumulado()

    def set_cache(self, cache_standar=True):
        json = {
            'jornada': self.jornada,
            'parley': self.get_parley(),
            'quiniela': self.get_quiniela(),
            'simple_bet': self.get_apuesta_simple(),
        }

        if self.quiniela:
            json['count_encuentros'] = self.count_encuentros
            json['valor'] = self.valor
            json['acumulado'] = self.get_acumulado()

        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )
        if cache_standar is False:
            json['deporte_id'] = self.temporadas.torneo.deporte_id
            json['liga_id'] = self.temporadas_id
            # si la temporada aun no esta en la tabla la genera
            self.temporadas.broadcast()
        return json

    def save(self, *args, **kwargs):
        super(Fechas, self).save()
        # hace la actualizacion en caliente solo
        # si hay Sorteo disponibles para la jornada
        if self.encuentros_set.filter(horajuego__gte=now()).exists():
            self.broadcast(
                sistema=self.sistema,
            )


class GruposSorteo(CachinEvent, models.Model):
    prefix_filter_plural = 'grupos_juegos'
    """GruposSorteo: Grupos de juego por temporadas

    Campos definidos:
        nombre(string): nombre del grupo de juego

        temporada(foreign): temporada a la cual pertenece el grupo

        orden(entero): entero que indica el orden de impresion de los grupos

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=200,
        verbose_name='Nombre (*)',
        help_text='Ingrese un nombre para el grupo'
    )
    temporada = models.ForeignKey(
        'admin_juego.PeriodoSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    orden = models.IntegerField(
        verbose_name='Orden (*)',
        help_text='Ingrese la numeraciÃ³n de orden'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('nombre', 'temporada')
        verbose_name = ('Grupo de juego')
        verbose_name_plural = ('Grupos de juegos')
        ordering = ['orden', ]

    def __str__(self):
        return self.nombre

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__encuentro__grupo_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_gruposjuego_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    name_cache = 'grupos_juego_json_event'
    name_data_type_origin = types_notification['data_type_origin']['grupos_juego'][0]
    broadcast_automatic = False

    def set_cache(self, cache_standar=True):
        json = {
            'nombre': str(self),
            'orden': self.orden,
            'liga_id': self.temporada_id,
            'deporte_id': self.temporada.torneo.deporte_id,
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )
        return json

    def save(self, *args, **kwargs):
        super(GruposSorteo, self).save()
        # hace la actualizacion en caliente solo
        # si hay Sorteo disponibles para el grupo
        if self.encuentros_set.filter(horajuego__gte=now()).exists():
            self.broadcast()


class ModalidadGrupo(models.Model):
    """ModalidadGrupo: ModalidadJuego por grupos de juego de temporadas

    Campos definidos:
        equipo(foreign): equipo que pertenece al grupo

        grupo(foreign): grupo al cual pertenecen los equipos

        created_at y updated_at: registros de creacion y actualizacion.
    """
    equipo = models.ForeignKey(
        'admin_juego.ModalidadJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    grupo = models.ForeignKey(
        'admin_juego.GruposSorteo',  # TODO: revisar modelo destino
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
        db_tablespace = 'ts_parley'
        unique_together = ('equipo', 'grupo')
        verbose_name = ('Equipo por grupo de juego')
        verbose_name_plural = ('ModalidadJuego por grupos de juego')

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.grupo.__module__.split('.')[0],
            self.grupo.__class__.__name__.lower(),
            self.grupo_id
        )


class Sorteo(BaseGenericProcessModelCache, CachinEvent, models.Model):
    prefix_filter = 'encuentro'
    prefix_filter_plural = 'Sorteo'

    """Sorteo: Sorteo

    Campos definidos:
        maximo_dias_olgura: constante entera que indica el maximo de dias
            de olgura para editar lo relacionado a un encuentro.

        horajuego(datetime): fecha y hora del inicio del encuentro

        horacierre(datetime): fecha y hora del cierre de apuesta del
            encuentro

        status(foreign): estatus del encuentro

        jornada(foreign): jornada a la cual pertenece el encuentro

        grupo(foreign): grupo al cual pertenece el encuentro

        created_at y updated_at: registros de creacion y actualizacion.
    """

    if DEBUG:
        maximo_dias_olgura = 360
    else:
        maximo_dias_olgura = 3

    horajuego = models.DateTimeField(
        verbose_name='Fecha y hora de inicio (*)',
        help_text='Seleccione la fecha y hora de inicio del encuentro',
        db_index=True,
    )
    horacierre = models.DateTimeField(
        verbose_name='Fecha y hora de cierre (*)',
        help_text='Seleccione la fecha y hora de cierre del encuentro',
        db_index=True,
    )
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    jornada = models.ForeignKey(
        'admin_juego.Fechas',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    grupo = models.ForeignKey(
        'admin_juego.GruposSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    created_at = models.DateTimeField(
        verbose_name='Creado',
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name='Actualizado',
        auto_now=True,
        editable=False,
    )
    updated_at_logros = models.DateTimeField(
        verbose_name='Actualizacion de logros',
        auto_now_add=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )
    exists_tickets = models.BooleanField(
        default=False,
        db_index=True,
        editable=False,
    )

    exists_logros = None
    exists_resultados = None
    resultado = None

    prefix_cache_manager = 'model_encuentros'
    objects = BaseGenericProcessManagerCache()

    audit_exclude = ('pk_clone', 'exists_tickets')

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Encuentro')
        verbose_name_plural = ('Sorteo')
        ordering = ('horajuego', )

    def __str__(self):
        return '{0}'.format(self.pk)

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__encuentro_id'

    def get_exists_tickets(self):
        from admin_apuestas.models import TicketsDetail
        kwargs = {}
        kwargs[self.get_prefix_kwargs_by_level_tickets_details()] = self.pk
        return TicketsDetail.objects.filter(**kwargs).exists()

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_encuentros_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    def get_is_edit(self):
        return self.horajuego > (
            now() - timedelta(days=self.maximo_dias_olgura))

    def get_exists_resultados(self, sistema_resultados, cache=True):
        """
        Verifica si hay resultados asociados al encuentro
        """
        if cache is False:
            self.exists_resultados = None
        if self.exists_resultados is None:
            self.resultado = self.get_resultado(
                sistema_resultados=sistema_resultados, cache=cache
            )
            if self.resultado:
                if self.resultado.created_at.second != self.resultado.updated_at.second:
                    self.exists_resultados = True
                else:
                    self.exists_resultados = False
            else:
                self.exists_resultados = False

        return self.exists_resultados

    def get_resultado(self, sistema_resultados, cache=True):
        """
        Verifica si hay resultados asociados al encuentro
        """
        if cache is False:
            self.resultado = None
        if self.resultado is None:
            try:
                self.resultado = self.resultados_set.select_related('admin_status.Status').get(
                    sistema_id=sistema_resultados.pk
                )
            except ObjectDoesNotExist:
                self.resultado = False
        return self.resultado

    def get_exists_logros(self):
        """
        Verifica si hay logros asociados al encuentro
        """
        if self.exists_logros is None:
            self.exists_logros = apuesta.objects.filter(
                encuentros_modalidad__encuentro_id=self.pk
            ).exclude(
                valor_americano=None
            ).exclude(
                valor_americano=0
            ).exists()

        return self.exists_logros

    name_cache = 'encuentros_json_event'
    name_cache_jugadas = 'encuentros_jugadas_all_json_event'
    name_cache_jugadas_quiniela = 'encuentros_jugadas_quiniela_all_json_event'
    name_cache_jugadores = 'encuentro_jugadores_json_event'
    name_data_type_origin = types_notification[
        'data_type_origin']['encuentro'][0]
    broadcast_automatic = False

    def get_grupo(self):
        return 0 if not self.grupo_id else self.grupo_id

    def encuentrosdetail_set_order(self):
        queryset = cache.get(
            '{0}_{1}'.format(
                'encuentrosdetail_set_order',
                self.pk))
        if not queryset:
            queryset = self.encuentrosdetail_set.select_related(
                'equipos_temporadas__equipo'
            ).all().order_by(
                self.jornada.temporadas.torneo.deporte.get_filter_orden_equipos()
            )
            cache.set(
                '{0}_{1}'.format('encuentrosdetail_set_order', self.pk),
                queryset,
                CACHES_CONF_TIME['registros_db']['Sorteo']
            )
        return queryset

    def encuentrosdetail_set_order_all(self):
        queryset = cache.get(
            '{0}_{1}'.format(
                'encuentrosdetail_set_order_all',
                self.pk))
        if not queryset:
            queryset = self.encuentrosdetail_set.select_related(
                'equipos_temporadas__equipo__deporte',
                'equipos_temporadas__temporada__torneo'
            ).all().order_by(
                self.jornada.temporadas.torneo.deporte.get_filter_orden_equipos()
            )
            cache.set(
                '{0}_{1}'.format('encuentrosdetail_set_order_all', self.pk),
                queryset,
                CACHES_CONF_TIME['registros_db']['Sorteo']
            )
        return queryset

    def save(self, *args, **kwargs):
        generate_broadcast = True
        generate_jugadas = False
        if self.pk:
            old = Sorteo.objects.only(
                'horajuego', 'status_id').get(
                pk=self.pk)
            if old.horajuego.date() != now().date():
                # En produccion el debug siempre sera falso
                # en cambio en desarrollo habilita su generacion
                generate_broadcast = DEBUG
                from admin_status.models import Status
                if old.status_id != Status.get_status_by_codename(
                        codename='status_habilitado').pk:
                    generate_jugadas = True
        super(Sorteo, self).save(*args, **kwargs)
        # hace la actualizacion en caliente solo si el encuentro
        # esta vigente y aun tiene logros

        if generate_broadcast and (
                self.get_exists_logros() or self.jornada.quiniela):
            self.broadcast(
                sistema=self.jornada.sistema,
            )
            if generate_jugadas and self.horacierre > now():
                self.generate_broadcast_jugadas()
        self.cache_clear()

    def generate_broadcast_jugadas(self):
        if self.jornada.sistema.notificacion_automatica:
            fecha_ini_notification = now()
            cache.set(
                '{0}_{1}'.format('block_event', self.jornada.sistema.pk),
                True,
            )
        from admin_status.models import Status
        pk_pendinte = Status.get_status_by_codename(
            codename='status_pendiente').pk
        for encuentro_modalidad in self.encuentrosmodalidades_set.filter(
                jugadas__status_id=pk_pendinte).distinct():
            encuentro_modalidad.broadcast(sistema=self.jornada.sistema)
            for jugada in encuentro_modalidad.jugadas_set.filter(
                    status_id=pk_pendinte):
                jugada.broadcast(sistema=self.jornada.sistema)

        if self.jornada.sistema.notificacion_automatica:
            EventNotification.objects.filter(
                sistema=self.jornada.sistema.pk,
                in_production=False,
                date_production__range=[fecha_ini_notification, now()]
            ).update(
                in_production=True
            )
            cache.delete(
                '{0}_{1}'.format(
                    'block_event',
                    self.jornada.sistema.pk))

    def cache_clear(self):
        cache.delete(
            '{0}_{1}'.format('encuentrosdetail_set_order', self.pk)
        )

    def set_cache(self, cache_standar=True):
        json_equipos = []
        for obj in self.encuentrosdetail_set.all().order_by('-indice'):

            # activo el broacas automatico,
            # para enviar la info del equipo como objeto aparte
            obj.equipos_temporadas.equipo.broadcast(
                day=self.horajuego.date()
            )
            equipos_data = {
                'id': obj.equipos_temporadas.equipo_id,
                'indice': obj.indice
            }
            json_equipos.append(equipos_data)

        json = {
            'hora': self.horajuego.strftime(FORMAT_STR_TIME),
            'fecha': self.horajuego.strftime(FORMAT_STR_DATE_2),
            'hora_cierre': self.horacierre.strftime(FORMAT_STR_DATETIME),
            'grupo_id': self.get_grupo(),
            'admin_status.Status': self.status_id,
            'deporte_id': self.jornada.temporadas.torneo.deporte_id,
            'equipos': json_equipos,
            'sistema': self.jornada.sistema_id,
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )

        if cache_standar is False:
            json['jornada_id'] = self.jornada_id
            json['liga_id'] = self.jornada.temporadas_id
            if EventNotification.objects.filter(
                pk_origin=self.jornada_id,
                data_origin=self.jornada.name_data_type_origin,
                sistema=get_sistema_juego(),
            ).exists() is False:
                if self.get_exists_logros():
                    self.jornada.broadcast(
                        sistema=self.jornada.sistema,
                    )
            if self.grupo_id:
                if EventNotification.objects.filter(
                    pk_origin=self.grupo_id,
                    data_origin=self.grupo.name_data_type_origin,
                    sistema=get_sistema_juego(),
                ).exists() is False:
                    if self.get_exists_logros():
                        self.grupo.broadcast(
                            sistema=self.jornada.sistema,
                        )

        return json

    def get_cache_jugadres(self):
        json = cache.get('{0}{1}'.format(self.name_cache_jugadores, self.pk))
        if not json:
            json = self.set_cache_jugadres()
        return json

    def set_cache_jugadres(self, generate_empty_jugadores=True):
        json = {}
        encuentro = self.get_cache()
        pk_grupo = -1
        order_filter = self.jornada.temporadas.torneo.deporte.get_filter_orden_equipos()

        for jugador_tipo in TipoNumeroSorteo.objects.filter(
                deporte_id=encuentro['deporte_id']):
            grupo_json = {
                'encuentro_modalidad': {}
            }

            pk_encuentro_modalidad = int(
                '-{0}{1}'.format(
                    self.pk,
                    jugador_tipo.pk
                )
            )

            pk_modalidad = jugador_tipo.pk * -1
            modalidad_json = {
                'ref_mod': '',
                'encuentro_id': self.pk,
                'grupo_id': pk_grupo,
                'modalidad_id': pk_modalidad,
                'origen': 0,
                'sistema': self.jornada.sistema_id,
                'deporte_id': encuentro['deporte_id'],
            }
            CachinEvent.broadcast_manual(
                json_new=modalidad_json,
                pk=pk_encuentro_modalidad,
                data_origin=types_notification[
                    'data_type_origin']['encuentro_modalidad'][0],
                sistema=self.jornada.sistema,
                day=self.horajuego.date(),
                force=True,
            )

            modalidad_json['jugadas'] = {}
            queryset = self.encuentrosdetail_set.all().filter(
                jugador__tipo_id=jugador_tipo.pk
            )
            if not queryset.exists() and generate_empty_jugadores:
                for detalle_encuentro in self.encuentrosdetail_set.all().order_by(order_filter):
                    jugada_json = {
                        'indice': detalle_encuentro.indice,
                        'favorito': 0,
                        'logro_americano': '0',
                        'logro_europeo': '0',
                        'ref': '',
                        'pertenece': '',
                        'is_equipo': 1,
                        'sistema': self.jornada.sistema_id,
                        'origen': 0,
                        'deporte_id': encuentro['deporte_id'],
                    }

                    pk_origin = int(
                        '-{0}{1}{2}'.format(
                            self.pk,
                            detalle_encuentro.indice,
                            jugador_tipo.pk,
                        )
                    )

                    modalidad_json['jugadas'][
                        '{0}'.format(pk_origin)
                    ] = jugada_json

                    """
                    Las jugadas por tipo de jugador si se envian de forma manual
                    """
                    jugada_json[
                        'encuentro_modalidad_id'] = pk_encuentro_modalidad
                    jugada_json['encuentro_id'] = self.pk
                    jugada_json['grupo_id'] = pk_grupo
                    jugada_json['modalidad_id'] = pk_modalidad
                    CachinEvent.broadcast_manual(
                        json_new=jugada_json,
                        pk=pk_origin,
                        data_origin=types_notification[
                            'data_type_origin']['jugada'][0],
                        sistema=self.jornada.sistema,
                        day=self.horajuego.date(),
                    )

            for detalle_encuentro in queryset.order_by(order_filter):
                jugada_json = {
                    'indice': detalle_encuentro.indice,
                    'favorito': 0,
                    'logro_americano': '0',
                    'logro_europeo': '0',
                    'ref': detalle_encuentro.referencia,
                    'pertenece': detalle_encuentro.jugador.get_display(),
                    'is_equipo': 1,
                    'sistema': self.jornada.sistema_id,
                    'origen': 0,
                    'deporte_id': encuentro['deporte_id'],
                }

                pk_origin = int(
                    '-{0}{1}{2}'.format(
                        self.pk,
                        detalle_encuentro.indice,
                        jugador_tipo.pk,
                    )
                )

                modalidad_json['jugadas'][
                    '{0}'.format(pk_origin)
                ] = jugada_json

                """
                Las jugadas por tipo de jugador si se envian de forma manual
                """
                jugada_json['encuentro_modalidad_id'] = pk_encuentro_modalidad
                jugada_json['encuentro_id'] = self.pk
                jugada_json['grupo_id'] = pk_grupo
                jugada_json['modalidad_id'] = pk_modalidad
                CachinEvent.broadcast_manual(
                    json_new=jugada_json,
                    pk=pk_origin,
                    data_origin=types_notification[
                        'data_type_origin']['jugada'][0],
                    sistema=self.jornada.sistema,
                    day=self.horajuego.date()
                )

            if modalidad_json['jugadas']:
                # si hay jugadas si lo agrega
                grupo_json['encuentro_modalidad'][
                    '{0}'.format(pk_encuentro_modalidad)
                ] = modalidad_json

            # la pos 0 es la de ModalidadJuego del grupo
            if grupo_json['encuentro_modalidad']:
                # agrega el pk del encuentro negativo como pk del grupo
                json['{0}'.format(pk_grupo)] = grupo_json

        cache.set(
            '{0}{1}'.format(
                self.name_cache_jugadores,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache_jugadores]
        )
        return json

    def get_cache_jugadas(self):
        json = cache.get('{0}{1}'.format(self.name_cache_jugadas, self.pk))
        if not json:
            json = self.set_cache_jugadas()
        return json

    def set_cache_jugadas(self, comercializadora=None):
        json = {}
        encuentro = self.get_cache()
        from admin_status.models import Status

        if (now().strptime(encuentro['hora_cierre'], FORMAT_STR_DATETIME) > now() and
                (encuentro['admin_status.Status'] == Status.get_status_by_codename('status_habilitado').pk or
                    encuentro['admin_status.Status'] == Status.get_status_by_codename('status_reanudado').pk)):

            validate = apuesta.objects.filter(
                status_id=Status.get_status_by_codename('status_pendiente').pk,
                encuentros_modalidad__encuentro_id=self.pk
            )

            if validate.exists():
                json = self.set_cache_jugadres(generate_empty_jugadores=False)

                # Restricciones de venta
                restrictions_grupos = []
                if comercializadora:
                    from admin_permisologia.models import PermissionsSales
                    restrictions_grupos = list(PermissionsSales.objects.filter(
                        deporte_id=encuentro['deporte_id'],
                        grupo__isnull=False,
                        modalidad__isnull=True,
                        comercializadora_id=comercializadora
                    ).values_list('grupo_id', flat=True))
                #############################################################

                # Buscando jugados por grupos de deporte
                for deporte_grupo in TipoProducto_Grupos.objects.filter(
                    deporte_id=encuentro['deporte_id']
                ).exclude(
                    grupo_id__in=restrictions_grupos
                ):
                    grupo_json = deporte_grupo.set_cache_by_encuentro(
                        self,
                        comercializadora=comercializadora
                    )

                    if grupo_json['encuentro_modalidad']:
                        # es esta pos esta el json de ModalidadJuego
                        json['{0}'.format(deporte_grupo.grupo_id)] = grupo_json

                if not comercializadora:
                    cache.set(
                        '{0}{1}'.format(
                            self.name_cache_jugadas,
                            self.pk
                        ),
                        json,
                        CACHES_CONF_TIME['admin_juegos'][
                            self.name_cache_jugadas]
                    )

        return json

    def get_cache_jugadas_quiniela(self):
        json = cache.get(
            '{0}{1}'.format(
                self.name_cache_jugadas_quiniela,
                self.pk))
        if not json:
            json = self.set_cache_jugadas_quiniela()
        return json

    def set_cache_jugadas_quiniela(self):
        json = {}

        for detail in SorteoDetalle.objects.filter(encuentro=self.pk):
            jugada_ganador = apuesta.objects.get(
                detalle_encuentro=detail,
                encuentros_modalidad__modalidad_grupo__grupo__codename='juego_completo',
                condicion__modalidad__codename='ganador',
                sistema=self.jornada.sistema
            )
            json[str(detail.equipos_temporadas.equipo_id)] = jugada_ganador.pk

        cache.set(
            '{0}{1}'.format(
                self.name_cache_jugadas_quiniela,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache_jugadas]
        )
        return json

    def broadcast(self, sistema=None, day=None):
        for obj in self.encuentrosdetail_set.all().order_by('-indice'):
            obj.equipos_temporadas.equipo.broadcast(
                day=day
            )
        super(Sorteo, self).broadcast(sistema, day)


class SorteoDetalle(ProtectDelete, models.Model):
    """SorteoDetalle: Detalle de encuentro

    Esta clase hereda de ProtectDelete, quien implementa
    un metodo de proteccion contra eliminacion

    Campos definidos:
        encuentro(foreign): encuentro al que hace referencia el detalle

        equipos_temporadas(foreign): equipo por temporada en el encuentro

        jugador(foreign): jugador del equipo por encuentro

        referencia(string): referencia del jugador en caso de existir

        indice(entero): indice del equipo, 0 o 1, visitante o local
            respectivamente

        created_at y updated_at: registros de creacion y actualizacion.
    """
    encuentro = models.ForeignKey(
        'admin_juego.Sorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    equipos_temporadas = models.ForeignKey(
        'admin_juego.ModalidadPeriodo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    jugador = models.ForeignKey(
        'admin_juego.NumeroSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    referencia = models.CharField(
        verbose_name="Referencia",
        max_length=140,
        blank=True,
        null=True
    )
    indice = models.IntegerField(
        verbose_name="Home/Visitante",
        null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    str_indice = {
        '1': 'Home',
        '2': 'Visitante'
    }

    audit_exclude = ('pk_clone',)

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('encuentro', 'equipos_temporadas')
        verbose_name = ('Detalle de encuentro')
        verbose_name_plural = ('Detalle de los Sorteo')

    def __str__(self):
        return '{0}'.format(self.pk)

    def get_ref_related_historic(self):
        """
        Retorna una relaciÃ³n de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.encuentro.__module__.split('.')[0],
            self.encuentro.__class__.__name__.lower(),
            self.encuentro_id)


class GruposApuesta(BaseGenericProcessModelCache, models.Model):
    """GruposApuesta: Grupos de apuesta

    Campos definidos:
        nombre(string): nombre del grupo de apuesta

        codename(string): codigo en texto del nombre de grupo de apuesta

        orden(entero): orden en que se imprimen los grupos de apuestas

        deporte(foreign): deporte a los cuales pertenece el grupo
            de apuesta

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre del grupo'
    )
    codename = models.CharField(
        max_length=140,
        editable=False
    )
    orden = models.IntegerField(
        verbose_name='Orden (*)',
        help_text='Ingrese la numeraciÃ³n de orden'
    )
    deporte = models.ManyToManyField(
        'TipoProducto',
        blank=True,
        symmetrical=False,
        through='admin_juego.TipoProducto_Grupos',
        verbose_name='Seleccione los deportes (*)',
        help_text='Seleccione los deportes a los que desea asignar el grupo'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    prefix_cache_manager = 'model_grupos_apuesta'
    objects = BaseGenericProcessManagerCache()

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Grupo de apuesta')
        verbose_name_plural = ('Grupos de apuestas')

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_gruposapuestas_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    def __str__(self):
        return self.nombre

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__encuentros_modalidad__modalidad_grupo__grupo_id'


class TipoProducto_Grupos(ProtectDelete, models.Model):
    """TipoProducto_Grupos: Deporte por grupo de apuesta

    Campos definidos:
        deporte(foreign): este deporte se vende en el grupo de apuesta
            referenciado

        grupo(foreign): grupos de apuesta referenciado
    """
    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',
        on_delete=models.CASCADE,
    )
    grupo = models.ForeignKey(
        'admin_juego.GruposApuesta',
        on_delete=models.CASCADE,
    )

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('deporte', 'grupo')
        verbose_name = ('Grupo de apuesta por deporte')
        verbose_name_plural = ('Grupos de apuestas  por deportes')

    def __str__(self):
        return '{0} | {1}'.format(self.deporte, self.grupo)

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.grupo.__module__.split('.')[0],
            self.grupo.__class__.__name__.lower(),
            self.grupo_id
        )

    def get_cache_by_encuentro(self, encuentro):
        json = cache.get(
            '{0}{1}_{2}'.format(
                TipoProducto.name_cache_deporte_grupo,
                self.pk,
                encuentro.pk
            )
        )
        if not json:
            json = self.set_cache_by_encuentro(encuentro)
        return json

    def set_cache_by_encuentro(self, encuentro, comercializadora=None):
        json = {
            'encuentro_modalidad': {}
        }

        # Restricciones de venta
        restrictions_modalidades = []
        if comercializadora:
            from admin_permisologia.models import PermissionsSales
            restrictions_modalidades = list(PermissionsSales.objects.filter(
                deporte_id=self.deporte_id,
                grupo_id=self.grupo_id,
                modalidad__isnull=False,
                comercializadora_id=comercializadora,
            ).values_list('modalidad_id', flat=True))

        for modalidad_grupo in self.grupo.modalidades_grupos_set.all().exclude(
            modalidad_id__in=restrictions_modalidades
        ):
            # si este deporte tiene restringiad cierta modalidad
            # continuo y no evaluo
            if modalidad_grupo.deporte_restriccion.filter(
                    pk=self.deporte_id).exists():
                continue

            for encuentro_modalidad in SorteoModalidades.objects.filter(
                encuentro_id=encuentro.pk,
                deporte_grupo_id=self.pk,
                modalidad_grupo_id=modalidad_grupo.pk
            ):
                encuentro_modalidad_json = encuentro_modalidad.set_cache()
                if encuentro_modalidad_json['jugadas']:
                    json['encuentro_modalidad'][
                        '{0}'.format(encuentro_modalidad.pk)
                    ] = encuentro_modalidad_json

        if not comercializadora:
            cache.set(
                '{0}{0}_{1}'.format(
                    TipoProducto.name_cache_deporte_grupo,
                    self.pk,
                    encuentro.pk
                ),
                json,
                CACHES_CONF_TIME['admin_juegos'][
                    TipoProducto.name_cache_deporte_grupo]
            )
        return json


class ModalidadApuesta(BaseGenericProcessModelCache, models.Model):
    """ModalidadApuesta: ModalidadApuesta de apuesta

    Campos definidos:
        modalidad(string): nombre de la modalidad

        grupo(foreign multi): grupos de apuesta al cual pertenece la modalidad

        orden(entero): orden en que se imprimen las ModalidadApuesta de apuesta

        descripcion(string): descripcion breve de la modalidad

        etiqueta_ref(booleano): bandera que indica si la modalidad es por
            etiqueta de referencia

        codename(string): codigo en texto del nombre de la modalidad

        restriction(self): otras ModalidadApuesta con las cuales se restringe,
            para validaciones en las apuestas. por ejmplo si apuesta a la
            modalidad de ganador no puede apostar a la modalidad de empate.

        created_at y updated_at: registros de creacion y actualizacion.
    """
    prefix_filter = 'modalidad'

    modalidad = models.CharField(
        max_length=200,
        unique=True,
        verbose_name='Nombre (*)',
        help_text='Ingrese nombre de la modalidad'
    )
    grupo = models.ManyToManyField(
        'GruposApuesta',
        blank=True,
        symmetrical=False,
        through='admin_juego.ModalidadJuego_Grupos',
        verbose_name='Seleccione los grupos (*)',
        help_text='Seleccione los grupos a los que pertenece la modalidad'
    )
    orden = models.IntegerField(
        verbose_name='Orden (*)',
        help_text='Ingrese la numeraciÃ³n de orden'
    )
    descripcion = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        verbose_name='DescripciÃ³n ',
        help_text='Ingrese la descriciÃ³n de la modalidad'
    )
    etiqueta_ref = models.BooleanField(
        default=False,
        verbose_name='Â¿Posee etiqueta de referencia? ',
        help_text='En caso de poseer etiqueta de referencia seleccione este campo'
    )
    bet = models.BooleanField(
        default=True,
        verbose_name='Â¿Modalidad de apuesta? ',
        help_text='Verifique si es una modalidad de apuesta'
    )
    codename = models.CharField(
        max_length=140,
        editable=False
    )
    restriction = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True,
        verbose_name='Restricciones ',
        help_text='Selecciones las restricciones a necesarias'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    prefix_cache_manager = 'model_modalidades'
    objects = BaseGenericProcessManagerCache()

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Modalidad de apuesta')
        verbose_name_plural = ('ModalidadApuesta de apuestas')

    def __str__(self):
        return self.modalidad

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__condicion__modalidad_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_modalidades_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'


class ModalidadJuego_Grupos(ProtectDelete, models.Model):
    """ModalidadJuego_Grupos: Modalidad por grupo de apuesta

    Campos definidos:
        modalidad(foreign): modalidad a la que se referencia

        grupo(foreign): grupos de apuesta que tiene dicha modalidad

        deporte_restriccion(foreign multi): deportes a los cuales se restringe
            la venta de la combinacion de esta modalidad y grupo de apuesta
    """
    prefix_filter = 'grupo_modalidad'

    modalidad = models.ForeignKey(
        'admin_juego.ModalidadApuesta',
        on_delete=models.CASCADE,
    )
    grupo = models.ForeignKey(
        'admin_juego.GruposApuesta',
        on_delete=models.CASCADE,
    )
    deporte_restriccion = models.ManyToManyField(
        'TipoProducto',
        blank=True,
        symmetrical=False,
        verbose_name='TipoProducto a restringir ',
        help_text='Seleccione los deportes a quitar de la relacion '
                  'entre grupos y modalidad, solo se puede restringir '
                  ' los seleccionados en un principio para el grupo'
    )

    class Meta:
        db_tablespace = 'ts_parley'
        unique_together = ('modalidad', 'grupo')
        verbose_name = ('Modalidad por grupo de apuesta')
        verbose_name_plural = ('ModalidadJuego por grupos de apuestas')

    def __str__(self):
        return '{0} | {1}'.format(self.grupo, self.modalidad)

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.modalidad.__module__.split('.')[0],
            self.modalidad.__class__.__name__.lower(),
            self.modalidad_id
        )


class SorteoModalidades(CachinEvent, models.Model):
    """SorteoModalidades: Modalida por encuentro

    Campos definidos:
        etiqueta_ref(string): referencia de la modalidad asociada

        encuentro(foreign): encuentro al cual se hace referencia

        deporte_grupo(foreign): grupo de apuesta por deporte al cual
            pertenece el registro

        modalidad_grupo(foreign): modalidad por grupo a la cual pertenece
            el registro

        sistema(foreign): sistema de juego al cual pertenece la referencia
            deencuentro modalidad

        created_at y updated_at: registros de creacion y actualizacion.
    """
    etiqueta_ref = models.CharField(
        verbose_name='Referencia',
        max_length=140,
        null=True,
        blank=True
    )
    encuentro = models.ForeignKey(
        'admin_juego.Sorteo',
        on_delete=models.CASCADE,
        related_name='modalidades_sorteo',
    )
    deporte_grupo = models.ForeignKey(
        'admin_juego.TipoProducto_Grupos',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    modalidad_grupo = models.ForeignKey(
        'admin_juego.ModalidadJuego_Grupos',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    sistema = models.ForeignKey(
        'admin_juego.SistemaJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    origen = models.ForeignKey(
        'admin_juego.Sorteo',
        on_delete=models.CASCADE,
        related_name='modalidades_origen',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )

    audit_exclude = ('pk_clone',)

    class Meta:

        db_tablespace = 'ts_parley'
        unique_together = (
            'encuentro',
            'deporte_grupo',
            'modalidad_grupo',
            'sistema')
        verbose_name = ('Modalidad por encuentro')
        verbose_name_plural = ('ModalidadJuego por Sorteo')

    def __str__(self):
        return '{0} | {1}'.format(
            self.encuentro,
            self.modalidad_grupo,
        )

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.encuentro.__module__.split('.')[0],
            self.encuentro.__class__.__name__.lower(),
            self.encuentro_id
        )

    def get_field_etiqueta_logro(self):
        """
        Devuelve una etiqueta con el pk para uso personalizado
        """
        return 'ref_encuentromodalidad_{0}'.format(self.pk)

    name_cache = 'encuentro_modalidad_json_event'
    name_data_type_origin = types_notification[
        'data_type_origin']['encuentro_modalidad'][0]
    broadcast_automatic = False

    def get_etiqueta_ref(self):
        return '' if not self.etiqueta_ref else self.etiqueta_ref

    def get_origen(self):
        return self.origen.pk if self.origen else 0

    def set_cache(self, cache_standar=True):

        modalidades_json = {
            'ref_mod': self.get_etiqueta_ref(),
            'jugadas': {},
            'modalidad_id': self.modalidad_grupo.modalidad_id,
            'origen': self.get_origen(),
            'sistema': self.sistema_id,
        }

        order_filter = self.encuentro.jornada.temporadas.torneo.deporte.get_filter_orden_equipos()
        from admin_status.models import Status
        status_pendiente = Status.get_status_by_codename(
            codename='status_pendiente')

        # buscamos las jugadas
        for condicion in self.modalidad_grupo.modalidad.condiciones_set.all().order_by('orden'):
            if condicion.equipo:
                if condicion.tipo == 4:
                    # verificamos nuevamente que sea una condicion de
                    # Informativa
                    for encuentro_detail in self.encuentro \
                            .encuentrosdetail_set.all().order_by(order_filter):

                        jugadas = JugadasInformativas.objects.filter(
                            detalle_encuentro_id=encuentro_detail.pk,
                            encuentros_modalidad_id=self.pk,
                            condicion_id=condicion.pk,
                        )
                        for jugada in jugadas:
                            modalidades_json['jugadas'][
                                '{0}'.format(jugada.pk)
                            ] = jugada.set_cache()
                else:
                    for encuentro_detail in self.encuentro \
                            .encuentrosdetail_set.all().order_by(order_filter):

                        jugadas = apuesta.objects.filter(
                            detalle_encuentro_id=encuentro_detail.pk,
                            encuentros_modalidad_id=self.pk,
                            condicion_id=condicion.pk,
                        )
                        for jugada in jugadas:
                            # si es un estatus a pendiente no se consulta esa
                            # jugada
                            if (jugada.status_id != status_pendiente.pk):
                                continue
                            if jugada.indice != encuentro_detail.indice:
                                jugada.indice = encuentro_detail.indice
                                jugada.save()
                                jugada.broadcast(
                                    sistema=self.sistema,
                                    day=self.encuentro.horajuego.date(),
                                )
                            modalidades_json['jugadas'][
                                '{0}'.format(jugada.pk)
                            ] = jugada.set_cache()

            else:
                for indice in range(1, condicion.tipo + 1):
                    jugadas = apuesta.objects.filter(
                        encuentros_modalidad_id=self.pk,
                        condicion_id=condicion.pk,
                        indice=indice,
                    )
                    for jugada in jugadas:
                        if jugada.status_id != status_pendiente.pk:
                            continue
                        modalidades_json['jugadas'][
                            '{0}'.format(jugada.pk)
                        ] = jugada.set_cache()

        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            modalidades_json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )

        if cache_standar is False:
            if EventNotification.objects.filter(
                pk_origin=self.encuentro_id,
                data_origin=self.encuentro.name_data_type_origin,
                sistema=self.encuentro.jornada.sistema_id,
            ).exists() is False:
                self.encuentro.broadcast(
                    sistema=self.encuentro.jornada.sistema,
                    day=self.encuentro.horajuego.date(),
                )
            return {
                'ref_mod': self.get_etiqueta_ref(),
                'encuentro_id': self.encuentro_id,
                'grupo_id': self.modalidad_grupo.grupo_id,
                'modalidad_id': self.modalidad_grupo.modalidad_id,
                'origen': self.get_origen(),
                'sistema': self.sistema_id,
                'deporte_id': self.encuentro.jornada.temporadas.torneo.deporte_id,
            }

        return modalidades_json

    @staticmethod
    def get_carefully(kwargs, sistemajuego, sistemalogros):
        try:
            kwargs['sistema'] = sistemalogros
            return SorteoModalidades.objects.get(
                **kwargs
            )
        except SorteoModalidades.DoesNotExist:
            kwargs['sistema'] = sistemajuego
            return SorteoModalidades.objects.get(
                **kwargs
            )

    def create_heir(self, sistemalogros):
        encuentro_modalidad = SorteoModalidades.objects.update_or_create(
            encuentro=self.encuentro,
            deporte_grupo=self.deporte_grupo,
            modalidad_grupo=self.modalidad_grupo,
            sistema=sistemalogros,
            defaults={
                'origen': self,
                'etiqueta_ref': self.etiqueta_ref,
            },
        )[0]

        for jugada in self.jugadasinformativas_set.all():
            jugada.create_heir(
                encuentro_modalidad=encuentro_modalidad,
                sistemalogros=sistemalogros
            )

        for jugada in self.jugadas_set.all():
            jugada.create_heir(
                encuentro_modalidad=encuentro_modalidad,
                sistemalogros=sistemalogros
            )

        return encuentro_modalidad

    def broadcast(self, sistema=None, day=None):
        if EventNotification.objects.filter(
            pk_origin=self.encuentro_id,
            data_origin=self.encuentro.name_data_type_origin,
            sistema=self.encuentro.jornada.sistema_id,
        ).exists() is False:
            self.encuentro.broadcast(sistema, day)
        super(SorteoModalidades, self).broadcast(sistema, day)


class Condiciones(BaseGenericProcessModelCache, models.Model):
    """Condiciones: Condiciones

    Campos definidos:
        modalidad(foreign): modalidad a la cual pertenece la condicion

        nombre(string): nombre de la condicion

        equipo(booleano): bandera que indica si es una condicion por equipo

        etiqueta_ref(booleano): bandera que indica si la condicion tiene rerefencia

        orden(entre): entero que indica el orden de imprecion de las condiciones

        tipo(entero): selector de tipo de condicion

        created_at y updated_at: registros de creacion y actualizacion.
    """

    modalidad = models.ForeignKey(
        'admin_juego.ModalidadJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    nombre = models.CharField(
        max_length=140,
        null=True,
        blank=True,
        verbose_name='Nombre ',
        help_text='Ingrese nombre de la condiciÃ³n'
    )
    equipo = models.BooleanField(
        default=False,
        verbose_name='Â¿CondiciÃ³n por equipo? ',
        help_text='Seleccione ese campo si se trata de una condiciÃ³n por equipo'
    )
    etiqueta_ref = models.BooleanField(
        default=False,
        verbose_name='Â¿Posee etiqueta de referencia ? ',
        help_text='Seleccione este campo si la condicion poseee eiqueta de referencia'
    )
    orden = models.IntegerField(
        null=True,
        blank=True,
        verbose_name='Numero de orden (*)',
        help_text='Ingrese el numero de orden de la condiciÃ³n'
    )
    CHOICES_TIPO = (
        (0, 'Por equipo'),
        (1, 'Individual'),
        (2, 'Doble'),
        (4, 'Informativa por equipo'),
    )
    tipo = models.IntegerField(
        verbose_name='Tipo de condiciÃ³n (*)',
        choices=CHOICES_TIPO
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    prefix_cache_manager = 'model_condiciones'
    objects = BaseGenericProcessManagerCache()

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Condicion de apuesta')
        verbose_name_plural = ('Condiciones de apuestas')

    def __str__(self):
        return '{0} {1}'.format(self.modalidad, self.nombre)

    def get_prefix_kwargs_by_level_tickets_details(self):
        """Retorna un prefijo, listo para hacer filtros a tickers, desde este nivel"""
        return 'jugada__condicion_id'

    # @models.permalink (eliminado en Django 3.1)
    def get_absolute_url(self):
        from django.urls import reverse, NoReverseMatch
        try:
            return reverse('admin_juego_condiciones_detail', kwargs={'pk': self.pk})
        except NoReverseMatch:
            return '/admin/'

    def get_is_equipo_by_number(self):
        return 1 if self.equipo else 0


class JugadasInformativas(CachinEvent, models.Model):
    """JugadasInformativas: apuesta informativas

    Campos definidos:
        detalle_encuentro(foreign): detalle del encuentro que define
            al equipo del encuentro al cual pertenece la informacion

        encuentros_modalidad(foreign): modalidad por encuentro que referencia
            a que modalidad pertenece la informacion

        condicion(foreign): condicion a la cual pertenece la informacion

        ref_principal(string): referencia principal

        ref_other_1(string): referencia nivel 1

        ref_other_2(string): referencia nivel 2

        ref_other_3(string): referencia nivel 3

        sistema(foreign): sistema de juego al cual pertenece la jugada

        created_at y updated_at: registros de creacion y actualizacion.
    """
    detalle_encuentro = models.ForeignKey(
        'admin_juego.Sorteo',
        on_delete=models.CASCADE,
        related_name='jugadas_detalle_sorteo',
    )
    encuentros_modalidad = models.ForeignKey(
        'admin_juego.SorteoModalidades',
        on_delete=models.CASCADE,
    )
    condicion = models.ForeignKey(
        'admin_juego.Condiciones',
        on_delete=models.CASCADE,
    )
    ref_principal = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    ref_other_1 = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    ref_other_2 = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    ref_other_3 = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    sistema = models.ForeignKey(
        'admin_juego.SistemaJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    origen = models.ForeignKey(
        'admin_juego.Sorteo',
        on_delete=models.CASCADE,
        related_name='jugadas_origen',
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
        db_tablespace = 'ts_parley'
        verbose_name = ('Jugada informativa')
        verbose_name_plural = ('apuesta informativas')

    def __str__(self):
        return '{0} | {1} | {2} | {3} | {4} | {5}'.format(
            self.encuentros_modalidad.encuentro,
            self.encuentros_modalidad.modalidad_grupo.grupo,
            self.encuentros_modalidad.modalidad_grupo.modalidad,
            self.condicion,
            self.ref_principal,
            self.sistema,
        )

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.encuentros_modalidad.encuentro.__module__.split('.')[0],
            self.encuentros_modalidad.encuentro.__class__.__name__.lower(),
            self.encuentros_modalidad.encuentro_id
        )

    name_cache = 'jugada_json_event'
    name_data_type_origin = types_notification['data_type_origin']['jugada'][0]
    broadcast_automatic = False

    def get_origen(self):
        return self.origen.pk if self.origen else 0

    def set_cache(self, cache_standar=True):
        json = {
            'indice': self.detalle_encuentro.indice,
            'favorito': 0,
            'logro_americano': '0',
            'logro_europeo': '0',
            'ref': self.ref_other_1,
            'pertenece': self.ref_principal,
            'is_equipo': 1,
            'origen': self.get_origen(),
            'sistema': self.sistema_id
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )

        if cache_standar is False:
            json['deporte_id'] = self.encuentros_modalidad.deporte_grupo.deporte_id
            json['encuentro_id'] = self.encuentros_modalidad.encuentro_id
            json['grupo_id'] = self.encuentros_modalidad.modalidad_grupo.grupo_id
            json['modalidad_id'] = self.encuentros_modalidad.modalidad_grupo.modalidad_id
            json['encuentro_modalidad_id'] = self.encuentros_modalidad.pk
            if EventNotification.objects.filter(
                    pk_origin=self.encuentros_modalidad_id,
                    data_origin=self.encuentros_modalidad.name_data_type_origin,
                    sistema=self.encuentros_modalidad.sistema_id,
            ).exists() is False:
                self.encuentros_modalidad.broadcast(
                    sistema=self.encuentros_modalidad.sistema,
                    day=self.encuentros_modalidad.encuentro.horajuego.date(),
                )
        return json

    @staticmethod
    def get_carefully(kwargs, sistemajuego, sistemalogros):
        try:
            kwargs['sistema'] = sistemalogros
            return JugadasInformativas.objects.get(
                **kwargs
            )
        except JugadasInformativas.DoesNotExist:
            kwargs['sistema'] = sistemajuego
            return JugadasInformativas.objects.get(
                **kwargs
            )

    def create_heir(self, encuentro_modalidad, sistemalogros):
        if JugadasInformativas.objects.filter(
            detalle_encuentro=self.detalle_encuentro,
            encuentros_modalidad=self.encuentros_modalidad,
            condicion=self.condicion,
            sistema=sistemalogros,
        ).exists():
            jugada = JugadasInformativas.objects.get(
                detalle_encuentro=self.detalle_encuentro,
                encuentros_modalidad=self.encuentros_modalidad,
                condicion=self.condicion,
                sistema=sistemalogros,
            )
            jugada.encuentros_modalidad = encuentro_modalidad
            jugada.origen = self
            jugada.ref_principal = self.ref_principal
            jugada.ref_other_1 = self.ref_other_1
            jugada.ref_other_2 = self.ref_other_2
            jugada.ref_other_3 = self.ref_other_3
            jugada.save(update_fields=[
                'encuentros_modalidad',
                'origen',
                'ref_principal',
                'ref_other_1',
                'ref_other_2',
                'ref_other_3',
            ])
            return jugada
        else:
            return JugadasInformativas.objects.update_or_create(
                detalle_encuentro=self.detalle_encuentro,
                encuentros_modalidad=encuentro_modalidad,
                condicion=self.condicion,
                sistema=sistemalogros,
                defaults={
                    'origen': self,
                    'ref_principal': self.ref_principal,
                    'ref_other_1': self.ref_other_1,
                    'ref_other_2': self.ref_other_2,
                    'ref_other_3': self.ref_other_3,
                }
            )[0]


class apuesta(CachinEvent, models.Model):
    """apuesta: apuesta

    Campos definidos:
        detalle_encuentro(foreign): detalle del encuentro que define
            al equipo del encuentro al cual pertenece la jugada

        encuentros_modalidad(foreign): modalidad por encuentro que referencia
            a que modalidad pertenece la jugada

        condicion(foreign): condicion a la cual pertenece la jugada

        indice(entero): entero que sirve para saber indices de todo tipo,
            ejemplo la condicion home/visitante 1=home 2=visitante

        valor_etq_ref(string): referencia de la condicion en caso de existir

        valor_americano(entero): entero que tiene el logro americano

        valor_europeo(decimal): decimal que guarda el logro tipo europeo

        status(foreign): estatus de la jugada

        favorito(booleano): indica si la jugada pertenece al equipo favorito

        sistema(foreign): sistema de juego al cual pertenece la jugada

        created_at y updated_at: registros de creacion y actualizacion.
    """

    prefix_filter = 'condicion'

    detalle_encuentro = models.ForeignKey(
        'admin_juego.Sorteo',
        on_delete=models.CASCADE,
        related_name='apuestas_detalle_sorteo',
    )
    encuentros_modalidad = models.ForeignKey(
        'admin_juego.SorteoModalidades',
        on_delete=models.CASCADE,
    )
    condicion = models.ForeignKey(
        'admin_juego.Condiciones',
        on_delete=models.CASCADE,
    )
    indice = models.IntegerField(
        verbose_name='Indices',
        null=True,
        blank=True
    )
    valor_etq_ref = models.CharField(
        verbose_name='Etiqueta referencia',
        max_length=140,
        null=True,
        blank=True
    )
    valor_americano = models.IntegerField(
        verbose_name='Logro americano',
        null=True,
        blank=True
    )
    valor_europeo = models.DecimalField(
        verbose_name='Logro europeo',
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    favorito = models.BooleanField(
        verbose_name='Favorito',
        null=True,
        blank=True,
        default=None,
    )
    sistema = models.ForeignKey(
        'admin_juego.SistemaJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    origen = models.ForeignKey(
        'admin_juego.Sorteo',
        on_delete=models.CASCADE,
        related_name='apuestas_origen',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )
    pk_clone = models.IntegerField(
        default=0,
        db_index=True,
        editable=False,
    )
    audit_exclude = ('admin_status.Status', 'valor_europeo', 'favorito', 'indice', 'pk_clone')

    class Meta:
        db_tablespace = 'ts_parley'
        verbose_name = ('Jugada por encuentro')
        verbose_name_plural = ('apuesta por Sorteo')

    def __str__(self):
        return '{0} | {1} | {2} | {3}'.format(
            self.encuentros_modalidad.encuentro,
            self.encuentros_modalidad.modalidad_grupo,
            self.get_pertenece(),
            self.valor_americano,
        )

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        return '{0}.{1}.{2}'.format(
            self.encuentros_modalidad.encuentro.__module__.split('.')[0],
            self.encuentros_modalidad.encuentro.__class__.__name__.lower(),
            self.encuentros_modalidad.encuentro_id
        )

    def get_field_etiqueta_logro(self):
        return 'ref_logro_{0}'.format(self.pk)

    def get_field_logro(self):
        return 'logro_{0}'.format(self.pk)

    def get_condicion(self):
        self._cache_condicion = getattr(self, '_cache_condicion', None)
        if not self._cache_condicion:
            self._cache_condicion = Condiciones.objects.get(
                pk=self.condicion_id)
        return self._cache_condicion

    def get_pertenece(self, is_equipo=True):
        try:
            if self.get_condicion().equipo:
                if is_equipo:
                    return self.detalle_encuentro.equipos_temporadas.equipo.nombre
                else:
                    return ''
            else:
                return self.get_condicion().nombre.split('/')[self.indice - 1]
        except Exception:
            return ''

    def get_pertenece_id(self):
        try:
            if self.get_condicion().equipo:
                return None
            else:
                return (self.indice - 1)
        except Exception:
            return None

    def get_logro_americano(self):
        if self.valor_americano is None:
            return 0
        else:
            return '{0}'.format(self.valor_americano) \
                if self.valor_americano < 0 else '+{0}'.format(self.valor_americano)

    def get_ref(self):
        return '' if not self.valor_etq_ref else self.valor_etq_ref

    def get_favorito(self):
        if self.favorito is True:
            return 1
        elif self.favorito is False:
            return 0
        elif self.favorito is None:
            return 2

    name_cache = 'jugada_json_event'
    name_data_type_origin = types_notification['data_type_origin']['jugada'][0]
    broadcast_automatic = False

    def get_origen(self):
        return self.origen.pk if self.origen else 0

    def set_cache(self, cache_standar=True):
        valor_europeo = self.valor_europeo
        if valor_europeo is None:
            valor_europeo = 0

        json = {
            'indice': self.indice,
            'favorito': self.get_favorito(),
            'logro_americano': self.get_logro_americano(),
            'logro_europeo': '{0}'.format(round(valor_europeo, 2)),
            'ref': self.get_ref(),
            'pertenece': self.get_pertenece(is_equipo=False),
            'is_equipo': self.get_condicion().get_is_equipo_by_number(),
            'origen': self.get_origen(),
            'sistema': self.sistema_id,
        }
        cache.set(
            '{0}{1}'.format(
                self.name_cache,
                self.pk
            ),
            json,
            CACHES_CONF_TIME['admin_juegos'][self.name_cache]
        )

        if cache_standar is False:
            json['deporte_id'] = self.encuentros_modalidad.deporte_grupo.deporte_id
            json['encuentro_id'] = self.encuentros_modalidad.encuentro_id
            json['grupo_id'] = self.encuentros_modalidad.modalidad_grupo.grupo_id
            json['modalidad_id'] = self.encuentros_modalidad.modalidad_grupo.modalidad_id
            json['encuentro_modalidad_id'] = self.encuentros_modalidad.pk
            if EventNotification.objects.filter(
                pk_origin=self.encuentros_modalidad_id,
                data_origin=self.encuentros_modalidad.name_data_type_origin,
                sistema=self.encuentros_modalidad.sistema_id,
            ).exists() is False:
                self.encuentros_modalidad.broadcast(
                    sistema=self.encuentros_modalidad.sistema,
                    day=self.encuentros_modalidad.encuentro.horajuego.date(),
                )
        return json

    @staticmethod
    def get_carefully(kwargs, sistemajuego, sistemalogros):
        try:
            kwargs['sistema'] = sistemalogros
            return apuesta.objects.get(
                **kwargs
            )
        except apuesta.DoesNotExist:
            kwargs['sistema'] = sistemajuego
            return apuesta.objects.get(
                **kwargs
            )

    def create_heir(self, encuentro_modalidad, sistemalogros):
        if apuesta.objects.filter(
            detalle_encuentro=self.detalle_encuentro,
            encuentros_modalidad=self.encuentros_modalidad,
            condicion=self.get_condicion(),
            indice=self.indice,
            sistema=sistemalogros,
        ).exists():
            jugada = apuesta.objects.get(
                detalle_encuentro=self.detalle_encuentro,
                encuentros_modalidad=self.encuentros_modalidad,
                condicion=self.get_condicion(),
                indice=self.indice,
                sistema=sistemalogros,
            )
            jugada.encuentros_modalidad = encuentro_modalidad
            jugada.origen = self
            jugada.valor_etq_ref = self.valor_etq_ref
            jugada.valor_americano = self.valor_americano
            jugada.valor_europeo = self.valor_europeo
            jugada.status = self.status
            jugada.favorito = self.favorito
            jugada.save(update_fields=[
                'encuentros_modalidad',
                'origen',
                'valor_etq_ref',
                'valor_americano',
                'valor_europeo',
                'admin_status.Status',
                'favorito',
            ])
            return jugada
        else:
            return apuesta.objects.update_or_create(
                detalle_encuentro=self.detalle_encuentro,
                encuentros_modalidad=encuentro_modalidad,
                condicion=self.get_condicion(),
                indice=self.indice,
                sistema=sistemalogros,
                defaults={
                    'origen': self,
                    'valor_etq_ref': self.valor_etq_ref,
                    'valor_americano': self.valor_americano,
                    'valor_europeo': self.valor_europeo,
                    'admin_status.Status': self.status,
                    'favorito': self.favorito,
                }
            )[0]

    def broadcast(self, sistema=None, day=None):
        if EventNotification.objects.filter(
            pk_origin=self.encuentros_modalidad_id,
            data_origin=self.encuentros_modalidad.name_data_type_origin,
            sistema=self.encuentros_modalidad.sistema_id,
        ).exists() is False:
            self.encuentros_modalidad.broadcast(sistema, day)
        super(apuesta, self).broadcast(sistema, day)


class RestriccionesSorteo(models.Model):
    """RestriccionesSorteo: Restricion de referencias

    Campos definidos:
        grupo(foreign): grupo al cual pertenece la restriccion
        modalidad(foreign): modalidad a la cual pertenece la restriccion
        condicion(foreign): condicion a la cual pertenece la restriccion

        Nota: el grupo la modalidad y restriccion conforman un arco

        deporte(foreign): deporte al cual pertenece la restriccion

        max_logro_favorito(entre): valor maximo del logro para un equipo
            favorito

        max_logro_no_favorito(entre): valor maximo del logro para un equipo no
            favorito

        min_ref(string): minimo de referencia

        max_ref(string): maximo de referencia

        created_at y updated_at: registros de creacion y actualizacion.
    """

    deporte = models.ForeignKey(
        'admin_juego.TipoProducto',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    grupo = models.ForeignKey(
        'admin_juego.GruposSorteo',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    modalidad = models.ForeignKey(
        'admin_juego.ModalidadJuego',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    condicion = models.ForeignKey(
        'admin_juego.Condiciones',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )

    max_logro_favorito = models.IntegerField(
        verbose_name='Logro maximo (-) favoritos (*)',
        help_text='Ingrese el valor debe ser negativo',
        null=True,
        blank=True
    )
    max_logro_no_favorito = models.IntegerField(
        verbose_name='Logro maximo (+) no favoritos (*)',
        help_text='Ingrese el valor debe ser positivo',
        null=True,
        blank=True
    )
    min_ref = models.CharField(
        max_length=140,
        null=True,
        blank=True,
        verbose_name='Referencia minima (*)',
        help_text='Ingrese la referencia minima'
    )
    max_ref = models.CharField(
        max_length=140,
        null=True,
        blank=True,
        verbose_name='Referencia maxima (*)',
        help_text='Ingrese la referencia maxima'
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
        db_tablespace = 'ts_parley'
        verbose_name = ('Restriccion de referencia y logro')
        verbose_name_plural = ('Restricciones de referencias y logros')

    def __str__(self):
        return '{0} | {1}'.format(
            self.deporte,
            self.get_pertenece()
        )

    def get_pertenece(self):
        """
        Retorna el objeto al cual pertenece la restriccion
        """
        if self.modalidad_id is not None:
            return '{0}'.format(self.modalidad)
        elif self.condicion_id is not None:
            return '{0}'.format(self.condicion)
        elif self.grupo_id is not None:
            return '{0}'.format(self.grupo)
        else:
            return ''

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        if self.modalidad_id is not None:
            return '{0}.{1}.{2}'.format(
                self.modalidad.__module__.split('.')[0],
                self.modalidad.__class__.__name__.lower(),
                self.modalidad_id
            )
        elif self.condicion_id is not None:
            return '{0}.{1}.{2}'.format(
                self.condicion.__module__.split('.')[0],
                self.condicion.__class__.__name__.lower(),
                self.condicion_id
            )
        elif self.grupo_id is not None:
            return '{0}.{1}.{2}'.format(
                self.grupo.__module__.split('.')[0],
                self.grupo.__class__.__name__.lower(),
                self.grupo_id
            )
        else:
            return ''

# =============================================================
# =============================================================
# ====================Modelos auditados========================


auditoria.register(
    SistemaJuego,
    TipoProducto,
    PeriodoSorteo,
    ModalidadJuego,
    ModalidadProducto,
    TipoNumeroSorteo,
    NumeroSorteo,
    ModalidadPeriodo,
    Fechas,
    GruposSorteo,
    ModalidadGrupo,
    Sorteo,
    SorteoDetalle,
    GruposApuesta,
    TipoProducto_Grupos,
    ModalidadJuego_Grupos,
    SorteoModalidades,
    Condiciones,
    JugadasInformativas,
    apuesta,
    RestriccionesSorteo,
)
# =============================================================
# =============================================================
