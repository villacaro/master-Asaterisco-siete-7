# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0008_auto_20150123_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='SistemaJuegoTipoRegla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('rango_inicial', models.IntegerField(help_text='Ingrese la numeración de orden', verbose_name='Rango inicial (*)', null=True, blank=True)),
                ('rango_final', models.IntegerField(help_text='Ingrese la numeración de orden', verbose_name='Rango final ', null=True, blank=True)),
                ('porcentaje_riesgo', models.IntegerField(help_text='Ingrese la numeración de orden', verbose_name='Porcentaje de riesgo (*)', null=True, blank=True)),
                ('sistemajuego', models.ForeignKey(to='admin_juego.SistemaJuego')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 12, 15, 23, 3, 51, 815480))),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 15, 23, 3, 51, 815537), auto_now=True)),
            
            ],
            options={
                'verbose_name_plural': 'Reglas por sistema de juegos',
                'verbose_name': 'Regla por sistema de juego',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TipoRegla',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('nombre', models.CharField(null=True, blank=True, max_length=200)),
                ('codename', models.CharField(null=True, blank=True, max_length=200)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2015, 1, 23, 16, 41, 53, 62534))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2015, 1, 23, 16, 41, 53, 62599))),
            ],
            options={
                'verbose_name_plural': 'Tipos de reglas',
                'verbose_name': 'Tipo de regla',
                'ordering': ['nombre'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='sistemajuegotiporegla',
            name='tiporegla',
            field=models.ForeignKey(to='admin_juego.TipoRegla'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='sistemajuegotiporegla',
            unique_together=set([('sistemajuego', 'tiporegla')]),
        ),
        migrations.AddField(
            model_name='sistemajuego',
            name='reglas',
            field=models.ManyToManyField(null=True, help_text='Asigne y configure las reglas de su sistema', verbose_name='Asigne las distintas reglas (*)', to='admin_juego.TipoRegla', through='admin_juego.SistemaJuegoTipoRegla', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuego',
            name='comercializadora',
            field=models.OneToOneField(blank=True, null=True, to='admin_finanzas.Comercializadora', editable=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sistemajuego',
            name='user',
            field=models.ForeignKey(null=True, to='admin_users.Users', editable=False, blank=True),
            preserve_default=True,
        ),
    ]
