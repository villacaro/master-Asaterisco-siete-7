# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0007_auto_20141216_1903'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permissions',
            name='content_type',
        ), 
    ]
