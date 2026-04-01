# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0036_auto_20150421_2221'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventNotificationCadena',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('bloque', models.IntegerField(blank=True, null=True)),
                ('banca', models.IntegerField(blank=True, null=True)),
                ('distribuidor', models.IntegerField(blank=True, null=True)),
                ('agencia', models.IntegerField(blank=True, null=True)),
                ('taquilla', models.IntegerField(blank=True, null=True)),
                ('data_origin', models.IntegerField(editable=False, choices=[(1, 'Preferencias'), (2, 'Factor de riesgo'), (3, 'Mensajes')])),
                ('data', jsonfield.fields.JSONField(blank=True, null=True)),
                ('date_production', models.DateTimeField(db_index=True, auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Actualizaciones por comercializadoras',
                'db_tablespace': 'ts_comer',
                'verbose_name': 'Actualizacion por comercializadora',
            },
            bases=(models.Model,),
        ),
    ]
