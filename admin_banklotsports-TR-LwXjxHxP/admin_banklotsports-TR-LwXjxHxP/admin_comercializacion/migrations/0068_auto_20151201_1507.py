# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0067_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='agencias',
            name='direccion',
            field=models.OneToOneField(blank=True, verbose_name='Dirección', to='admin_profiles.Direcciones', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico ', help_text='Ingrese el correo electrónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='factor_riesgo',
            field=models.IntegerField(default=1, choices=[[1, 'Activado'], [0, 'Desactivado']], null=True, verbose_name='Factor de riesgo (*)', help_text='Seleccione una opcion de factor de riesgo'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='status',
            field=models.ForeignKey(help_text='Seleccione el estatus deseado', to='admin_status.Status', verbose_name='Estatus (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='agencias',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Número Telefónico ', help_text='Ingrese el número telefónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='direccion',
            field=models.OneToOneField(blank=True, verbose_name='Dirección', to='admin_profiles.Direcciones', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico ', help_text='Ingrese el correo electrónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='status',
            field=models.ForeignKey(help_text='Seleccione el estatus deseado', to='admin_status.Status', verbose_name='Estatus (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bancas',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Número Telefónico ', help_text='Ingrese el número telefónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='direccion',
            field=models.OneToOneField(blank=True, verbose_name='Dirección', to='admin_profiles.Direcciones', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico ', help_text='Ingrese el correo electrónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='status',
            field=models.ForeignKey(help_text='Seleccione el estatus deseado', to='admin_status.Status', verbose_name='Estatus (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='bloques',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Número Telefónico ', help_text='Ingrese el número telefónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='direccion',
            field=models.OneToOneField(blank=True, verbose_name='Dirección', to='admin_profiles.Direcciones', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico ', help_text='Ingrese el correo electrónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='status',
            field=models.ForeignKey(help_text='Seleccione el estatus deseado', to='admin_status.Status', verbose_name='Estatus (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='distribuidores',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Número Telefónico ', help_text='Ingrese el número telefónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='direccion',
            field=models.OneToOneField(blank=True, verbose_name='Dirección', to='admin_profiles.Direcciones', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo electrónico ', help_text='Ingrese el correo electrónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='status',
            field=models.ForeignKey(help_text='Seleccione el estatus deseado', to='admin_status.Status', verbose_name='Estatus (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='operadoras',
            name='telefono',
            field=models.CharField(blank=True, max_length=12, null=True, verbose_name='Número Telefónico ', help_text='Ingrese el número telefónico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='agencia',
            field=models.ForeignKey(blank=True, verbose_name='Agencia', to='admin_comercializacion.Agencias', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='agencia_porc',
            field=models.DecimalField(max_digits=15, verbose_name='Agencia porcentaje', default=None, decimal_places=4, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='banca',
            field=models.ForeignKey(blank=True, verbose_name='Banca', to='admin_comercializacion.Bancas', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='banca_porc',
            field=models.DecimalField(max_digits=15, verbose_name='Banca porcentaje', default=None, decimal_places=4, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='bloque',
            field=models.ForeignKey(blank=True, verbose_name='Multi Banca', to='admin_comercializacion.Bloques', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='bloque_porc',
            field=models.DecimalField(max_digits=15, verbose_name='Bloque porcentaje', default=None, decimal_places=4, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='distribuidor',
            field=models.ForeignKey(blank=True, verbose_name='Distribuidor', to='admin_comercializacion.Distribuidores', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='distribuidor_porc',
            field=models.DecimalField(max_digits=15, verbose_name='Distribuidor porcentaje', default=None, decimal_places=4, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='operadora',
            field=models.ForeignKey(blank=True, verbose_name='Operadora', to='admin_comercializacion.Operadoras', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='porcentaje_ganancia',
            field=models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Porcentaje ganancia '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='porcentaje_maximo',
            field=models.DecimalField(max_digits=15, decimal_places=4, verbose_name='Porcentaje máximo '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='relacion',
            field=models.BooleanField(default=True, verbose_name='Relación '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='taquilla',
            field=models.ForeignKey(blank=True, verbose_name='Taquilla', to='admin_comercializacion.Taquillas', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='taquilla_porc',
            field=models.DecimalField(max_digits=15, verbose_name='Taquilla porcentaje', default=None, decimal_places=4, blank=True, null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='porcentajes',
            name='tipo',
            field=models.ForeignKey(verbose_name='Tipo de porcentaje ', to='admin_comercializacion.TipoPorcentajes'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='taquilladatadefault',
            name='passwd',
            field=models.CharField(max_length=160, verbose_name='Contraseña (*)', help_text='Ingrese la contraseña por defecto para las taquillas'),
            preserve_default=True,
        ),
    ]
