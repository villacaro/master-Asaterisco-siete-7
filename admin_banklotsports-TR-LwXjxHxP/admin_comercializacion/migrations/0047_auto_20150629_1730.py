# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0046_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='bancas',
            name='is_logros',
            field=models.BooleanField(default=False, help_text='Seleccione este campo solo si desea que la comercializadora administe sus propios logros', verbose_name='¿Administra sus propios logros? '),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bloques',
            name='is_logros',
            field=models.BooleanField(default=False, help_text='Seleccione este campo solo si desea que la comercializadora administe sus propios logros', verbose_name='¿Administra sus propios logros? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='is_sistema_juego',
            field=models.BooleanField(default=False, help_text='Seleccione este campo solo si desea que la comercializadora tenga su propio sistema de juego', verbose_name='¿Administra su propio sistema de juego? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='is_sistema_juego',
            field=models.BooleanField(default=False, help_text='Seleccione este campo solo si desea que la comercializadora tenga su propio sistema de juego', verbose_name='¿Administra su propio sistema de juego? '),
            preserve_default=True,
        ),
    ]
