# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

def MigrateDataInitial(apps, schema_editor):
    from admin_historic.models import UsersProcesses
    UsersProcesses.objects.all().delete()
    #userprocess predefinidos para el panel,
    #los demas se crean automagicamente :)
    process_login, create = UsersProcesses.objects.update_or_create(
        codename = "process_login",
        defaults = {
                        "name": "Inicio de sesión",
                        "content_type":  "admin_principal",
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_logout",
        defaults = {
                        "name": "Cerrar sesión",
                        "content_type":  "admin_principal",
                        "process_suc": process_login
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_expiresession",
        defaults = {
                        "name": "Sesión expirada",
                        "content_type":  "admin_principal",
                        "process_suc": process_login
                    }
    )

    #userprocess definidos para el ws
    UsersProcesses.objects.update_or_create(
        codename = "process_conn",
        defaults = {
                        "name": "Conexión",
                        "content_type":  "admin_principal",
                    }
    )
    audorizacion, create = UsersProcesses.objects.update_or_create(
        codename = "process_auth",
        defaults = {
                        "name": "Autorización",
                        "content_type":  "admin_principal",
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_getgata",
        defaults = {
                        "name": "Descarga de datos de taquilla",
                        "content_type":  "admin_comercializacion",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_getgames_initial",
        defaults = {
                        "name": "Descarga de juegos inicial",
                        "content_type":  "admin_juego",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_getgames_result",
        defaults = {
                        "name": "Descarga de resultados de juegos",
                        "content_type":  "admin_juego",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_bet",
        defaults = {
                        "name": "Apuesta",
                        "content_type":  "admin_apuestas",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_checkinglastbet",
        defaults = {
                        "name": "Confirmación de Último Ticket",
                        "content_type":  "admin_apuestas",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_tickets_forward",
        defaults = {
                        "name": "Reenviar ticket",
                        "content_type":  "admin_apuestas",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "conn_keepalive",
        defaults = {
                        "name": "Keep Alive",
                        "content_type":  "admin_principal",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "process_getnotifications",
        defaults = {
                        "name": "Descarga de notificaciones",
                        "content_type":  "admin_juego",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "auth_installation",
        defaults = {
                        "name": "Instalación",
                        "content_type":  "admin_comercializacion",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "auth_reinstallation",
        defaults = {
                        "name": "Reinstalación",
                        "content_type":  "admin_comercializacion",
                        "process_suc": audorizacion,
                    }
    )
    
    reportes, create = UsersProcesses.objects.update_or_create(
        codename = "process_queries",
        defaults = {
                        "name": "Consulta de Reportes",
                        "content_type":  "admin_reportes",
                        "process_suc": audorizacion,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_tickets",
        defaults = {
                        "name": "Lista de Tickets",
                        "content_type":  "admin_apuestas",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_winningtickets",
        defaults = {
                        "name": "Lista de Tickets ganadores",
                        "content_type":  "admin_apuestas",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_cancelticket",
        defaults = {
                        "name": "Anular Ticket",
                        "content_type":  "admin_apuestas",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_searchticket",
        defaults = {
                        "name": "Buscar Ticket",
                        "content_type":  "admin_apuestas",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_payticket",
        defaults = {
                        "name": "Pagar Ticket",
                        "content_type":  "admin_apuestas",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_dailyanalysis",
        defaults = {
                        "name": "Análisis Diario",
                        "content_type":  "admin_reportes",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_periodicanalysis",
        defaults = {
                        "name": "Análisis Periódico",
                        "content_type":  "admin_reportes",
                        "process_suc": reportes,
                    }
    )
    UsersProcesses.objects.update_or_create(
        codename = "query_cashbox",
        defaults = {
                        "name": "Cuadre de Caja",
                        "content_type":  "admin_reportes",
                        "process_suc": reportes,
                    }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_historic', '0008_auto_20141223_1759'),
    ]

    operations = [
    	migrations.RunPython(MigrateDataInitial),
    ]
