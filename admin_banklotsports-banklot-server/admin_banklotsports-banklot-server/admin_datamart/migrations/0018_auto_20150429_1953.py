# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0017_hecho2_ventascadenaslinea'),
    ]

    operations = [
        migrations.AddField(
            model_name='hecho5_comisionescadena',
            name='queda',
            field=models.DecimalField(default=0, null=True, decimal_places=8, max_digits=15),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hecho5_comisionescadena',
            name='queda_down',
            field=models.DecimalField(default=0, null=True, decimal_places=8, max_digits=15),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hecho6_comisionescadenajuego',
            name='queda',
            field=models.DecimalField(default=0, null=True, decimal_places=8, max_digits=15),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='hecho6_comisionescadenajuego',
            name='queda_down',
            field=models.DecimalField(default=0, null=True, decimal_places=8, max_digits=15),
            preserve_default=True,
        ),
    ]
