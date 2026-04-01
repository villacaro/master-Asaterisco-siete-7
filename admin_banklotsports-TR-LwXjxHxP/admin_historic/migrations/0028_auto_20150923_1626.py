# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0027_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sessions',
            name='id',
            field=models.CharField(primary_key=True, serialize=False, db_index=True, max_length=36),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sessionsdetail',
            name='id',
            field=models.CharField(primary_key=True, serialize=False, db_index=True, max_length=36),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillasessions',
            name='id',
            field=models.CharField(primary_key=True, serialize=False, db_index=True, max_length=36),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillasessionsdetail',
            name='id',
            field=models.CharField(primary_key=True, serialize=False, db_index=True, max_length=36),
            preserve_default=True,
        ),
    ]
