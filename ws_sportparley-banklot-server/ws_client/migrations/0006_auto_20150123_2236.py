# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0005_auto_20150123_2234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 276286, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 276340, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 273328, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 273382, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 272183, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 272222, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 274633, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 4, 274686, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
