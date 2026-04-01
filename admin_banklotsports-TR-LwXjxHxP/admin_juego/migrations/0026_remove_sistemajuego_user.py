# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0025_auto_20150410_0051'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sistemajuego',
            name='user',
        ),
    ]
