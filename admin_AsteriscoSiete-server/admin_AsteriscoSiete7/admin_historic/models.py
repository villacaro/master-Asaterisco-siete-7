# -*- coding: utf-8 -*-
import re

from admin_lib.util_models import AbstractBaseUUID
from django.conf import settings as django_settings
from django.conf import settings
from django.core.cache import cache
try:
    from django.urls import reverse
except ImportError:
    from django.urls import reverse  # noqa (Django <2.0 fallback)
from django.db import models
from django.utils.timezone import now
try:
    from jsonfield import JSONField
except ImportError:
    from django.db.models import JSONField

# Constantes de configuracion - compatibles con settings_local y settings
CACHES_CONF_TIME = getattr(django_settings, 'CACHES_CONF_TIME', {
    'registros_db': {
        'user_process': 60 * 60 * 24 * 7,
        'session_expire': 60 * 20,
    }
})
PAGE_404_URL = getattr(django_settings, 'PAGE_404_URL', '#404-page-not-found')

"""
Inicializa el choice del content_type con las app instaladas,
cada app es una posible opcion.
"""
choices_apps = []
for content_type in settings.INSTALLED_APPS:
    if content_type.find('admin_') >= 0:
        label = re.sub('[^a-zA-Z0-9]', ' ', content_type)
        choices_apps.append(
            (content_type,
                label.capitalize()
             )
        )

MODULES = {
    'mc': (
        'admin_comercializacion',
        'admin_permisologia.permissionssales',
        'admin_profiles',
    ),
    'md': (
        'admin_juego',
        'admin_resultados',
    ),
    'ma': (
        'admin_finanzas',
    ),
    'ms': (
        'admin_permisologia.groups',
        'admin_users',
    ),
}

MODULES_VERBOSE = (
    ('', 'Seleccione un modulo',),
    ('mc', 'Comercial',),
    ('md', 'Deportivo',),
    ('ma', 'Administrativo',),
    ('ms', 'Sesion',),
)

MODULES_DISPLAY = {
    'admin_comercializacion': 'Comercial',
    'admin_permisologia.permissionssales': 'Comercial',
    'admin_profiles': 'Comercial',
    'admin_juego': 'Deportivo',
    'admin_resultados': 'Deportivo',
    'admin_finanzas': 'Administrativo',
    'admin_permisologia.groups': 'Sesion',
    'admin_users': 'Sesion',
}


