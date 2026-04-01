# -*- coding: utf-8 -*-
from admin_banklotsports.settings import THEME_DEFAULT
from django.core.cache import cache
from django.db import models


# Create your models here.
class Company(models.Model):
    """
    Table admin_themes_company
    Attributes
        * name: Nombre de la empresa.
        * logo: Logo de la empresa.
    """
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre de la empresa (*)'
    )
    logo = models.ImageField(
        upload_to='company',
        blank=True,
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

    class Meta:
        db_tablespace = "ts_comer"
        verbose_name = ('Empresa')
        verbose_name_plural = ('Empresas')
        ordering = ["name", ]

    def __str__(self):
        return "{0}".format(self.name)

    def save(self, *args, **kwargs):
        super(Company, self).save(*args, **kwargs)
        self.cache_clear()

    def cache_clear(self):
        cache.delete(
            '{0}_{1}'.format('company', self.pk)
        )


class Theme(models.Model):
    """
    Table admin_themes_theme
    Attributes
        * name: Nombre del tema.
        * codename: Codename del tema.
        + description: Descripción del tema.
        + screenshoot: Captura de referencia del tema.
        * template_dir: Dirección de las plantillas (En caso de tener plantillas
            distintas a las generales).
        * static_url: URL de los archivos estáticos.
        * media_url: URL de la carpeta de media.
    """
    name = models.CharField(
        max_length=140,
        verbose_name='Nombre del tema (*)'
    )
    codename = models.CharField(
        max_length=140,
        verbose_name='Codename del tema (*)'
    )
    description = models.CharField(
        max_length=140,
        verbose_name='Descripción del tema (*)'
    )
    screenshoot = models.ImageField(
        upload_to='themes',
        blank=True,
        null=True
    )
    template_dir = models.CharField(
        max_length=140,
        verbose_name='Dirección de template'
    )
    static_url = models.CharField(
        max_length=140,
        verbose_name='URL de los archivos estáticos'
    )
    media_url = models.CharField(
        max_length=140,
        verbose_name='URL de la carpeta de media'
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
        verbose_name = ('Tema')
        verbose_name_plural = ('Temas')
        ordering = ["name", ]

    def __str__(self):
        return "{0}".format(self.name)

    def get_app_label(self):
        return self._meta.app_label

    def is_default(self):
        # Tema por defecto
        if(self.codename == THEME_DEFAULT):
            return True
        return False

    def save(self, *args, **kwargs):
        super(Theme, self).save(*args, **kwargs)
        self.cache_clear()

    def cache_clear(self):
        cache.delete(
            '{0}_{1}'.format('theme', self.pk)
        )


class Color(models.Model):
    """
    Table admin_themes_color
    Attributes
        * theme: Objeto de Theme.
        * color: Código hexadecimal de color.
        * color_type: Tipo de color.
    """
    theme = models.ForeignKey(
        'Theme',
        verbose_name='Tema (*)'
    )
    color = models.CharField(
        max_length=140,
        verbose_name='Color (*)'
    )
    COLOR_TYPE_CHOICES = (
        (0, 'Primary'),
        (1, 'Secondary'),
        (2, 'Default'),
    )
    color_type = models.IntegerField(
        verbose_name='Tipo de color (*)',
        choices=COLOR_TYPE_CHOICES
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
        verbose_name = ('Color')
        verbose_name_plural = ('Colores')
        unique_together = [('theme', 'color_type'), ('theme', 'color')]

    def __str__(self):
        return "{0} - {1}".format(self.theme.name, self.color_type)

    def get_app_label(self):
        return self._meta.app_label
