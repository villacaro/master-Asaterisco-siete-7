# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0020_auto_20150123_0253'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='factor_riesgo',
            field=models.IntegerField(help_text='Seleccione una opcion de factor de riesgo', default=0, verbose_name='Factor de riesgo (*)', choices=[[0, 'Activado'], [1, 'Desactivado']]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='factor_riesgo',
            field=models.IntegerField(help_text='Seleccione una opcion de factor de riesgo', default=0, verbose_name='Factor de riesgo (*)', choices=[[0, 'Activado'], [1, 'Desactivado']]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='factor_riesgo',
            field=models.IntegerField(help_text='Seleccione una opcion de factor de riesgo', default=0, verbose_name='Factor de riesgo (*)', choices=[[0, 'Activado'], [1, 'Desactivado']]),
            preserve_default=True,
        ),
    ]
