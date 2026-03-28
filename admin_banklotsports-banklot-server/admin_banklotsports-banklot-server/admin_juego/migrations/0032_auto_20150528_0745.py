# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0031_jornadas_monto_inicial'),
    ]

    operations = [
        migrations.AddField(
            model_name='gruposjuego',
            name='orden',
            field=models.IntegerField(help_text='Ingrese la numeración de orden', default=0, verbose_name='Orden (*)'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jornadas',
            name='valor',
            field=models.IntegerField(help_text='Ingrese la cantidad del valor en Bs, este campo solo sera util, para las jornadas de quiniela.', default=0, verbose_name='Valor por ticket Bs'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jornadas',
            name='monto_inicial',
            field=models.IntegerField(help_text='Ingrese la cantidad de monto inicial, este campo solo sera util, para las jornadas de quiniela.', default=0, verbose_name='Monto inicial Bs'),
            preserve_default=True,
        ),
    ]
