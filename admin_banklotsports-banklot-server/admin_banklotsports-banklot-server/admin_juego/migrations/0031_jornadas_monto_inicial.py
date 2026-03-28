# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0030_jornadas_count_encuentros'),
    ]

    operations = [
        migrations.AddField(
            model_name='jornadas',
            name='monto_inicial',
            field=models.IntegerField(verbose_name='Monto inicial', default=0, help_text='Ingrese la cantidad de monto inicial, este campo solo sera util, para las jornadas de quiniela.'),
        ),
    ]
