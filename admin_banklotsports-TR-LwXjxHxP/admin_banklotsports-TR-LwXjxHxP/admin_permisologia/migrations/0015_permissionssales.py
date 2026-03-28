# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0011_auto_20150814_0834'),
        ('admin_juego', '0035_sistemajuego_banner'),
        ('admin_permisologia', '0014_auto_20150617_0936'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionsSales',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializadora', models.ForeignKey(to='admin_finanzas.Comercializadora')),
                ('deporte', models.ForeignKey(null=True, editable=False, blank=True, to='admin_juego.Deportes')),
                ('encuentro', models.ForeignKey(null=True, editable=False, blank=True, to='admin_juego.Encuentros')),
                ('grupo', models.ForeignKey(null=True, editable=False, blank=True, to='admin_juego.GruposApuestas')),
                ('modalidad', models.ForeignKey(null=True, editable=False, blank=True, to='admin_juego.Modalidades')),
                ('torneo', models.ForeignKey(null=True, editable=False, blank=True, to='admin_juego.Torneos')),
            ],
            options={
                'verbose_name': 'Permiso Venta',
                'verbose_name_plural': 'Permisos ventas',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
    ]
