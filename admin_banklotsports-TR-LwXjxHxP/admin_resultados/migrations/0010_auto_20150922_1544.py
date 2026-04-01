# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0009_auto_20150909_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='anotacionesdetail',
            name='puntaje',
            field=models.IntegerField(null=True, blank=True, verbose_name='Puntaje'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='anotacionesdetail',
            name='referencia',
            field=models.CharField(null=True, blank=True, max_length=100, verbose_name='Referencia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resultados',
            name='status',
            field=models.ForeignKey(to='admin_status.Status', verbose_name='Status', blank=True, null=True),
            preserve_default=True,
        ),
    ]
