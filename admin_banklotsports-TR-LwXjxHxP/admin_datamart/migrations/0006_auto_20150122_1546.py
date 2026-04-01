# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0005_auto_20150122_1525'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dimensionarcocomercializacion',
            name='agencia',
        ),
        migrations.RemoveField(
            model_name='dimensionarcocomercializacion',
            name='banca',
        ),
        migrations.RemoveField(
            model_name='dimensionarcocomercializacion',
            name='bloque',
        ),
        migrations.RemoveField(
            model_name='dimensionarcocomercializacion',
            name='distribuidor',
        ),
        migrations.RemoveField(
            model_name='dimensionarcocomercializacion',
            name='operadora',
        ),
        migrations.RemoveField(
            model_name='dimensionarcocomercializacion',
            name='user',
        ),
        migrations.RemoveField(
            model_name='hecho3_pagoscadena',
            name='comercializacion',
        ),
        migrations.RemoveField(
            model_name='hecho3_pagoscadena',
            name='tiempo',
        ),
        migrations.DeleteModel(
            name='Hecho3_PagosCadena',
        ),
        migrations.RemoveField(
            model_name='hecho4_depositoscadena',
            name='comercializacion',
        ),
        migrations.DeleteModel(
            name='DimensionArcoComercializacion',
        ),
        migrations.RemoveField(
            model_name='hecho4_depositoscadena',
            name='tiempo',
        ),
        migrations.DeleteModel(
            name='Hecho4_DepositosCadena',
        ),
        migrations.AlterModelOptions(
            name='dimensioncomercializacion',
            options={'verbose_name': 'Dimension de comercializacion', 'verbose_name_plural': 'Dimension de comercializaciones'},
        ),
        migrations.AlterModelOptions(
            name='dimensioncomercializacionporcentajes',
            options={'verbose_name': 'Dimension de arco comercializacion', 'verbose_name_plural': 'Dimension de arco comercializaciones'},
        ),
        migrations.AlterModelOptions(
            name='dimensionjuegos',
            options={'verbose_name': 'Dimension de juego', 'verbose_name_plural': 'Dimension de juegos'},
        ),
        migrations.AlterModelOptions(
            name='dimensiontiempo',
            options={'verbose_name': 'Dimension de tiempo', 'verbose_name_plural': 'Dimension de tiempos'},
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacionporcentajes',
            name='agencia',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacionporcentajes',
            name='banca',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacionporcentajes',
            name='bloque',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacionporcentajes',
            name='distribuidor',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacionporcentajes',
            name='taquilla',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
