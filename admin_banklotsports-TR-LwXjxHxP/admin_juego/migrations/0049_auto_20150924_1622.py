# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0048_auto_20150922_2219'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jornadas',
            name='fechafin',
            field=models.DateField(help_text='Fecha de fin de la jornada', verbose_name='Fecha de fin (*)', db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='temporadas',
            name='fechafin',
            field=models.DateField(help_text='Seleccione la fecha de fin de la temporada', verbose_name='Fecha de fin (*)', db_index=True),
            preserve_default=True,
        ),
    ]
