# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateData(apps, schema_editor):
    pass
    '''
    from admin_apuestas.models import Tickets

    querryset = Tickets.objects.filter(status=None)
    count = querryset.count()
    i = 1
    for ticket in querryset:
        print ('Procesando estatus: {0} de {1}'.format(i, count))
        ticket.get_new_status()
        i += 1
    '''

class Migration(migrations.Migration):

    dependencies = [
        ('admin_status', '0008_auto_20150429_1326'),
        ('admin_apuestas', '0007_auto_20150819_1602'),
    ]

    operations = [
        migrations.AddField(
            model_name='tickets',
            name='status',
            field=models.ForeignKey(null=True, to='admin_status.Status', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='ticketsdetail',
            name='status',
            field=models.ForeignKey(null=True, to='admin_status.Status', blank=True),
            preserve_default=True,
        ),
        migrations.RunPython(MigrateData),
    ]
