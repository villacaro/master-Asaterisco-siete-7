# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0040_auto_20150429_2023'),
    ]

    operations = [
        migrations.AlterField(
            model_name='porcentajes',
            name='agencia_porc',
            field=models.DecimalField(blank=True, null=True, max_digits=15, default=None, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='banca_porc',
            field=models.DecimalField(blank=True, null=True, max_digits=15, default=None, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='bloque_porc',
            field=models.DecimalField(blank=True, null=True, max_digits=15, default=None, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='distribuidor_porc',
            field=models.DecimalField(blank=True, null=True, max_digits=15, default=None, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='porcentaje_ganancia',
            field=models.DecimalField(max_digits=15, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='porcentaje_maximo',
            field=models.DecimalField(max_digits=15, decimal_places=4),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='taquilla_porc',
            field=models.DecimalField(blank=True, null=True, max_digits=15, default=None, decimal_places=4),
            preserve_default=True,
        ),
    ]
