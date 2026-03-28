# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0013_auto_20150122_1253'),
        ('admin_users', '0018_auto_20150122_1253'),
        ('admin_juego', '0007_auto_20150122_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='DimensionArcoComercializacion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 667683))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 667740))),
                ('agencia', models.ForeignKey(null=True, to='admin_comercializacion.Agencias', blank=True)),
                ('banca', models.ForeignKey(null=True, to='admin_comercializacion.Bancas', blank=True)),
                ('bloque', models.ForeignKey(null=True, to='admin_comercializacion.Bloques', blank=True)),
                ('distribuidor', models.ForeignKey(null=True, to='admin_comercializacion.Distribuidores', blank=True)),
                ('operadora', models.ForeignKey(null=True, to='admin_comercializacion.Operadoras', blank=True)),
                ('user', models.ForeignKey(null=True, to='admin_users.Users', blank=True)),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DimensionComercializacion',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 663763))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 663819))),
                ('agencia', models.ForeignKey(to='admin_comercializacion.Agencias')),
                ('banca', models.ForeignKey(to='admin_comercializacion.Bancas')),
                ('bloque', models.ForeignKey(to='admin_comercializacion.Bloques')),
                ('distribuidor', models.ForeignKey(to='admin_comercializacion.Distribuidores')),
                ('taquilla', models.ForeignKey(to='admin_comercializacion.Taquillas')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DimensionComercializacionPorcentajes',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 669365))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 669424))),
                ('agencia', models.ForeignKey(null=True, to='admin_comercializacion.Agencias', blank=True)),
                ('banca', models.ForeignKey(null=True, to='admin_comercializacion.Bancas', blank=True)),
                ('bloque', models.ForeignKey(null=True, to='admin_comercializacion.Bloques', blank=True)),
                ('distribuidor', models.ForeignKey(null=True, to='admin_comercializacion.Distribuidores', blank=True)),
                ('taquilla', models.ForeignKey(null=True, to='admin_comercializacion.Taquillas', blank=True)),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DimensionJuegos',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('pertenece', models.CharField(null=True, max_length=140, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 665814))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 665879))),
                ('condicion', models.ForeignKey(to='admin_juego.Condiciones')),
                ('deporte', models.ForeignKey(to='admin_juego.Deportes')),
                ('encuentro', models.ForeignKey(to='admin_juego.Encuentros')),
                ('encuentros_modalidad', models.ForeignKey(to='admin_juego.EncuentrosModalidades')),
                ('jornada', models.ForeignKey(to='admin_juego.Jornadas')),
                ('modalidad', models.ForeignKey(to='admin_juego.Modalidades')),
                ('temporada', models.ForeignKey(to='admin_juego.Temporadas')),
                ('torneo', models.ForeignKey(to='admin_juego.Torneos')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DimensionTiempo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('fecha', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 662480))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 662542))),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho1_VentasCadenasJuegos',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('monto_total', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('monto_premios', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('count_apuestas', models.IntegerField(null=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 673952))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 674030))),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacion')),
                ('juegos', models.ForeignKey(to='admin_datamart.DimensionJuegos')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho2_VentasCadenas',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('monto_total', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('monto_premios', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('count_apuestas', models.IntegerField(null=True, default=0)),
                ('count_tickets', models.IntegerField(null=True, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 675793))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 675854))),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacion')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho3_PagosCadena',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('monto_pago', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('abono', models.NullBooleanField()),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 677506))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 677600))),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionArcoComercializacion')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho4_DepositosCadena',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('monto_deposito', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('abono', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 679533))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 679608))),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionArcoComercializacion')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho5_ComisionesCadena',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('venta', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('premio', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('comision', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('comision_down', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('participacion', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('participacion_down', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('regalia', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('regalia_down', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('saldo_bruto', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('saldo_comer', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('saldo_oper', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 681294))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 681351))),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacionPorcentajes')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Hecho6_ComisionesCadenaJuego',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('venta', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('premio', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('comision', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('comision_down', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('participacion', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('participacion_down', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('regalia', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('regalia_down', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('saldo_bruto', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('saldo_comer', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('saldo_oper', models.DecimalField(null=True, decimal_places=8, max_digits=15, default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 683328))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 22, 12, 53, 30, 683384))),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacionPorcentajes')),
                ('juegos', models.ForeignKey(to='admin_datamart.DimensionJuegos')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
    ]
