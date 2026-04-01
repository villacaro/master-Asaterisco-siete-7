# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0015_auto_20150113_1744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='id',
            field=models.CharField(primary_key=True, max_length=36, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sessionsdetail',
            name='id',
            field=models.CharField(primary_key=True, max_length=36, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillasessions',
            name='id',
            field=models.CharField(primary_key=True, max_length=36, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillasessionsdetail',
            name='id',
            field=models.CharField(primary_key=True, max_length=36, serialize=False),
            preserve_default=True,
        ),
    ]
