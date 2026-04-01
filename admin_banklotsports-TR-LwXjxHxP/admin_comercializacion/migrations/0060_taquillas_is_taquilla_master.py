# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0059_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='taquillas',
            name='is_taquilla_master',
            field=models.BooleanField(default=True, verbose_name='Taquilla master ', help_text='Si este campo esta activo, se crea la taquilla con todos los permisos'),
            preserve_default=True,
        ),
    ]
