# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0021_hecho5_comisionescadena_alquiler'),
    ]

    operations = [
        migrations.AddField(
            model_name='hecho7_comisionesquedacadena',
            name='queda_taquilla',
            field=models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8),
            preserve_default=True,
        ),
    ]
