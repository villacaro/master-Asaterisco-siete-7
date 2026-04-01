# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0003_auto_20150302_1941'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tickets',
            name='confirmacion',
        ),
    ]
