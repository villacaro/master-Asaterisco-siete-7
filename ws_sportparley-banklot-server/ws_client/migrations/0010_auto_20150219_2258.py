# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataInitial(apps, schema_editor):
    from ws_client.models import ClientStatus

    ClientStatus.objects.bulk_create([
        ClientStatus(
            status = "Archivo no disponible",
            codename = "client_status_file_unavailable",
            content_type = 3,
        ),
        ClientStatus(
            status = "Archivo disponible",
            codename = "client_status_file_available",
            content_type = 3,
        ),
        ClientStatus(
            status = "IP Activa",
            codename = "client_status_ip_active",
            content_type = 1,
        ),
        ClientStatus(
            status = "IP Bloqueada",
            codename = "client_status_ip_inactive",
            content_type = 1,
        ),
        ClientStatus(
            status = "IP Estandar",
            codename = "client_status_ip_default",
            content_type = 1,
        ),
        ClientStatus(
            status = "Versión activa",
            codename = "client_status_vs_active",
            content_type = 2,
        ),
        ClientStatus(
            status = "Versión inactiva",
            codename = "client_status_vs_inactive",
            content_type = 2,
        ),
    ])

    from ws_client.models import ClientVersion

    ClientVersion.objects.bulk_create([
        ClientVersion(
            version = "1.0.1",
            status = ClientStatus.objects.get( codename = "client_status_vs_active" )
        ),
    ])

    from ws_client.models import ClientIPAddress
    status = ClientStatus.objects.get(codename="client_status_ip_default")

    ClientIPAddress.objects.bulk_create([
        ClientIPAddress(
            ip_address = "179.43.114.158",
            ip_type = 1,
            protocol = 1,
            status = status,
        ),
        ClientIPAddress(
            ip_address = "179.43.114.158",
            ip_type = 2,
            protocol = 1,
            status = status,
        ),
        ClientIPAddress(
            ip_address = "179.43.114.158",
            ip_type = 3,
            protocol = 1,
            status = status,
        ),
        ClientIPAddress(
            ip_address = "179.43.114.158",
            ip_type = 4,
            protocol = 1,
            status = status,
        ),
    ])

class Migration(migrations.Migration):

    dependencies = [
        ('ws_client', '0009_auto_20150126_2156'),
    ]

    operations = [
        migrations.RunPython(MigrateDataInitial),
    ]
