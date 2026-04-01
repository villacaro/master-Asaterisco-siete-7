# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0034_sistemajuego_is_resultados'),
        ('admin_resultados', '0006_auto_20150624_1514'),
    ]

    operations = [
        migrations.AddField(
            model_name='resultados',
            name='sistema',
            field=models.ForeignKey(null=True, to='admin_juego.SistemaJuego'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='resultados',
            unique_together=set([('encuentro', 'sistema')]),
        ),
    ]
