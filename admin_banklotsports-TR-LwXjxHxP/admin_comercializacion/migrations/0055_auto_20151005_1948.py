# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0054_auto_20151005_1700'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenciadatadefault',
            name='ticket_pie',
            field=models.CharField(null=True, blank=True, max_length=100, help_text='Ingrese el pie del ticket', verbose_name='Ticket: Pie del ticket (*)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agenciadatadefault',
            name='ticket_titulo',
            field=models.CharField(null=True, blank=True, max_length=100, help_text='Ingrese el titulo del ticket', verbose_name='Ticket: Titulo del ticket (*)'),
            preserve_default=True,
        ),
    ]
