# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    from admin_comercializacion.models import AgenciaDataDefault
    AgenciaDataDefault.objects.all().update(
        frecuencia_queda = "frecuencia_mensual",
    )

    from admin_comercializacion.models import DataDefault
    DataDefault.objects.all().update(
        frecuencia_queda = "frecuencia_mensual",
    )

    from admin_comercializacion.models import TipoPorcentajes
    defaults = {
        "nombre": "Queda",
        "orden": 4,
        "bloque": True,
        "banca": True,
        "distribuidor": True,
        "agencia": True,
        "taquilla": True,
    }
    TipoPorcentajes.objects.update_or_create(
        codename = "porcentaje_queda",
        defaults = defaults
    )

    from admin_comercializacion.models import DataDefault
    DataDefault.objects.all().update(
        porcentaje_queda = 0,
    )

    from admin_comercializacion.models import Agencias
    Agencias.objects.all().update(
        frecuencia_queda = "frecuencia_mensual",
    )


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0039_auto_20150429_2023'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
