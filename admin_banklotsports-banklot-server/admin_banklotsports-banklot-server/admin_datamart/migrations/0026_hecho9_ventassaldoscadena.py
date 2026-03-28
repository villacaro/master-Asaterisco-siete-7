# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0025_hecho6_comisionescadenajuego_queda_ref'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hecho9_VentasSaldosCadena',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('saldo_actual', models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8)),
                ('saldo_anterior', models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8)),
                ('depositos', models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8)),
                ('pagos', models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8)),
                ('ajustes', models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8)),
                ('cargos', models.DecimalField(null=True, default=0, max_digits=15, decimal_places=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionArcoComercializacion')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
                'verbose_name': 'Hecho 9 Saldos Cadena',
                'verbose_name_plural': 'Hecho 9: Saldos Cadena',
            },
            bases=(models.Model,),
        ),
    ]
