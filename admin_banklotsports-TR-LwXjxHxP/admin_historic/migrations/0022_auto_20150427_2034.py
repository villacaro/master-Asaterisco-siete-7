# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataInitial(apps, schema_editor):
    from admin_historic.models import UsersProcesses
    
    UsersProcesses.objects.update_or_create(
        codename = "process_getnotifications",
        defaults = {
                        "name": "Descarga de notificaciones de juegos",
                        "content_type":  "admin_juego",
                        "process_suc": UsersProcesses.objects.get(codename = "conn_keepalive"),
                    }
    )

    UsersProcesses.objects.update_or_create(
        codename = "process_getnotificationscadena",
        defaults = {
                        "name": "Descarga notificaciones de la cadena",
                        "content_type":  "admin_comercializacion",
                        "process_suc": UsersProcesses.objects.get(codename = "conn_keepalive"),
                    }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0021_auto_20150329_1759'),
    ]

    operations = [
    	migrations.RunPython(MigrateDataInitial),
    ]
