# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):

    #En una db ya inicializada transforma todos los correos que son "", osea 
    #vacias en nulos, como deben estar, ya que el email es un campo unique
    from admin_comercializacion.models import Operadoras, Bloques, Bancas, \
                                              Distribuidores, Agencias
    Operadoras.objects.filter( email = "").update(email = None)
    Bloques.objects.filter( email = "").update(email = None)
    Bancas.objects.filter( email = "").update(email = None)
    Distribuidores.objects.filter( email = "").update(email = None)
    Agencias.objects.filter( email = "").update(email = None)

class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0004_auto_20150116_1350'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
