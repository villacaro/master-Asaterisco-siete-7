# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0008_auto_20150819_1642'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticketsdetail',
            name='monto',
            field=models.DecimalField(max_digits=30, decimal_places=16),
            preserve_default=True,
        ),
    ]
