# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0010_auto_20150219_2258'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientfiles',
            name='file',
            field=models.FileField(default='', upload_to='download'),
            preserve_default=False,
        ),
    ]
