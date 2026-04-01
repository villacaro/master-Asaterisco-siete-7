# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0005_auto_20150324_2018'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='puntaje_calculado',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketsdetail',
            name='puntaje_apostado',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketsdetail',
            name='puntaje_calculado',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdetail',
            name='logro_apostado',
            field=models.IntegerField(blank=True, null=True),
            preserve_default=True,
        ),
    ]
