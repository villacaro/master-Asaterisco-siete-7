# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('profile', models.CharField(max_length=160)),
                ('codename', models.CharField(unique=True, max_length=160)),
                ('content_type', models.IntegerField(null=True, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 11, 26, 21, 28, 30, 421270))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2014, 11, 26, 21, 28, 30, 421327))),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Users',
            fields=[
                ('id', models.AutoField(auto_created=True, serialize=False, verbose_name='ID', primary_key=True)),
                ('user', models.CharField(unique=True, verbose_name='Nombre de usuario (*)', max_length=100, help_text='Ingrese el nombre de usuario')),
                ('passwd', models.CharField(null=True, verbose_name='Contraseña', max_length=200, blank=True)),
                ('email', models.EmailField(help_text='Ingrese el correo electronico', max_length=254, null=True, unique=True, verbose_name='Correo electronico ', blank=True)),
                ('token', models.CharField(null=True, max_length=200, blank=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, default=datetime.datetime(2014, 11, 26, 21, 28, 30, 422815))),
                ('updated_at', models.DateTimeField(auto_now=True, default=datetime.datetime(2014, 11, 26, 21, 28, 30, 422874))),
                ('profile', models.ForeignKey(help_text='Seleccione el perfil de usuario', null=True, to='admin_users.UserProfile', verbose_name='Perfil de usuario (*)', blank=True)),
                ('user_ref', models.ForeignKey(null=True, to='admin_users.Users', blank=True)),
            ],
            options={
                'db_tablespace': 'ts_comer',
            },
            bases=(models.Model,),
        ),
    ]
