# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0002_auto_20150123_2029'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 321312, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 321340, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 319362, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 319388, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 318754, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 318785, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 320256, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 31, 38, 320283, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
