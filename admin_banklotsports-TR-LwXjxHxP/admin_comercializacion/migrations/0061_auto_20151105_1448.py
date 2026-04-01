# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0060_auto_20151105_1212'),
    ]

    operations = [
        migrations.AddField(
            model_name='preferences',
            name='distribute',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='typepreferences',
            name='distribute',
            field=models.BooleanField(default=False, verbose_name='¿Distribuida? ', help_text='Seleccione de si una preferencia editable'),
            preserve_default=True,
        ),
    ]
