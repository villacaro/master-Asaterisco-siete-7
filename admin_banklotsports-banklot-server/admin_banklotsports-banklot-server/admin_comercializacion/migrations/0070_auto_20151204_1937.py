# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0069_auto_20151203_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factorriesgo',
            name='comercializadora',
            field=models.OneToOneField(editable=False, to='admin_finanzas.Comercializadora', verbose_name='Comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='factorriesgo',
            name='factores',
            field=jsonfield.fields.JSONField(blank=True, verbose_name='Factores', null=True),
            preserve_default=True,
        ),
    ]
