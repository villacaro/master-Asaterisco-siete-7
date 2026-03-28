# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def CreateNewStatus(apps, schema_editor):
    from admin_status.models import Status

    Status.objects.update_or_create(
        codename = "status_reanudado",
        defaults = {
            "content_type": -1
        }
    )
    Status.objects.update_or_create(
        codename = "status_deshabilitado",
        defaults = {
            "content_type": -1
        }
    )
    Status.objects.update_or_create(
        codename = "status_valido_no_terminado",
        defaults = {
            "name": "Valido no terminado",
            "content_type": 2
        }
    )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0006_status_order'),
    ]

    operations = [
    	migrations.RunPython(CreateNewStatus),
    ]
