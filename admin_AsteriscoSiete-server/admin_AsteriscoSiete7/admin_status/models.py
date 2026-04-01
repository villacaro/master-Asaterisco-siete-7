# -*- coding: utf-8 -*-

from admin_asterisco7.settings import CACHES_CONF_TIME
from django.core.cache import cache
from django.db import models
from django.utils.timezone import now


class Status(models.Model):
    """Status: tabla parametro de los distintos estatus gestionados
    en el sistema

    Atributos:
        name: nombre del status

        codename: codename en string del status, para manejarlo en codigo,
            sin afectar su nombre

        content_type: tipo de contenido del estatus, si es de usuarios,
            de tickets, de taquillas etc.

        order: orden de impresion de los estatus, util solo para la taquilla

        created_at y updated_at: registros de creacion y actualizacion.
    """
    name = models.CharField(
        max_length=160
    )
    codename = models.CharField(
        max_length=160,
        unique=True,
        db_index=True,
    )

    content_type_choices = [
        [0, "Status de actualizacion"],
        [1, "Status de usuarios"],
        [2, "Status de encuentros"],
        [3, "Status de taquillas"],
        [4, "Status de jugadas"],
        [5, "Status de encuentro resultado"],
        [6, "Status de venta de tickets"],
        [7, "Status de ??????"],
        [8, "Status de tickets"],
    ]

    content_type = models.IntegerField(
        choices=content_type_choices,
        db_index=True,
    )
    order = models.IntegerField(
        verbose_name="Orden (*)",
        help_text="Ingrese la numeraciÃ³n de orden",
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

    def __str__(self):
        return self.name

    class Meta:
        db_tablespace = "ts_comer"
        verbose_name = ('Estatus')
        verbose_name_plural = ('Estatus')
        ordering = ["content_type", ]

    def save(self, *args, **kwargs):
        """
        Al guardar un status se busca actualizar una cache que es la que siempre
        se consulta.
        """
        super(Status, self).save(*args, **kwargs)
        cache.delete('status_{0}'.format(self.codename))

    @staticmethod
    def get_status_by_codename(codename):
        status = cache.get('status_{0}'.format(codename))
        if not status:
            status = Status.objects.get(codename=codename)
            cache.set(
                'status_{0}'.format(codename),
                status,
                CACHES_CONF_TIME['registros_db']['admin_status.Status']
            )
        return status


class StatusDetail(models.Model):
    """StatusDetail: es esta tabla se guarda todo el historico de los status,
    respecto a un usuario en particular

    Atributos:
        status: clave foranea de tipo de status

        user: clave foranea del usuario al cual se le asigno
            el status

        startdate: fecha de inicio del status.

        comment: posible comentario, para observaciones, este campo actualmente no se usa

        enddate: fecha de fin del status, en caso de ser None es el status activo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        'admin_users.Users',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    startdate = models.DateField(
        auto_now_add=True,
    )
    enddate = models.DateField(
        null=True,
        blank=True
    )
    comment = models.CharField(
        max_length=160,
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
        db_tablespace = "ts_comer"
        verbose_name = ('Detalle de estatus')
        verbose_name_plural = ('Detalle de estatus de los usuario')

    def __str__(self):
        """
        Retorna el string representativo de la tabla
        """
        return "{0} | {1}".format(self.user, self.status)

    @staticmethod
    def close_status(object_):
        """
        Metodo statico que dado una StatusDetail, lo cierra
        """
        try:
            object_.enddate = now()
            object_.save()
            return True
        except Exception:
            return False

    @staticmethod
    def close_status_to(object_, status_codename):
        """
        Metodo statico que dado una StatusDetail, y un codename, asigna un
        nuevo status
        """
        try:
            object_.enddate = now()
            object_.save()
            return Status.get_status_by_codename(codename=status_codename)
        except Exception:
            return None


class TaquillaStatusDetail(models.Model):
    """TaquillaStatusDetail: es esta tabla se guarda todo el historico de los status,
    respecto a un usuario de taquilla en particular

    Atributos:
        status: clave foranea de tipo de status

        usuariotaquilla: clave foranea del usuario de taquilla
            al cual se le asigno el status

        startdate: fecha de inicio del status.

        comment: posible comentario, para observaciones, este campo actualmente no se usa

        enddate: fecha de fin del status, en caso de ser None es el status activo

        created_at y updated_at: registros de creacion y actualizacion.
    """
    status = models.ForeignKey(
        'admin_status.Status',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    usuariotaquilla = models.ForeignKey(
        'admin_comercializacion.UsuariosTaquilla',  # TODO: revisar modelo destino
        on_delete=models.CASCADE,
    )
    startdate = models.DateField(
        auto_now_add=True,
    )
    enddate = models.DateField(
        null=True,
        blank=True
    )
    comment = models.CharField(
        max_length=160,
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
        db_tablespace = "ts_comer"
        verbose_name = ('Detalle de estatus')
        verbose_name_plural = ('Detalle de estatus de las taquillas')

    def compare_status(self, status_pk):
        return self.status_id == status_pk

    def close_status_to(self, codename):
        try:
            self.enddate = now()
            self.save(update_fields=['enddate', 'updated_at'])
            status = Status.get_status_by_codename(codename=codename)
            TaquillaStatusDetail.objects.create(
                status=status,
                usuariotaquilla=self.usuariotaquilla
            )
            self.usuariotaquilla.status = status
            self.usuariotaquilla.save(update_fields=['admin_status.Status', 'updated_at'])
            return True
        except Exception:
            return False
