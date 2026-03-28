# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0001_initial'),
        ('admin_users', '0009_auto_20141212_0936'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='comercializadora',
            field=models.ManyToManyField(to='admin_finanzas.Comercializadora', blank=True),
            preserve_default=True,
        ),
    ]
