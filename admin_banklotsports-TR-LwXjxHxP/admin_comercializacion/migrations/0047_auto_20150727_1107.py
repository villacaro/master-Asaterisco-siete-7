# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0046_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencias',
            name='resumen_automatic',
            field=models.BooleanField(default=False, verbose_name='Cierre administrativo Automático', help_text='Seleccione este campo solo si desea que el resumen administrativo se gestione de forma automática, importacion de saldos y cierre de dias.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bancas',
            name='resumen_automatic',
            field=models.BooleanField(default=False, verbose_name='Cierre administrativo Automático', help_text='Seleccione este campo solo si desea que el resumen administrativo se gestione de forma automática, importacion de saldos y cierre de dias.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bloques',
            name='resumen_automatic',
            field=models.BooleanField(default=False, verbose_name='Cierre administrativo Automático', help_text='Seleccione este campo solo si desea que el resumen administrativo se gestione de forma automática, importacion de saldos y cierre de dias.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distribuidores',
            name='resumen_automatic',
            field=models.BooleanField(default=False, verbose_name='Cierre administrativo Automático', help_text='Seleccione este campo solo si desea que el resumen administrativo se gestione de forma automática, importacion de saldos y cierre de dias.'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operadoras',
            name='resumen_automatic',
            field=models.BooleanField(default=False, verbose_name='Cierre administrativo Automático', help_text='Seleccione este campo solo si desea que el resumen administrativo se gestione de forma automática, importacion de saldos y cierre de dias.'),
            preserve_default=True,
        ),
    ]
