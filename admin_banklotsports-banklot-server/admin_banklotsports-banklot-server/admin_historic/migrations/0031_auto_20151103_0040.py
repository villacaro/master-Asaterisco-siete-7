# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0030_auto_20151019_1656'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taquillasessions',
            name='key',
            field=models.CharField(max_length=1000, default=''),
            preserve_default=True,
        ),
    ]
