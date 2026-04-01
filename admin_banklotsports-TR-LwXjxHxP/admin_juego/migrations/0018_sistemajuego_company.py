# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_themes', '0003_auto_20150204_1915'),
        ('admin_juego', '0017_auto_20150210_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemajuego',
            name='company',
            field=models.ForeignKey(verbose_name='Compañia', blank=True, null=True, to='admin_themes.Company'),
            preserve_default=True,
        ),
    ]
