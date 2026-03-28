# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def MigrateDataProcess(apps, schema_editor):
    from admin_historic.models import UsersProcesses
    
    UsersProcesses.objects.update_or_create(
        codename='process_getnotificationslost',
        defaults={
                    'name': 'Obtener una notificacion perdida',
                    'content_type':  'admin_juego',
                    'process_suc': UsersProcesses.objects.get(codename = 'process_auth'),
                }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0032_auto_20151103_0134'),
    ]

    operations = [
        migrations.RunPython(MigrateDataProcess),
    ]
