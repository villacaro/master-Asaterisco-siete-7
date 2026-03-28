# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0024_deportes_orden_equipos'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deportes',
            options={'ordering': ['nombre'], 'verbose_name': 'Deporte', 'verbose_name_plural': 'Deportes'},
        ),
        migrations.AlterModelOptions(
            name='encuentros',
            options={'ordering': ['horajuego'], 'verbose_name': 'Encuentro', 'verbose_name_plural': 'Encuentros'},
        ),
        migrations.AlterModelOptions(
            name='jugador',
            options={'ordering': ['nombre', 'lateralidad'], 'verbose_name': 'Jugador', 'verbose_name_plural': 'Jugadores'},
        ),
    ]
