# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0010_auto_20150812_1250'),
    ]

    operations = [
        migrations.AlterField(
            model_name='configuracion',
            name='max',
            field=models.DecimalField(max_digits=15, default=0, decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='configuracion',
            name='min',
            field=models.DecimalField(max_digits=15, default=0, decimal_places=2),
            preserve_default=True,
        ),
    ]
