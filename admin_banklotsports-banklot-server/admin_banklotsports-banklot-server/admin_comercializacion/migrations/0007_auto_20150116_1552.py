# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0006_auto_20150116_1524'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operadoras',
            options={'verbose_name_plural': 'Operadora', 'verbose_name': 'Operadora'},
        ),
        migrations.AlterModelOptions(
            name='preferencias',
            options={'verbose_name_plural': 'Tipos de preferencias', 'ordering': ['user_type', 'tipo'], 'verbose_name': 'Tipo de preferencia'},
        ),
        migrations.AlterField(
            model_name='bloques',
            name='email',
            field=models.EmailField(help_text='Ingrese el correo electronico', max_length=254, null=True, blank=True, verbose_name='Correo electronico ', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='nombre',
            field=models.CharField(help_text='Ingrese nombre de la operadora', max_length=100, null=True, blank=True, verbose_name='Nombre ', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='rif',
            field=models.CharField(help_text='Ingrese el rif de la operadora', max_length=15, null=True, blank=True, verbose_name='Rif '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='telefono',
            field=models.CharField(help_text='Ingrese el telefono de la operadora', max_length=12, null=True, blank=True, verbose_name='Número Telefonico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='nombre',
            field=models.CharField(help_text='Ingrese nombre de la operadora', max_length=100, null=True, blank=True, verbose_name='Nombre ',unique=True),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='operadoras',
            unique_together=set([('nombre',)]),
        ),
    ]