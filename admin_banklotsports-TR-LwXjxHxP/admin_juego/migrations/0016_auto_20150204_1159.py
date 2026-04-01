# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_themes', '0001_initial'),
        ('admin_juego', '0015_auto_20150126_1731'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='deportes',
            options={'verbose_name': 'Deporte', 'verbose_name_plural': 'Deportes'},
        ),
        migrations.AlterModelOptions(
            name='temporadas',
            options={'verbose_name': 'Temporada', 'verbose_name_plural': 'Temporadas'},
        ),
        migrations.AddField(
            model_name='sistemajuego',
            name='theme',
            field=models.ForeignKey(blank=True, null=True, to='admin_themes.Theme'),
            preserve_default=True,
        ),
    ]
