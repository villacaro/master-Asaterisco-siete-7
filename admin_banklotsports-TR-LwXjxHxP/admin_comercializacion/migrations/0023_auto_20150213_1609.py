# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0022_auto_20150126_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='factor_riesgo',
            field=models.IntegerField(help_text='Seleccione una opcion de factor de riesgo', verbose_name='Factor de riesgo (*)', choices=[[1, 'Activado'], [0, 'Desactivado']], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='factor_riesgo',
            field=models.IntegerField(help_text='Seleccione una opcion de factor de riesgo', verbose_name='Factor de riesgo (*)', choices=[[1, 'Activado'], [0, 'Desactivado']], default=1),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='factor_riesgo',
            field=models.IntegerField(help_text='Seleccione una opcion de factor de riesgo', verbose_name='Factor de riesgo (*)', choices=[[1, 'Activado'], [0, 'Desactivado']], default=1),
            preserve_default=True,
        ),
    ]
