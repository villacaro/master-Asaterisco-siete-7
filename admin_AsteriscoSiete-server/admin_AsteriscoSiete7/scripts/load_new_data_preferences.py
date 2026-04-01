def run(*args):
    """
         >> python manage.py runscript load_new_data_preferences
    """
    from admin_comercializacion.models import GroupPreferences, TypePreferences, \
        DefaultPreferences
    from admin_users.models import UserProfile
    from django.core.cache import cache

    cache.clear()

    #####################################################################
    print('Creando Grupos de preferencias')
    group_bet = GroupPreferences.objects.update_or_create(
        codename='group_bet',
        defaults={
            'name': 'Apuesta',
            'order': 1
        }
    )

    group_parley = GroupPreferences.objects.update_or_create(
        codename='group_parley',
        defaults={
            'name': 'Parley',
            'order': 2
        }
    )

    group_ticket = GroupPreferences.objects.update_or_create(
        codename='group_ticket',
        defaults={
            'name': 'Ticket',
            'order': 3
        }
    )

    group_finance = GroupPreferences.objects.update_or_create(
        codename='group_finance',
        defaults={
            'name': 'Finanzas',
            'order': 4
        }
    )
    print('Grupos de preferencias creados')
#####################################################################

#####################################################################
    comparison_codenames = {
        'codename_min': 1,
        'codename_max': 2,
        'codename_free': 3,
    }

    comparison_type = {
        'codename_int': 1,
        'codename_decimal': 2,
        'codename_string': 3,
    }

    profiles = UserProfile.objects.all().exclude(
        codename='userprofile_master'
    )
#####################################################################
    print('Creando tipos de preferencias')

#####################################################################
    print(group_bet[0])

    preference_amount_min = TypePreferences.objects.update_or_create(
        codename='preference_amount_min',
        defaults={
            'name': 'Monto mínimo Bs.',
            'comparison': comparison_codenames['codename_min'],
            'order': 1,
            'group': group_bet[0],
            'type_data': comparison_type['codename_decimal'],
        }
    )
    preference_amount_min[0].profile.add(*profiles)
    #
    #
    preference_amount_max = TypePreferences.objects.update_or_create(
        codename='preference_amount_max',
        defaults={
            'name': 'Monto máximo Bs.',
            'comparison': comparison_codenames['codename_max'],
            'order': 2,
            'group': group_bet[0],
            'type_data': comparison_type['codename_decimal'],
        }
    )
    preference_amount_max[0].profile.add(*profiles)
    #
    #
    preference_amount_price_max = TypePreferences.objects.update_or_create(
        codename='preference_amount_price_max',
        defaults={
            'name': 'Monto de premio por ticket máximo Bs.',
            'comparison': comparison_codenames['codename_max'],
            'order': 3,
            'group': group_bet[0],
            'distribute': True,
            'type_data': comparison_type['codename_decimal'],
        }
    )
    preference_amount_price_max[0].profile.add(*profiles)
    #
    #
    preference_amount_price_clone_max = TypePreferences.objects.update_or_create(
        codename='preference_amount_price_clone_max',
        defaults={
            'name': 'Monto de premio en tickets clonados máximo Bs.',
            'comparison': comparison_codenames['codename_max'],
            'order': 4,
            'group': group_bet[0],
            'distribute': True,
            'type_data': comparison_type['codename_decimal'],
        }
    )
    preference_amount_price_clone_max[0].profile.add(*profiles)

