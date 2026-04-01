# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessions',
            name='cookie',
            field=models.CharField(max_length=160, null=True, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='usersprocesses',
            name='content_type',
            field=models.CharField(choices=[('django.contrib.auth', 'Django.contrib.auth'), ('django.contrib.contenttypes', 'Django.contrib.contenttypes'), ('django.contrib.sessions', 'Django.contrib.sessions'), ('django.contrib.sites', 'Django.contrib.sites'), ('django.contrib.messages', 'Django.contrib.messages'), ('django.contrib.staticfiles', 'Django.contrib.staticfiles'), ('django.contrib.admin', 'Django.contrib.admin'), ('django.contrib.humanize', 'Django.contrib.humanize'), ('djcelery', 'Djcelery'), ('gunicorn', 'Gunicorn'), ('crequest', 'Crequest'), ('django_extensions', 'Django_extensions'), ('admin_apuestas', 'Admin_apuestas'), ('admin_comercializacion', 'Admin_comercializacion'), ('admin_finanzas', 'Admin_finanzas'), ('admin_historic', 'Admin_historic'), ('admin_juego', 'Admin_juego'), ('admin_logros', 'Admin_logros'), ('admin_permisologia', 'Admin_permisologia'), ('admin_principal', 'Admin_principal'), ('admin_profiles', 'Admin_profiles'), ('admin_status', 'Admin_status'), ('admin_users', 'Admin_users'), ('admin_soporte', 'Admin_soporte'), ('admin_datamart', 'Admin_datamart'), ('admin_resultados', 'Admin_resultados'), ('scripts', 'Scripts')], max_length=50, verbose_name='App'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sessionsdetail',
            name='session',
            field=models.ForeignKey(blank=True, to='admin_historic.Sessions', null=True),
            preserve_default=True,
        ),
    ]
