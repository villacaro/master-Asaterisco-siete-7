# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime

def MigrateDataAll(apps, schema_editor):
    '''
    from admin_comercializacion.models import AgenciaDataDefault
    AgenciaDataDefault.objects.bulk_create([
        AgenciaDataDefault(
            montomin = 20, 
            montomax = 1000,
            montomax_ganancia = 30000,
            cantidad_apuesta_max = 8,
            cantidad_apuesta_min = 3,
            tiempoexpiracion = 5,
            parley_machos_max = 20,
            parley_machos_min = 0,
            parley_hembras_max = 4,
            parley_hembras_min = 0,
            parley_clonados_maxima_ganancia = 35000,
            monto_alquiler = 0,
            frecuencia_monto_alquiler = "frecuencia_mensual",
            factor_riesgo = 0,
            everyone = False,
        ),
    ])
    '''

    from admin_comercializacion.models import TaquillaDataDefault

    TaquillaDataDefault.objects.update_or_create(
        user_name = "taquilla",
        defaults = {
                        "passwd": "123456",
                    }
    )

    from admin_comercializacion.models import TicketsDataDefault
    TicketsDataDefault.objects.filter( everyone = True ).update(
        everyone = False
    )
    TicketsDataDefault.objects.bulk_create([
        TicketsDataDefault(
            titulo1 = "Sports Parley",
            titulo2 = "",
            titulo3 = "",
            pie1 = "¡Buena suerte!",
            pie2 = "",
            pie3 = "",
            everyone = True,
        ),
    ])

    '''
    from admin_comercializacion.models import DataDefault
    from admin_users.models import UserProfile
    defaults = {
        "cupo": 0,
        "porcentaje_comision": 0,
        "porcentaje_regalia": 0,
        "porcentaje_participacion": 0,
        "porcentaje_maximo": 0,
        "monto_alquiler": 0,
        "frecuencia_monto_alquiler": "frecuencia_mensual",
        "factor_riesgo": 1,
    }
    DataDefault.objects.update_or_create(
            user_type = UserProfile.objects.get( codename = "userprofile_bloque" ),
            defaults = defaults
    )
    DataDefault.objects.update_or_create(
            user_type = UserProfile.objects.get( codename = "userprofile_banca" ),
            defaults = defaults
    )
    DataDefault.objects.update_or_create(
            user_type = UserProfile.objects.get( codename = "userprofile_distribuidor" ),
            defaults = defaults
    )
    DataDefault.objects.update_or_create(
            user_type = UserProfile.objects.get( codename = "userprofile_agencia" ),
            defaults = defaults
    )
    '''

    from admin_comercializacion.models import TipoPorcentajes
    defaults = {
        "nombre": "Comisión",
        "orden": 1,
        "bloque": True,
        "banca": True,
        "distribuidor": True,
        "agencia": True,
        "taquilla": True,
    }
    TipoPorcentajes.objects.update_or_create(
        codename = "porcentaje_comision",
        defaults = defaults
    )
    defaults["nombre"] = "Regalía"
    defaults["orden"] = 2
    TipoPorcentajes.objects.update_or_create(
        codename = "porcentaje_regalia",
        defaults = defaults
    )
    defaults["nombre"] = "Participación"
    defaults["orden"] = 3
    TipoPorcentajes.objects.update_or_create(
        codename = "porcentaje_participacion",
        defaults = defaults
    )

    
class Migration(migrations.Migration):

    dependencies = [
        ('admin_comercializacion', '0018_auto_20150122_2300'),
    ]

    operations = [
        migrations.AddField(
            model_name='agenciadatadefault',
            name='monto_alquiler',
            field=models.DecimalField(decimal_places=5, verbose_name='Monto de alquiler por taquilla(*)', max_digits=15, help_text='Ingrese el monto por alquier de taquilla', default=0.0),
            preserve_default=True,
        ),
        migrations.RunPython(MigrateDataAll),
    ]
