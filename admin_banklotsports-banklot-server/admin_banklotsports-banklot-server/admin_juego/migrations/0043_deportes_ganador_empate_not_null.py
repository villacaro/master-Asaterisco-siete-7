# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0042_auto_20150903_1456'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportes',
            name='ganador_empate_not_null',
            field=models.BooleanField(help_text='Seleccione este campo solo si esta seguro de que el  algotitmo de resultados no debe poner como anuladas las jugadas  relacionadas a ganador si hay un empate', verbose_name='¿Al procesar resultados, la modalidad ganador no se anula si detecta un empate? ', default=False),
            preserve_default=True,
        ),
    ]
