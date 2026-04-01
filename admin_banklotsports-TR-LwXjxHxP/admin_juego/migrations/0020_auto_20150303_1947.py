# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0019_auto_20150302_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sistemajuegotiporegla',
            name='sistemajuego',
        ),
        migrations.RemoveField(
            model_name='sistemajuegotiporegla',
            name='tiporegla',
        ),
        migrations.DeleteModel(
            name='SistemaJuegoTipoRegla',
        ),
        migrations.DeleteModel(
            name='TipoRegla',
        ),
    ]
