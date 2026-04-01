# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0064_auto_20151105_1737'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='cantidad_apuesta_max',
            field=models.IntegerField(verbose_name='Cantidad máxima de combinaciones ', null=True, help_text='Seleccione la cantidad máxima de combinaciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='cantidad_apuesta_min',
            field=models.IntegerField(verbose_name='Cantidad minima de combinaciones ', null=True, help_text='Seleccione la cantidad minima de combinaciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='montomax',
            field=models.DecimalField(verbose_name='Monto máximo de apuesta ', null=True, max_digits=15, help_text='Seleccione el monto máximo de apuesta', decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='montomax_ganancia',
            field=models.DecimalField(verbose_name='Monto máximo de ganancia ', null=True, max_digits=15, help_text='Seleccione el monto máximo de ganancia', decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='montomin',
            field=models.DecimalField(verbose_name='Monto mínimo de apuesta ', null=True, max_digits=15, help_text='Seleccione el monto mínimo de apuesta', decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_clonados_maxima_ganancia',
            field=models.DecimalField(verbose_name='Parley: Monto máximo de ganancia para combinaciones repetidas en tickets', null=True, max_digits=15, help_text='Parley: Seleccione el monto máximo para la ganancia de apuestas con combinaciones repetidas en los tickets', decimal_places=2),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_empates_max',
            field=models.IntegerField(verbose_name='Parley: Cantidad máxima de apuesta a empate por ticket', null=True, help_text='Parley: Indique la cantidad máxima permitida de apuestas a empate en un ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_hembras_max',
            field=models.IntegerField(verbose_name='Parley: Máximo de apuestas a una hembra por ticket', null=True, help_text='Parley: Seleccione el numero máximo de apuesta a una en un ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_hembras_min',
            field=models.IntegerField(verbose_name='Parley: cantidad minima de hembras (*)', null=True, help_text='Ingrese la cantidad minima de hembras por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_machos_max',
            field=models.IntegerField(verbose_name='Parley: Máximo de apuestas a un macho por ticket', null=True, help_text='Parley: Seleccione el numero máximo de apuesta a un macho en un ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='parley_machos_min',
            field=models.IntegerField(verbose_name='Parley: Mínimo de apuestas a un macho por ticket', null=True, help_text='Parley: Seleccione el numero mínimo de apuesta a un macho en un ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='tiempoexpiracion',
            field=models.IntegerField(verbose_name='Días de expiración del los tickets ', null=True, help_text='Seleccione la cantidad de días de expiración para los tickets'),
            preserve_default=True,
        ),
    ]
