# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0004_auto_20141216_2004'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionsdetail',
            name='id',
        ), 
        migrations.RemoveField(
            model_name='sessionsdetaildetail',
            name='id',
        ), 
        migrations.AddField(
            model_name='sessionsdetail',
            name='id',
            field=models.CharField(max_length=48, serialize=False, primary_key=True, default=None),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='sessionsdetaildetail',
            name='id',
            field=models.CharField(max_length=48, serialize=False, primary_key=True, default=None),
            preserve_default=True,
        ),
    ]
