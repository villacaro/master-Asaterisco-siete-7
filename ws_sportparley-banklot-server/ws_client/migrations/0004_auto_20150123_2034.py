# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0003_auto_20150123_2031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 838954, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 838987, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 836893, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 836923, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 836095, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 836217, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 837626, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 20, 34, 59, 837666, tzinfo=utc), auto_now=True),
            preserve_default=True,
        ),
    ]
