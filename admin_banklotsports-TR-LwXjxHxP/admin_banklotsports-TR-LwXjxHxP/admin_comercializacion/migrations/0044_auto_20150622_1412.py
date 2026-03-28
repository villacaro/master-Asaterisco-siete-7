# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateNameRegaliaForServicios(apps, schema_editor):
    from admin_comercializacion.models import TipoPorcentajes

    try:
        porc = TipoPorcentajes.objects.get(codename='porcentaje_regalia')
        porc.nombre = 'Servicios'
        porc.save(update_fields=['nombre'])
    except TipoPorcentajes.DoesNotExist:
        pass

class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0043_auto_20150511_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='datadefault',
            name='porcentaje_regalia',
            field=models.DecimalField(verbose_name='Porcentaje de servicios (*)', decimal_places=5, help_text='Ingrese el porcentaje de servicios por tipo de comercializadora', max_digits=15, default=0.0),
            preserve_default=True,
        ),
        migrations.RunPython(MigrateNameRegaliaForServicios),
    ]
