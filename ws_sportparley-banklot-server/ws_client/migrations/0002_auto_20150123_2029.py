# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 816197, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 816223, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 814745, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 814770, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 814161, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 814191, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 815370, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 20, 29, 55, 815395, tzinfo=utc)),
            preserve_default=True,
        ),
    ]
