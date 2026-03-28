# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0002_auto_20150108_0942'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anotaciones',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='anotaciones',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='anotacionesdetail',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='anotacionesdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resultados',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resultados',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
