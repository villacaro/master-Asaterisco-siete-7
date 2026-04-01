# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0008_auto_20150429_1326'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='codename',
            field=models.CharField(unique=True, max_length=160, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='status',
            name='content_type',
            field=models.IntegerField(db_index=True, choices=[[0, 'Status de actualizacion'], [1, 'Status de usuarios'], [2, 'Status de encuentros'], [3, 'Status de taquillas'], [4, 'Status de jugadas'], [5, 'Status de encuentro resultado'], [6, 'Status de venta de tickets'], [7, 'Status de ??????'], [8, 'Status de tickets']]),
            preserve_default=True,
        ),
    ]
