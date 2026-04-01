# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0052_usuariostaquilla_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariostaquilla',
            name='user',
            field=models.CharField(verbose_name='Usuario (*)', help_text='Ingrese un usuario', db_index=True, max_length=200),
            preserve_default=True,
        ),
    ]
