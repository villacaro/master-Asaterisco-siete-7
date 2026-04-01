# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0027_sistemajuego_notificacion_automatica'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportes',
            name='count_apuesta',
            field=models.IntegerField(choices=[(1, '1 apuesta'), (2, '2 apuestas'), (3, '3 apuestas'), (4, '4 apuestas'), (5, '5 apuestas')], verbose_name='Número máximo de apuesta por encuentro (*)', default=5, help_text='Indique el número de logros que se deben apostar como máximo por cada encuentro'),
            preserve_default=True,
        ),
    ]
