# -*- coding: utf-8 -*-

from admin_historic import auditoria
from django.db import models


class Paises(models.Model):
    """Paises: Paises

    Tabla parametro que define todos los paises del sistema.

    Campos definidos:
        nombre(string): nombre del pais

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=100
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
        db_tablespace = 'ts_comer'
        verbose_name = ('Pais')
        verbose_name_plural = ('Paises')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}'.format(self.nombre)


class Estados(models.Model):
    """Estados: Estados de un pais

    Tabla parametro que define todos los estados de paises del sistema.

    Campos definidos:
        nombre(string): nombre del estado

        pais(foreign): pais al que hace referencia el estado

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=100
    )
    pais = models.ForeignKey(
        'Paises',
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
        db_tablespace = 'ts_comer'
        verbose_name = ('Estado')
        verbose_name_plural = ('Estados')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}'.format(self.nombre)


class Municipios(models.Model):
    """Municipios: Municipios de un estado de un pais

    Tabla parametro que define todos los municipios en los
    estados de paises del sistema.


        nombre(string): nombre del municipio

        capital(string): capital del municipio

        estado(foreign): estado de un pais al que hace referencia el municipio

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=100
    )
    capital = models.CharField(
        max_length=100,
        null=True,
    )
    estado = models.ForeignKey(
        'Estados',
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
        db_tablespace = 'ts_comer'
        verbose_name = ('Municipio')
        verbose_name_plural = ('Municipios')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}, {1}'.format(self.nombre, self.estado)


class Parroquias(models.Model):
    """Parroquias: Parroquias de un municipio

    Tabla parametro que define todos las Parroquias en los
    estados de paises del sistema.

    Campos definidos:
        nombre(string): nombre del estado

        municipio(foreign): municipio de un estado de un pais al
                que hace referencia la ciudad

        created_at y updated_at: registros de creacion y actualizacion.
    """
    nombre = models.CharField(
        max_length=100
    )
    municipio = models.ForeignKey(
        'Municipios',
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
        verbose_name = ('Parroquia')
        verbose_name_plural = ('Parroquias')
        ordering = ['nombre', ]

    def __str__(self):
        return '{0}, {1}'.format(self.nombre, self.municipio)


class Direcciones(models.Model):
    """Direcciones: Direcciones

    Tabla parametro que define todos los municipios en los
    estados de paises del sistema.

    Campos definidos:
        direccion(string): direccion exacta de ubicacion

        ciudad(foreign): ciudad de un municipio de estado de un pais al
                que hace referencia la direccion

        municipio(foreign): municipio de un estado de un pais al
                que hace referencia la direccion

        estado(foreign): estado de un pais al que hace referencia la direccion

        created_at y updated_at: registros de creacion y actualizacion.

    Nota:
        en caso de existir una ciudad se omite, el municipio y el estado
        en caso de existir un municipio se omite el estado

        Es decir ciudad, municipio y estado representan un arco
    """
    direccion = models.CharField(
        max_length=200
    )
    parroquia = models.ForeignKey(
        'Parroquias',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    municipio = models.ForeignKey(
        'Municipios',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    estado = models.ForeignKey(
        'Estados',
        on_delete=models.CASCADE,
        null=True, blank=True,
    )
    longitud = models.IntegerField(null=True, blank=True)
    latitud = models.IntegerField(null=True, blank=True)
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
        db_tablespace = 'ts_comer'
        verbose_name = ('Direccione')
        verbose_name_plural = ('Direcciones')

    def __str__(self):
        return '{0} - {1}'.format(self.direccion, self.__str_relate__())

    def __str_relate__(self):
        if self.parroquia_id is not None:
            return '{0}'.format(self.parroquia)
        elif self.municipio_id is not None:
            return '{0}'.format(self.municipio)
        elif self.estado_id is not None:
            return '{0}'.format(self.estado)
        else:
            return ''

    def get_object(self):
        for key in ['agencias', 'distribuidores', 'bancas', 'bloques', 'operadoras']:
            try:
                obj = getattr(self, key)
                return obj
            except Exception:
                pass
        return None

    def get_ref_related_historic(self):
        """
        Retorna una relacion de referencia, hacia el modelo donde se crea,
        pertenece la instancia actual
        """
        obj = self.get_object()
        if obj:
            return '{0}.{1}.{2}'.format(
                obj.__module__.split('.')[0],
                obj.__class__.__name__.lower(),
                obj.pk
            )
        else:
            return ''

# =============================================================
# =============================================================
# ====================Modelos auditados========================


auditoria.register(
    Direcciones
)
# =============================================================
# =============================================================
# =============================================================
