# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0012_auto_20150123_0120'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dimensionjuegos',
            old_name='pertenece_id',
            new_name='pertenece',
        ),
    ]
