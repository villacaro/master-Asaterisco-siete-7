# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0033_auto_20150601_2208'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemajuego',
            name='is_resultados',
            field=models.BooleanField(default=False, editable=False),
            preserve_default=True,
        ),
    ]
