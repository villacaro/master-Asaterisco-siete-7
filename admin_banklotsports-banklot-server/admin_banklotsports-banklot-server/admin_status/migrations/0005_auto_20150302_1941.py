# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0004_auto_20150126_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='status',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='status',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='statusdetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='statusdetail',
            name='startdate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='statusdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='taquillastatusdetail',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='taquillastatusdetail',
            name='startdate',
            field=models.DateField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='taquillastatusdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
