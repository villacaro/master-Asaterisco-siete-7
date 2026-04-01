# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone

def MigrateDataAddTictesType(apps, schema_editor):
    from admin_apuestas.models import TicketsType
    TicketsType.objects.update_or_create(
        codename = "type_parley",
        defaults = {
                        "nombre": "Parley",
                        "descripcion":  "La modalidad parley de caracteriza por "
                                        "realizar apuestas deportivas combinadas, "
                                        "y entre mas combinaciones, "
                                        "es mayor el monto de ganancia." 
                    }
    )
    TicketsType.objects.update_or_create(
        codename = "type_simple",
        defaults = {
                        "nombre": "Simple",
                        "descripcion":  "La modalidad de apuesta simple no tiene "
                                        "restricciones para combinaciones de apuestas, "
                                        "se apuesta a cada modalidad independientemente."
                    }
    )
    TicketsType.objects.update_or_create(
        codename = "type_quiniela",
        defaults = {
                        "nombre": "Quiniela",
                        "descripcion":  "Este tipo de apuesta abarca multiples apuestas "
                                        "obligatorias combinadas entre si, generalmente "
                                        "se usa para apostarle al inicio de una copa, quien "
                                        "sera el ganador."
                    }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_apuestas', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(MigrateDataAddTictesType),
        migrations.AlterField(
            model_name='tickets',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='tickets',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdetail',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdetail',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdetailstatus',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketsdetailstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketstatus',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketstatus',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketstype',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, auto_now_add=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='ticketstype',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=True,
        ),
    ]
