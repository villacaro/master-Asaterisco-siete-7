# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigratePreferenciasTickets(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0053_auto_20150924_1044'),
    ]

    operations = [
    	migrations.RunPython(MigratePreferenciasTickets)
    ]