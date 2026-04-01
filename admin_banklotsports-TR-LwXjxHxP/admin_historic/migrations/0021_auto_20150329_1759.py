# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def MigrateDataInitial(apps, schema_editor):
    from admin_historic.models import UsersProcesses
    UsersProcesses.objects.update_or_create(
        codename = "process_getfather",
        defaults = {
                        "name": "Descarga el padre de una notificacion",
                        "content_type":  "admin_juego",
                        "process_suc": UsersProcesses.objects.get(codename = "process_getnotifications"),
                    }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0020_auto_20150302_1941'),
    ]

    operations = [
    	migrations.RunPython(MigrateDataInitial),
    ]
