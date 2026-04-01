# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def CreateNewStatus(apps, schema_editor):
    from admin_status.models import Status

    Status.objects.update_or_create(
        codename = "status_actualizar",
        defaults = {
            "name": "Actualizar",
            "content_type": 0
        }
    )
    Status.objects.update_or_create(
        codename = "status_activo",
        defaults = {
            "name": "Activo",
            "content_type": 1
        }
    )
    Status.objects.update_or_create(
        codename = "status_activo_sin_venta",
        defaults = {
            "name": "Activo - sin venta",
            "content_type": 1
        }
    )
    Status.objects.update_or_create(
    	codename = "status_bloqueado",
        defaults = {
            "name": "Bloqueado",
            "content_type": 1
        }
    )

    Status.objects.update_or_create(
        codename = "status_habilitado",
        defaults = {
            "name": "Habilitado",
            "content_type": 2
        }
    )
    Status.objects.update_or_create(
        codename = "status_inhabilitado",
        defaults = {
            "name": "Suspendido",
            "content_type": 2
        }
    )
    Status.objects.update_or_create(
        codename = "status_reanudado",
        defaults = {
            "name": "Reanudado",
            "content_type": 2
        }
    )
    Status.objects.update_or_create(
        codename = "status_deshabilitado",
        defaults = {
            "name": "Deshabilitado",
            "content_type": 2
        }
    )

    Status.objects.update_or_create(
        codename = "status_instalacion",
        defaults = {
            "name": "Instalación",
            "content_type": 3
        }
    )
    Status.objects.update_or_create(
        codename = "status_reinstalacion",
        defaults = {
            "name": "Reinstalación",
            "content_type": 3
        }
    )

    Status.objects.update_or_create(
        codename = "status_eliminado",
        defaults = {
            "name": "Eliminado",
            "content_type": 4
        }
    )
    Status.objects.update_or_create(
        codename = "status_pendiente",
        defaults = {
            "name": "Vendido",
            "content_type": 4
        }
    )

    Status.objects.update_or_create(
        codename = "status_ganado",
        defaults = {
            "name": "Ganado",
            "content_type": 5
        }
    )
    Status.objects.update_or_create(
        codename = "status_perdido",
        defaults = {
            "name": "Perdido",
            "content_type": 5
        }
    )

    Status.objects.update_or_create(
        codename = "status_vendido",
        defaults = {
            "name": "Vendido",
            "content_type": 6,
        }
    )
    Status.objects.update_or_create(
        codename = "status_novendido",
        defaults = {
            "name": "No vendido",
            "content_type": 6
        }
    )

    Status.objects.update_or_create(
        codename = "status_completado",
        defaults = {
            "name": "Completado",
            "content_type": 7
        }
    )

    Status.objects.update_or_create(
        codename = "status_procesadoperdedor",
        defaults = {
            "name": "Perdido",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_procesandoganador",
        defaults = {
            "name": "Ganador",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_ganado_frio",
        defaults = {
            "name": "Ticket Frío",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_anulado_automatico",
        defaults = {
            "name": "Anulación Automática",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_ticketpendiente",
        defaults = {
            "name": "Vendido",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_pagado",
        defaults = {
            "name": "Pagado",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_anulado",
        defaults = {
            "name": "Anulado",
            "content_type": 8
        }
    )
    Status.objects.update_or_create(
        codename = "status_procesandose",
        defaults = {
            "name": "Procesandose",
            "content_type": 8
        }
    )
    
class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0002_auto_20150123_0253'),
    ]

    operations = [
    	migrations.RunPython(CreateNewStatus),
    ]
