# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0001_initial'),
        ('admin_comercializacion', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Status',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=160)),
                ('codename', models.CharField(unique=True, max_length=160)),
                ('content_type', models.IntegerField(choices=[[0, 'Status de actualizacion'], [1, 'Status de usuarios'], [2, 'Status de encuentros'], [3, 'Status de taquillas'], [4, 'Status de jugadas'], [5, 'Status de encuentro resultado'], [6, 'Status de venta de tickets'], [7, 'Status de ??????'], [8, 'Status de tickets']])),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 614681), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 614743), auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Estatus',
                'verbose_name': 'Estatus',
                'ordering': ['content_type'],
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StatusDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('startdate', models.DateField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 616165), auto_now_add=True)),
                ('enddate', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(null=True, blank=True, max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 616300), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 616342), auto_now=True)),
                ('status', models.ForeignKey(to='admin_status.Status')),
                ('user', models.ForeignKey(to='admin_users.Users')),
            ],
            options={
                'verbose_name_plural': 'Detalle de estatus de los usuario',
                'verbose_name': 'Detalle de estatus',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaquillaStatusDetail',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('startdate', models.DateField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 617766), auto_now_add=True)),
                ('enddate', models.DateField(blank=True, null=True)),
                ('comment', models.CharField(null=True, blank=True, max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 617927), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 33, 617992), auto_now=True)),
                ('status', models.ForeignKey(to='admin_status.Status')),
                ('usuariotaquilla', models.ForeignKey(to='admin_comercializacion.UsuariosTaquilla')),
            ],
            options={
                'verbose_name_plural': 'Detalle de estatus de las taquillas',
                'verbose_name': 'Detalle de estatus',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
    ]
