# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0028_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bancas',
            name='modelo_negocio',
            field=models.IntegerField(default=1, verbose_name='Modelo de negocio (*)', help_text='Seleccione el modelo de negocio', choices=[[1, 'Porcentajes'], [2, 'Alquiler']]),
            preserve_default=True,
        ),
    ]
