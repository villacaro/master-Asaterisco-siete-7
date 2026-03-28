# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0013_auto_20150125_1938'),
        ('admin_comercializacion', '0017_auto_20150122_1953'),
    ]

    operations = [
    	migrations.AddField(
            model_name='tipopreferencias',
            name='orden',
            field=models.IntegerField(help_text='Ingrese el orden del tipo de preferencia', default=1, verbose_name='Orden (*)'),
            preserve_default=True,
        ),
    ]
