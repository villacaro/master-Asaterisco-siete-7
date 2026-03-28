# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0032_auto_20150528_0745'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gruposjuego',
            options={'verbose_name_plural': 'Grupos de juegos', 'ordering': ['orden'], 'verbose_name': 'Grupo de juego'},
        ),
    ]
