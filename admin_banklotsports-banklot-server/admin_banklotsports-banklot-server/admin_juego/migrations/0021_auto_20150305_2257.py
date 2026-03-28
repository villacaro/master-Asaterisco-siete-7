# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0020_auto_20150303_1947'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sistemajuego',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, null=True, to='admin_users.Users', editable=False, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='condiciones',
            name='modalidad',
            field=models.ForeignKey(unique=True, to='admin_juego.Modalidades'),
            preserve_default=True,
        ),
    ]
