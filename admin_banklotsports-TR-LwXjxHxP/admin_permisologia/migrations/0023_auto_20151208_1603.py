# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0022_auto_20151208_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissionssalesrestrictions',
            name='comercializadora',
            field=models.ForeignKey(verbose_name='Comercializadora', to='admin_finanzas.Comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissionssalesrestrictions',
            name='deporte',
            field=models.ForeignKey(verbose_name='Deporte', to='admin_juego.Deportes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissionssalesrestrictions',
            name='restrictions',
            field=jsonfield.fields.JSONField(verbose_name='Restricciones', blank=True, null=True),
            preserve_default=True,
        ),
    ]
