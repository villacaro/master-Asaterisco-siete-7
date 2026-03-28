# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0012_auto_20150501_1912'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='file_type',
            field=models.CharField(choices=[('client', 'Cliente'), ('updater', 'Actualizador'), ('lib', 'Librería'), ('docs', 'Documentación'), ('other', 'Otro')], verbose_name='Tipo', max_length=140),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientipaddress',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='codename',
            field=models.CharField(unique=True, default='client_status_', verbose_name='Codename', db_index=True, max_length=140),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientversion',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
            preserve_default=True,
        ),
    ]
