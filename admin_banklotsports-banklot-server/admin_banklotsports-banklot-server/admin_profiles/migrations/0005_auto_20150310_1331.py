# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models, migrations
import json


def MigrateDataProfileAll(apps, schema_editor):

    # En una db ya inicializada transforma todos los correos que son "", osea
    # vacias en nulos, como deben estar, ya que el email es un campo unique
    # from admin_profiles.models import Paises, Estados, Municipios, Parroquias
    # with open("admin_lib/resources/venezuela.json") as json_file:
    #     json_data = json.load(json_file)
    #     pais = Paises.objects.get(nombre="Venezuela")
    #     for estado in json_data:
    #         estado_obj = Estados.objects.create(
    #                 pais=pais,
    #                 nombre=estado["estado"]
    #                 )
    #         for municipio in estado["municipios"]:
    #             municipio_obj = Municipios.objects.create(
    #                 estado=estado_obj,
    #                 nombre=municipio["municipio"],
    #                 capital=municipio["capital"]
    #             )
    #             for parroquia in municipio["parroquias"]:
    #                 Parroquias.objects.create(
    #                     municipio=municipio_obj,
    #                     nombre=parroquia
    #                 )
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('admin_profiles', '0004_auto_20150310_1256'),
    ]

    operations = [
        migrations.RunPython(MigrateDataProfileAll),
    ]
