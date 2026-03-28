# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0009_auto_20141230_1253'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groups',
            options={'verbose_name_plural': 'Grupos', 'ordering': ['name'], 'verbose_name': 'Grupo'},
        ),
        migrations.AlterModelOptions(
            name='menu',
            options={'verbose_name_plural': 'Menus (enlaces)', 'ordering': ['orden'], 'verbose_name': 'Menu (url)'},
        ),
        migrations.AlterModelOptions(
            name='permissions',
            options={'verbose_name_plural': 'Permisos', 'ordering': ['content_type', 'name'], 'verbose_name': 'Permiso'},
        ),
        migrations.AlterField(
            model_name='groups',
            name='codename',
            field=models.CharField(verbose_name='Codename (*)', editable=False, unique=True, max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groups',
            name='name',
            field=models.CharField(verbose_name='Nombre del grupo (*)', unique=True, max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='codename',
            field=models.CharField(verbose_name='Codigo', editable=False, unique=True, max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='content_type',
            field=models.CharField(max_length=50, verbose_name='App '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='name',
            field=models.CharField(verbose_name='Nombre', unique=True, max_length=160),
            preserve_default=True,
        ),
    ]
