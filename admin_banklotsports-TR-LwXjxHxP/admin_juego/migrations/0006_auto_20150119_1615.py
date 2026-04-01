# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0005_auto_20150112_2149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jugador',
            options={'verbose_name': 'Jugador', 'ordering': ['lateralidad', 'nombre'], 'verbose_name_plural': 'Jugadores'},
        ),
        migrations.AlterModelOptions(
            name='jugadortipo',
            options={'verbose_name': 'Tipo de jugador', 'verbose_name_plural': 'Tipos de jugadores'},
        ),
        migrations.AlterModelOptions(
            name='torneos',
            options={'verbose_name': 'Liga', 'ordering': ['nombre'], 'verbose_name_plural': 'Ligas'},
        ),
        migrations.AlterField(
            model_name='sistemajuego',
            name='comercializadora',
            field=models.OneToOneField(blank=True, to='admin_finanzas.Comercializadora', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuego',
            name='user',
            field=models.ForeignKey(blank=True, to='admin_users.Users', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torneos',
            name='por_grupos',
            field=models.BooleanField(verbose_name='Liga por grupos ', help_text='De ser una liga que admite grupos, seleccione el campo', default=False),
            preserve_default=True,
        ),
    ]
