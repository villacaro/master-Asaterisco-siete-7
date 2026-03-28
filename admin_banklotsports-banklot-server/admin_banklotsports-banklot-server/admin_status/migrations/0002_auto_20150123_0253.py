# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='statusdetail',
            name='startdate',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 810091)),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillastatusdetail',
            name='startdate',
            field=models.DateField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 811746)),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='status',
            name='order',
            field=models.IntegerField(default=0, help_text='Ingrese la numeración de orden', verbose_name='Orden (*)'),
            preserve_default=True,
        ),
    ]
