# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('admin_permisologia', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Groups',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=160)),
                ('codename', models.CharField(unique=True, max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 3, 22, 47, 6, 703265), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 3, 22, 47, 6, 703325), auto_now=True)),
            ],
            options={
                'verbose_name_plural': 'Grupos',
                'verbose_name': 'Grupo',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Permissions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', auto_created=True, serialize=False, primary_key=True)),
                ('name', models.CharField(max_length=160)),
                ('codename', models.CharField(unique=True, max_length=160)),
                ('created_at', models.DateTimeField(default=datetime.datetime(2014, 12, 3, 22, 47, 6, 700713), auto_now_add=True)),
                ('updated_at', models.DateTimeField(default=datetime.datetime(2014, 12, 3, 22, 47, 6, 700772), auto_now=True)),
                ('content_type', models.ForeignKey(to='contenttypes.ContentType')),
                ('menu', models.ManyToManyField(blank=True, verbose_name='Menus', to='admin_permisologia.Menu')),
            ],
            options={
                'verbose_name_plural': 'Permisos',
                'verbose_name': 'Permiso',
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='menupermissions',
            name='menu',
        ),
        migrations.RemoveField(
            model_name='menupermissions',
            name='user_type',
        ),
        migrations.RemoveField(
            model_name='userspermissions',
            name='permissiontype',
        ),
        migrations.RemoveField(
            model_name='userspermissions',
            name='user',
        ),
        migrations.RemoveField(
            model_name='userspermissions',
            name='user_type',
        ),
        migrations.DeleteModel(
            name='UsersPermissions',
        ),
        migrations.RemoveField(
            model_name='usersrestrictions',
            name='permissiontype',
        ),
        migrations.DeleteModel(
            name='PermissionsType',
        ),
        migrations.RemoveField(
            model_name='usersrestrictions',
            name='user',
        ),
        migrations.RemoveField(
            model_name='usersrestrictions',
            name='user_type',
        ),
        migrations.DeleteModel(
            name='UsersRestrictions',
        ),
        migrations.AddField(
            model_name='groups',
            name='permissions',
            field=models.ManyToManyField(blank=True, verbose_name='Permissions', to='admin_permisologia.Permissions'),
            preserve_default=True,
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name_plural': 'Menus', 'verbose_name': 'Menu'},
        ),
        migrations.RemoveField(
            model_name='menu',
            name='user_permiso',
        ),
        migrations.DeleteModel(
            name='MenuPermissions',
        ),
        migrations.AddField(
            model_name='menu',
            name='is_public',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='menu',
            name='is_view',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='content_type',
            field=models.IntegerField(choices=[(1, 'Nivel 1: Titulo princial.'), (2, 'Nivel 2: Subtitulo.'), (3, 'Nivel 3: Enlace.')]),
            preserve_default=True,
        ),
    ]
