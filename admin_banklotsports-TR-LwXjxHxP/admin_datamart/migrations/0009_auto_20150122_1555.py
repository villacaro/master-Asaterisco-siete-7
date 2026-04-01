# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0008_auto_20150122_1552'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='DimensionComercializacionPorcentajes',
            new_name='DimensionArcoComercializacion',
        ),
    ]
