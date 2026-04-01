# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0013_auto_20150125_1938'),
        ('admin_finanzas', '0002_auto_20150126_1347'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cuenta',
            options={'verbose_name_plural': 'Cuentas bancarias', 'verbose_name': 'Cuenta bancaria'},
        ),
        migrations.AlterModelOptions(
            name='dia',
            options={'verbose_name_plural': 'Dias', 'verbose_name': 'Dias'},
        ),
        migrations.AlterModelOptions(
            name='diatrabajo',
            options={'verbose_name_plural': 'Dia de trabajos', 'verbose_name': 'Dia de trabajo'},
        ),
        migrations.AlterModelOptions(
            name='estatocuenta',
            options={'verbose_name_plural': 'Estados de cuenta', 'verbose_name': 'Estado de cuenta'},
        ),
        migrations.AlterModelOptions(
            name='movimiento',
            options={'verbose_name_plural': 'Movimientos bancarios', 'verbose_name': 'Movimiento bancario'},
        ),
        migrations.AlterModelOptions(
            name='resumenadministrativo',
            options={'verbose_name_plural': 'Resumenes administrativos', 'verbose_name': 'Resumen administrativo'},
        ),
        migrations.AddField(
            model_name='resumenadministrativo',
            name='comercializacion',
            field=models.ForeignKey(default=None, to='admin_datamart.DimensionArcoComercializacion'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='saldo_fecha',
            field=models.DateField(help_text='Introdusca la fecha del saldo inicial de la comercializadora', blank=True, verbose_name='Fecha de saldo inicial (*)', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comercializadora',
            name='saldo_inicial',
            field=models.DecimalField(default=0.0, verbose_name='Saldo inicial (*)', help_text='Introdusca el saldo inicial de la comercializadora', max_digits=15, blank=True, decimal_places=2, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='dia',
            name='fecha',
            field=models.DateField(default=datetime.datetime(2015, 1, 26, 15, 17, 13, 595367), unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='movimiento',
            name='fecha',
            field=models.DateField(help_text='Fecha del movimiento', verbose_name='Fecha (*)'),
            preserve_default=True,
        ),
    ]
