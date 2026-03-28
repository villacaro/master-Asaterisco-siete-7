# -*- coding: utf-8 -*-
from admin_banklotsports.settings import FORMAT_STR_DATETIME
from admin_comercializacion.models import AgenciaDataDefault, TicketsDataDefault
from admin_comercializacion.views.preferencias_views import LoadPreferences
from admin_juego.models import Deportes, GruposApuestas, JugadorTipo, Modalidades
from admin_mail.models import MessageComer
from admin_status.models import Status
from django.core.cache import cache
from django.db.models import Q
from django.utils.timezone import now
from ws_lib.views import RESTView
from ws_sportparley.settings import CACHES_CONF_TIME


class GetData(RESTView):
    process_db = 'process_getgata'

    def __init__(self):
        super(GetData, self).__init__()
        self.entrys = ['message', 'session']

    def request_valid(self, content, data, session, *args, **kwargs):
        content = super(GetData, self).request_valid(
            content, data, session, *args, **kwargs
        )

        if not content.error:
            taquilla = session.user.taquilla
            comercializadora = session.user.taquilla.agencia.get_comercializadora()
            agencia = session.user.taquilla.agencia

            content.set_message_entry(
                'info',
                {
                    'client_name': taquilla.taquilla,
                    'agencia_name': taquilla.agencia.nombre,
                    'server_datetime': now().strftime(FORMAT_STR_DATETIME),
                    'master': 1 if taquilla.is_taquilla_master else 0,
                }
            )

            gamesystem = kwargs['sistema_']
            logrossystem = kwargs['sistema_logros']

            content.set_message_entry('gamesystem_info',
                                      {
                                          'gamesystem_logo': gamesystem.get_logo(),
                                          'company': gamesystem.get_company(json=True),
                                          'theme': gamesystem.get_theme(json=True),
                                          'juegos': gamesystem.pk,
                                          'logros': logrossystem.pk,
                                      }
                                      )

            """
            Agregacion de reglas de factor de riesgo

            aqui se envia un array, en cada posicion tiene un array
            de 3 posiciones, Ejemplo:

            [ [100,200,10], [201,500,15] ]

            El primer array, quiere decir que los tickets con apuesta
            entre 100 y 200 se les aplicara un factor de 10%, y lo mismo
            para los rangos del 201 al 500 aplicando un factor de 15%, solo
            se aplica un factor por apuesta, ya que es imposible que un ticket
            este en 2 rangos al mismo tiempo, estos rangos se cargan de manera
            rigurosa cuidando que no se solapen.
            en conclusion,
            pos 0 = rango inicial
            pos 1 = rango final
            pos 2 = porcentaje a aplicar
            """
            content.set_message_entry(
                'factor_riesgo',
                comercializadora.get_factores_riesgo().factores
            )

            """
            En caso de que exista en AgenciaDataDefault everyone=True,
            para todos los clientes.
            """

            agencia_restrictions = AgenciaDataDefault.get_everyone()
            if agencia_restrictions is False:
                agencia_restrictions = LoadPreferences(agencia)

            content.set_message_entry('agencia_restrictions',
                                      {
                                          'bet_mount':
                                          {
                                              'min': agencia_restrictions.montomin,
                                              'max': agencia_restrictions.montomax
                                          },
                                          'gain': {
                                              'max': agencia_restrictions.montomax_ganancia,
                                          },
                                          'bet_count':
                                          {
                                              'min': agencia_restrictions.cantidad_apuesta_min,
                                              'max': agencia_restrictions.cantidad_apuesta_max
                                          },
                                          'expiration_days': agencia_restrictions.tiempoexpiracion,
                                          'parley':
                                          {
                                              'machos': {
                                                  'min': agencia_restrictions.parley_machos_min,
                                                  'max': agencia_restrictions.parley_machos_max
                                              },
                                              'hembras': {
                                                  'min': agencia_restrictions.parley_hembras_min,
                                                  'max': agencia_restrictions.parley_hembras_max
                                              },
                                              'empate': {
                                                  'max': agencia_restrictions.parley_empates_max,
                                              }
                                          },
                                          'cancel_ticket': agencia_restrictions.cancel_ticket,
                                      }
                                      )

            print_info = TicketsDataDefault.get_everyone_json(agencia)
            print_info['heads']['head1'] = gamesystem.nombre
            content.set_message_entry('print_info',
                                      print_info
                                      )

            status_list = cache_groups = cache.get('cache_status_get_data')
            if not status_list:
                status_list = list(
                    Status.objects.filter(
                        Q(content_type=2) | Q(content_type=8)
                    ).order_by('name').values('pk', 'name', 'codename', 'order', 'content_type')
                )
                cache.set(
                    'cache_status_get_data',
                    status_list,
                    CACHES_CONF_TIME['Consultas']['get_data_juegos'] * 7
                )

            content.set_message_entry(
                'status',
                status_list
            )

            cache_groups = cache.get('cache_groups_get_data')
            if not cache_groups:
                cache_groups = [
                    obj for obj
                    in GruposApuestas.objects.all().values(
                        'pk', 'nombre', 'orden'
                    )
                ]
                cache.set(
                    'cache_groups_get_data',
                    cache_groups,
                    CACHES_CONF_TIME['Consultas']['get_data_juegos'] * 7
                )
            content.set_message_entry('groups',
                                      cache_groups
                                      )

            cache_modalidades = cache.get('cache_modalidades_get_data')
            if not cache_modalidades:
                cache_modalidades = [
                    {
                        'pk': obj.pk,
                        'name': obj.modalidad,
                        'orden': obj.orden,
                        'restrictions': [
                            restrictions.pk
                            for restrictions in obj.restriction.all()
                        ]
                    }
                    for obj in Modalidades.objects.all().prefetch_related('restriction')
                ]
                cache_modalidades += [
                    {
                        'pk': obj.pk * -1,
                        'name': obj.nombre,
                        'orden': -1,
                        'restrictions': []
                    }
                    for obj in JugadorTipo.objects.only('pk', 'nombre').all()
                ]
                cache.set(
                    'cache_modalidades_get_data',
                    cache_modalidades,
                    CACHES_CONF_TIME['Consultas']['get_data_juegos'] * 7
                )
            content.set_message_entry('modalidades',
                                      cache_modalidades
                                      )

            content.set_message_entry('modalidades_restrictions',
                                      agencia.get_restrictions_modalidades()
                                      )

            cache_sports = cache.get('cache_sports_get_data')
            if not cache_sports:
                sports = {}
                sports['deportes'] = [
                    {
                        'pk': obj.pk,
                        'name': obj.nombre,
                        'orden': obj.orden,
                        'orden_equipos': obj.orden_equipos,
                        'count_apuesta': obj.count_apuesta,
                        'logo': obj.get_logo(),
                        'bg': obj.get_fondo(),
                        'grupos': obj
                    }
                    for obj in Deportes.objects.all().order_by('nombre')
                ]

                for deporte in sports['deportes']:
                    modalidades = [
                        {'pk': jugador_tipo['pk'] * -1}
                        for jugador_tipo in deporte['grupos']
                        .jugadortipo_set.all().values('pk')
                    ]
                    grupos = deporte['grupos'].deportes_grupos_set.all() \
                        .order_by('grupo__orden')

                    deporte['grupos'] = []
                    if modalidades:
                        deporte['grupos'].append(
                            {'pk': -1, 'modalidades': modalidades}
                        )
                    for obj in grupos:
                        grupo = obj.grupo
                        modalidades = []
                        for modalidad in grupo.modalidades_grupos_set.all() \
                                .order_by('modalidad__orden'):
                            if modalidad.deporte_restriccion.filter(
                                pk=deporte['pk']
                            ).exists():
                                continue
                            else:
                                modalidades.append(
                                    {'pk': modalidad.modalidad_id}
                                )
                        if modalidades:
                            deporte['grupos'].append(
                                {'pk': grupo.pk, 'modalidades': modalidades}
                            )
                cache_sports = sports
                cache.set(
                    'cache_sports_get_data',
                    cache_sports,
                    CACHES_CONF_TIME['Consultas']['get_data_juegos'] * 7
                )
            content.set_message_entry('sports', cache_sports['deportes'])

            restrictions = {}
            restrictions_ventas = comercializadora.get_restrictions_ventas()

            restrictions['deportes'] = list(restrictions_ventas.filter(
                deporte__isnull=False,
                grupo__isnull=True,
                modalidad__isnull=True,
            ).values('deporte_id'))

            restrictions['grupos'] = list(restrictions_ventas.filter(
                deporte__isnull=False,
                grupo__isnull=False,
                modalidad__isnull=True,
            ).values('deporte_id', 'grupo_id'))

            restrictions['modalidades'] = list(restrictions_ventas.filter(
                deporte__isnull=False,
                grupo__isnull=False,
                modalidad__isnull=False,
            ).values('deporte_id', 'grupo_id', 'modalidad_id'))

            content.set_message_entry('restrictions', restrictions)

            """
            Envio del ultimo mensaje a la taquilla
            """
            comercializadora_taquilla = session.user.taquilla.get_comercializadora()

            content.set_message_entry(
                'list_message',
                list(MessageComer.objects.filter(
                    comercializadora_id=comercializadora_taquilla,
                    read=False
                ).values_list('message_id', flat=True))
            )

        return content
