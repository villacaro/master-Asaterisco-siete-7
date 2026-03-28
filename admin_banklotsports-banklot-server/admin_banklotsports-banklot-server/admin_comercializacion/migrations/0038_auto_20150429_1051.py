# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0037_eventnotificationcadena'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='agencias',
            name='user',
        ),
        migrations.RemoveField(
            model_name='bancas',
            name='user',
        ),
        migrations.RemoveField(
            model_name='bloques',
            name='user',
        ),
        migrations.RemoveField(
            model_name='distribuidores',
            name='user',
        ),
        migrations.RemoveField(
            model_name='operadoras',
            name='user',
        ),
    ]
