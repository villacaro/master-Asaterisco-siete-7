# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models

def MigrateDataProcess(apps, schema_editor):
    from admin_historic.models import UsersProcesses
    
    UsersProcesses.objects.update_or_create(
        codename = "process_getmail",
        defaults = {
                        "name": "Obtener un mensaje",
                        "content_type":  "admin_comercializacion",
                        "process_suc": UsersProcesses.objects.get(codename = "process_auth"),
                    }
    )

    UsersProcesses.objects.update_or_create(
        codename = "process_getmails",
        defaults = {
                        "name": "Obtener lista de mensajes",
                        "content_type":  "admin_comercializacion",
                        "process_suc": UsersProcesses.objects.get(codename = "process_auth"),
                    }
    )

    UsersProcesses.objects.update_or_create(
        codename = "process_readmail",
        defaults = {
                        "name": "Mensaje leido",
                        "content_type":  "admin_comercializacion",
                        "process_suc": UsersProcesses.objects.get(codename = "process_auth"),
                    }
    )

    UsersProcesses.objects.update_or_create(
        codename = "process_sendmail",
        defaults = {
                        "name": "Mensaje enviado",
                        "content_type":  "admin_comercializacion",
                        "process_suc": UsersProcesses.objects.get(codename = "process_auth"),
                    }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0029_auto_20151009_1242'),
    ]

    operations = [
    	migrations.RunPython(MigrateDataProcess),
    ]
