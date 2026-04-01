# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0036_deportes_runline_positivo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentros',
            name='created_at',
            field=models.DateTimeField(verbose_name='Creado', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentros',
            name='updated_at',
            field=models.DateTimeField(verbose_name='Actualizado', auto_now=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentrosdetail',
            name='indice',
            field=models.IntegerField(null=True, verbose_name='Home/Visitante'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentrosdetail',
            name='jugador',
            field=models.ForeignKey(null=True, verbose_name='Jugador', to='admin_juego.Jugador'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentrosdetail',
            name='referencia',
            field=models.CharField(null=True, blank=True, verbose_name='Referencia', max_length=140),
            preserve_default=True,
        ),
    ]
