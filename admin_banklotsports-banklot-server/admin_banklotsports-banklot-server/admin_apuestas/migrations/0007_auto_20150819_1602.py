# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0006_auto_20150601_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tickets',
            name='fecha',
            field=models.DateTimeField(db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketstype',
            name='codename',
            field=models.CharField(max_length=160, db_index=True, unique=True),
            preserve_default=True,
        ),
    ]
