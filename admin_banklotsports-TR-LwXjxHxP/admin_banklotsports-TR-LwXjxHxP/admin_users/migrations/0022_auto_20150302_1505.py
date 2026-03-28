# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateUserProfile(apps, schema_editor):

    #En una db ya inicializada transforma todos los correos que son "", osea 
    #vacias en nulos, como deben estar, ya que el email es un campo unique
    from admin_users.models import UserProfile
    
    profile = UserProfile.objects.get(codename="userprofile_bloque")
    profile.nombre = "Multi banca"
    profile.save()

    profile = UserProfile.objects.get(codename="userprofile_agencia")
    profile.nombre = "Centro de apuesta"
    profile.save()

class Migration(migrations.Migration):

    dependencies = [
        ('admin_users', '0021_auto_20150126_1726'),
    ]

    operations = [
        migrations.RunPython(MigrateUserProfile),
    ]
