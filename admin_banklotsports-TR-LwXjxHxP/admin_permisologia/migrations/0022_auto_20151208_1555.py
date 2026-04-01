# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def MigrateDataAll(apps, schema_editor):
    from admin_permisologia.models import PermissionsSales
    from django.core.cache import cache
    cache.clear()

    permissions_agencias = PermissionsSales.objects.filter(comercializadora__agencia__isnull=False)
    permissions_distribuidores = PermissionsSales.objects.filter(comercializadora__distribuidor__isnull=False)
    permissions_bancas = PermissionsSales.objects.filter(comercializadora__banca__isnull=False)
    #permissions_bloques = PermissionsSales.objects.filter(comercializadora__bloque__isnull=False)

    for restrictions in [permissions_agencias, permissions_distribuidores, permissions_bancas]:
        if restrictions:
            print('{0} Registros de {1} totales'.format(
                len(restrictions),
                restrictions[0].comercializadora.get_object().prefix_filter)
            )
            count = 0
            for restriction in restrictions:
                origen = restriction.comercializadora.get_origen()
                kwargs = {}
                kwargs['deporte'] = restriction.deporte
                kwargs['grupo'] = restriction.grupo
                kwargs['modalidad'] = restriction.modalidad
                kwargs['comercializadora'] = origen
                try:
                    parent = PermissionsSales.objects.get(**kwargs)
                except PermissionsSales.DoesNotExist:
                    parent = None
                if parent:
                    count += 1
                    restriction.audit_save = False
                    restriction.delete()
            print('{0} Registros eliminados'.format(count))


class Migration(migrations.Migration):

    dependencies = [
        ('admin_permisologia', '0021_auto_20151204_1937'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
