# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0022_hecho7_comisionesquedacadena_queda_taquilla'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dimensioncomercializacion',
            name='taquilla_id',
            field=models.IntegerField(db_index=True),
            preserve_default=True,
        ),
    ]
