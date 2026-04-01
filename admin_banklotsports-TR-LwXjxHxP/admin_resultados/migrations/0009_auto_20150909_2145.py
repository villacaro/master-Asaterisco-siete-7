# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0008_resultadosrestric'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultados',
            name='created_at',
            field=models.DateTimeField(verbose_name='Creado', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resultados',
            name='encuentro',
            field=models.ForeignKey(to='admin_juego.Encuentros', verbose_name='Encuentro'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resultados',
            name='sistema',
            field=models.ForeignKey(null=True, verbose_name='Sistema', to='admin_juego.SistemaJuego'),
            preserve_default=True,
        ),
    ]
