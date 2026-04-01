# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0028_auto_20150923_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersprocesses',
            name='content_type',
            field=models.CharField(null=True, blank=True, max_length=50, choices=[('admin_apuestas', 'Admin apuestas'), ('admin_comercializacion', 'Admin comercializacion'), ('admin_datamart', 'Admin datamart'), ('admin_finanzas', 'Admin finanzas'), ('admin_historic', 'Admin historic'), ('admin_juego', 'Admin juego'), ('admin_logros', 'Admin logros'), ('admin_mail', 'Admin mail'), ('admin_permisologia', 'Admin permisologia'), ('admin_principal', 'Admin principal'), ('admin_profiles', 'Admin profiles'), ('admin_reportes', 'Admin reportes'), ('admin_resultados', 'Admin resultados'), ('admin_status', 'Admin status'), ('admin_soporte', 'Admin soporte'), ('admin_themes', 'Admin themes'), ('admin_users', 'Admin users'), ('admin_lib', 'Admin lib')], verbose_name='App'),
            preserve_default=True,
        ),
    ]
