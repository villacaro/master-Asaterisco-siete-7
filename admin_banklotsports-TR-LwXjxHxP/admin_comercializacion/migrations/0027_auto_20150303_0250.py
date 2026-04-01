# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    from scripts import migrate_data_comercializadoras_001
    migrate_data_comercializadoras_001.run( )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0026_auto_20150303_0243'),
    ]

    operations = [
       
    ]
