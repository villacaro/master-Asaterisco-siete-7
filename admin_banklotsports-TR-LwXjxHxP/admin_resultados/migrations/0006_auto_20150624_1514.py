# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0005_anotacionesdetail_referencia'),
    ]

    operations = [
        migrations.AlterField(
            model_name='resultados',
            name='encuentro',
            field=models.ForeignKey(to='admin_juego.Encuentros'),
            preserve_default=True,
        ),
    ]
