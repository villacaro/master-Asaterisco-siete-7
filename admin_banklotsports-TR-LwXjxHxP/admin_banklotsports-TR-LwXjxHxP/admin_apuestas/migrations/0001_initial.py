# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0008_auto_20150123_0253'),
        ('admin_status', '0002_auto_20150123_0253'),
        ('admin_comercializacion', '0020_auto_20150123_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tickets',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('key', models.CharField(null=True, max_length=1000, blank=True)),
                ('monto', models.DecimalField(decimal_places=2, max_digits=15)),
                ('monto_premio', models.DecimalField(decimal_places=2, max_digits=15)),
                ('monto_ganancia', models.DecimalField(decimal_places=2, max_digits=15)),
                ('fecha', models.DateTimeField()),
                ('confirmacion', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 582675))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 582746))),
            ],
            options={
                'verbose_name_plural': 'Tickets',
                'verbose_name': 'Ticket',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketsDetail',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=15)),
                ('logro_apostado', models.IntegerField()),
                ('modalidad_ref', models.CharField(null=True, max_length=140, blank=True)),
                ('condicion_ref', models.CharField(null=True, max_length=140, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 584406))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 584464))),
                ('jugada', models.ForeignKey(to='admin_juego.Jugadas')),
                ('ticket', models.ForeignKey(to='admin_apuestas.Tickets')),
            ],
            options={
                'verbose_name_plural': 'Items de los tickets',
                'ordering': ['created_at'],
                'verbose_name': 'Item de un ticket',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketsDetailStatus',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('startdate', models.DateTimeField()),
                ('enddate', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 587694))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 587750))),
                ('detalle_ticket', models.ForeignKey(to='admin_apuestas.TicketsDetail')),
                ('status', models.ForeignKey(to='admin_status.Status')),
            ],
            options={
                'verbose_name_plural': 'Estatus de los items de los tickets',
                'ordering': ['startdate'],
                'verbose_name': 'Estatus de un item de un ticket',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketStatus',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('startdate', models.DateTimeField()),
                ('enddate', models.DateTimeField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 586002))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 586056))),
                ('status', models.ForeignKey(to='admin_status.Status')),
                ('ticket', models.ForeignKey(to='admin_apuestas.Tickets')),
            ],
            options={
                'verbose_name_plural': 'Estatus de los tickets',
                'ordering': ['startdate'],
                'verbose_name': 'Estatus de un ticket',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TicketsType',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('codename', models.CharField(max_length=160, unique=True)),
                ('descripcion', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 580346))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 2, 53, 32, 580412))),
            ],
            options={
                'verbose_name_plural': 'Tipos de apuestas para los tickes',
                'ordering': ['nombre'],
                'verbose_name': 'Tipo de apuesta para un ticket',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tickets',
            name='ticket_type',
            field=models.ForeignKey(to='admin_apuestas.TicketsType'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tickets',
            name='user',
            field=models.ForeignKey(to='admin_comercializacion.UsuariosTaquilla'),
            preserve_default=True,
        ),
    ]
