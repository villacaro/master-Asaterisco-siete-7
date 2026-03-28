# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0077_auto_20160321_2314'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariostaquilla',
            name='keys_date',
            field=models.DateTimeField(editable=False, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuariostaquilla',
            name='priv_key',
            field=models.CharField(default='', editable=False, max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuariostaquilla',
            name='pub_key',
            field=models.CharField(default='', editable=False, max_length=1000),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuariostaquilla',
            name='pub_key_client',
            field=models.CharField(default='', editable=False, max_length=1000),
            preserve_default=True,
        ),
    ]
