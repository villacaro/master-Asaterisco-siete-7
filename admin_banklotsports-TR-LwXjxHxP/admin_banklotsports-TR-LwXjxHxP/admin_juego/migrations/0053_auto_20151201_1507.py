# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0052_auto_20151104_1738'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='encuentros',
            options={'ordering': ('horajuego',), 'verbose_name_plural': 'Encuentros', 'verbose_name': 'Encuentro'},
        ),
        migrations.AlterField(
            model_name='encuentrosmodalidades',
            name='etiqueta_ref',
            field=models.CharField(blank=True, max_length=140, null=True, verbose_name='Referencia'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipos',
            name='logo',
            field=models.ImageField(blank=True, upload_to='equipos', null=True, verbose_name='Logo '),
            preserve_default=True,
        ),
    ]
