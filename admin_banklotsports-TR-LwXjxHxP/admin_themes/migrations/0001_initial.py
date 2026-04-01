# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=200, verbose_name='Nombre de la empresa (*)')),
                ('logo', models.ImageField(null=True, upload_to='company', blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Empresas',
                'ordering': ['name'],
                'verbose_name': 'Empresa',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Theme',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('name', models.CharField(max_length=140, verbose_name='Nombre del tema (*)')),
                ('codename', models.CharField(max_length=140, verbose_name='Codename del tema (*)')),
                ('description', models.CharField(max_length=140, verbose_name='Descripción del tema (*)')),
                ('screenshoot', models.ImageField(null=True, upload_to='themes', blank=True)),
                ('template_dir', models.CharField(max_length=140, verbose_name='Dirección de template')),
                ('static_url', models.CharField(max_length=140, verbose_name='URL de los archivos estáticos')),
                ('media_url', models.CharField(max_length=140, verbose_name='URL de la carpeta de media')),
                ('created_at', models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(auto_now=True, default=django.utils.timezone.now)),
            ],
            options={
                'verbose_name_plural': 'Temas',
                'ordering': ['name'],
                'verbose_name': 'Tema',
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
    ]
