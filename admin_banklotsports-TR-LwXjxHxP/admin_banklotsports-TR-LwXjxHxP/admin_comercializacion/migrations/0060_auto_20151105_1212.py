# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_finanzas', '0013_comercializadora_resumen_personalizado_comer'),
        ('admin_users', '0029_auto_20150920_2016'),
        ('admin_comercializacion', '0059_merge'),
    ]

    operations = [
        migrations.CreateModel(
            name='DefaultPreferences',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=100, verbose_name='Valor (*)', help_text='Ingrese el valor de la data')),
                ('default', models.BooleanField(verbose_name='¿Por defecto?', default=False, help_text='Seleccione solo si esta es la preferecnia por defecto, para el tipo de preferencia asociada y la comercialzadora.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name': 'Preferencia por defecto',
                'verbose_name_plural': 'Preferencias por defecto',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='GroupPreferences',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre (*)', help_text='Ingrese el nombre para el grupo de preferencia')),
                ('codename', models.CharField(max_length=100, verbose_name='Codename (*)', help_text='Ingrese el codename para el grupo de preferencia')),
                ('order', models.IntegerField(verbose_name='Orden (*)', default=1, help_text='Ingrese el orden del grupo de preferencia')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name': 'Grupo de preferencia',
                'verbose_name_plural': 'Grupos de preferencias',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Preferences',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=100, null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('comercializacion', models.ForeignKey(to='admin_finanzas.Comercializadora')),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name': 'Preferencia de una comercializadora',
                'verbose_name_plural': 'Preferencias de las comercializadoras',
                'ordering': ['-created_at'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TypePreferences',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100, verbose_name='Nombre (*)', help_text='Ingrese el nombre para el tipo de preferencia')),
                ('codename', models.CharField(max_length=100, verbose_name='Codename (*)', help_text='Ingrese el codename para el tipo de preferencia')),
                ('comparison', models.IntegerField(verbose_name='Compraracion nivel (*)', choices=[[1, 'Menor'], [2, 'Mayor'], [3, 'Libre']], help_text='Seleccione la compraracion de nivel')),
                ('order', models.IntegerField(verbose_name='Orden (*)', default=1, help_text='Ingrese el orden del tipo de preferencia')),
                ('edit', models.BooleanField(verbose_name='¿Editable? ', default=True, help_text='Seleccione de si una preferencia editable')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('group', models.ForeignKey(help_text='Seleccione el grupo de preferencia', to='admin_comercializacion.GroupPreferences', verbose_name='Grupo de preferencia (*)')),
                ('profile', models.ManyToManyField(to='admin_users.UserProfile', verbose_name='Perfiles de configuracion (*)', blank=True, help_text='Seleccione los perfiles de usuario que editan la preferencia')),
            ],
            options={
                'db_tablespace': 'ts_comer',
                'verbose_name': 'Tipo de preferencia',
                'verbose_name_plural': 'Tipos de preferencias',
                'ordering': ['name'],
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='preferences',
            name='typepreference',
            field=models.ForeignKey(to='admin_comercializacion.TypePreferences'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='defaultpreferences',
            name='typepreference',
            field=models.ForeignKey(help_text='Seleccione el tipo de preferencia', to='admin_comercializacion.TypePreferences', verbose_name='Tipo de preferencia (*)'),
            preserve_default=True,
        ),
    ]
