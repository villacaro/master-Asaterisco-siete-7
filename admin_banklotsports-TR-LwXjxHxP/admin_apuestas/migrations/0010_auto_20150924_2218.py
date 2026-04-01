# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0009_auto_20150821_1742'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='pks_jugadas',
            field=models.CharField(db_index=True, max_length=300, default=''),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='key',
            field=models.CharField(blank=True, null=True, max_length=140),
            preserve_default=True,
        ),
    ]
