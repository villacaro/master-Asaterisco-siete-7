# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0047_auto_20150727_1107'),
    ]

    operations = [
        migrations.AddField(
            model_name='porcentajes',
            name='relacion',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
    ]
