# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0043_deportes_ganador_empate_not_null'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentros',
            name='horacierre',
            field=models.DateTimeField(help_text='Seleccione la fecha y hora de cierre del encuentro', verbose_name='Fecha y hora de cierre (*)', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentros',
            name='horajuego',
            field=models.DateTimeField(help_text='Seleccione la fecha y hora de inicio del encuentro', verbose_name='Fecha y hora de inicio (*)', db_index=True),
            preserve_default=True,
        ),
    ]
