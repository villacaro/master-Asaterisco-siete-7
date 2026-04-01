# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0020_auto_20150511_1318'),
    ]

    operations = [
        migrations.AddField(
            model_name='hecho5_comisionescadena',
            name='alquiler',
            field=models.DecimalField(null=True, default=0, decimal_places=8, max_digits=15),
            preserve_default=True,
        ),
    ]
