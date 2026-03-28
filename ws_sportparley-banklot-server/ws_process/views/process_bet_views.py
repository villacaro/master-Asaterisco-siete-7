# -*- coding: utf-8 -*-

from admin_comercializacion.models import Taquillas
from ws_auth.middleware import get_access_ws
from ws_lib.views import RESTView
from ws_process.process_bet.type_parley import type_parley


class Bet(RESTView):
    process_db = 'process_bet'

    def __init__(self):
        super(Bet, self).__init__()
        self.entrys = ['message', 'session']
        self.message_entrys = ['type_bet', 'total_bet', 'array_bet']

        """
            Formato de data recibida, posibles valores:
                type_bet: type_parley, type_simple, type_quiniela
                total_bet: 20.00
                array_bet: [
                    {
                        'pk': 349,
                        'logro': '+100',
                        'ref': '-0,5',
                        'ref_m': '',
                    },
                    {
                        'pk': 350,
                        'logro': '-100',
                        'ref': '',
                        'ref_m': '-0,5',
                    },
                    {
                        'pk': 351,
                        'logro': '-250',
                        'ref': '',
                        'ref_m': '',
                    },
                ]


            En caso de retornar error: mostrar el mensaje, solo se debe tomar en cuenta un mensaje de error,
            y es cuando se envia la variable 'array_bet', se envia con la misma estructura que la recibe.

            Ejemplo:

            array_bet: [
                {
                    'pk': 349,
                    'logro': '+101',
                    'ref': '-0,5',
                    'ref_m': '',
                },
            ]

            Alli se indica que de la jugada 349, el logro cambio, teniendo un nuevo valor de '+101'

        """

    def get_content_data(self):
        content = super(Bet, self).get_content_data()
        content.set_entry('error_bet', 0)
        return content

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(Bet, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            access = get_access_ws('WS_MAINTENANCE_BET', kwargs['comercializadora'])
            if not access:
                content.set_entry('error_bet', 1)
                content.set_entry(
                    'errormessage_bet',
                    'Esta opción no está disponible, intente más tarde.',
                )
            else:
                permisos = Taquillas.objects.filter(
                    pk=session.user.taquilla_id
                ).values_list(
                    'agencia__status__codename',
                    'agencia__distribuidores__status__codename',
                    'agencia__distribuidores__banca__status__codename',
                    'agencia__distribuidores__banca__bloque__status__codename',
                    'agencia__distribuidores__banca__bloque__operadora__status__codename'
                )[0]
                permissions = True
                for cadena in set(permisos):
                    # solo recorro lo necesario con set quito lo repetido :)
                    if cadena != 'status_activo':
                        permissions = False
                        break

                if permissions:

                    process = type_parley(
                        session=session,
                        sistema=kwargs['sistema_'],
                        type_bet=self.data_object.get_entry('type_bet'),
                        total_bet=self.data_object.get_entry('total_bet'),
                        array_bet=self.data_object.get_entry('array_bet'),
                        content=content
                    )
                    """
                    process = type_parley(
                        user=session.user,
                        sistema=kwargs['sistema_'],
                        type_bet='type_parley',
                        total_bet=20,
                        array_bet=[
                                {
                                    'pk': 138355,
                                    'logro': '+701',
                                    'ref': '',
                                    'ref_m': '',
                                },
                                {
                                    'pk': 138353,
                                    'logro': '+601',
                                    'ref': '-2',
                                    'ref_m': '',
                                },
                                {
                                    'pk': 138339,
                                    'logro': '+600',
                                    'ref': '-2',
                                    'ref_m': '',
                                },
                            ],
                        content=content
                    )
                    """

                    bandera, obj_error = process.check_exists_porcentajes()
                    if not bandera:
                        content.set_entry('error_bet', 1)
                        content.set_entry(
                            'errormessage_bet',
                            'No se encontraron porcentajes definidos a '
                            'nivel de {0}, contacte con soporte técnico.'.format(
                                obj_error._meta.verbose_name
                            )
                        )
                    else:
                        process.run()
                    content.error = False
                else:
                    content.error = False
                    content.set_entry('error_bet', 1)
                    content.set_entry(
                        'errormessage_bet',
                        'No tiene permisos de venta, contacte con soporte técnico.'
                    )

        return content
