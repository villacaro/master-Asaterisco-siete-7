# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0020_auto_20151106_1440'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='permissionssales',
            name='encuentro',
        ),
        migrations.RemoveField(
            model_name='permissionssales',
            name='torneo',
        ),
        migrations.AddField(
            model_name='permissionssales',
            name='breaking',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissionssales',
            name='comercializadora',
            field=models.ForeignKey(to='admin_finanzas.Comercializadora', verbose_name='Comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissionssales',
            name='deporte',
            field=models.ForeignKey(blank=True, null=True, editable=False, to='admin_juego.Deportes', verbose_name='Deporte'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissionssales',
            name='grupo',
            field=models.ForeignKey(blank=True, null=True, editable=False, to='admin_juego.GruposApuestas', verbose_name='Grupo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissionssales',
            name='modalidad',
            field=models.ForeignKey(blank=True, null=True, editable=False, to='admin_juego.Modalidades', verbose_name='Modalidad'),
            preserve_default=True,
        ),
    ]
