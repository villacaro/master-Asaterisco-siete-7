# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0035_sistemajuego_is_logros'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentrosmodalidades',
            name='sistema',
            field=models.ForeignKey(to='admin_juego.SistemaJuego', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugadas',
            name='origen',
            field=models.ForeignKey(to='admin_juego.Jugadas', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugadas',
            name='sistema',
            field=models.ForeignKey(to='admin_juego.SistemaJuego', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugadasinformativas',
            name='sistema',
            field=models.ForeignKey(to='admin_juego.SistemaJuego', null=True),
            preserve_default=True,
        ),
    ]
