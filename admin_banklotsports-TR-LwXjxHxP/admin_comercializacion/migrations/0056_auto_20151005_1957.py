# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0055_auto_20151005_1948'),
    ]

    operations = [
        migrations.AddField(
            model_name='agencias',
            name='ticket_pie',
            field=models.CharField(null=True, verbose_name='Ticket: Pie del ticket (*)', max_length=100, blank=True, help_text='Ingrese el pie del ticket'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agencias',
            name='ticket_titulo',
            field=models.CharField(null=True, verbose_name='Ticket: Titulo del ticket (*)', max_length=100, blank=True, help_text='Ingrese el titulo del ticket'),
            preserve_default=True,
        ),
    ]
