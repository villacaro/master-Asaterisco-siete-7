# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0010_auto_20150123_1643'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sistemajuegotiporegla',
            name='porcentaje_riesgo',
            field=models.IntegerField(null=True, verbose_name='Porcentaje de riesgo (*)', help_text='Ingrese el porcentaje de riergo', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuegotiporegla',
            name='rango_final',
            field=models.IntegerField(null=True, verbose_name='Rango final (*)', help_text='Ingrese el rango final', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuegotiporegla',
            name='rango_inicial',
            field=models.IntegerField(null=True, verbose_name='Rango inicial (*)', help_text='Ingrese el rango inicial', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuegotiporegla',
            name='tiporegla',
            field=models.ForeignKey(verbose_name='Tipo de regla (*)', help_text='Seleeccione el tipo de regla', to='admin_juego.TipoRegla'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='sistemajuegotiporegla',
            unique_together=set([]),
        ),
    ]
