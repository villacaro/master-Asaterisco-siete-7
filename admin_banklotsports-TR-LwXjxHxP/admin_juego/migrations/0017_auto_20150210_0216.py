# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0016_auto_20150204_1159'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sistemajuego',
            name='theme',
            field=models.ForeignKey(verbose_name='Tema', null=True, to='admin_themes.Theme', blank=True),
            preserve_default=True,
        ),
    ]
