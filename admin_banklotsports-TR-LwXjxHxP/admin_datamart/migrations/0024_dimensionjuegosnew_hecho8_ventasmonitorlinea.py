# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0023_auto_20150520_2021'),
    ]

    operations = [
        migrations.CreateModel(
            name='DimensionJuegosNew',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('sistema_id', models.IntegerField()),
                ('deporte_id', models.IntegerField()),
                ('torneo_id', models.IntegerField()),
                ('temporada_id', models.IntegerField()),
                ('jornada_id', models.IntegerField()),
                ('encuentro_id', models.IntegerField()),
                ('encuentros_modalidad_id', models.IntegerField()),
                ('grupo_id', models.IntegerField()),
                ('modalidad_id', models.IntegerField()),
                ('condicion_id', models.IntegerField()),
                ('equipo_id', models.IntegerField(blank=True, null=True)),
                ('pertenece_id', models.IntegerField(blank=True, null=True)),
                ('grupojuego_id', models.IntegerField(blank=True, null=True)),
                ('jugador_id', models.IntegerField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Dimension de juego',
                'db_tablespace': 'ts_finance',
                'verbose_name_plural': 'Dimension de juegos',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho8_VentasMonitorLinea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('monto_venta', models.DecimalField(decimal_places=8, max_digits=15, default=0, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacion')),
                ('juegos', models.ForeignKey(to='admin_datamart.DimensionJuegosNew')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'verbose_name': 'Hecho 8: Monitor de ventas',
                'db_tablespace': 'ts_finance',
                'verbose_name_plural': 'Hecho 8: Monitor de ventas',
            },
            bases=(models.Model,),
        ),
    ]
