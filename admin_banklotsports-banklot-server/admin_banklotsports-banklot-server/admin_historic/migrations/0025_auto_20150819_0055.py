# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0024_hechoconnectionscomer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionsdetail',
            name='ref',
            field=models.CharField(max_length=200, db_index=True, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sessionsdetail',
            name='ref_related',
            field=models.CharField(max_length=200, db_index=True, blank=True, null=True),
            preserve_default=True,
        ),
    ]
