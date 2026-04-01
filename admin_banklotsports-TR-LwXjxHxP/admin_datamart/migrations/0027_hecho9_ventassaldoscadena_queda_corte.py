# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0026_hecho9_ventassaldoscadena'),
    ]

    operations = [
        migrations.AddField(
            model_name='hecho9_ventassaldoscadena',
            name='queda_corte',
            field=models.DecimalField(default=0, decimal_places=8, max_digits=15, null=True),
            preserve_default=True,
        ),
    ]
