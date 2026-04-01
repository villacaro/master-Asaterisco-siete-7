# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0031_consolidado'),
    ]

    operations = [
        migrations.AddField(
            model_name='consolidado',
            name='dfecha',
            field=models.DateField(default=datetime.datetime(2016, 2, 1, 11, 39, 56, 878745)),
            preserve_default=False,
        ),
    ]
