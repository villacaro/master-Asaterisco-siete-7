# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0005_auto_20141211_1617'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='etiqueta',
            field=models.CharField(verbose_name='Etiqueta ', blank=True, null=True, max_length=200),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(verbose_name='Correo electronico ', help_text='Ingrese el correo electronico', blank=True, unique=True, null=True, max_length=254),
            preserve_default=True,
        ),
    ]
