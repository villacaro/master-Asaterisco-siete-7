# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0007_auto_20141223_1754'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sessionsdetail',
            name='model',
        ),   
    ]
