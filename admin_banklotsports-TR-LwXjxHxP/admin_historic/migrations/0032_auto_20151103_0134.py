# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0031_auto_20151103_0040'),
    ]

    operations = [
        migrations.RenameField(
            model_name='taquillasessions',
            old_name='key',
            new_name='priv_key',
        ),
        migrations.AddField(
            model_name='taquillasessions',
            name='pub_key',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
