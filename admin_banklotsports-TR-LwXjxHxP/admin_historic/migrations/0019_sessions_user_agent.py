# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0018_auto_20150210_0216'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='user_agent',
            field=models.CharField(null=True, blank=True, max_length=200),
            preserve_default=True,
        ),
    ]
