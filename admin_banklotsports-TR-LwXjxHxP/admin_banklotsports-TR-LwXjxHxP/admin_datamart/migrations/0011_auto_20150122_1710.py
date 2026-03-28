# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0010_auto_20150122_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hecho1_ventascadenasjuegos',
            options={'verbose_name': 'Hecho 1: Ventas por cadena y juego', 'verbose_name_plural': 'Hecho 1: ventas por toda la cadena y juegos'},
        ),
        migrations.AlterModelOptions(
            name='hecho2_ventascadenas',
            options={'verbose_name': 'Hecho 2: Ventas por cadena', 'verbose_name_plural': 'Hecho 2: ventas por toda la cadena'},
        ),
        migrations.AlterModelOptions(
            name='hecho5_comisionescadena',
            options={'verbose_name': 'Hecho 5: Comisiones de ventas por cadena', 'verbose_name_plural': 'Hecho 5: Comisiones de ventas por toda la cadena'},
        ),
        migrations.AlterModelOptions(
            name='hecho6_comisionescadenajuego',
            options={'verbose_name': 'Hecho 6: Comisiones de ventas por cadena y juegos', 'verbose_name_plural': 'Hecho 6: Comisiones de ventas por toda la cadena y juegos'},
        ),
    ]
