# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import ws_client.models


class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0011_auto_20150501_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientfiles',
            name='crc',
            field=models.CharField(verbose_name='Hash CRC', max_length=140, default='0', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='clientfiles',
            name='file',
            field=models.FileField(upload_to=ws_client.models.get_image_path),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='clientfiles',
            unique_together=set([('file', 'client_version')]),
        ),
        migrations.RemoveField(
            model_name='clientfiles',
            name='name',
        ),
        migrations.RemoveField(
            model_name='clientfiles',
            name='download_url',
        ),
    ]
