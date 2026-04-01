# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0005_auto_20141211_1617'),
        ('admin_comercializacion', '0002_auto_20141216_2200'),
    ]

    operations = [
        migrations.CreateModel(
            name='Banco',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 62462), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 62542), auto_now=True)),
            ],
            options={
                'ordering': ['nombre'],
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comercializadora',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('saldo_inicial', models.DecimalField(default=0.0, blank=True, null=True, decimal_places=2, verbose_name='Saldo inicial (*)', max_digits=15)),
                ('saldo_fecha', models.DateField(blank=True, default=datetime.datetime(2015, 1, 26, 9, 39, 46, 69542), verbose_name='Fecha de saldo inicial (*)', null=True, help_text='date')),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 69617), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 69682), auto_now=True)),
                ('agencia', models.ForeignKey(blank=True, null=True, to='admin_comercializacion.Agencias', editable=False)),
                ('banca', models.ForeignKey(blank=True, null=True, to='admin_comercializacion.Bancas', editable=False)),
                ('bloque', models.ForeignKey(blank=True, null=True, to='admin_comercializacion.Bloques', editable=False)),
                ('distribuidor', models.ForeignKey(blank=True, null=True, to='admin_comercializacion.Distribuidores', editable=False)),
                ('operadora', models.ForeignKey(blank=True, null=True, to='admin_comercializacion.Operadoras', editable=False)),
                ('taquilla', models.ForeignKey(blank=True, null=True, to='admin_comercializacion.Taquillas', editable=False)),
            ],
            options={
                'verbose_name_plural': 'Comercializadoras',
                'ordering': ['operadora', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla'],
                'verbose_name': 'Comercializadora',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('numero', models.CharField(verbose_name='Numero de cuenta (*)', max_length=20)),
                ('description', models.CharField(verbose_name='Descripcion (*)', max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 71564), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 71627), auto_now=True)),
                ('banco', models.ForeignKey(to='admin_finanzas.Banco', help_text='Seleccione un banco', verbose_name='Banco (*)')),
                ('comercializadora', models.ForeignKey(blank=True, null=True, to='admin_finanzas.Comercializadora', editable=False)),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Dia',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('fecha', models.DateField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 72905), unique=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 72969), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 73011), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DiaTrabajo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('procesado', models.BooleanField(default=False)),
                ('actual', models.BooleanField(default=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 75709), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 75766), auto_now=True)),
                ('comercializadora', models.ForeignKey(to='admin_finanzas.Comercializadora')),
                ('dia', models.ForeignKey(to='admin_finanzas.Dia')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DimensionComercializadora',
            fields=[
                ('pk_relate', models.IntegerField(serialize=False, primary_key=True)),
                ('pk_origen', models.IntegerField()),
                ('pk_origen_ref', models.IntegerField(blank=True, null=True)),
                ('nombre', models.CharField(blank=True, null=True, max_length=100)),
                ('tipo', models.IntegerField(choices=[[0, 'Error de usuario'], [1, 'Operadora'], [2, 'Bloque'], [3, 'Banca'], [4, 'Distribuidor'], [5, 'Agencia'], [6, 'Taquilla']], blank=True, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 67110), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 67217), auto_now=True)),
                ('pk_relate_ref', models.ForeignKey(blank=True, null=True, to='admin_finanzas.DimensionComercializadora')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='EstatoCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('saldo', models.DecimalField(decimal_places=2, default=0.0, max_digits=15)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 74035), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 74089), auto_now=True)),
                ('cuenta', models.ForeignKey(to='admin_finanzas.Cuenta')),
                ('dia', models.ForeignKey(to='admin_finanzas.Dia')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Movimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('numero', models.CharField(blank=True, verbose_name='Número referencia (*)', null=True, max_length=5)),
                ('monto', models.DecimalField(decimal_places=2, verbose_name='Monto (*)', max_digits=15)),
                ('fecha', models.DateField(verbose_name='Fecha (*)', help_text='date')),
                ('observacion', models.CharField(verbose_name='Observación (*)', max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 77277), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 77341), auto_now=True)),
                ('comercializadora', models.ForeignKey(verbose_name='Comercializadora (*)', to='admin_finanzas.Comercializadora')),
                ('cuenta', models.ForeignKey(verbose_name='Cuenta (*)', to='admin_finanzas.Cuenta')),
                ('dia', models.ForeignKey(to='admin_finanzas.Dia')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ResumenAdministrativo',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('venta', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('premio', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('comision', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('regalia', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('participacion', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('saldo_bruto', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('saldo_comer', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('saldo_oper', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('deposito', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('pago', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('ajuste', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('cargo', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('saldo_anterior', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('saldo_actual', models.DecimalField(decimal_places=8, default=0, max_digits=15, null=True)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 79323), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 79384), auto_now=True)),
                ('comercializadora', models.ForeignKey(to='admin_finanzas.DimensionComercializadora')),
                ('dia', models.ForeignKey(to='admin_finanzas.Dia')),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoCuenta',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=10)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 64065), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 64154), auto_now=True)),
            ],
            options={
                'ordering': ['nombre'],
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoMovimiento',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=50)),
                ('codename', models.CharField(verbose_name='Codigo (*)', max_length=100)),
                ('description', models.CharField(verbose_name='Descripcion (*)', max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 65680), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 26, 9, 39, 46, 65741), auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='movimiento',
            name='tipo',
            field=models.ForeignKey(to='admin_finanzas.TipoMovimiento'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='movimiento',
            name='user',
            field=models.ForeignKey(to='admin_users.Users'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='cuenta',
            name='tipocuenta',
            field=models.ForeignKey(verbose_name='Tipo de cuenta (*)', to='admin_finanzas.TipoCuenta'),
            preserve_default=True,
        ),
    ]
