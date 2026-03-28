# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dimensioncomercializacion',
            options={'verbose_name_plural': 'Dimencios de comercializacion', 'verbose_name': 'Dimencion de comercializacion'},
        ),
        migrations.AlterModelOptions(
            name='dimensiontiempo',
            options={'verbose_name_plural': 'Dimencion de tiempos', 'verbose_name': 'Dimencion de tiempo'},
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacion',
            name='agencia',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacion',
            name='banca',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacion',
            name='bloque',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacion',
            name='distribuidor',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensioncomercializacion',
            name='taquilla',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
