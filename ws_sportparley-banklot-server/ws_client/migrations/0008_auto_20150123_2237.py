# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0007_auto_20150123_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 933907, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 933934, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 932351, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 932380, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 931600, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 931634, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 933160, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 37, 18, 933187, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clientfiles',
            unique_together=set([('name', 'client_version')]),
        ),
    ]
