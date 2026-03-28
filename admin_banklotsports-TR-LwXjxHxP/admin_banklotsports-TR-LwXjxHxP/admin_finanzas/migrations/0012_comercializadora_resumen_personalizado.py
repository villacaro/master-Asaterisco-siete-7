# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0011_auto_20150814_0834'),
    ]

    operations = [
        migrations.AddField(
            model_name='comercializadora',
            name='resumen_personalizado',
            field=models.BooleanField(verbose_name='Resumen personalizado', help_text='En caso de estar activada esta opcion la comercializadora sera gestionada solo desde resumen personalizado.', default=False),
            preserve_default=True,
        ),
    ]
