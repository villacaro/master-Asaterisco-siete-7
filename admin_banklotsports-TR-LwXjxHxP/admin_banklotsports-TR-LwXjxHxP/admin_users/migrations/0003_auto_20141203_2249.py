# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0003_auto_20141203_2249'),
        ('admin_users', '0002_auto_20141202_2203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'verbose_name_plural': 'Tipos de usuarios', 'verbose_name': 'Tipo de usuario'},
        ),
        migrations.AlterModelOptions(
            name='users',
            options={'verbose_name_plural': 'Usuaios', 'verbose_name': 'Usuario'},
        ),
        migrations.AddField(
            model_name='users',
            name='groups',
            field=models.ManyToManyField(help_text='Seleccione los grupos disponibles', related_name='user_set', blank=True, to='admin_permisologia.Groups', related_query_name='user', verbose_name='Grupos de usuario'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='users',
            name='superuser',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='users',
            name='user_permissions',
            field=models.ManyToManyField(help_text='Seleccione los permisos para el usuario.', related_name='user_set', blank=True, to='admin_permisologia.Permissions', related_query_name='user', verbose_name='Permisos de usuario'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='content_type',
            field=models.IntegerField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='email',
            field=models.EmailField(max_length=254, help_text='Ingrese el correo electronico', blank=True, null=True, unique=True, verbose_name='Correo electronico'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='profile',
            field=models.ForeignKey(help_text='Seleccione el perfil de usuario', to='admin_users.UserProfile', verbose_name='Perfil de usuario (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='users',
            name='user',
            field=models.CharField(unique=True, max_length=100, db_index=True, help_text='Ingrese el nombre de usuario', verbose_name='Nombre de usuario (*)'),
            preserve_default=True,
        ),
    ]
