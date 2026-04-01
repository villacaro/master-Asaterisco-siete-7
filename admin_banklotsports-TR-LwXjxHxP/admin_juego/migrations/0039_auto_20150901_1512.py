# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    
    from admin_juego.models import Encuentros, EncuentrosModalidades, JugadasInformativas, Jugadas
    from django.utils.timezone import now
    from datetime import timedelta

    count = Encuentros.objects.all().count()
    i = 1
    for encuentro in Encuentros.objects.all().values_list('pk', 'jornada__sistema_id'):
        print ('{0} de {1}'.format(i, count))
        EncuentrosModalidades.objects.filter(encuentro_id=encuentro[0]).update(sistema_id=encuentro[1])
        JugadasInformativas.objects.filter(encuentros_modalidad__encuentro_id=encuentro[0]).update(sistema_id=encuentro[1])
        Jugadas.objects.filter(encuentros_modalidad__encuentro_id=encuentro[0]).update(sistema_id=encuentro[1])
        i += 1


class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0038_auto_20150901_1511'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAll),
    ]
