# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0008_movimiento_comprobante'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='ajuste',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='cargo',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='comision',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='deposito',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='pago',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='participacion',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='premio',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='queda',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='regalia',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='saldo_actual',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='saldo_anterior',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='saldo_bruto',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='saldo_comer',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='saldo_oper',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='resumenadministrativo',
            name='venta',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
    ]
