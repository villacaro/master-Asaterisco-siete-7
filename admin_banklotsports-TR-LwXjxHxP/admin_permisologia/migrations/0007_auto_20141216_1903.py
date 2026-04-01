# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0006_auto_20141216_1325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menu',
            name='codename',
            field=models.CharField(max_length=160, verbose_name='Codigo'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='menu',
            unique_together=set([('codename', 'url')]),
        ),
    ]
