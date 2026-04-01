# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0015_permissionssales'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='codename',
            field=models.CharField(max_length=160, verbose_name='Codigo ', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.CharField(max_length=160, verbose_name='Url ', blank=True, db_index=True, null=True),
            preserve_default=True,
        ),
    ]
