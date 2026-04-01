# -*- coding: utf-8 -*-

import uuid

from admin_asterisco7.settings import CACHES_CONF_TIME
from django.core.cache import cache
from django.db import models


class AbstractBaseUUID(models.Model):
    """
    Clase base con la que se crean modelos con un pk tipo uuid,
    es decir, es un pk comprendido por digitos y letras que alargan
    la vida util de los pk de un modelo en base de datos, tipo
    base de datos orientadas a archivos.
    """

    id = models.CharField(
        max_length=36,
        primary_key=True,
        db_index=True,
    )

    # id = models.UUIDField(
    #    primary_key=True,
    #    default=uuid.uuid4,
    #    editable=False
    # )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.pk:
            while True:
                try:
                    self.pk = uuid.uuid4().hex
                    super(AbstractBaseUUID, self).save(*args, **kwargs)
                    break
                except Exception:
                    pass
        else:
            super(AbstractBaseUUID, self).save(*args, **kwargs)


class ProtectDelete(models.Model):
    """
    Protege los modelos contra eliminacion
    usado en modelos importantes como por ejemplo EncuentroDetail
    """

    not_delete = False

    class Meta:
        abstract = True

    # Se desactivo el seguro contra eliminación
    """
    def delete(self, *args, **kwargs):
        delete = False
        if not self.not_delete:
            if not self.get_relate():
                delete = True
                super(ProtectDelete, self).delete(*args, **kwargs)

        if delete:
            from crequest.middleware import CrequestMiddleware
            request = CrequestMiddleware.get_request()
            if request:
                if type(self._meta.verbose_name) == str:
                    verbose = self._meta.verbose_name
                else:
                    verbose = self.__class__.__name__.lower()

                from django.contrib import messages
                messages.error(
                        request,
                        "¡El objeto de {0} {1} no se puede eliminar!".format(
                                    verbose,
                                    self
                        )
                )
    """

    def get_relate(self):
        """
        Consulta todos los hijos relacionados con el
        objeto de la instancia actual
        """
        process_delete = False
        for attr in dir(self):
            # recorre todos los atributos
            # (que terminan en _set) ya que
            # son relaciones hacia abajo
            if attr.endswith("_set"):
                querryset = getattr(self, attr)
                if querryset.all().exists():
                    process_delete = True
        return process_delete


class BaseGenericProcessModelCache(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        super(BaseGenericProcessModelCache, self).save()
        self.base_cache_clear_manage()

    def delete(self, *args, **kwargs):
        super(BaseGenericProcessModelCache, self).delete(*args, **kwargs)
        self.base_cache_clear_manage()

    def base_cache_clear_manage(self):
        cache.delete(
            '{0}_{1}'.format(self.prefix_cache_manager, self.pk)
        )


class BaseGenericProcessManagerCache(models.Manager):
    """
        Esta Clase generara cache unica por objeto en el get
        Debe invalidarse en el save
    """
    def get(self, *args, **kwargs):
        if len(kwargs) == 1 and kwargs.get('pk'):
            _object = cache.get(
                '{0}_{1}'.format(self.model.prefix_cache_manager, kwargs.get('pk'))
            )
            if not _object:
                _object = super(BaseGenericProcessManagerCache, self).get(*args, **kwargs)
                cache.set(
                    '{0}_{1}'.format(self.model.prefix_cache_manager, kwargs.get('pk')),
                    _object,
                    CACHES_CONF_TIME['registros_db']['objects_games'],
                )
            return _object
        else:
            return super(BaseGenericProcessManagerCache, self).get(*args, **kwargs)
