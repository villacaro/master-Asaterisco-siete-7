# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0035_sistemajuego_banner'),
        ('admin_resultados', '0007_auto_20150624_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='ResultadosRestric',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('grupo', models.ForeignKey(to='admin_juego.GruposApuestas')),
                ('modalidad', models.ForeignKey(to='admin_juego.Modalidades')),
                ('resultado', models.ForeignKey(to='admin_resultados.Resultados')),
            ],
            options={
                'verbose_name_plural': 'Restricciones de resultados',
                'verbose_name': 'Restriccion de resultado',
                'db_tablespace': 'ts_parley',
            },
            bases=(models.Model,),
        ),
    ]
