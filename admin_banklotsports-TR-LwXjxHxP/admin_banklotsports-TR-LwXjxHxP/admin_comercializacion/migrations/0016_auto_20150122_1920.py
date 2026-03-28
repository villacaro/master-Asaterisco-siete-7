# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0015_auto_20150122_1719'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='direccion_id',
            field=models.OneToOneField(blank=True, null=True, to='admin_profiles.Direcciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='status_id',
            field=models.ForeignKey(help_text='Seleccione el status deseado', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='direccion_id',
            field=models.OneToOneField(blank=True, null=True, to='admin_profiles.Direcciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='status_id',
            field=models.ForeignKey(help_text='Seleccione el status deseado', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='direccion_id',
            field=models.OneToOneField(blank=True, null=True, to='admin_profiles.Direcciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='status_id',
            field=models.ForeignKey(help_text='Seleccione el status deseado', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='direccion_id',
            field=models.OneToOneField(blank=True, null=True, to='admin_profiles.Direcciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='status_id',
            field=models.ForeignKey(help_text='Seleccione el status deseado', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='direccion_id',
            field=models.OneToOneField(blank=True, null=True, to='admin_profiles.Direcciones'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='status_id',
            field=models.ForeignKey(help_text='Seleccione el status deseado', verbose_name='Estatus (*)', to='admin_status.Status'),
            preserve_default=True,
        ),
    ]
