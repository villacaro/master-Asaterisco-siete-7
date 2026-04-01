# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataDimencionArcoComercializacion(apps, schema_editor):
    pass
    # from scripts import migrate_data_dimension_datamart_001
    # migrate_data_dimension_datamart_001.run( )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_datamart', '0011_auto_20150122_1710'),
    ]

    operations = [
    	migrations.RunPython(MigrateDataDimencionArcoComercializacion),
    ]
