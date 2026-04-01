# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0018_auto_20150429_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hecho6_comisionescadenajuego',
            name='queda',
        ),
        migrations.RemoveField(
            model_name='hecho6_comisionescadenajuego',
            name='queda_down',
        ),
    ]
