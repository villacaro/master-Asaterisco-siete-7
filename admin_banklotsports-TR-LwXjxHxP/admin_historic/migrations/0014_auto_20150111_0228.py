# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0013_auto_20141230_1108'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taquillasessions',
            name='id',
        ), 
        migrations.AddField(
            model_name='taquillasessions',
            name='id',
            field=models.CharField(serialize=False, max_length=48, primary_key=True, default=None),
            preserve_default=True,
        ),
        migrations.RemoveField(
            model_name='taquillasessionsdetail',
            name='id',
        ), 
        migrations.AddField(
            model_name='taquillasessionsdetail',
            name='id',
            field=models.CharField(serialize=False, max_length=48, primary_key=True, default=None),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersprocesses',
            name='content_type',
            field=models.CharField(verbose_name='App', null=True, choices=[('django.contrib.auth', 'Django contrib auth'), ('django.contrib.contenttypes', 'Django contrib contenttypes'), ('django.contrib.sessions', 'Django contrib sessions'), ('django.contrib.sites', 'Django contrib sites'), ('django.contrib.messages', 'Django contrib messages'), ('django.contrib.staticfiles', 'Django contrib staticfiles'), ('django.contrib.admin', 'Django contrib admin'), ('django.contrib.humanize', 'Django contrib humanize'), ('djcelery', 'Djcelery'), ('gunicorn', 'Gunicorn'), ('crequest', 'Crequest'), ('django_extensions', 'Django extensions'), ('admin_apuestas', 'Admin apuestas'), ('admin_comercializacion', 'Admin comercializacion'), ('admin_finanzas', 'Admin finanzas'), ('admin_historic', 'Admin historic'), ('admin_juego', 'Admin juego'), ('admin_logros', 'Admin logros'), ('admin_permisologia', 'Admin permisologia'), ('admin_principal', 'Admin principal'), ('admin_profiles', 'Admin profiles'), ('admin_status', 'Admin status'), ('admin_users', 'Admin users'), ('admin_soporte', 'Admin soporte'), ('admin_datamart', 'Admin datamart'), ('admin_resultados', 'Admin resultados'), ('admin_lib', 'Admin lib'), ('scripts', 'Scripts')], max_length=50, blank=True),
            preserve_default=True,
        ),
    ]
