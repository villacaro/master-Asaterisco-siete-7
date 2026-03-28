# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '__first__'),
        ('admin_juego', '0004_auto_20150108_0942'),
    ]

    operations = [
        migrations.CreateModel(
            name='Anotaciones',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 8, 9, 42, 11, 253175))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 8, 9, 42, 11, 253236))),
                ('grupo', models.ForeignKey(to='admin_juego.GruposApuestas')),
            ],
            options={
                'verbose_name_plural': 'Anotaciones por grupo',
                'verbose_name': 'Anotacion',
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AnotacionesDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('puntaje', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 8, 9, 42, 11, 254458))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 8, 9, 42, 11, 254514))),
                ('anotacion', models.ForeignKey(to='admin_resultados.Anotaciones')),
                ('condicion', models.ForeignKey(to='admin_juego.Condiciones', null=True, blank=True)),
                ('encuentro_detail', models.ForeignKey(to='admin_juego.EncuentrosDetail', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Anotaciones por grupo',
                'verbose_name': 'Anotacion',
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Resultados',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 8, 9, 42, 11, 251671))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 8, 9, 42, 11, 251738))),
                ('encuentro', models.ForeignKey(to='admin_juego.Encuentros')),
                ('status', models.ForeignKey(to='admin_status.Status', null=True, blank=True)),
            ],
            options={
                'verbose_name_plural': 'Resultados por encuentros',
                'verbose_name': 'Resultado de un ecuentro',
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='anotaciones',
            name='resultado',
            field=models.ForeignKey(to='admin_resultados.Resultados'),
            preserve_default=True,
        ),
    ]
