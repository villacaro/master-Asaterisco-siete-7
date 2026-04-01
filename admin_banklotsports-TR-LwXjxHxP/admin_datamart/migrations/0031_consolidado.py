# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0030_auto_20151103_0040'),
    ]

    operations = [
        migrations.CreateModel(
            name='Consolidado',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('id_sorteo', models.IntegerField()),
                ('id_lista', models.IntegerField()),
                ('id_tipo_lista', models.IntegerField()),
                ('id_prestador_servicio', models.IntegerField()),
                ('id_comercializador', models.IntegerField()),
                ('id_banca', models.IntegerField()),
                ('id_distribuidor', models.IntegerField()),
                ('id_agencia', models.IntegerField()),
                ('id_taquilla', models.IntegerField()),
                ('id_operador', models.IntegerField()),
                ('nporcentaje_comision_com', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_participacion_com', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_regalia_com', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_comision_ban', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_participacion_ban', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_regalia_ban', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_comision_dis', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_participacion_dis', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_regalia_dis', models.DecimalField(decimal_places=2, max_digits=5)),
                ('nporcentaje_comision_agc', models.DecimalField(decimal_places=2, max_digits=5)),
                ('mmonto_venta', models.DecimalField(decimal_places=2, max_digits=13)),
                ('mmonto_venta_externa', models.DecimalField(decimal_places=2, max_digits=13)),
                ('mmonto_venta_ganador', models.DecimalField(decimal_places=2, max_digits=13)),
                ('mmonto_premios', models.DecimalField(decimal_places=2, max_digits=13)),
                ('mmonto_comision_com', models.DecimalField(decimal_places=16, max_digits=30)),
                ('mmonto_regalia_com', models.DecimalField(decimal_places=16, max_digits=30)),
                ('mmonto_comision_ban', models.DecimalField(decimal_places=16, max_digits=30)),
                ('mmonto_regalia_ban', models.DecimalField(decimal_places=16, max_digits=30)),
                ('mmonto_comision_dis', models.DecimalField(decimal_places=16, max_digits=30)),
                ('mmonto_regalia_dis', models.DecimalField(decimal_places=16, max_digits=30)),
                ('mmonto_comision_agc', models.DecimalField(decimal_places=16, max_digits=30)),
                ('msaldo_oper', models.DecimalField(decimal_places=16, max_digits=30)),
                ('msaldo_com', models.DecimalField(decimal_places=16, max_digits=30)),
                ('msaldo_ban', models.DecimalField(decimal_places=16, max_digits=30)),
                ('msaldo_dis', models.DecimalField(decimal_places=16, max_digits=30)),
                ('msaldo_agc', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_bruto_com', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_bruto_ban', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_bruto_dis', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_oper_ban', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_oper_dis', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_oper_cm', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('msaldo_cm', models.DecimalField(null=True, max_digits=30, decimal_places=16)),
                ('tserial_ifa', models.CharField(max_length=50)),
                ('id_perfil_pago_premios', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Consolidado',
                'verbose_name_plural': 'Consolidado',
                'db_tablespace': 'ts_finance',
            },
        ),
    ]
