# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0022_auto_20150427_2034'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usersprocesses',
            name='content_type',
            field=models.CharField(choices=[('admin_apuestas', 'Admin apuestas'), ('admin_comercializacion', 'Admin comercializacion'), ('admin_finanzas', 'Admin finanzas'), ('admin_reportes', 'Admin reportes'), ('admin_historic', 'Admin historic'), ('admin_juego', 'Admin juego'), ('admin_logros', 'Admin logros'), ('admin_permisologia', 'Admin permisologia'), ('admin_principal', 'Admin principal'), ('admin_profiles', 'Admin profiles'), ('admin_status', 'Admin status'), ('admin_themes', 'Admin themes'), ('admin_users', 'Admin users'), ('admin_soporte', 'Admin soporte'), ('admin_datamart', 'Admin datamart'), ('admin_resultados', 'Admin resultados'), ('admin_lib', 'Admin lib')], blank=True, verbose_name='App', null=True, max_length=50),
            preserve_default=True,
        ),
    ]
