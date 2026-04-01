# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0023_auto_20150213_1609'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='preferenciascadena',
            options={'verbose_name': 'Preferencia de una comercializadora', 'ordering': ['-created_at'], 'verbose_name_plural': 'Preferencias de las comercializadoras'},
        ),
        migrations.AlterModelOptions(
            name='ticketsdatadefault',
            options={'verbose_name': 'Data por defecto de impresion', 'ordering': ['titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3'], 'verbose_name_plural': 'Data por defecto para la impresion'},
        ),
    ]
