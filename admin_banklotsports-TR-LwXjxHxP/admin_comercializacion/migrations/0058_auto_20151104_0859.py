# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0057_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='codigo',
            field=models.CharField(null=True, db_index=True, max_length=30, help_text='Introduzca un código de centro de apuesta', blank=True, verbose_name='Código '),
            preserve_default=True,
        ),
    ]
