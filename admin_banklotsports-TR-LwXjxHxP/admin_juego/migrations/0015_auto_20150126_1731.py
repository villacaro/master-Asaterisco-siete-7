# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0014_auto_20150126_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventnotification',
            name='data_origin',
            field=models.IntegerField(choices=[(0, 'Preferencias'), (1, 'Deportes'), (2, 'Temporadas'), (3, 'Jornadas'), (4, 'Equipos'), (5, 'Encuentros'), (6, 'Referencias'), (7, 'Logros')], editable=False),
            preserve_default=True,
        ),
    ]
