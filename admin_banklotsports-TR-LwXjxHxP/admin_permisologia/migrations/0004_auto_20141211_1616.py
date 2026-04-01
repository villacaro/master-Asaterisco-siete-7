# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0004_auto_20141211_1616'),
        ('admin_permisologia', '0003_auto_20141203_2249'),
    ]

    operations = [
        migrations.AddField(
            model_name='permissions',
            name='profiles',
            field=models.ManyToManyField(verbose_name='Perfil de usuario (*)', to='admin_users.UserProfile'),
            preserve_default=True,
        ),
    ]
