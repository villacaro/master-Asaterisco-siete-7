# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):
    from admin_juego.models import Encuentros
    
    print ('Migrando indicador en encuentros')
    count = Encuentros.objects.all().count()
    i = 1
    for encuentro in Encuentros.objects.only('pk', 'exists_tickets').all():
        print ('{0} de {1}'.format(i, count))
        encuentro.exists_tickets = encuentro.get_exists_tickets()
        if encuentro.exists_tickets:
            encuentro.save(update_fields=['exists_tickets'])
        i += 1

class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0045_auto_20150922_1243'),
    ]

    operations = [
        migrations.AddField(
            model_name='encuentros',
            name='exists_tickets',
            field=models.BooleanField(default=False, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentros',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentrosdetail',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='encuentrosmodalidades',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='equipos',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='gruposjuego',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jornadas',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadas',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugador',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='jugadortipo',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='temporadas',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='torneos',
            name='pk_clone',
            field=models.IntegerField(default=0, editable=False, db_index=True),
            preserve_default=True,
        ),
        migrations.RunPython(MigrateDataAll),
    ]
