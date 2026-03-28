# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0005_auto_20150116_1457'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='operadoras',
            options={'verbose_name_plural': 'Data por defecto para las comercializadoras', 'ordering': ['nombre'], 'verbose_name': 'Data por defecto por comercializadora'},
        ),
        migrations.AlterModelOptions(
            name='tipoporcentajes',
            options={'verbose_name_plural': 'Tipos de porcentajes', 'ordering': ['nombre'], 'verbose_name': 'Tipo de porcentaje'},
        ),
        migrations.AlterModelOptions(
            name='tipopreferencias',
            options={'verbose_name_plural': 'Tipos de preferencias', 'ordering': ['nombre'], 'verbose_name': 'Tipo de preferencia'},
        ),
        
        migrations.AlterField(
            model_name='preferencias',
            name='defecto',
            field=models.BooleanField(default=False, help_text='Seleccione solo si esta es la preferecnia por defecto, para el tipo de preferencia asociada y la comercialzadora.', verbose_name='¿Por defecto?'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='preferencias',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo de preferencia (*)', to='admin_comercializacion.TipoPreferencias', help_text='Seleccione el tipo de preferencia a la cual pertenece la data'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='preferencias',
            name='user_type',
            field=models.ForeignKey(verbose_name='Tipo de comercializadora (*)', to='admin_users.UserProfile', help_text='Seleccione el tipo de comercializadora a la cual pertenece la data'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='preferencias',
            name='valor',
            field=models.CharField(max_length=100, help_text='Ingrese el valor de la data', verbose_name='Valor (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='agencia',
            field=models.BooleanField(default=False, help_text='Seleccione solo en caso de que el porcentaje sea por agencia', verbose_name='¿Tipo de porcentaje por agencia? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='banca',
            field=models.BooleanField(default=False, help_text='Seleccione solo en caso de que el porcentaje sea por banca', verbose_name='¿Tipo de porcentaje por banca? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='bloque',
            field=models.BooleanField(default=False, help_text='Seleccione solo en caso de que el porcentaje sea por bloque', verbose_name='¿Tipo de porcentaje por bloque? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='codename',
            field=models.CharField(max_length=100, help_text='Ingrese el codename del tipo de porcentaje', verbose_name='Codename (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='distribuidor',
            field=models.BooleanField(default=False, help_text='Seleccione solo en caso de que el porcentaje sea por distribuidor', verbose_name='¿Tipo de porcentaje por distribuidor? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese el nombre del tipo de porcentaje', verbose_name='Nombre (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='orden',
            field=models.IntegerField(default=0, help_text='Ingrese el orden del tipo de porcentaje', verbose_name='Orden (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipoporcentajes',
            name='taquilla',
            field=models.BooleanField(default=False, help_text='Seleccione solo en caso de que el porcentaje sea por taquilla', verbose_name='¿Tipo de porcentaje por taquilla? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipopreferencias',
            name='codename',
            field=models.CharField(max_length=100, help_text='Ingrese el codename para el tipo de preferencia', verbose_name='Codename (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipopreferencias',
            name='comparacion',
            field=models.IntegerField(choices=[[1, 'Menor'], [2, 'Mayor'], [3, 'Libre']], help_text='Seleccione la compraracion de nivel', verbose_name='Compraracion nivel (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tipopreferencias',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese el nombre para el tipo de preferencia', verbose_name='Nombre (*)'),
            preserve_default=True,
        ),
    ]