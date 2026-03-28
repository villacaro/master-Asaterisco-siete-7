# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0002_auto_20150122_1312'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dimensioncomercializacion',
            old_name='agencia',
            new_name='agencia_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacion',
            old_name='banca',
            new_name='banca_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacion',
            old_name='bloque',
            new_name='bloque_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacion',
            old_name='distribuidor',
            new_name='distribuidor_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacion',
            old_name='taquilla',
            new_name='taquilla_id',
        ),
    ]
