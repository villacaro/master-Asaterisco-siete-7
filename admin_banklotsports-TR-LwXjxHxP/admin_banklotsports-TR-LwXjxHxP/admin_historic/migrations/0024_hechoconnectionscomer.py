# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0023_auto_20150617_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='HechoConnectionsComer',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, auto_created=True, verbose_name='ID')),
                ('operadora_id', models.IntegerField()),
                ('bloque_id', models.IntegerField()),
                ('banca_id', models.IntegerField()),
                ('distribuidor_id', models.IntegerField()),
                ('agencia_id', models.IntegerField()),
                ('taquilla_id', models.IntegerField(db_index=True)),
                ('connection_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Hecho de conexiones',
                'db_tablespace': 'ts_comer',
                'verbose_name': 'Hecho de conexion',
            },
            bases=(models.Model,),
        ),
    ]