class UsersProcesses(models.Model):
    """UsersProcesses: procesos de los uaurios

    Tabla parametro que define tipos de procesos de usuario.

    Campos definidos:
        name(string): nombre del procedo de usuario, por ejemplo: login

        codename(string): codigo en minusculas del proceso de usuario,
            por ejemplo: process_login

        content_type(string): indica la app a la cual pertenece el proceso

        process_suc(self): proceso padre, por ejemplo la modificacion de un modelo,
        debe ser despues de un login, esto indica que hereda del login.

        created_at y updated_at: registros de creacion y actualizacion.
    """
    name = models.CharField(
        max_length=140,
        null=True,
        blank=True
    )
    codename = models.CharField(
        max_length=140,
        unique=True
    )
    content_type = models.CharField(
        max_length=50,
        null=True,
        blank=True,
        choices=choices_apps,
        verbose_name="App"
    )
    process_suc = models.ForeignKey(
        'UsersProcesses',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
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
        verbose_name = ('Tipo de proceso')
        verbose_name_plural = ('Tipos de procesos')
        ordering = ["content_type", ]

    def __str__(self):
        """
        Devuelve el nombre de la app a la cual pertenece y el nombre del proceso.
        """
        return "{0} | {1}".format(self.get_content_type_display(), self.name)

    @staticmethod
    def get_userprocess_by_codename(codename):
        process = cache.get('user_process_{0}'.format(codename))
        if not process:
            try:
                process = UsersProcesses.objects.get(codename=codename)
            except UsersProcesses.DoesNotExist:
                raise
            cache.set(
                'user_process_{0}'.format(codename),
                process,
                CACHES_CONF_TIME['registros_db']['user_process'],
            )
        return process


class Sessions(AbstractBaseUUID):
    """Sessions: session de los usuarios, hereda de la clase abstracta token,
    que predefine un primary_key de tipo token para alargar la vida de la tabla.

    En dicha tabla se guardan las distintas sessiones de los usuarios.

    Campos definidos:
        startdate(datetime): indica el tiempo en el cual la session se inicio

        enddate(datetime): indica el tiempo en el cual la session se cerro

        user(ForeignKey): indica el asuario al cual pertenece la session

        ip(GenericIPAddressField): indica la direccion ip desde la cual se creo la session

        user_agent(string): guardamos la variable HTTP_USER_AGENT, recibida en el
            request en bruto, para futuros calculos estadisticos

        cookie(string): es la variable de session guardada para verificaciones de seguridad

        created_at y updated_at: registros de creacion y actualizacion.
    """
    startdate = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
    )
    enddate = models.DateTimeField(
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'admin_users.Users',
        on_delete=models.CASCADE,
    )
    ip = models.GenericIPAddressField(
    )
    user_agent = models.CharField(
        max_length=200,
        null=True,
        blank=True
    )
    cookie = models.CharField(
        max_length=1000,
        null=True,
        blank=True
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
        verbose_name = ('Session de usuario')
        verbose_name_plural = ('Sessiones por usuario')
        ordering = ["-enddate", ]

    def get_comercializadora(self):
        if self.cookie:
            from admin_finanzas.models import Comercializadora
            texto = self.cookie.split(",")
            try:
                return Comercializadora.objects.get(
                    pk=texto[2]
                )
            except Exception:
                return "No encontrada"
        return ""

    def new_process_session(self, codename):
        """
        Creamos un nuevo proceso en detalle de session
        """
        return SessionsDetail.objects.create(
            userprocess=UsersProcesses.get_userprocess_by_codename(
                codename=codename),
            session_id=self.pk
        )

    def check_seccion(self):
        if self.enddate is not None:
            return False

        active = cache.get('sessions_expire_{0}'.format(self.pk))
        if not active:
            self.new_process_session(codename="process_expiresession")
            self.enddate = now()
            self.save(update_fields=['enddate'])
        else:
            cache.set(
                'sessions_expire_{0}'.format(self.pk),
                True,
                CACHES_CONF_TIME['registros_db']['session_expire'],
            )
        return active


class SessionsDetail(AbstractBaseUUID):
    """SessionsDetail: detalle de las sessiones, hereda de la clase abstracta token,
    que predefine un primary_key de tipo token para alargar la vida de la tabla.

    Campos definidos:
        userprocess(foreign): proceso al cual se hace referencia

        session(foreign): session a la cual se hace referencia

        ref(string): referencia del modelo al cual le pertenece
            la auditoria

        ref_related(string): relacion indirecta con modelos padres, por ejemplo el
            modelo usuarios no puede guardar la auditoria de los estatus que se
            aplican dado que la relacion no esta directamente enlazada con dicha
            tabla, entonces en la tabla de estatus de los usuarios se añade un
            metodo que al momento de ser auditada la relaciona con usuarios,
            asi luego al ver el historial de un usuario es posible rescatar
            dichos registros.

        json(json): archivo json que contiene toda la data guardada,
            debe contener algo similar a esto:
                {
                    "model": instance.__module__.split(".")[0]+"."+instance.__class__.__name__,
                    "url": request.path,
                    "attr": { "fields": {},
                             "foreign": {},
                             "m2m": {}
                            },
                    "process": process,
                  }
            para mas detaller ver el archivo de auditoria

        created_at y updated_at: registros de creacion y actualizacion.
    """
    userprocess = models.ForeignKey(
        'UsersProcesses',
        on_delete=models.CASCADE,
    )
    session = models.ForeignKey(
        'Sessions',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )
    ref = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True,
    )
    ref_related = models.CharField(
        max_length=200,
        null=True,
        blank=True,
        db_index=True,
    )
    json = JSONField(
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        db_index=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        verbose_name = ('Detalle de una session')
        verbose_name_plural = ('Detalle de las sessiones por usuario')
        ordering = ["-created_at", ]

    def get_json_count_attr(self):
        """
        Devuelve la cantidad de atributos auditados
        """
        if self.ref:
            return int(
                len(self.json["attr"]["fields"]) +
                len(self.json["attr"]["foreign"]) +
                len(self.json["attr"]["m2m"])
            )
        else:
            return 0

    def get_json_object(self):
        """
        Devuelve el objeto auditado
        """

        try:
            # Por cualquier exeption ya no se muestra el link
            app_model = self.json["model"].split(".")
            from django.apps import apps
            app_config = apps.get_app_config(app_model[0])
            _object = app_config.models.get(app_model[1].lower())
            if _object:
                return _object.objects.get(pk=self.ref.split(".")[-1])
        except Exception:
            pass
        return None

    def get_json_filter_url(self):
        """
        Devuelve el url del filtro para este objeto,
        con este url se filtros todas las sessiones que han
        modificado al mismo objeto
        """
        if self.ref:
            return reverse("admin_historic_app_model_ref", kwargs={
                'app': self.ref.split(".")[0],
                'model': self.ref.split(".")[1],
                'ref': self.ref.split(".")[2],
            })
        else:
            return PAGE_404_URL

    def get_json_object_url(self):
        """
        Devuelve el url absoluta de detalle para visualizar los
        cambios realizados en la instanca
        """
        if self.ref:
            return reverse("admin_historic_app_model_ref_detail", kwargs={
                'app': self.ref.split(".")[0],
                'model': self.ref.split(".")[1],
                'ref': self.ref.split(".")[2],
                'pk': self.pk
            })
        else:
            return PAGE_404_URL

    def get_json_absolute_url(self):
        """
        Devuelve el url del detalle del objeto auditado
        """
        try:
            # Por cualquier exeption ya no se muestra el link
            obj = self.get_json_object()
            if hasattr(obj, "get_absolute_url"):
                return obj.get_absolute_url()
        except Exception:
            pass

        return PAGE_404_URL

    def get_app(self):
        """
        Devuelve la app del objeto auditado
        """
        return self.ref.split(".")[0]

    def get_model(self):
        """
        Devuelve la app del objeto auditado
        """
        return self.ref.split(".")[1]

    def get_obj_id(self):
        """
        Devuelve el id del objeto auditado
        """
        return self.ref.split(".")[2]

    def get_module(self):
        if not self.ref:
            return ''
        app = self.get_app()
        module = MODULES_DISPLAY.get(app)
        if not module:
            app = '{0}.{1}'.format(app, self.get_model())
            module = MODULES_DISPLAY.get(app)
            if not module:
                module = ''
        return module


class TaquillaSessions(AbstractBaseUUID):
    """TaquillaSessions: Sessiones de las taquillas, hereda de la clase abstracta token,
    que predefine un primary_key de tipo token para alargar la vida de la tabla.

    Campos definidos:
        startdate(datetime): indica el tiempo en el cual la session se inicio

        enddate(datetime): indica el tiempo en el cual la session se cerro

        user(ForeignKey): indica el asuario de taquilla al cual pertenece la session

        ip(GenericIPAddressField): indica la direccion ip desde la cual se creo la session

        package(entero): entero usado como nivel de seguridad para monirorear
            solicitudes de la conexion de las taquillas, este campo esta en des uso
            y debe ser eliminado cuando ya no se referencie en ningun lado del proyecto

        created_at y updated_at: registros de creacion y actualizacion.
    """
    startdate = models.DateField(
        auto_now_add=True,
    )
    enddate = models.DateField(
        null=True,
        blank=True
    )
    user = models.ForeignKey(
        'admin_comercializacion.UsuariosTaquilla',
        on_delete=models.CASCADE,
    )
    ip = models.GenericIPAddressField(
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
        verbose_name = ('Session por taquilla')
        verbose_name_plural = ('Sessiones por taquillas')
        ordering = ["-enddate", ]


class TaquillaSessionsDetail(AbstractBaseUUID):
    """SessionsDetail: detalle de las sessiones, hereda de la clase abstracta token,
    que predefine un primary_key de tipo token para alargar la vida de la tabla.

    Campos definidos:
        userprocess(foreign): proceso al cual se hace referencia

        session(foreign): session a la cual se hace referencia

        ref(string): referencia del modelo al cual le pertenece
            la auditoria

        ref_related(string): relacion indirecta con modelos padres, por ejemplo el
            modelo usuarios no puede guardar la auditoria de los estatus que se
            aplican dado que la relacion no esta directamente enlazada con dicha
            tabla, entonces en la tabla de estatus de los usuarios se añade un
            metodo que al momento de ser auditada la relaciona con usuarios,
            asi luego al ver el historial de un usuario es posible rescatar
            dichos registros.

        detail(json): archivo json que contiene toda la data guardada

        enrro(booleano): campo usado para saber si hubo un error

        created_at y updated_at: registros de creacion y actualizacion.
    """
    userprocess = models.ForeignKey(
        'UsersProcesses',
        on_delete=models.CASCADE,
    )
    session = models.ForeignKey(
        'TaquillaSessions',
        on_delete=models.CASCADE,
    )
    detail = JSONField(
        null=True,
        blank=True
    )
    enrro = models.BooleanField(
        default=False
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
        verbose_name = ('Detalle de la session por taquilla')
        verbose_name_plural = ('Detalle de las sessiones por taquillas')
        ordering = ["-created_at", ]


class HechoConnectionsComer(models.Model):
    """DimensionComercializacion: Hecho de comercializacion para conexiones

    Campos definidos:
        operadora_id(entero): hace referencia al foraneo del operadora

        bloque_id(entero): hace referencia al foraneo del bloque

        banca_id(entero): hace referencia al foraneo de la banca

        distribuidor_id(entero): hace referencia al foraneo del distribuidor

        agencia_id(entero): hace referencia al foraneo de la agencia

        taquilla_id(entero): hace referencia al foraneo de la taquilla

        connection_at: que indica la hora de la ultima conexion.
    """

    operadora_id = models.IntegerField()
    bloque_id = models.IntegerField()
    banca_id = models.IntegerField()
    distribuidor_id = models.IntegerField()
    agencia_id = models.IntegerField()
    taquilla_id = models.IntegerField(
        db_index=True,
    )

    connection_at = models.DateTimeField(
        auto_now=True,
        editable=False,
    )

    class Meta:
        verbose_name = ('Hecho de conexion')
        verbose_name_plural = ('Hecho de conexiones')

    @staticmethod
    def register_connection(taquilla):
        exist = HechoConnectionsComer.objects.filter(taquilla_id=taquilla.pk).update(
            connection_at=now()
        )
        if not exist:
            HechoConnectionsComer.objects.create(
                taquilla_id=taquilla.pk,
                agencia_id=taquilla.agencia_id,
                distribuidor_id=taquilla.agencia.distribuidores_id,
                banca_id=taquilla.agencia.distribuidores.banca_id,
                bloque_id=taquilla.agencia.distribuidores.banca.bloque_id,
                operadora_id=taquilla.agencia.distribuidores.banca.bloque.operadora_id,
            )

    def get_agencia_conections(self, objecto):
        kwargs = {}
        kwargs[objecto.prefix_filter + '_id'] = objecto.id
        return list(HechoConnectionsComer.objects.filter(
                    **kwargs
                    ).distinct('agencia_id').values_list('agencia_id', flat=True))
