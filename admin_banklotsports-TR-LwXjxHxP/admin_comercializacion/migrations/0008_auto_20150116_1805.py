# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0007_auto_20150116_1552'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agencias',
            options={'verbose_name_plural': 'Agencias', 'verbose_name': 'Agencia'},
        ),
        migrations.AlterModelOptions(
            name='bancas',
            options={'verbose_name_plural': 'Bancas', 'verbose_name': 'Banca'},
        ),
        migrations.AlterModelOptions(
            name='bloques',
            options={'verbose_name_plural': 'Bloques', 'verbose_name': 'Bloque'},
        ),
        migrations.AlterModelOptions(
            name='cupos',
            options={'verbose_name_plural': 'Cupos de las comercializadoras', 'ordering': ['-fecha_inicio'], 'verbose_name': 'Cupo de una comercializadora'},
        ),
        migrations.AlterModelOptions(
            name='distribuidores',
            options={'verbose_name_plural': 'Distribuidores', 'verbose_name': 'Distribuidor'},
        ),
        migrations.AlterModelOptions(
            name='porcentajes',
            options={'verbose_name_plural': 'Porcentajes de las comercializadoras', 'ordering': ['-fecha_inicio'], 'verbose_name': 'Porcentaje de una comercializadora'},
        ),
        migrations.AlterModelOptions(
            name='preferencias',
            options={'verbose_name_plural': 'Preferencias de las comercializadoras', 'ordering': ['user_type', 'tipo'], 'verbose_name': 'Preferencia de comercialzadora'},
        ),
        migrations.AlterModelOptions(
            name='preferenciascadena',
            options={'verbose_name_plural': 'Valor de preferencias de las comercializadoras', 'ordering': ['-created_at'], 'verbose_name': 'Valor de preferencia de una comercializadora'},
        ),
        migrations.AlterModelOptions(
            name='taquillas',
            options={'verbose_name_plural': 'Taquillas', 'verbose_name': 'Taquilla'},
        ),
        migrations.AlterModelOptions(
            name='usuariostaquilla',
            options={'verbose_name_plural': 'Usuarios de taquillas', 'verbose_name': 'Usuario de taquilla'},
        ),
        
        migrations.AlterField(
            model_name='agencias',
            name='email',
            field=models.EmailField(blank=True, help_text='Ingrese el correo electronico', max_length=254, null=True, unique=True, verbose_name='Correo electronico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='monto_alquiler',
            field=models.DecimalField(blank=True, help_text='Ingrese el monto por alquier de taquilla', decimal_places=5, max_digits=15, default=None, null=True, verbose_name='Monto de alquiler por taquilla (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='montomax',
            field=models.DecimalField(help_text='Seleccione el monto máximo de apuesta', decimal_places=2, max_digits=15, verbose_name='Monto máximo de apuesta '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='montomin',
            field=models.DecimalField(help_text='Seleccione el monto mínimo de apuesta', decimal_places=2, max_digits=15, verbose_name='Monto mínimo de apuesta '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese nombre de la operadora', default='', verbose_name='Nombre (*)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='rif',
            field=models.CharField(max_length=15, blank=True, help_text='Ingrese el rif', null=True, verbose_name='Rif '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='telefono',
            field=models.CharField(max_length=12, blank=True, help_text='Ingrese el número telefico', null=True, verbose_name='Número Telefonico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='email',
            field=models.EmailField(blank=True, help_text='Ingrese el correo electronico', max_length=254, null=True, unique=True, verbose_name='Correo electronico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='is_sistema_juego',
            field=models.BooleanField(help_text='Seleccione este campo solo si desea que la banca tenga su propio sistema de juego', default=False, verbose_name='¿Posee un sistema de juego? '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='modelo_negocio',
            field=models.IntegerField(choices=[[1, 'Por porcentajes'], [2, 'Por alquiler']], help_text='Seleccione el modelo de negocio', default=1, verbose_name='Modelo de negocio (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese nombre de la operadora', default='', verbose_name='Nombre (*)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='rif',
            field=models.CharField(max_length=15, blank=True, help_text='Ingrese el rif', null=True, verbose_name='Rif '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='telefono',
            field=models.CharField(max_length=12, blank=True, help_text='Ingrese el número telefico', null=True, verbose_name='Número Telefonico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese nombre de la operadora', default='', verbose_name='Nombre (*)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='rif',
            field=models.CharField(max_length=15, blank=True, help_text='Ingrese el rif', null=True, verbose_name='Rif '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='telefono',
            field=models.CharField(max_length=12, blank=True, help_text='Ingrese el número telefico', null=True, verbose_name='Número Telefonico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='agencia',
            field=models.ForeignKey(blank=True, help_text='Seleccione la agencia', to='admin_comercializacion.Agencias', null=True, verbose_name='Agencia '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='banca',
            field=models.ForeignKey(blank=True, help_text='Seleccione la Banca', to='admin_comercializacion.Bancas', null=True, verbose_name='Banca '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='bloque',
            field=models.ForeignKey(blank=True, help_text='Seleccione el bloque', to='admin_comercializacion.Bloques', null=True, verbose_name='Bloque '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='distribuidor',
            field=models.ForeignKey(blank=True, help_text='Seleccione el distribuidor', to='admin_comercializacion.Distribuidores', null=True, verbose_name='Distribuidor '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='fecha_fin',
            field=models.DateTimeField(blank=True, help_text='Ingrese la fecha de fin ', null=True, verbose_name='Fecha de fin '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='fecha_inicio',
            field=models.DateTimeField(help_text='Ingrese la fecha de inicio ', verbose_name='Fecha de inicio (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='monto_diario',
            field=models.DecimalField(help_text='Ingrese el monto diario ', decimal_places=2, max_digits=15, verbose_name='Monto diario de venta (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='cupos',
            name='operadora',
            field=models.ForeignKey(blank=True, help_text='Seleccione la operadora', to='admin_comercializacion.Operadoras', null=True, verbose_name='Operadora '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='email',
            field=models.EmailField(blank=True, help_text='Ingrese el correo electronico', max_length=254, null=True, unique=True, verbose_name='Correo electronico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese nombre de la operadora', default='', verbose_name='Nombre (*)'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='rif',
            field=models.CharField(max_length=15, blank=True, help_text='Ingrese el rif', null=True, verbose_name='Rif '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='telefono',
            field=models.CharField(max_length=12, blank=True, help_text='Ingrese el número telefico', null=True, verbose_name='Número Telefonico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='nombre',
            field=models.CharField(max_length=100, help_text='Ingrese nombre de la operadora', default='', verbose_name='Nombre (*)',),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='rif',
            field=models.CharField(max_length=15, blank=True, help_text='Ingrese el rif', null=True, verbose_name='Rif '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='telefono',
            field=models.CharField(max_length=12, blank=True, help_text='Ingrese el número telefico', null=True, verbose_name='Número Telefonico '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='fecha_fin',
            field=models.DateTimeField(blank=True, help_text='Ingrese la fecha de fin ', null=True, verbose_name='Fecha de fin '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='fecha_inicio',
            field=models.DateTimeField(help_text='Ingrese la fecha de inicio ', verbose_name='Fecha de inicio (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillas',
            name='serial',
            field=models.CharField(max_length=200, blank=True, help_text='Ingrese el serial de la taquilla', null=True, verbose_name='Serial (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquillas',
            name='taquilla',
            field=models.CharField(max_length=100, help_text='Ingrese el nombre de la taquilla', verbose_name='Nombre de la taquilla (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariostaquilla',
            name='nombre',
            field=models.CharField(max_length=200, blank=True, help_text='Ingrese un nombre para el usuario', null=True, verbose_name='Nombre (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariostaquilla',
            name='taquilla',
            field=models.OneToOneField(help_text='Ingrese la taquilla ', to='admin_comercializacion.Taquillas', verbose_name='Taquilla (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usuariostaquilla',
            name='user',
            field=models.CharField(max_length=200, help_text='Ingrese un usuario', verbose_name='Usuario (*)'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='taquillas',
            unique_together=set([('taquilla', 'agencia')]),
        ),
        migrations.AlterUniqueTogether(
            name='usuariostaquilla',
            unique_together=set([('user', 'taquilla')]),
        ),
    ]