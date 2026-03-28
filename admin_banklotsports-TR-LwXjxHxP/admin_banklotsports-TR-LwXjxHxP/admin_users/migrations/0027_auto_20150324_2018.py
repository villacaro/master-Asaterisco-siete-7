# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0026_users_comercializadora_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='comercializadora',
            field=models.ManyToManyField(to='admin_finanzas.Comercializadora'),
            preserve_default=True,
        ),
    ]
