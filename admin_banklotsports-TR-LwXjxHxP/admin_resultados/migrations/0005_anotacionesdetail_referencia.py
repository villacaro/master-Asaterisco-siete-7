# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0004_auto_20150302_1941'),
    ]

    operations = [
        migrations.AddField(
            model_name='anotacionesdetail',
            name='referencia',
            field=models.CharField(null=True, max_length=100, blank=True),
            preserve_default=True,
        ),
    ]
