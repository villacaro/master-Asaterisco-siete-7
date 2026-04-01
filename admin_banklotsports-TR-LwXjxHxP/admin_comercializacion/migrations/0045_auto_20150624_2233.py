# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def NewDataFactorRiesgo(apps, schema_editor):
    from admin_comercializacion.models import FactorRiesgo
    
    factores = FactorRiesgo.objects.all().update(factores=[])

class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0044_auto_20150622_1412'),
    ]

    operations = [
        migrations.RunPython(NewDataFactorRiesgo),
    ]


    
