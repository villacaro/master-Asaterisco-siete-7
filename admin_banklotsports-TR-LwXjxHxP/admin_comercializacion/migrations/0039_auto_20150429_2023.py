# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0038_auto_20150429_1051'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenciadatadefault',
            name='frecuencia_queda',
            field=models.CharField(choices=[['frecuencia_semanal', 'Queda semanal'], ['frecuencia_quincenal', 'Queda quincenal'], ['frecuencia_mensual', 'Queda mensual']], help_text='Seleccione la frecuencia de corte para la queda', max_length=30, null=True, verbose_name='Frecuencia de corte de la queda (*)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agencias',
            name='frecuencia_queda',
            field=models.CharField(choices=[['frecuencia_semanal', 'Queda semanal'], ['frecuencia_quincenal', 'Queda quincenal'], ['frecuencia_mensual', 'Queda mensual']], help_text='Seleccione la frecuencia de corte para la queda', max_length=30, null=True, verbose_name='Frecuencia de corte de la queda (*)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datadefault',
            name='frecuencia_queda',
            field=models.CharField(choices=[['frecuencia_semanal', 'Queda semanal'], ['frecuencia_quincenal', 'Queda quincenal'], ['frecuencia_mensual', 'Queda mensual']], help_text='Seleccione la frecuencia de corte para la queda', max_length=30, null=True, verbose_name='Frecuencia de corte de la queda (*)', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datadefault',
            name='porcentaje_queda',
            field=models.DecimalField(decimal_places=5, help_text='Ingrese el porcentaje de queda por tipo de comercializadora', verbose_name='Porcentaje de queda (*)', max_digits=15, default=0.0),
            preserve_default=True,
        ),
    ]
