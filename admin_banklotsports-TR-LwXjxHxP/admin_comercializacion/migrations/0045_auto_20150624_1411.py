# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0044_auto_20150622_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='bancas',
            name='is_resultados',
            field=models.BooleanField(verbose_name='¿Administra sus propios resultados? ', help_text='Seleccione este campo solo si desea que la comercializadora administe su propios resultados', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bloques',
            name='is_resultados',
            field=models.BooleanField(verbose_name='¿Administra sus propios resultados? ', help_text='Seleccione este campo solo si desea que la comercializadora administe su propios resultados', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='is_sistema_juego',
            field=models.BooleanField(verbose_name='¿Administra sus propios logros? ', help_text='Seleccione este campo solo si desea que la comercializadora tenga su propio sistema de juego', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='permissions_create_user',
            field=models.BooleanField(verbose_name='¿Tiene permisos de crear usuarios de su mismo nivel? ', help_text='Seleccione este campo solo si desea que la comercializadora pueda crear mas usuarios de su mismo nivel', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='is_sistema_juego',
            field=models.BooleanField(verbose_name='¿Administra sus propios logros? ', help_text='Seleccione este campo solo si desea que la comercializadora tenga su propio sistema de juego', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='permissions_create_user',
            field=models.BooleanField(verbose_name='¿Tiene permisos de crear usuarios de su mismo nivel? ', help_text='Seleccione este campo solo si desea que la comercializadora pueda crear mas usuarios de su mismo nivel', default=False),
            preserve_default=True,
        ),
    ]
