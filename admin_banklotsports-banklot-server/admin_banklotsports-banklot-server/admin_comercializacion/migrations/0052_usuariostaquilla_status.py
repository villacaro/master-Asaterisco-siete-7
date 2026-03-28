# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0009_auto_20150922_1258'),
        ('admin_comercializacion', '0051_auto_20150922_1544'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuariostaquilla',
            name='status',
            field=models.ForeignKey(null=True, to='admin_status.Status', verbose_name='Estatus (*)', editable=False),
            preserve_default=True,
        ),
    ]
