# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0022_auto_20150306_1123'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gruposjuego',
            options={'verbose_name': 'Grupo de juego', 'verbose_name_plural': 'Grupos de juegos'},
        ),
    ]
