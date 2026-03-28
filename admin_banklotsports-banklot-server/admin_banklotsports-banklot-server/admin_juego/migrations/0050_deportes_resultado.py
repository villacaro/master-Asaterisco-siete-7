# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0049_auto_20150924_1622'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportes',
            name='resultado',
            field=models.CharField(verbose_name='Modo de ganar (*)', choices=[['-', 'Por puntaje'], ['+', 'Por posicion']], max_length=1, default='-', help_text='Seleccione el modo de ganar en un deporte'),
        ),
    ]
