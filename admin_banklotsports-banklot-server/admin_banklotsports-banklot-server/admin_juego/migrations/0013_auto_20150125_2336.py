# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0012_auto_20150125_1229'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('sistema', models.IntegerField(null=True, db_index=True, editable=False)),
                ('data_origin', models.IntegerField(choices=[(6, 'Referencias'), (0, 'Preferencias'), (1, 'Deportes'), (7, 'Logros'), (2, 'Temporadas'), (5, 'Encuentros'), (4, 'Equipos'), (3, 'Jornadas')], editable=False)),
                ('pk_origin', models.IntegerField(editable=False)),
                ('data', jsonfield.fields.JSONField(editable=False)),
                ('in_production', models.BooleanField(editable=False, db_index=True, default=False)),
                ('date_production', models.DateTimeField(null=True, db_index=True, editable=False)),
            ],
            options={
                'verbose_name_plural': 'Actualizaciones',
                'verbose_name': 'Actualizacion',
            },
            bases=(models.Model,),
        ),
        migrations.AlterModelOptions(
            name='sistemajuegotiporegla',
            options={'verbose_name_plural': 'Reglas por sistema de juegos', 'ordering': ['tiporegla', 'rango_inicial'], 'verbose_name': 'Regla por sistema de juego'},
        ),
    ]
