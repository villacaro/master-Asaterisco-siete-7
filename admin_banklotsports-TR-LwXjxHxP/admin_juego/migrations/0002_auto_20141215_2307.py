# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0001_initial'),
        ('admin_juego', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemajuego',
            name='comercializadora',
            field=models.OneToOneField(null=True, to='admin_finanzas.Comercializadora'),
            preserve_default=True,
        ),
    ]
