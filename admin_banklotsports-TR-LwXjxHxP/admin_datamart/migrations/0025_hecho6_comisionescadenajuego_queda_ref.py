# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0024_dimensionjuegosnew_hecho8_ventasmonitorlinea'),
    ]

    operations = [
        migrations.AddField(
            model_name='hecho6_comisionescadenajuego',
            name='queda_ref',
            field=models.DecimalField(default=0, decimal_places=8, null=True, max_digits=15),
            preserve_default=True,
        ),
    ]
