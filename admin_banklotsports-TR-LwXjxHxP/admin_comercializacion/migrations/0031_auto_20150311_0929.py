# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0030_auto_20150305_2253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operadoras',
            options={'verbose_name': 'Operadora', 'verbose_name_plural': 'Operadoras'},
        ),
    ]
