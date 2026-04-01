# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0037_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentrosmodalidades',
            name='origen',
            field=models.ForeignKey(null=True, to='admin_juego.EncuentrosModalidades'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='jugadasinformativas',
            name='origen',
            field=models.ForeignKey(null=True, to='admin_juego.JugadasInformativas'),
            preserve_default=True,
        ),
    ]
