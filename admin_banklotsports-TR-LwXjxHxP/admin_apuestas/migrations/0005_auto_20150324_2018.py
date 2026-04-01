# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0004_remove_tickets_confirmacion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ticketsdetail',
            options={'verbose_name': 'Detalle de ticket', 'ordering': ['created_at'], 'verbose_name_plural': 'Detalle de tickets'},
        ),
    ]
