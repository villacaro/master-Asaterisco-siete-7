# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0003_auto_20150122_1313'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='condicion',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='deporte',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='encuentro',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='encuentros_modalidad',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='jornada',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='modalidad',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='temporada',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dimensionjuegos',
            name='torneo',
            field=models.IntegerField(),
            preserve_default=True,
        ),
    ]
