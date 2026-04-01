# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0053_auto_20150924_1044'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencias',
            name='codigo',
            field=models.CharField(db_index=True, help_text='Introduzca un código de centro de apuesta', null=True, max_length=30, verbose_name='Código (*)', blank=True),
            preserve_default=True,
        ),
    ]
