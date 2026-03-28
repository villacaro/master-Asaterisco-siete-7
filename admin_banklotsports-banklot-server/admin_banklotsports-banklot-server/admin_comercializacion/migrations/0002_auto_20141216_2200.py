# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='bancas',
            name='is_sistema_juego',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bloques',
            name='is_sistema_juego',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bancas',
            name='modelo_negocio',
            field=models.IntegerField(choices=[[1, 'Por porcentajes'], [2, 'Por alquiler']], verbose_name='Modelo de negocio (*)', default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bancas',
            name='permissions_create_user',
            field=models.BooleanField(verbose_name='¿Tiene permisos de crear usuarios de su mismo nivel? ', help_text='Seleccione este campo solo si desea que la banca pueda crear mas usuarios de banca', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='bloques',
            name='permissions_create_user',
            field=models.BooleanField(verbose_name='¿Tiene permisos de crear usuarios de su mismo nivel? ', help_text='Seleccione este campo solo si desea que la banca pueda crear mas usuarios de banca', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taquillas',
            name='modo_alquiler',
            field=models.BooleanField(verbose_name='¿Modo de alquiler activo? ', editable=False, help_text='si este campo esta activo, esta taquilla pasa a modo alquiler', default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='taquillas',
            name='monto_alquiler',
            field=models.DecimalField(help_text='Ingrese el monto por alquier de taquilla', default=0.0, decimal_places=5, max_digits=15, verbose_name='Monto de alquiler por taquilla (*)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuariostaquilla',
            name='last_login',
            field=models.DateTimeField(default=datetime.datetime(2014, 12, 16, 21, 55, 48, 236501), verbose_name='last login'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='usuariostaquilla',
            name='password',
            field=models.CharField(max_length=128, default='', verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='agencias',
            name='monto_alquiler',
            field=models.DecimalField(default=0.0, max_digits=15, decimal_places=5, help_text='Ingrese el monto por alquier de taquilla', verbose_name='Monto de alquiler por taquilla(*)'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datadefault',
            name='monto_alquiler',
            field=models.DecimalField(decimal_places=5, verbose_name='Monto de alquiler por taquilla(*)', max_digits=15, default=0.0, help_text='Ingrese el monto por alquier de taquilla'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agenciadatadefault',
            name='frecuencia_monto_alquiler',
            field=models.CharField(blank=True, max_length=30, verbose_name='Frecuencia de cobro de monto de alquiler (*)', null=True, choices=[['frecuencia_semanal', 'Alquiler semanal'], ['frecuencia_quincenal', 'Alquiler quincenal'], ['frecuencia_mensual', 'Alquiler mensual']], help_text='Seleccione la frecuencia de cobro de monto de alquiler'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agencias',
            name='frecuencia_monto_alquiler',
            field=models.CharField(blank=True, max_length=30, verbose_name='Frecuencia de cobro de monto de alquiler (*)', null=True, choices=[['frecuencia_semanal', 'Alquiler semanal'], ['frecuencia_quincenal', 'Alquiler quincenal'], ['frecuencia_mensual', 'Alquiler mensual']], help_text='Seleccione la frecuencia de cobro de monto de alquiler'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datadefault',
            name='frecuencia_monto_alquiler',
            field=models.CharField(blank=True, max_length=30, verbose_name='Frecuencia de cobro de monto de alquiler (*)', null=True, choices=[['frecuencia_semanal', 'Alquiler semanal'], ['frecuencia_quincenal', 'Alquiler quincenal'], ['frecuencia_mensual', 'Alquiler mensual']], help_text='Seleccione la frecuencia de cobro de monto de alquiler'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agenciadatadefault',
            name='factor_riesgo',
            field=models.IntegerField(choices=[[0, 'Activar factor de riesgo'], [1, 'Desactivar factor de riesgo']], default=0, verbose_name='Factor de riesgo (*)', help_text='Seleccione una opcion de factor de riesgo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='agencias',
            name='factor_riesgo',
            field=models.IntegerField(choices=[[0, 'Activar factor de riesgo'], [1, 'Desactivar factor de riesgo']], default=0, verbose_name='Factor de riesgo (*)', help_text='Seleccione una opcion de factor de riesgo'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='datadefault',
            name='factor_riesgo',
            field=models.IntegerField(choices=[[0, 'Activar factor de riesgo'], [1, 'Desactivar factor de riesgo']], default=0, verbose_name='Factor de riesgo (*)', help_text='Seleccione una opcion de factor de riesgo'),
            preserve_default=True,
        ),
    ]
