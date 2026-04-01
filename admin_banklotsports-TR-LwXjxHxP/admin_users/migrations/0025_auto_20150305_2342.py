# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0024_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='comercializadora_session',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comercializadora_session', to='admin_finanzas.Comercializadora', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user_ref',
            field=models.ForeignKey(to='admin_users.Users', null=True, blank=True, on_delete=django.db.models.deletion.SET_NULL),
            preserve_default=True,
        ),
    ]
