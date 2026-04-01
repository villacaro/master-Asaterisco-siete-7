# -*- coding: utf-8 -*-
import os

from admin_comercializacion import models
from admin_finanzas.models import Comercializadora
from admin_status.models import TaquillaStatusDetail
from django.core.serializers import serialize

# from optparse import OptionParser


os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings'


def run(*args):
    """
         >> python manage.py runscript get_data
    """
    """usage = "usage: %prog -s SETTINGS | --settings=SETTINGS"
    parser = OptionParser(usage)
    parser.add_option('-s', '--settings', dest='settings', metavar='SETTINGS',
                      help="The Django settings module to use")
    (options, args) = parser.parse_args()
    if not options.settings:
        parser.error("You must specify a settings module")"""
    print("Devolviendo data de comercializadores hasta 22-04-2015")
    tipo_comercializador = input("Tipo de comercializador: ")
    if(int(tipo_comercializador) == 1):
        # Para tipo = 1, modelos a partir de ese nivel
        print("== Devolviendo data de Multi Bancas ==")
        model = "Bloques"
        model_names = [
            "Bloques",
            "Bancas",
            "Distribuidores",
            "Agencias",
            "Taquillas",
            "UsuariosTaquilla",
            "Cupos",
            "Porcentajes",
            "PreferenciasCadena",
            "TaquillaStatusDetail",
            "Comercializadora"]
        filename = "00{0}_{1}.json".format(tipo_comercializador, model.lower())
        cls = getattr(models, model)
        multibancas = input("IDs de las Multi Bancas: ")
        multibancas = [int(x) for x in eval(multibancas)]
        bloques = cls.objects.filter(pk__in=multibancas)
        file = open(filename, "w")
        file.write(serialize("json", bloques))
        print(bloques)
        filename1 = "002_{0}.json".format(model_names[1].lower())
        filename2 = "003_{0}.json".format(model_names[2].lower())
        filename3 = "004_{0}.json".format(model_names[3].lower())
        filename4 = "005_{0}.json".format(model_names[4].lower())
        filename5 = "006_{0}.json".format(model_names[5].lower())
        filename6 = "007_{0}.json".format(model_names[6].lower())
        filename7 = "008_{0}.json".format(model_names[7].lower())
        filename8 = "009_{0}.json".format(model_names[8].lower())
        filename9 = "010_{0}.json".format(model_names[9].lower())
        filename10 = "011_{0}.json".format(model_names[10].lower())
        bancas = []
        distribudores = []
        agencias = []
        taquillas = []
        usuariostaq = []
        cupos = []
        porcentajes = []
        preferencias = []
        taquillastatus = []
        comercializadoras = []

        for bloque in bloques:
            cls = getattr(models, model_names[1])
            bancas += cls.objects.filter(bloque=bloque)
        for banca in bancas:
            cls = getattr(models, model_names[2])
            distribudores += cls.objects.filter(banca=banca)
        for distribuidor in distribudores:
            cls = getattr(models, model_names[3])
            agencias += cls.objects.filter(distribuidores=distribuidor)
        for agencia in agencias:
            cls = getattr(models, model_names[4])
            taquillas += cls.objects.filter(agencia=agencia)
        for taquilla in taquillas:
            cls = getattr(models, model_names[5])
            usuariostaq += cls.objects.filter(taquilla=taquilla)

        # Cupos
        cupos_obj = getattr(models, model_names[6])
        cupos += cupos_obj.objects.filter(bloque__in=bloques)
        cupos += cupos_obj.objects.filter(banca__in=bancas)
        cupos += cupos_obj.objects.filter(distribuidor__in=distribudores)
        cupos += cupos_obj.objects.filter(agencia__in=agencias)

        # Porcentajes
        porcentajes_obj = getattr(models, model_names[7])
        porcentajes += porcentajes_obj.objects.filter(bloque__in=bloques)
        porcentajes += porcentajes_obj.objects.filter(banca__in=bancas)
        porcentajes += porcentajes_obj.objects.filter(distribuidor__in=distribudores)
        porcentajes += porcentajes_obj.objects.filter(agencia__in=agencias)

        # Preferencias
        preferencias_obj = getattr(models, model_names[8])
        preferencias += preferencias_obj.objects.filter(bloque__in=bloques)
        preferencias += preferencias_obj.objects.filter(banca__in=bancas)
        preferencias += preferencias_obj.objects.filter(distribuidor__in=distribudores)
        preferencias += preferencias_obj.objects.filter(agencia__in=agencias)

        # Status taquilla
        taquillastatus += TaquillaStatusDetail.objects.filter(usuariotaquilla__in=usuariostaq)

        # Comercializadoras
        comercializadoras += Comercializadora.objects.filter(bloque__in=bloques)
        comercializadoras += Comercializadora.objects.filter(banca__in=bancas)
        comercializadoras += Comercializadora.objects.filter(distribuidor__in=distribudores)
        comercializadoras += Comercializadora.objects.filter(agencia__in=agencias)
        comercializadoras += Comercializadora.objects.filter(taquilla__in=taquillas)

        print(bancas)
        print(distribudores)
        print(agencias)
        print(taquillas)
        print(usuariostaq)
        print(cupos)
        print(porcentajes)
        print(preferencias)
        print(taquillastatus)
        print(comercializadoras)

        file = open(filename1, "w")
        file.write(serialize("json", bancas))
        file = open(filename2, "w")
        file.write(serialize("json", distribudores))
        file = open(filename3, "w")
        file.write(serialize("json", agencias))
        file = open(filename4, "w")
        file.write(serialize("json", taquillas))
        file = open(filename5, "w")
        file.write(serialize("json", usuariostaq))
        file = open(filename6, "w")
        file.write(serialize("json", cupos))
        file = open(filename7, "w")
        file.write(serialize("json", porcentajes))
        file = open(filename8, "w")
        file.write(serialize("json", preferencias))
        file = open(filename9, "w")
        file.write(serialize("json", taquillastatus))
        file = open(filename10, "w")
        file.write(serialize("json", comercializadoras))
