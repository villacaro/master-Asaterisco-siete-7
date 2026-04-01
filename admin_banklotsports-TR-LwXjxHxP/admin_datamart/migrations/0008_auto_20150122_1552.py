# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0007_auto_20150122_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='comercializacion',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='comercializacion',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
