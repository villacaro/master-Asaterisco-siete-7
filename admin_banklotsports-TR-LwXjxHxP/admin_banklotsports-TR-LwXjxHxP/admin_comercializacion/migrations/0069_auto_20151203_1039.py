# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def MigrateDataAll(apps, schema_editor):
    pass
    '''
    from admin_comercializacion.models import FactorRiesgo
    from django.core.cache import cache
    cache.clear()

    factores_agencias = FactorRiesgo.objects.filter(
        comercializadora__agencia__isnull=False)
    factores_distribuidores = FactorRiesgo.objects.filter(
        comercializadora__distribuidor__isnull=False)
    factores_bancas = FactorRiesgo.objects.filter(
        comercializadora__banca__isnull=False)

    for factores in [factores_agencias, factores_distribuidores, factores_bancas]:
        print('{0} Registros de {1} totales'.format(
            len(factores),
            factores[0].get_object().prefix_filter)
        )
        count = 0
        for factor in factores:
            origen = factor.comercializadora.get_origen()
            parent = FactorRiesgo.objects.get(comercializadora=origen)
            if parent.factores == factor.factores:
                count += 1
                factor.audit_save = False
                factor.delete()
        print('{0} Registros eliminados'.format(count))
    '''


class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0068_auto_20151201_1507'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
