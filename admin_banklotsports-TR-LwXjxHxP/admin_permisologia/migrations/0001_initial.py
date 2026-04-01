# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('name', models.CharField(max_length=160)),
                ('codename', models.CharField(max_length=160, unique=True)),
                ('url', models.CharField(null=True, blank=True, max_length=160)),
                ('icon', models.CharField(null=True, blank=True, max_length=50)),
                ('content_type', models.IntegerField()),
                ('orden', models.IntegerField()),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 339358), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 339418), auto_now=True)),
                ('menu_suc', models.ForeignKey(null=True, blank=True, to='admin_permisologia.Menu')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('state', models.BooleanField(default=False)),
                ('view', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 341135), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 341202), auto_now=True)),
                ('menu', models.ForeignKey(to='admin_permisologia.Menu')),
                ('user_type', models.ForeignKey(to='admin_users.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PermissionsType',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('codename', models.CharField(max_length=160, unique=True)),
                ('description', models.CharField(max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 342826), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 342908), auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersPermissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('value', models.CharField(null=True, blank=True, max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 344247), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 344314), auto_now=True)),
                ('permissiontype', models.ForeignKey(to='admin_permisologia.PermissionsType')),
                ('user', models.ForeignKey(null=True, blank=True, to='admin_users.Users')),
                ('user_type', models.ForeignKey(null=True, blank=True, to='admin_users.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UsersRestrictions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('value', models.CharField(max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 345722), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 2, 22, 3, 31, 345778), auto_now=True)),
                ('permissiontype', models.ForeignKey(to='admin_permisologia.PermissionsType')),
                ('user', models.ForeignKey(null=True, blank=True, to='admin_users.Users')),
                ('user_type', models.ForeignKey(null=True, blank=True, to='admin_users.UserProfile')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='menu',
            name='user_permiso',
            field=models.ManyToManyField(null=True, through='admin_permisologia.MenuPermissions', to='admin_users.UserProfile'),
            preserve_default=True,
        ),
    ]
