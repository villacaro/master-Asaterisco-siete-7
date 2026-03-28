# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0047_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='encuentros',
            name='updated_at_logros',
            field=models.DateTimeField(verbose_name='Actualizacion de logros', auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='favorito',
            field=models.NullBooleanField(verbose_name='Favorito'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='indice',
            field=models.IntegerField(verbose_name='Indices', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='status',
            field=models.ForeignKey(blank=True, verbose_name='Status', null=True, to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='valor_americano',
            field=models.IntegerField(verbose_name='Logro americano', null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='valor_etq_ref',
            field=models.CharField(verbose_name='Etiqueta referencia', null=True, max_length=140, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='valor_europeo',
            field=models.DecimalField(verbose_name='Logro europeo', decimal_places=2, null=True, blank=True, max_digits=10),
            preserve_default=True,
        ),
    ]
