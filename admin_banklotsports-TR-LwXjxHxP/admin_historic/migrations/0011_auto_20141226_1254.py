# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0010_auto_20141226_1154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessionsdetail',
            name='ref',
            field=models.CharField(null=True, max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
