# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0053_auto_20151201_1507'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sistemajuego',
            name='is_logros',
            field=models.BooleanField(default=False, verbose_name='¿Permite cargar logros?', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuego',
            name='is_resultados',
            field=models.BooleanField(default=False, verbose_name='¿Permite cargar resultados?', editable=False),
            preserve_default=True,
        ),
    ]
