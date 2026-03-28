# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0029_auto_20150305_1929'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='admin_users.Users', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='admin_users.Users', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='admin_users.Users', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='admin_users.Users', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='admin_users.Users', blank=True, null=True),
            preserve_default=True,
        ),
    ]
