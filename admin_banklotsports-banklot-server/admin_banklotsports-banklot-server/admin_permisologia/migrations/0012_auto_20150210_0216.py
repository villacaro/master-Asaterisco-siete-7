# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0011_auto_20150126_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissions',
            name='content_type',
            field=models.CharField(verbose_name='App ', choices=[('django.contrib.auth', 'Django contrib auth'), ('django.contrib.contenttypes', 'Django contrib contenttypes'), ('django.contrib.sessions', 'Django contrib sessions'), ('django.contrib.sites', 'Django contrib sites'), ('django.contrib.messages', 'Django contrib messages'), ('django.contrib.staticfiles', 'Django contrib staticfiles'), ('django.contrib.admin', 'Django contrib admin'), ('django.contrib.humanize', 'Django contrib humanize'), ('djcelery', 'Djcelery'), ('gunicorn', 'Gunicorn'), ('crequest', 'Crequest'), ('django_extensions', 'Django extensions'), ('admin_apuestas', 'Admin apuestas'), ('admin_comercializacion', 'Admin comercializacion'), ('admin_finanzas', 'Admin finanzas'), ('admin_reportes', 'Admin reportes'), ('admin_historic', 'Admin historic'), ('admin_juego', 'Admin juego'), ('admin_logros', 'Admin logros'), ('admin_permisologia', 'Admin permisologia'), ('admin_principal', 'Admin principal'), ('admin_profiles', 'Admin profiles'), ('admin_status', 'Admin status'), ('admin_themes', 'Admin themes'), ('admin_users', 'Admin users'), ('admin_soporte', 'Admin soporte'), ('admin_datamart', 'Admin datamart'), ('admin_resultados', 'Admin resultados'), ('admin_lib', 'Admin lib'), ('scripts', 'Scripts')], max_length=50),
            preserve_default=True,
        ),
    ]
