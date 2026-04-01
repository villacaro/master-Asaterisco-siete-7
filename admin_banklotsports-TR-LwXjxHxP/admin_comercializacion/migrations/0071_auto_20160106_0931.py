# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0070_auto_20151204_1937'),
    ]

    operations = [
        migrations.AddField(
            model_name='cupos',
            name='monto_premio',
            field=models.DecimalField(verbose_name='Monto diario de premio (*)', blank=True, help_text='Ingrese el monto diario de premio ', null=True, decimal_places=2, max_digits=15),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='preferences',
            name='value',
            field=models.CharField(blank=True, max_length=100, verbose_name='Valor', null=True),
            preserve_default=True,
        ),
    ]
