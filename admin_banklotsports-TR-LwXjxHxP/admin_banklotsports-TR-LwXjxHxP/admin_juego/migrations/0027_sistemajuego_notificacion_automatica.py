# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0026_remove_sistemajuego_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemajuego',
            name='notificacion_automatica',
            field=models.BooleanField(choices=[(True, 'Automática'), (False, 'Manual')], default=False, verbose_name='Tipo de actualización (*)', help_text='Seleccione el tipo de actualización que desea'),
            preserve_default=True,
        ),
    ]
