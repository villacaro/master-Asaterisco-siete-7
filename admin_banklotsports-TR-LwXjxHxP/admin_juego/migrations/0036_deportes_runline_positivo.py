# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0035_sistemajuego_banner'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportes',
            name='runline_positivo',
            field=models.BooleanField(verbose_name='¿Desea poder cargar logros con runline y referencia positiva para este  deporte? ', help_text='Seleccione este campo solo si esta seguro de permitir editar el runline sin restriccion de positivos', default=False),
            preserve_default=True,
        ),
    ]
