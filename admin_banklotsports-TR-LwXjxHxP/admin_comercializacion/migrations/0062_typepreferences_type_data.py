# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0061_auto_20151105_1448'),
    ]

    operations = [
        migrations.AddField(
            model_name='typepreferences',
            name='type_data',
            field=models.IntegerField(verbose_name='Tipo de dato (*)', help_text='Seleccione el tipo de dato', choices=[[1, 'Entero'], [2, 'Decimal'], [3, 'String']], default=1),
            preserve_default=False,
        ),
    ]
