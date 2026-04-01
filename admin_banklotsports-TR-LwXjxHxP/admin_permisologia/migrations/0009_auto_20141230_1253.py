# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0008_auto_20141224_1222'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='codename',
            field=models.CharField(unique=True, verbose_name='Codename (*)', max_length=160),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groups',
            name='name',
            field=models.CharField(max_length=160, verbose_name='Nombre del grupo (*)'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groups',
            name='permissions',
            field=models.ManyToManyField(verbose_name='Permisos asociados (*)', to='admin_permisologia.Permissions'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='content_type',
            field=models.IntegerField(blank=True, verbose_name='Nivel', null=True, choices=[(1, 'Titulo princial.'), (2, 'Subtitulo.'), (3, 'Enlace.')]),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_view',
            field=models.BooleanField(verbose_name='Visible', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(blank=True, max_length=160, verbose_name='Titulo', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='orden',
            field=models.IntegerField(verbose_name='Orden', default=0),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='permissions',
            name='content_type',
            field=models.CharField(max_length=50, verbose_name='App '),
            preserve_default=True,
        ),
    ]
