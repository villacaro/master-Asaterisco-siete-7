# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0027_auto_20150324_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='users',
            name='passwd',
        ),
    ]
