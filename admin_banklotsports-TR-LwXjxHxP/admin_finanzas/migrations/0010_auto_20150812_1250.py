# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0009_auto_20150728_2346'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('tipo', models.CharField(max_length=2, choices=[('pc', 'Por cobrar'), ('pp', 'Por pagar')])),
                ('min', models.IntegerField(default=0)),
                ('max', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializadora', models.ForeignKey(editable=False, to='admin_finanzas.Comercializadora')),
            ],
            options={
                'verbose_name_plural': 'Configuraciones de las comercializadoras',
                'verbose_name': 'Configuracion comercializadora',
                'db_tablespace': 'ts_finance',
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='configuracion',
            unique_together=set([('comercializadora', 'tipo')]),
        ),
    ]
