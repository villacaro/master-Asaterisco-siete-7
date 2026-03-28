# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0012_auto_20141229_0918'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessionsdetail',
            name='ref_related',
            field=models.CharField(null=True, blank=True, max_length=50),
            preserve_default=True,
        ),
    ]
