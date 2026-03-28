# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0023_auto_20150311_0929'),
    ]

    operations = [
        migrations.AddField(
            model_name='deportes',
            name='orden_equipos',
            field=models.IntegerField(verbose_name='Orden de equipos (*)', choices=[(1, 'Home/Visitante'), (2, 'Visitante/Home')], help_text='Seleccione el orden de impresion de logros de los equipos', default=2),
            preserve_default=True,
        ),
    ]
