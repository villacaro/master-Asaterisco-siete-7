# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0041_auto_20150505_1548'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenciadatadefault',
            name='parley_empates_max',
            field=models.IntegerField(default=5, verbose_name='Parley: Cantidad máxima de apuesta a empate por ticket', help_text='Parley: Indique la cantidad máxima permitida de apuestas a empate en un ticket'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agencias',
            name='parley_empates_max',
            field=models.IntegerField(default=5, verbose_name='Parley: Cantidad máxima de apuesta a empate por ticket', help_text='Parley: Indique la cantidad máxima permitida de apuestas a empate en un ticket'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_hembras_min',
            field=models.IntegerField(verbose_name='Parley: cantidad minima de hembras (*)', help_text='Ingrese la cantidad minima de hembras por ticket'),
            preserve_default=True,
        ),
    ]
