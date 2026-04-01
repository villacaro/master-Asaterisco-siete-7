# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultados',
            name='encuentro',
            field=models.OneToOneField(to='admin_juego.Encuentros'),
            preserve_default=True,
        ),
    ]
