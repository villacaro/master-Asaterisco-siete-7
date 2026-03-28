# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0071_auto_20160106_0931'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencias',
            name='pk_clone',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bancas',
            name='pk_clone',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bloques',
            name='pk_clone',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='distribuidores',
            name='pk_clone',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='operadoras',
            name='pk_clone',
            field=models.PositiveIntegerField(editable=False, db_index=True, default=0),
            preserve_default=True,
        ),
    ]
