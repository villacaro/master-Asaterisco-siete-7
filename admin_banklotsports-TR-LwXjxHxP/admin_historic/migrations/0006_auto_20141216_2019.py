# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0005_auto_20141216_2008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='cookie',
            field=models.CharField(null=True, blank=True, max_length=1000),
            preserve_default=True,
        ),
    ]
