# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0011_auto_20150125_0145'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sistemajuegotiporegla',
            options={'verbose_name_plural': 'Reglas por sistema de juegos', 'verbose_name': 'Regla por sistema de juego', 'ordering': ['tiporegla']},
        ),
        migrations.RemoveField(
            model_name='sistemajuego',
            name='reglas',
        ),
    ]
