# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

def MigrateDataAll(apps, schema_editor):

    from admin_juego.models import GruposApuestas
    grupo_referencia = GruposApuestas.objects.update_or_create(
                                codename = "referencia",
                                defaults = {
                                            "nombre": "Referencia",
                                            "orden": 0
                                        }
                        )[0]

    grupo_juego_completo = GruposApuestas.objects.update_or_create(
                                codename = "juego_completo",
                                defaults = {
                                            "nombre": "Juego Completo",
                                            "orden": 1
                                        }
                            )[0]
    grupo_medio_juego = GruposApuestas.objects.update_or_create(
                                codename = "medio_juego",
                                defaults = {
                                            "nombre": "Medio Juego",
                                            "orden": 2
                                        }
                            )[0]
    grupo_segunda_mitad = GruposApuestas.objects.update_or_create(
                                codename = "segunda_mitad",
                                defaults = {
                                            "nombre": "Segunda Mitad",
                                            "orden": 3
                                        }
                            )[0]
    grupo_combinadas = GruposApuestas.objects.update_or_create(
                                codename = "combinadas",
                                defaults = {
                                            "nombre": "Combinadas",
                                            "orden": 4
                                        }
                            )[0]
    
    from admin_juego.models import Modalidades
    from admin_juego.models import Modalidades_Grupos
    modalidad_pitcher = Modalidades.objects.update_or_create(
        codename = "pitcher",
        defaults = {
                        "modalidad": "Pitcher",
                        "orden": 0,
                        "descripcion": "Pitcher en beisbol",
                        "etiqueta_ref": False,
                    }
    )[0]

    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_pitcher,
        grupo = grupo_referencia,
    )

    modalidad_ganador = Modalidades.objects.update_or_create(
        codename = "ganador",
        defaults = {
                        "modalidad": "Ganador",
                        "orden": 1,
                        "descripcion": "Equipo a ganar",
                        "etiqueta_ref": False,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_ganador,
        grupo = grupo_juego_completo,
    )
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_ganador,
        grupo = grupo_medio_juego,
    )

    modalidad_altabaja = Modalidades.objects.update_or_create(
        codename = "alta/baja",
        defaults = {
                        "modalidad": "Alta/Baja",
                        "orden": 2,
                        "descripcion": "Ganar por encima o por debajo del numero de referencia",
                        "etiqueta_ref": True,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_altabaja,
        grupo = grupo_juego_completo,
    )
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_altabaja,
        grupo = grupo_medio_juego,
    )

    modalidad_runline = Modalidades.objects.update_or_create(
        codename = "runline",
        defaults = {
                        "modalidad": "Runline",
                        "orden": 3,
                        "descripcion": "Ganar por una diferencia entre los equipos",
                        "etiqueta_ref": False,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_runline,
        grupo = grupo_juego_completo,
    )
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_runline,
        grupo = grupo_medio_juego,
    )

    modalidad_empate = Modalidades.objects.update_or_create(
        codename = "empate",
        defaults = {
                        "modalidad": "Empate",
                        "orden": 4,
                        "descripcion": "Igual marcador entre los equipos",
                        "etiqueta_ref": False,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_empate,
        grupo = grupo_juego_completo,
    )
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_empate,
        grupo = grupo_medio_juego,
    )

    modalidad_super_runline = Modalidades.objects.update_or_create(
        codename = "super_runline",
        defaults = {
                        "modalidad": "Super Runline",
                        "orden": 5,
                        "descripcion": "Runline con mas score",
                        "etiqueta_ref": False,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_super_runline,
        grupo = grupo_combinadas,
    )

    modalidad_h_c_e = Modalidades.objects.update_or_create(
        codename = "h+c+e",
        defaults = {
                        "modalidad": "H+C+E",
                        "orden": 6,
                        "descripcion": "Sumatoria de hit mas carreras mas errores",
                        "etiqueta_ref": True,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_h_c_e,
        grupo = grupo_combinadas,
    )

    modalidad_anota_1ro = Modalidades.objects.update_or_create(
        codename = "anota_1ro",
        defaults = {
                        "modalidad": "Anota 1ro",
                        "orden": 7,
                        "descripcion": "Quien anote primero en el encuentro",
                        "etiqueta_ref": False,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_anota_1ro,
        grupo = grupo_combinadas,
    )

    modalidad_si_no = Modalidades.objects.update_or_create(
        codename = "si/no",
        defaults = {
                        "modalidad": "Si/No",
                        "orden": 8,
                        "descripcion": "Si se anota en el primer ining",
                        "etiqueta_ref": False,
                    }
    )[0]
    Modalidades_Grupos.objects.get_or_create(
        modalidad = modalidad_si_no,
        grupo = grupo_combinadas,
    )

    modalidad_ganador.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_runline,
        modalidad_anota_1ro,
    )

    modalidad_altabaja.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_si_no,
        modalidad_h_c_e,
    )

    modalidad_altabaja.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_si_no,
        modalidad_h_c_e,
    )

    modalidad_runline.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_anota_1ro,
        modalidad_ganador,
        modalidad_h_c_e,
    )

    modalidad_empate.restriction.add(
        modalidad_super_runline,
        modalidad_anota_1ro,
        modalidad_si_no,
        modalidad_ganador,
        modalidad_h_c_e,
        modalidad_altabaja,
        modalidad_runline,
    )

    modalidad_super_runline.restriction.add(
        modalidad_empate,
        modalidad_anota_1ro,
        modalidad_si_no,
        modalidad_ganador,
        modalidad_h_c_e,
        modalidad_altabaja,
        modalidad_runline,
    )

    modalidad_h_c_e.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_anota_1ro,
        modalidad_si_no,
        modalidad_altabaja,
        modalidad_runline,
    )

    modalidad_anota_1ro.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_si_no,
        modalidad_ganador,
        modalidad_h_c_e,
        modalidad_runline,
    )

    modalidad_si_no.restriction.add(
        modalidad_empate,
        modalidad_super_runline,
        modalidad_anota_1ro,
        modalidad_h_c_e,
        modalidad_altabaja,
    )

    from admin_juego.models import Condiciones

    Condiciones.objects.update_or_create(
        modalidad = modalidad_pitcher,
        defaults = {
                        "nombre": "",
                        "orden": 0,
                        "etiqueta_ref": True,
                        "equipo": False,
                        "tipo": 4,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_empate,
        defaults = {
                        "nombre": "",
                        "orden": 1,
                        "etiqueta_ref": False,
                        "equipo": False,
                        "tipo": 1,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_si_no,
        defaults = {
                        "nombre": "Si/No",
                        "orden": 2,
                        "etiqueta_ref": False,
                        "equipo": False,
                        "tipo": 2,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_ganador,
        defaults = {
                        "nombre": "",
                        "orden": 3,
                        "etiqueta_ref": False,
                        "equipo": True,
                        "tipo": 0,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_runline,
        defaults = {
                        "nombre": "",
                        "orden": 4,
                        "etiqueta_ref": True,
                        "equipo": True,
                        "tipo": 0,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_super_runline,
        defaults = {
                        "nombre": "",
                        "orden": 5,
                        "etiqueta_ref": True,
                        "equipo": True,
                        "tipo": 0,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_altabaja,
        defaults = {
                        "nombre": "Alta/Baja",
                        "orden": 6,
                        "etiqueta_ref": False,
                        "equipo": False,
                        "tipo": 2,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_h_c_e,
        defaults = {
                        "nombre": "Alta/Baja",
                        "orden": 7,
                        "etiqueta_ref": False,
                        "equipo": False,
                        "tipo": 2,
                    }
    )

    Condiciones.objects.update_or_create(
        modalidad = modalidad_anota_1ro,
        defaults = {
                        "nombre": "Visitante/Home",
                        "orden": 8,
                        "etiqueta_ref": False,
                        "equipo": False,
                        "tipo": 2,
                    }
    )

class Migration(migrations.Migration):

    dependencies = [
        ('admin_juego', '0021_auto_20150305_2257'),
    ]

    operations = [
        migrations.AddField(
            model_name='modalidades',
            name='bet',
            field=models.BooleanField(default=True, help_text='Verifique si es una modalidad de apuesta', verbose_name='¿Modalidad de apuesta? '),
            preserve_default=True,
        ),
        migrations.RunPython(MigrateDataAll),
    ]
