# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.utils.timezone import utc
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0004_auto_20150123_2034'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='clientfiles',
            options={'verbose_name': 'Archivo de cliente', 'verbose_name_plural': 'Archivos de cliente'},
        ),
        migrations.AlterModelOptions(
            name='clientipaddress',
            options={'verbose_name': 'Dirección IP', 'verbose_name_plural': 'Direcciones IP'},
        ),
        migrations.AlterModelOptions(
            name='clientstatus',
            options={'verbose_name': 'Estado de cliente', 'verbose_name_plural': 'Estados de cliente'},
        ),
        migrations.AlterModelOptions(
            name='clientversion',
            options={'verbose_name': 'Versión de cliente', 'verbose_name_plural': 'Versiones de cliente'},
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 701127, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 701152, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 699665, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 699692, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 699005, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 699037, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 700275, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 22, 34, 30, 700303, tzinfo=utc)),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clientfiles',
            unique_together=set([('name', 'client_version')]),
        ),
    ]
