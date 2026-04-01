# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0019_auto_20150511_1004'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hecho7_ComisionesQuedaCadena',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, primary_key=True, verbose_name='ID')),
                ('queda_agencia', models.DecimalField(null=True, max_digits=15, default=0, decimal_places=8)),
                ('queda_distribuidor', models.DecimalField(null=True, max_digits=15, default=0, decimal_places=8)),
                ('queda_banca', models.DecimalField(null=True, max_digits=15, default=0, decimal_places=8)),
                ('queda_bloque', models.DecimalField(null=True, max_digits=15, default=0, decimal_places=8)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializacion', models.ForeignKey(to='admin_datamart.DimensionComercializacion')),
                ('tiempo', models.ForeignKey(to='admin_datamart.DimensionTiempo')),
            ],
            options={
                'verbose_name_plural': 'Hecho 7: Comisiones de la queda por toda la cadena',
                'db_tablespace': 'ts_finance',
                'verbose_name': 'Hecho 7: Comisiones de la queda',
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='hecho5_comisionescadena',
            name='queda_ref',
            field=models.DecimalField(null=True, max_digits=15, default=0, decimal_places=8),
            preserve_default=True,
        ),
    ]
