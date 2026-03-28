# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0011_auto_20141226_1254'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='enddate',
            field=models.DateTimeField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
