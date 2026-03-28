# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0029_auto_20150920_2016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='users',
            name='comercializadora',
            field=models.ManyToManyField(verbose_name='Comercializadora', to='admin_finanzas.Comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='superuser',
            field=models.BooleanField(verbose_name='Superusuario', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_ref',
            field=models.ForeignKey(blank=True, null=True, verbose_name='Usuario creador', on_delete=django.db.models.deletion.SET_NULL, to='admin_users.Users'),
            preserve_default=True,
        ),
    ]
