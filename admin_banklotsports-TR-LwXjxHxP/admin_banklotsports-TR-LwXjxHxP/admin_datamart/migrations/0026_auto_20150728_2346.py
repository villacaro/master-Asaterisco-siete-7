# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0025_hecho6_comisionescadenajuego_queda_ref'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hecho1_ventascadenasjuegos',
            name='monto_premios',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho1_ventascadenasjuegos',
            name='monto_total',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho2_ventascadenas',
            name='monto_premios',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho2_ventascadenas',
            name='monto_total',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho2_ventascadenaslinea',
            name='monto_premios',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho2_ventascadenaslinea',
            name='monto_total',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='alquiler',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='comision',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='comision_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='participacion',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='participacion_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='premio',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='queda',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='queda_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='queda_ref',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='regalia',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='regalia_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='saldo_bruto',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='saldo_comer',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='saldo_oper',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho5_comisionescadena',
            name='venta',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='comision',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='comision_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='participacion',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='participacion_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='premio',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='queda_ref',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='regalia',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='regalia_down',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='saldo_bruto',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='saldo_comer',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='saldo_oper',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho6_comisionescadenajuego',
            name='venta',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho7_comisionesquedacadena',
            name='queda_agencia',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho7_comisionesquedacadena',
            name='queda_banca',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho7_comisionesquedacadena',
            name='queda_bloque',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho7_comisionesquedacadena',
            name='queda_distribuidor',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho7_comisionesquedacadena',
            name='queda_taquilla',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='hecho8_ventasmonitorlinea',
            name='monto_venta',
            field=models.DecimalField(max_digits=30, decimal_places=16, null=True, default=0),
            preserve_default=True,
        ),
    ]
