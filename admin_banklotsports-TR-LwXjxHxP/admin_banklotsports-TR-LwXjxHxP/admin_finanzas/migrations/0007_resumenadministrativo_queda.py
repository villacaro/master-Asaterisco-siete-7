# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0006_auto_20150305_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='resumenadministrativo',
            name='queda',
            field=models.DecimalField(default=0, null=True, decimal_places=8, max_digits=15),
            preserve_default=True,
        ),
    ]
