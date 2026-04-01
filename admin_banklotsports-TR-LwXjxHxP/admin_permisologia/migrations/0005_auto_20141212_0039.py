# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0004_auto_20141211_1616'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='codename',
            field=models.CharField(unique=True, verbose_name='Codigo', max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='content_type',
            field=models.IntegerField(verbose_name='Nivel', choices=[(1, 'Titulo princial.'), (2, 'Subtitulo.'), (3, 'Enlace.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(null=True, blank=True, verbose_name='Icono', max_length=50),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_public',
            field=models.BooleanField(default=False, verbose_name='Público'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_view',
            field=models.BooleanField(default=True, verbose_name='Visible'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='menu_suc',
            field=models.ForeignKey(verbose_name='Origen', to='admin_permisologia.Menu', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(verbose_name='Titulo', max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='orden',
            field=models.IntegerField(verbose_name='Orden'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.CharField(null=True, blank=True, verbose_name='Url', max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='content_type',
            field=models.IntegerField(verbose_name='Nivel', choices=[(0, 'django.contrib.auth'), (1, 'django.contrib.contenttypes'), (2, 'django.contrib.sessions'), (3, 'django.contrib.sites'), (4, 'django.contrib.messages'), (5, 'django.contrib.staticfiles'), (6, 'django.contrib.admin'), (7, 'django.contrib.humanize'), (8, 'djcelery'), (9, 'gunicorn'), (10, 'crequest'), (11, 'django_extensions'), (12, 'admin_apuestas'), (13, 'admin_comercializacion'), (14, 'admin_finanzas'), (15, 'admin_historic'), (16, 'admin_juego'), (17, 'admin_logros'), (18, 'admin_permisologia'), (19, 'admin_principal'), (20, 'admin_profiles'), (21, 'admin_status'), (22, 'admin_users'), (23, 'admin_soporte'), (24, 'admin_datamart'), (25, 'admin_resultados'), (26, 'scripts')]),
            preserve_default=True,
        ),
    ]
