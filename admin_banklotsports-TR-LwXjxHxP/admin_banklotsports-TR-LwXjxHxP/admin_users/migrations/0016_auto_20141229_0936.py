# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0015_auto_20141216_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='token_time',
            field=models.DateTimeField(editable=False, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='passwd',
            field=models.CharField(editable=False, blank=True, verbose_name='Contraseña ', max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_ref',
            field=models.ForeignKey(null=True, blank=True, to='admin_users.Users'),
            preserve_default=True,
        ),
    ]
