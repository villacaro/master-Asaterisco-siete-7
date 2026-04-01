# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0010_auto_20150106_2026'),
    ]

    operations = [
        migrations.AlterField(
            model_name='groups',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='groups',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='codename',
            field=models.CharField(max_length=160, verbose_name='Codigo '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='content_type',
            field=models.IntegerField(verbose_name='Nivel ', null=True, choices=[(1, 'Titulo princial.'), (2, 'Subtitulo.'), (3, 'Enlace.')], blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='icon',
            field=models.CharField(max_length=50, null=True, blank=True, verbose_name='Icono '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_global',
            field=models.BooleanField(verbose_name='Global ', help_text='Enlace privado, pero global', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_public',
            field=models.BooleanField(verbose_name='Público ', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='is_view',
            field=models.BooleanField(verbose_name='Visible ', default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='menu_suc',
            field=models.ForeignKey(to='admin_permisologia.Menu', null=True, blank=True, verbose_name='Origen '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='name',
            field=models.CharField(max_length=160, null=True, blank=True, verbose_name='Titulo '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='orden',
            field=models.IntegerField(verbose_name='Orden ', default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='menu',
            name='url',
            field=models.CharField(max_length=160, null=True, blank=True, verbose_name='Url '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='codename',
            field=models.CharField(max_length=160, unique=True, editable=False, verbose_name='Codigo '),
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
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='menu',
            field=models.ManyToManyField(verbose_name='Vistas asociadas ', to='admin_permisologia.Menu'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='name',
            field=models.CharField(max_length=160, unique=True, verbose_name='Nombre '),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='profiles',
            field=models.ManyToManyField(verbose_name='Perfiles asociados ', to='admin_users.UserProfile'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='permissions',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
