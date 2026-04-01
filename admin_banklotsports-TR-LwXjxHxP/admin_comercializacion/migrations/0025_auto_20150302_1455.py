# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0024_auto_20150213_1838'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencias',
            options={'verbose_name_plural': 'Centros de apuesta', 'verbose_name': 'Centro de apuesta'},
        ),
        migrations.AlterModelOptions(
            name='bloques',
            options={'verbose_name_plural': 'Multi Bancas', 'verbose_name': 'Multi Banca'},
        ),
        migrations.AlterField(
            model_name='bancas',
            name='bloque',
            field=models.ForeignKey(help_text='Seleccione una multi banca', blank=True, null=True, to='admin_comercializacion.Bloques', verbose_name='Multi Banca (*)'),
            preserve_default=True,
        ),
    ]
