# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0029_jugador_equipos'),
    ]

    operations = [
        migrations.AddField(
            model_name='jornadas',
            name='count_encuentros',
            field=models.IntegerField(help_text='Ingrese la cantidad de encuentros a realizar en la jornada, este campo solo sera util, para las jornadas de quiniela.', verbose_name='Cantidad de encuentros', default=0),
            preserve_default=True,
        ),
    ]
