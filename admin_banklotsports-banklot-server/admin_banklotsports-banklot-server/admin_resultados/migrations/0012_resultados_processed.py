# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0011_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultados',
            name='processed',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
