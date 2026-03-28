# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0008_auto_20150123_2237'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now=True),
            preserve_default=True,
        ),
    ]
