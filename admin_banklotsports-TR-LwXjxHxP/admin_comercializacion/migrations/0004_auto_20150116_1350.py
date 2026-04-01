# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0003_auto_20141216_2201'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='agenciadatadefault',
            options={'verbose_name_plural': 'Data por defecto de las agencias', 'verbose_name': 'Data por defecto de una agencias', 'ordering': ['created_at']},
        ),
        migrations.AlterModelOptions(
            name='datadefault',
            options={'verbose_name_plural': 'Data por defecto para las comercializadoras', 'verbose_name': 'Data por defecto por comercializadora', 'ordering': ['user_type']},
        ),
        migrations.AlterModelOptions(
            name='taquilladatadefault',
            options={'verbose_name_plural': 'Data por defecto de las taquillas', 'verbose_name': 'Data por defecto de una taquilla', 'ordering': ['user_name']},
        ),
        migrations.AlterModelOptions(
            name='ticketsdatadefault',
            options={'verbose_name_plural': 'Data por defecto para la impresion de los tickets', 'verbose_name': 'Data por defecto para impresion de un ticket', 'ordering': ['titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3']},
        ),
        migrations.RemoveField(
            model_name='datadefault',
            name='dias',
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='cantidad_apuesta_max',
            field=models.IntegerField(verbose_name='Cantidad maxima de apuesta (*)', help_text='Ingrese la cantidad maxima de apuestas por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='cantidad_apuesta_min',
            field=models.IntegerField(verbose_name='Cantidad minima de apuesta (*)', help_text='Ingrese la cantidad minima de apuestas por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='everyone',
            field=models.BooleanField(verbose_name='¿Para todos? ', default=False, help_text='En caso de estar activada esta opcion todas las agencias aplicaran esta configuracion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='montomax',
            field=models.DecimalField(verbose_name='Monto maximo (*)', max_digits=15, decimal_places=2, help_text='Ingrese el monto maximo por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='montomax_ganancia',
            field=models.DecimalField(verbose_name='Monto maximo ganancia (*)', max_digits=15, decimal_places=2, help_text='Ingrese el monto maximo de ganancia por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='montomin',
            field=models.DecimalField(verbose_name='Monto minimo (*)', max_digits=15, decimal_places=2, help_text='Ingrese el monto minimo por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='parley_clonados_maxima_ganancia',
            field=models.DecimalField(verbose_name='Parley: cantidad maxima de ganancia para tickets clonados (*)', max_digits=15, decimal_places=2, help_text='Ingrese la cantidad maxima de ganancia para tickets clonados'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='parley_hembras_max',
            field=models.IntegerField(verbose_name='Parley: cantidad maxima de hembras (*)', help_text='Ingrese la cantidad maxima de hembras por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='parley_hembras_min',
            field=models.IntegerField(verbose_name='Parley: cantidad minima de hembras (*)', help_text='Ingrese la cantidad minima de hembras por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='parley_machos_max',
            field=models.IntegerField(verbose_name='Parley: cantidad maxima de machos (*)', help_text='Ingrese la cantidad maxima de machos por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='parley_machos_min',
            field=models.IntegerField(verbose_name='Parley: cantidad minima de machos (*)', help_text='Ingrese la cantidad minima de machos por ticket'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agenciadatadefault',
            name='tiempoexpiracion',
            field=models.IntegerField(verbose_name='Tiempo de expiracion (*)', help_text='Ingrese el tiempo de expiracion de los tickets en dias, ejemplo: 2 = 2 dias'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='cupo',
            field=models.DecimalField(verbose_name='Cupo de venta (*)', max_digits=15, decimal_places=5, help_text='Ingrese el cupo maximo de venta diaria por tipo comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='porcentaje_comision',
            field=models.DecimalField(decimal_places=5, verbose_name='Porcentaje de comision (*)', max_digits=15, default=0.0, help_text='Ingrese el porcentaje de comision por tipo de comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='porcentaje_maximo',
            field=models.DecimalField(decimal_places=5, verbose_name='Porcentaje de maximo (*)', max_digits=15, default=0.0, help_text='Ingrese el porcentaje de maximo por tipo de comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='porcentaje_participacion',
            field=models.DecimalField(decimal_places=5, verbose_name='Porcentaje de participacion (*)', max_digits=15, default=0.0, help_text='Ingrese el porcentaje de participacion por tipo de comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='porcentaje_regalia',
            field=models.DecimalField(decimal_places=5, verbose_name='Porcentaje de regalia (*)', max_digits=15, default=0.0, help_text='Ingrese el porcentaje de regalia por tipo de comercializadora'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='datadefault',
            name='user_type',
            field=models.ForeignKey(verbose_name='Tipo de comercializadora (*)', to='admin_users.UserProfile', help_text='Seleccione el tipo de comercializadora a la cual pertenece la data', unique=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquilladatadefault',
            name='passwd',
            field=models.CharField(verbose_name='Contraseña (*)', max_length=160, help_text='Ingrese la contrasela por defecto para las taquillas'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquilladatadefault',
            name='user_name',
            field=models.CharField(verbose_name='Prefijo de usuario (*)', max_length=160, help_text='Ingrese el prefijo de usuarios por defecto para las taquillas'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='everyone',
            field=models.BooleanField(verbose_name='¿Para todos? (*)', default=False, help_text='En caso de estar activada esta opcion todas los tickets se imprimiran con esta configuracion'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='pie1',
            field=models.CharField(verbose_name='Primer pie de pagina (*)', max_length=160, help_text='Ingrese el primer pie de pagina para impresion de tickets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='pie2',
            field=models.CharField(verbose_name='Segundo pie de pagina ', null=True, blank=True, max_length=160, help_text='Ingrese el segundo pie de pagina para impresion de tickets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='pie3',
            field=models.CharField(verbose_name='Tercer pie de pagina ', null=True, blank=True, max_length=160, help_text='Ingrese el tercer pie de pagina para impresion de tickets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='titulo1',
            field=models.CharField(verbose_name='Primer titulo de pagina (*)', max_length=160, help_text='Ingrese el primer titulo de pagina para impresion de tickets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='titulo2',
            field=models.CharField(verbose_name='Segundo titulo de pagina ', null=True, blank=True, max_length=160, help_text='Ingrese el segundo titulo de pagina para impresion de tickets'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdatadefault',
            name='titulo3',
            field=models.CharField(verbose_name='Tercer titulo de pagina ', null=True, blank=True, max_length=160, help_text='Ingrese el tercer titulo de pagina para impresion de tickets'),
            preserve_default=True,
        ),
    ]