# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    from admin_comercializacion.models import AgenciaDataDefault
    AgenciaDataDefault.objects.all().update(
        parley_empates_max = 5,
    )

    from admin_comercializacion.models import Agencias
    Agencias.objects.all().update(
        parley_empates_max = 5,
    )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0042_auto_20150511_1032'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
