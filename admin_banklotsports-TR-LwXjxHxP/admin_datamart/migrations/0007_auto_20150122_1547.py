# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0006_auto_20150122_1546'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dimensioncomercializacionporcentajes',
            old_name='agencia',
            new_name='agencia_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacionporcentajes',
            old_name='banca',
            new_name='banca_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacionporcentajes',
            old_name='bloque',
            new_name='bloque_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacionporcentajes',
            old_name='distribuidor',
            new_name='distribuidor_id',
        ),
        migrations.RenameField(
            model_name='dimensioncomercializacionporcentajes',
            old_name='taquilla',
            new_name='taquilla_id',
        ),
    ]
