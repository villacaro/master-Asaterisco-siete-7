# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0014_auto_20150111_0228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sessions',
            options={'verbose_name': 'Session de usuario', 'ordering': ['-enddate'], 'verbose_name_plural': 'Sessiones por usuario'},
        ),
        migrations.AlterModelOptions(
            name='sessionsdetail',
            options={'verbose_name': 'Detalle de una session', 'ordering': ['-created_at'], 'verbose_name_plural': 'Detalle de las sessiones por usuario'},
        ),
        migrations.AlterModelOptions(
            name='taquillasessions',
            options={'verbose_name': 'Session por taquilla', 'ordering': ['-enddate'], 'verbose_name_plural': 'Sessiones por taquillas'},
        ),
        migrations.AlterModelOptions(
            name='taquillasessionsdetail',
            options={'verbose_name': 'Detalle de la session por taquilla', 'ordering': ['-created_at'], 'verbose_name_plural': 'Detalle de las sessiones por taquillas'},
        ),
        migrations.AlterModelOptions(
            name='usersprocesses',
            options={'verbose_name': 'Tipo de proceso', 'ordering': ['content_type'], 'verbose_name_plural': 'Tipos de procesos'},
        ),
        migrations.AlterField(
            model_name='sessionsdetail',
            name='ref_related',
            field=models.CharField(null=True, blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
