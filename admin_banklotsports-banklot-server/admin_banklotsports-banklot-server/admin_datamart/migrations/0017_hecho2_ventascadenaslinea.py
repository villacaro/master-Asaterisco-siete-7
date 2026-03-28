# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0016_auto_20150302_1941'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hecho2_VentasCadenasLinea',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('monto_total', models.DecimalField(max_digits=15, null=True, decimal_places=8, default=0)),
                ('monto_premios', models.DecimalField(max_digits=15, null=True, decimal_places=8, default=0)),
                ('count_apuestas', models.IntegerField(null=True, default=0)),
                ('count_tickets', models.IntegerField(null=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacion')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'verbose_name': 'Hecho 2 en linea: Ventas por cadena',
                'verbose_name_plural': 'Hecho 2 en linea: ventas por toda la cadena',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
    ]
