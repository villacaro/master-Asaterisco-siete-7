# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0014_auto_20150617_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='permissions',
            name='content_type',
            field=models.CharField(verbose_name='App ', choices=[('admin_apuestas', 'Admin apuestas'), ('admin_comercializacion', 'Admin comercializacion'), ('admin_datamart', 'Admin datamart'), ('admin_finanzas', 'Admin finanzas'), ('admin_historic', 'Admin historic'), ('admin_juego', 'Admin juego'), ('admin_logros', 'Admin logros'), ('admin_mail', 'Admin mail'), ('admin_permisologia', 'Admin permisologia'), ('admin_principal', 'Admin principal'), ('admin_profiles', 'Admin profiles'), ('admin_reportes', 'Admin reportes'), ('admin_resultados', 'Admin resultados'), ('admin_status', 'Admin status'), ('admin_soporte', 'Admin soporte'), ('admin_themes', 'Admin themes'), ('admin_users', 'Admin users'), ('admin_lib', 'Admin lib')], max_length=50),
            preserve_default=True,
        ),
    ]
