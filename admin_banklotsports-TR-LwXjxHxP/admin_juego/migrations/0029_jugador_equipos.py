# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0028_deportes_count_apuesta'),
    ]

    operations = [
        migrations.AddField(
            model_name='jugador',
            name='equipos',
            field=models.ManyToManyField(to='admin_juego.Equipos', verbose_name='Seleccione los equipos (*)', help_text='Seleccione los equipos a los que desea asignar el jugador.', blank=True),
        ),
    ]
