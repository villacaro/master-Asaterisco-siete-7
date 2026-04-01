# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

def CreateUserProfiles(apps, schema_editor):
    from admin_users.models import UserProfile

    UserProfile.objects.update_or_create(
        codename = "userprofile_master",
        defaults = {
            "nombre": "Master",
            "content_type": 1000,
        }
    )
    UserProfile.objects.update_or_create(
        codename = "userprofile_operadora",
        defaults = {
            "nombre": "Operadora",
            "content_type": 2000
        }
    )
    UserProfile.objects.update_or_create(
        codename = "userprofile_bloque",
        defaults = {
            "nombre": "Bloque",
            "content_type": 3000
        }
    )
    UserProfile.objects.update_or_create(
        codename = "userprofile_banca",
        defaults = {
            "nombre": "Banca",
            "content_type": 4000
        }
    )
    UserProfile.objects.update_or_create(
        codename = "userprofile_distribuidor",
        defaults = {
            "nombre": "Distribuidor",
            "content_type": 5000
        }
    )
    UserProfile.objects.update_or_create(
        codename = "userprofile_agencia",
        defaults = {
            "nombre": "Agencia",
            "content_type": 6000
        }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0003_auto_20141203_2249'),
    ]

    operations = [
    	migrations.RunPython(CreateUserProfiles),
    ]
