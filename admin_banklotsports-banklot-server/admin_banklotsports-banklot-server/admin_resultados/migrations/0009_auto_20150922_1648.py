# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    from admin_resultados.models import Resultados, AnotacionesDetail

    querry = Resultados.objects.only('pk', 'updated_at').all()
    count = querry.count()
    i = 1

    print ("Migrando resultados con indicador")
    for resultado in querry:
        print ('{0} de {1}'.format(i, count))
        exists = AnotacionesDetail.objects.filter(
            anotacion__resultado_id=resultado.pk,
            puntaje__isnull=False
        ).exists()
    
        if exists:
            resultado.save(update_fields=['updated_at'])

        i += 1

class Migration(migrations.Migration):

    dependencies = [
        ('admin_resultados', '0008_resultadosrestric'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
