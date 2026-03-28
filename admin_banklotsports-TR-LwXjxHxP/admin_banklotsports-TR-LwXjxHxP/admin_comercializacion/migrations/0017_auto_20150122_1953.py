# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0016_auto_20150122_1920'),
    ]

    operations = [
        migrations.RenameField(
            model_name='agencias',
            old_name='direccion_id',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='agencias',
            old_name='status_id',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='bancas',
            old_name='direccion_id',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='bancas',
            old_name='status_id',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='bloques',
            old_name='direccion_id',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='bloques',
            old_name='status_id',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='distribuidores',
            old_name='direccion_id',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='distribuidores',
            old_name='status_id',
            new_name='status',
        ),
        migrations.RenameField(
            model_name='operadoras',
            old_name='direccion_id',
            new_name='direccion',
        ),
        migrations.RenameField(
            model_name='operadoras',
            old_name='status_id',
            new_name='status',
        ),
    ]
