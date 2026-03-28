# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0033_auto_20151110_0134'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taquillasessions',
            name='priv_key',
        ),
        migrations.RemoveField(
            model_name='taquillasessions',
            name='pub_key',
        ),
    ]
