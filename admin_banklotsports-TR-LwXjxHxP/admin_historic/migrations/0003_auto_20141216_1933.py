# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0002_auto_20141216_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessions',
            name='id',
        ), 
        migrations.AddField(
            model_name='sessions',
            name='id',
            field=models.CharField(primary_key=True, serialize=False, default=None, max_length=48),
            preserve_default=True,
        ),
    ]
