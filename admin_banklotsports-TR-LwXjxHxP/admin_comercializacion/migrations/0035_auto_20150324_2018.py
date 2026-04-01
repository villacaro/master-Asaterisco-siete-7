# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0034_auto_20150312_2006'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancas',
            name='is_sistema_juego',
            field=models.BooleanField(verbose_name='¿Administra sus propios logros? ', help_text='Seleccione este campo solo si desea que la banca tenga su propio sistema de juego', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='is_sistema_juego',
            field=models.BooleanField(verbose_name='¿Administra sus propios logros? ', help_text='Seleccione este campo solo si desea que la banca tenga su propio sistema de juego', default=False),
            preserve_default=True,
        ),
    ]
