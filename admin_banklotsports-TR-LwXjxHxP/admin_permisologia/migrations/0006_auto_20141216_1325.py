# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0005_auto_20141212_0039'),
    ]

    operations = [
        migrations.AddField(
            model_name='menu',
            name='is_global',
            field=models.BooleanField(help_text='Enlace privado, pero global', verbose_name='Global', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='codename',
            field=models.CharField(max_length=160, verbose_name='Codigo', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='content_type',
            field=models.IntegerField(verbose_name='App', choices=[(0, 'Admin apuestas'), (1, 'Admin comercializacion'), (2, 'Admin finanzas'), (3, 'Admin historic'), (4, 'Admin juego'), (5, 'Admin logros'), (6, 'Admin permisologia'), (7, 'Admin principal'), (8, 'Admin profiles'), (9, 'Admin status'), (10, 'Admin users'), (11, 'Admin soporte'), (12, 'Admin datamart'), (13, 'Admin resultados')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='menu',
            field=models.ManyToManyField(to='admin_permisologia.Menu', verbose_name='Vistas asociadas'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='name',
            field=models.CharField(max_length=160, verbose_name='Nombre'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='profiles',
            field=models.ManyToManyField(to='admin_users.UserProfile', verbose_name='Perfiles asociados'),
            preserve_default=True,
        ),
    ]
