# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0014_auto_20150126_1726'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hecho5_comisionescadena',
            options={'verbose_name': 'Hecho 5: Comisiones por cadena', 'verbose_name_plural': 'Hecho 5: Comisiones por toda la cadena'},
        ),
        migrations.AlterModelOptions(
            name='hecho6_comisionescadenajuego',
            options={'verbose_name': 'Hecho 6: Comisiones por cadena y juegos', 'verbose_name_plural': 'Hecho 6: Comisiones por toda la cadena y juegos'},
        ),
    ]
