# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ciudades',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 803694), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 803753), auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Ciudades',
                'ordering': ['nombre'],
                'verbose_name': 'Ciudad',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Direcciones',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('direccion', models.CharField(max_length=200)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 805154), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 805219), auto_now=True)),
                ('ciudad', models.ForeignKey(null=True, blank=True, to='admin_profiles.Ciudades')),
            ],
            options={
                'verbose_name_plural': 'Direcciones',
                'verbose_name': 'Direccione',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Estados',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 801186), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 801260), auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Estados',
                'ordering': ['nombre'],
                'verbose_name': 'Estado',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Municipios',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 802451), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 802513), auto_now=True)),
                ('estado', models.ForeignKey(to='admin_profiles.Estados')),
            ],
            options={
                'verbose_name_plural': 'Municipios',
                'ordering': ['nombre'],
                'verbose_name': 'Municipio',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Paises',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('nombre', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 799699), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2015, 1, 22, 17, 19, 49, 799766), auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Paises',
                'ordering': ['nombre'],
                'verbose_name': 'Pais',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='estados',
            name='pais',
            field=models.ForeignKey(to='admin_profiles.Paises'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direcciones',
            name='estado',
            field=models.ForeignKey(null=True, blank=True, to='admin_profiles.Estados'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='direcciones',
            name='municipio',
            field=models.ForeignKey(null=True, blank=True, to='admin_profiles.Municipios'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ciudades',
            name='municipio',
            field=models.ForeignKey(to='admin_profiles.Municipios'),
            preserve_default=True,
        ),
    ]
