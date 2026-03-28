# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0006_auto_20141216_2019'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContentTypes',
        ),
        migrations.RemoveField(
            model_name='sessionsdetaildetail',
            name='sessiondetail',
        ),
        migrations.RemoveField(
            model_name='sessionsdetaildetail',
            name='userprocess',
        ),
        migrations.DeleteModel(
            name='SessionsDetailDetail',
        ),
    ]
