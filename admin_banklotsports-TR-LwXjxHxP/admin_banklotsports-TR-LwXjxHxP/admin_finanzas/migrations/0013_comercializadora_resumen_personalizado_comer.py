# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0012_comercializadora_resumen_personalizado'),
    ]

    operations = [
        migrations.AddField(
            model_name='comercializadora',
            name='resumen_personalizado_comer',
            field=models.ForeignKey(to='admin_finanzas.Comercializadora', blank=True, on_delete=django.db.models.deletion.SET_NULL, null=True),
            preserve_default=True,
        ),
    ]
