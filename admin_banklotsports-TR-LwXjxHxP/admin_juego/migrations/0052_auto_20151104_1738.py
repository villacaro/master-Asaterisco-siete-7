# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    
    from admin_juego.models import Modalidades
    
    modalidad = Modalidades.objects.get(
    	codename='pitcher'
    	)
    modalidad.bet = False
    modalidad.save()

class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0051_modalidades_bet'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
