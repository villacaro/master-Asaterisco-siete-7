# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0004_auto_20150122_1523'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='condicion',
            new_name='condicion_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='deporte',
            new_name='deporte_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='encuentro',
            new_name='encuentro_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='encuentros_modalidad',
            new_name='encuentros_modalidad_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='jornada',
            new_name='jornada_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='modalidad',
            new_name='modalidad_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='pertenece',
            new_name='pertenece_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='temporada',
            new_name='temporada_id',
        ),
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='torneo',
            new_name='torneo_id',
        ),
    ]
