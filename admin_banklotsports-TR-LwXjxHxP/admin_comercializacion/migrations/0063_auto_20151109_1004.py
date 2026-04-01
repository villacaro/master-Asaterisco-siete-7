# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0062_typepreferences_type_data'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typepreferences',
            name='distribute',
            field=models.BooleanField(help_text='Seleccione si es una preferencia distribuida', default=False, verbose_name='¿Distribuida? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='typepreferences',
            name='edit',
            field=models.BooleanField(help_text='Seleccione si es una preferencia editable', default=True, verbose_name='¿Editable? '),
            preserve_default=True,
        ),
    ]
