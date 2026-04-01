# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0050_auto_20150918_1203'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='direccion',
            field=models.OneToOneField(to='admin_profiles.Direcciones', verbose_name='Direccion', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='direccion',
            field=models.OneToOneField(to='admin_profiles.Direcciones', verbose_name='Direccion', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='direccion',
            field=models.OneToOneField(to='admin_profiles.Direcciones', verbose_name='Direccion', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='operadora',
            field=models.ForeignKey(to='admin_comercializacion.Operadoras', verbose_name='Operadora', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='direccion',
            field=models.OneToOneField(to='admin_profiles.Direcciones', verbose_name='Direccion', blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='direccion',
            field=models.OneToOneField(to='admin_profiles.Direcciones', verbose_name='Direccion', blank=True, null=True),
            preserve_default=True,
        ),
    ]
