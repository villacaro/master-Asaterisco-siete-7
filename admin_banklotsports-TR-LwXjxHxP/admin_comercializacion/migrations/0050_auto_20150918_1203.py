# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0049_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='eventnotificationcadena',
            name='data_origin',
            field=models.IntegerField(choices=[(1, 'Preferencias'), (2, 'Factor de riesgo'), (3, 'Mensajes'), (4, 'Permiso de venta')], editable=False),
            preserve_default=True,
        ),
    ]
