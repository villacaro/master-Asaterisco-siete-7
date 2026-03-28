# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0045_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentros',
            name='updated_at_logros',
            field=models.DateTimeField(default=datetime.datetime(2015, 9, 22, 15, 44, 47, 18412), auto_now_add=True),
            preserve_default=False,
        ),
    ]
