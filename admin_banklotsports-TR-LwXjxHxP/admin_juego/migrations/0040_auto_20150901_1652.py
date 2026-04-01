# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0039_auto_20150901_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condiciones',
            name='modalidad',
            field=models.ForeignKey(to='admin_juego.Modalidades'),
            preserve_default=True,
        ),
    ]
