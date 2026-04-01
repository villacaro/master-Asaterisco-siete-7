# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0007_resumenadministrativo_queda'),
    ]

    operations = [
        migrations.AddField(
            model_name='movimiento',
            name='comprobante',
            field=models.ImageField(blank=True, upload_to='movimientos', null=True),
            preserve_default=True,
        ),
    ]
