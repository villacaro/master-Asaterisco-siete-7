# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0006_auto_20150123_2236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 43, 882679, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 36, 43, 882703, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 43, 881230, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 36, 43, 881259, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 43, 880394, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 36, 43, 880435, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime(2015, 1, 23, 22, 36, 43, 881976, tzinfo=utc), auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 36, 43, 882002, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clientfiles',
            unique_together=set([]),
        ),
    ]
