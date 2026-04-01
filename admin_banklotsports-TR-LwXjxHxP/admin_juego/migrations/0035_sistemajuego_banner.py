# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0034_sistemajuego_is_resultados'),
    ]

    operations = [
        migrations.AddField(
            model_name='sistemajuego',
            name='banner',
            field=models.ImageField(blank=True, null=True, upload_to='sistema'),
            preserve_default=True,
        ),
    ]
