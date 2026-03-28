# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0009_auto_20150122_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='comercializacion',
            field=models.ForeignKey(to='admin_datamart.DimensionArcoComercializacion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='comercializacion',
            field=models.ForeignKey(to='admin_datamart.DimensionArcoComercializacion'),
            preserve_default=True,
        ), 
        migrations.AddField(
            model_name='dimensionarcocomercializacion',
            name='operadora_id',
            field=models.IntegerField( blank=True, null=True ),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='dimensioncomercializacion',
            name='operadora_id',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
