# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0011_auto_20150121_1525'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preferencias',
            options={'verbose_name_plural': 'Preferencias de las comercializadoras', 'verbose_name': 'Preferencia de comercialzadora'},
        ),
    ]
