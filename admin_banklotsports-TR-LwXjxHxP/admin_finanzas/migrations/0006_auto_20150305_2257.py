# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0005_auto_20150302_1941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movimiento',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='admin_users.Users', blank=True),
            preserve_default=True,
        ),
    ]
