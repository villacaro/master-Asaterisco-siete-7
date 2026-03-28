# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0072_auto_20160112_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='taquillas',
            name='pk_clone',
            field=models.PositiveIntegerField(default=0, db_index=True, editable=False),
        ),
        migrations.AddField(
            model_name='usuariostaquilla',
            name='pk_clone',
            field=models.PositiveIntegerField(default=0, db_index=True, editable=False),
        ),
    ]