#####################################################################

    print(group_parley[0])

    preference_quantity_combinations_min = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_min',
        defaults={
            'name': 'Cantidad de combinaciones mínimo',
            'comparison': comparison_codenames['codename_min'],
            'order': 1,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_min[0].profile.add(*profiles)
    #
    #
    preference_quantity_combinations_max = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_max',
        defaults={
            'name': 'Cantidad de combinaciones máximo',
            'comparison': comparison_codenames['codename_max'],
            'order': 2,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_max[0].profile.add(*profiles)
    #
    #
    preference_quantity_combinations_male_min = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_male_min',
        defaults={
            'name': 'Cantidad de combinaciones de machos mínimo',
            'comparison': comparison_codenames['codename_min'],
            'order': 3,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_male_min[0].profile.add(*profiles)
    #
    #
    preference_quantity_combinations_male_max = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_male_max',
        defaults={
            'name': 'Cantidad de combinaciones de machos máximo',
            'comparison': comparison_codenames['codename_max'],
            'order': 4,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_male_max[0].profile.add(*profiles)
    #
    #
    preference_quantity_combinations_female_min = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_female_min',
        defaults={
            'name': 'Cantidad de combinaciones de hembras mínimo',
            'comparison': comparison_codenames['codename_min'],
            'order': 5,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_female_min[0].profile.add(*profiles)
    #
    #
    preference_quantity_combinations_female_max = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_female_max',
        defaults={
            'name': 'Cantidad de combinaciones de hembras máximo',
            'comparison': comparison_codenames['codename_max'],
            'order': 6,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_female_max[0].profile.add(*profiles)
    #
    #
    preference_quantity_combinations_draw_max = TypePreferences.objects.update_or_create(
        codename='preference_quantity_combinations_draw_max',
        defaults={
            'name': 'Cantidad de combinaciones de empate máximo',
            'comparison': comparison_codenames['codename_max'],
            'order': 7,
            'group': group_parley[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_quantity_combinations_draw_max[0].profile.add(*profiles)
#####################################################################

    print(group_ticket[0])

    preference_time_expire_max = TypePreferences.objects.update_or_create(
        codename='preference_time_expire_max',
        defaults={
            'name': 'Tiempo de expiración (Días).',
            'comparison': comparison_codenames['codename_max'],
            'order': 1,
            'group': group_ticket[0],
            'type_data': comparison_type['codename_int'],
        }
    )
    preference_time_expire_max[0].profile.add(*profiles)
    #
    #
    preference_title = TypePreferences.objects.update_or_create(
        codename='preference_title',
        defaults={
            'name': 'Titulo',
            'comparison': comparison_codenames['codename_free'],
            'order': 2,
            'group': group_ticket[0],
            'type_data': comparison_type['codename_string'],
        }
    )
    preference_title[0].profile.add(*profiles.filter(
        codename__in=['userprofile_bloque', 'userprofile_banca']
    )
    )
    #
    #
    preference_foot = TypePreferences.objects.update_or_create(
        codename='preference_foot',
        defaults={
            'name': 'Pie',
            'comparison': comparison_codenames['codename_free'],
            'order': 3,
            'group': group_ticket[0],
            'type_data': comparison_type['codename_string'],
        }
    )
    preference_foot[0].profile.add(*profiles.filter(
        codename__in=['userprofile_bloque', 'userprofile_banca']
    )
    )
#####################################################################

    print(group_finance[0])

    preference_amount_rental = TypePreferences.objects.update_or_create(
        codename='preference_amount_rental',
        defaults={
            'name': 'Monto de alquiler por taquilla Bs.',
            'comparison': comparison_codenames['codename_max'],
            'order': 1,
            'group': group_finance[0],
            'type_data': comparison_type['codename_decimal'],
        }
    )
    preference_amount_rental[0].profile.add(*profiles.filter(
        codename__in=['userprofile_bloque', 'userprofile_banca']
    )
    )
    #
    #
    preference_amount_rental_frequency = TypePreferences.objects.update_or_create(
        codename='preference_amount_rental_frequency',
        defaults={
            'name': 'Frecuencia de cobro de alquiler por taquilla',
            'comparison': comparison_codenames['codename_free'],
            'order': 2,
            'group': group_finance[0],
            'edit': False,
            'type_data': comparison_type['codename_string'],
        }
    )
    preference_amount_rental_frequency[0].profile.add(*profiles.filter(
        codename__in=['userprofile_bloque', 'userprofile_banca']
    )
    )
    #
    #
    preference_queda_frequency = TypePreferences.objects.update_or_create(
        codename='preference_queda_frequency',
        defaults={
            'name': 'Frecuencia de corte de la queda',
            'comparison': comparison_codenames['codename_free'],
            'order': 3,
            'group': group_finance[0],
            'edit': False,
            'type_data': comparison_type['codename_string'],
        }
    )
    preference_queda_frequency[0].profile.add(*profiles.filter(
        codename__in=['userprofile_bloque', 'userprofile_banca']
    )
    )
    print('Tipo de preferencias creadas')
#####################################################################

    print('Creando datos por defecto para los tipos de preferencias')

    DefaultPreferences.objects.bulk_create([

        DefaultPreferences(
            value=20,
            default=True,
            typepreference=preference_amount_min[0],
        ),
        DefaultPreferences(
            value=5000,
            default=True,
            typepreference=preference_amount_max[0],
        ),
        DefaultPreferences(
            value=10000,
            default=True,
            typepreference=preference_amount_price_max[0],
        ),
        DefaultPreferences(
            value=20000,
            default=True,
            typepreference=preference_amount_price_clone_max[0],
        ),

        DefaultPreferences(
            value=3,
            default=True,
            typepreference=preference_quantity_combinations_min[0],
        ),
        DefaultPreferences(
            value=8,
            default=True,
            typepreference=preference_quantity_combinations_max[0],
        ),
        DefaultPreferences(
            value=0,
            default=True,
            typepreference=preference_quantity_combinations_male_min[0],
        ),
        DefaultPreferences(
            value=4,
            default=True,
            typepreference=preference_quantity_combinations_male_max[0],
        ),
        DefaultPreferences(
            value=0,
            default=True,
            typepreference=preference_quantity_combinations_female_min[0],
        ),
        DefaultPreferences(
            value=20,
            default=True,
            typepreference=preference_quantity_combinations_female_max[0],
        ),
        DefaultPreferences(
            value=5,
            default=True,
            typepreference=preference_quantity_combinations_draw_max[0],
        ),

        DefaultPreferences(
            value=4,
            default=True,
            typepreference=preference_time_expire_max[0],
        ),
        DefaultPreferences(
            value='',
            default=True,
            typepreference=preference_title[0],
        ),
        DefaultPreferences(
            value='',
            default=True,
            typepreference=preference_foot[0],
        ),

        DefaultPreferences(
            value=1000,
            default=True,
            typepreference=preference_amount_rental[0],
        ),
        DefaultPreferences(
            value='frecuencia_mensual',
            default=True,
            typepreference=preference_amount_rental_frequency[0],
        ),
        DefaultPreferences(
            value='frecuencia_mensual',
            default=True,
            typepreference=preference_queda_frequency[0],
        ),
    ])

    print('Datos por defecto creados')
#####################################################################
    """
    print('Exportando datos de preferenciascadena al nuevo de modelo de preferences')

    preferenciascadenas = PreferenciasCadena.objects.all().exclude(
        preferencia__tipo__codename='codename_factor_riesgo'
    )

    keys_new = {
        'codename_montomin': 'preference_amount_min',
        'codename_montomax': 'preference_amount_max',
        'codename_montomax_ganancia': 'preference_amount_price_max',
        'codename_cantidad_apuesta_max': 'preference_quantity_combinations_max',
        'codename_cantidad_apuesta_min': 'preference_quantity_combinations_min',
        'codename_tiempoexpiracion': 'preference_time_expire_max',
        'codename_parley_machos_max': 'preference_quantity_combinations_male_max',
        'codename_parley_machos_min': 'preference_quantity_combinations_male_min',
        'codename_parley_hembras_max': 'preference_quantity_combinations_female_max',
        'codename_parley_hembras_min': 'preference_quantity_combinations_female_min',
        'codename_parley_clonados_maxima_ganancia': 'preference_amount_price_clone_max',
        'codename_monto_alquiler': 'preference_amount_rental',
        'codename_frecuencia_monto_alquiler': 'preference_amount_rental_frequency',
        'codename_frecuencia_queda': 'preference_queda_frequency',
        'codename_parley_empates_max': 'preference_quantity_combinations_draw_max',
        'codename_ticket_titulo': 'preference_title',
        'codename_ticket_pie': 'preference_foot',
    }

    preferencesArray = []
    for preferencia in preferenciascadenas:
        if preferencia.valor:
            parent = preferencia.get_object().get_origen()
            if parent.prefix_filter != 'operadora':
                kwargs = {}
                kwargs[parent.prefix_filter + '_id'] = parent.id
                kwargs['preferencia_id'] = preferencia.preferencia.id
                try:
                    preferenciacadena = PreferenciasCadena.objects.get(
                        **kwargs
                    )
                except Exception:
                    preferenciacadena = None

                if preferenciacadena:
                    if preferenciacadena.valor == preferencia.valor:
                        msg = 'Excluida por igualdad con padre {0} -> {1}'.format(
                            str(preferencia.get_object()),
                            str(parent),
                        )
                        print(msg)
                        continue

            preference = Preferences(
                value=preferencia.valor,
                typepreference=TypePreferences.objects.get(
                    codename=keys_new[preferencia.preferencia.tipo.codename]
                ),
                comercializacion=preferencia.get_object().get_comercializadora()
            )
            preferencesArray.append(preference)
        else:
            msg = 'Excluida por valor nulo {0}'.format(
                str(preferencia.get_object()),
            )
            print(msg)

    print('Preferencias a procesar de la tabla PreferenciasCadena {0}'.format(len(preferencesArray)))
    Preferences.objects.bulk_create(
        preferencesArray
    )

    preferencesArray = []
    agencias = Agencias.objects.all()
    total = len(agencias)
    print("Total de agencias {0}".format(total))
    count = 0
    for agencia in agencias:
        ##############################################################################################
        if agencia.montomin != float(agencia.distribuidores
                                     .get_preference_value_by_codename('preference_amount_min')):
            preference = Preferences(
                value=agencia.montomin,
                typepreference=TypePreferences.objects.get(
                    codename='preference_amount_min'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.montomax != float(agencia.distribuidores.get_preference_value_by_codename('preference_amount_max')):
            preference = Preferences(
                value=agencia.montomax,
                typepreference=TypePreferences.objects.get(
                    codename='preference_amount_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.montomax_ganancia != float(
                agencia.distribuidores.get_preference_value_by_codename('preference_amount_price_max')):
            preference = Preferences(
                value=agencia.montomax_ganancia,
                typepreference=TypePreferences.objects.get(
                    codename='preference_amount_price_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.parley_clonados_maxima_ganancia != float(
                agencia.distribuidores.get_preference_value_by_codename('preference_amount_price_clone_max')):
            preference = Preferences(
                value=agencia.parley_clonados_maxima_ganancia,
                typepreference=TypePreferences.objects.get(
                    codename='preference_amount_price_clone_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)
        ################################################################################################
        if agencia.cantidad_apuesta_min != int(
            float(agencia.distribuidores
                  .get_preference_value_by_codename('preference_quantity_combinations_min'))):
            preference = Preferences(
                value=agencia.cantidad_apuesta_min,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_min'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.cantidad_apuesta_max != int(
            float(agencia.distribuidores
                  .get_preference_value_by_codename('preference_quantity_combinations_max'))):
            preference = Preferences(
                value=agencia.cantidad_apuesta_max,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.parley_machos_min != int(float(
                agencia.distribuidores.get_preference_value_by_codename('preference_quantity_combinations_male_min'))):
            preference = Preferences(
                value=agencia.parley_machos_min,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_male_min'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.parley_machos_max != int(float(
                agencia.distribuidores.get_preference_value_by_codename('preference_quantity_combinations_male_max'))):
            preference = Preferences(
                value=agencia.parley_machos_max,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_male_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.parley_hembras_min != int(float(
                agencia.distribuidores.get_preference_value_by_codename(
                    'preference_quantity_combinations_female_min'))):
            preference = Preferences(
                value=agencia.parley_hembras_min,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_female_min'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.parley_hembras_max != int(
                float(agencia.distribuidores.get_preference_value_by_codename(
                    'preference_quantity_combinations_female_max'))):
            preference = Preferences(
                value=agencia.parley_hembras_max,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_female_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.parley_empates_max != int(float(
                agencia.distribuidores.get_preference_value_by_codename(
                    'preference_quantity_combinations_draw_max'))):
            preference = Preferences(
                value=agencia.parley_empates_max,
                typepreference=TypePreferences.objects.get(
                    codename='preference_quantity_combinations_draw_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)
        ########################################################################################

        if agencia.tiempoexpiracion != int(agencia.distribuidores
                                           .get_preference_value_by_codename('preference_time_expire_max')):
            preference = Preferences(
                value=agencia.tiempoexpiracion,
                typepreference=TypePreferences.objects.get(
                    codename='preference_time_expire_max'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        if agencia.ticket_titulo:
            if agencia.ticket_titulo != agencia.distribuidores\
                    .get_preference_value_by_codename('preference_title'):
                preference = Preferences(
                    value=agencia.ticket_titulo,
                    typepreference=TypePreferences.objects.get(
                        codename='preference_title'
                    ),
                    comercializacion=agencia.get_comercializadora()
                )
                preferencesArray.append(preference)

        if agencia.ticket_pie:
            if agencia.ticket_pie != agencia.distribuidores\
                    .get_preference_value_by_codename('preference_foot'):
                preference = Preferences(
                    value=agencia.ticket_pie,
                    typepreference=TypePreferences.objects.get(
                        codename='preference_foot'
                    ),
                    comercializacion=agencia.get_comercializadora()
                )
                preferencesArray.append(preference)
        ########################################################################################

        if agencia.frecuencia_queda:
            if agencia.frecuencia_queda != agencia.distribuidores\
                    .get_preference_value_by_codename('preference_queda_frequency'):
                preference = Preferences(
                    value=agencia.frecuencia_queda,
                    typepreference=TypePreferences.objects.get(
                        codename='preference_queda_frequency'
                    ),
                    comercializacion=agencia.get_comercializadora()
                )
                preferencesArray.append(preference)

        if agencia.frecuencia_monto_alquiler:
            if agencia.frecuencia_monto_alquiler != agencia.distribuidores\
                    .get_preference_value_by_codename('preference_amount_rental_frequency'):
                preference = Preferences(
                    value=agencia.frecuencia_monto_alquiler,
                    typepreference=TypePreferences.objects.get(
                        codename='preference_amount_rental_frequency'
                    ),
                    comercializacion=agencia.get_comercializadora()
                )
                preferencesArray.append(preference)

        if agencia.monto_alquiler != float(agencia.distribuidores
                                           .get_preference_value_by_codename('preference_amount_rental')):
            preference = Preferences(
                value=agencia.monto_alquiler,
                typepreference=TypePreferences.objects.get(
                    codename='preference_amount_rental'
                ),
                comercializacion=agencia.get_comercializadora()
            )
            preferencesArray.append(preference)

        count += 1
        print('Agencias procesadas {0}'.format(count))

    print('Preferencias a procesar de la tabla Agencias {0}'.format(len(preferencesArray)))
    Preferences.objects.bulk_create(
        preferencesArray
    )
    print('Exportados datos de preferenciascadena al nuevo de modelo de preferences')

    print('*****MIGRACION DE DATOS DE PREFERENCIAS COMPLETADA*****')
    """
