# -*- coding: utf-8 -*-
from datetime import timedelta

from admin_banklotsports.settings import DEBUG, FORMAT_STR_DATE_REPORTS, FORMAT_STR_DATETIME_SECONDS
from admin_juego.models import (
    Deportes, Deportes_Grupos, Encuentros, EncuentrosDetail, Equipos, EventNotification, GruposJuego, Jornadas,
    Jugadas, SistemaJuego, Temporadas,
)
from admin_resultados.models import Anotaciones, AnotacionesDetail, Resultados
from admin_status.models import Status
from django.core.cache import cache
from django.db.models import Q
from django.template import Context, loader
from django.utils.timezone import now
from ws_lib.date import hora_23, hora_cero, strFecha
from ws_sportparley.settings import CACHES_CONF_TIME


class ParleyResult(object):
    """

    Se definen 2 funiones para consultar los resultados,
    uno con respuesta sencilla y otro con respuesta compleja devolviendo una tablas

    """

    def __init__(self, session):
        super(ParleyResult, self).__init__()
        session_cache = cache.get(
            'ws_session_{0}'.format(session.session.pk)
        )

        comercializadora = session.user.taquilla.agencia.get_comercializadora()

        if session_cache:
            self.sistema = session_cache['sistema_juego'].pk
        else:
            self.sistema = SistemaJuego.objects.get_sistema_juego_by_comercializadora(
                comercializadora
            ).pk

        self.sistema_resultados = SistemaJuego.objects.get_sistema_resultados_by_comercializadora(
            comercializadora
        )

    def get_result_by_deports(self, fecha_ini, fecha_fin, deporte):
        message = []
        if '{0}'.format(deporte) == '0':
            deportes = Deportes.objects.all()
        else:
            deportes = Deportes.objects.filter(
                pk=deporte
            )

        fecha_ini = fecha_ini + hora_cero
        fecha_fin = fecha_fin + hora_23

        for deporte in deportes:
            resultados = Resultados.objects.filter(
                encuentro__jornada__sistema_id=self.sistema,
                encuentro__jornada__temporadas__torneo__deporte=deporte,
                encuentro__horajuego__range=(fecha_ini, fecha_fin),
                sistema=self.sistema_resultados,
                status__codename__in=['status_habilitado', 'status_valido_no_terminado'],
                encuentro__status__codename__in=['status_habilitado', 'status_valido_no_terminado'],
            ).distinct('pk')

            for resultado in resultados:
                json_resultado = {}
                detalle_enuentros = resultado.encuentro.encuentrosdetail_set.order_by('-indice')

                json_equipos = []
                for x in detalle_enuentros:
                    equipos_data = {}
                    equipos_data['nombre'] = x.equipos_temporadas.equipo.nombre

                    equipos_data['logo'] = '' if x.equipos_temporadas.equipo.logo == '' \
                        else x.equipos_temporadas.equipo.logo.url

                    json_equipos.append(equipos_data)

                objFecha = strFecha(resultado.encuentro.horajuego)
                json_resultado['id'] = resultado.encuentro.pk
                json_resultado['fecha'] = objFecha.getFecha()
                json_resultado['hora'] = objFecha.getHora()
                json_resultado['grupo'] = '' if resultado.encuentro.grupo is None \
                    else resultado.encuentro.grupo.nombre

                json_resultado['jornada'] = resultado.encuentro.jornada.jornada
                json_resultado['temporada'] = resultado.encuentro.jornada.temporadas.nombre
                json_resultado['torneo'] = resultado.encuentro.jornada.temporadas.torneo.nombre
                json_resultado['equipos'] = json_equipos

                json_resultado['resultado'] = {}
                json_resultado['resultado']['primera_mita'] = []
                for anotacion in resultado.anotaciones_set.filter(
                    grupo__codename='medio_juego'
                ):
                    for anotacion_detail in anotacion.anotacionesdetail_set.exclude(
                        condicion__isnull=False
                    ).order_by('-encuentro_detail__indice'):
                        json_anotacion = {}
                        json_anotacion['equipo'] = anotacion_detail \
                            .encuentro_detail.equipos_temporadas.equipo.nombre

                        json_anotacion['puntaje'] = str(anotacion_detail.puntaje)
                        json_resultado['resultado']['primera_mita'].append(json_anotacion)

                json_resultado['resultado']['juego_completo'] = []
                for anotacion in resultado.anotaciones_set.filter(
                    grupo__codename='juego_completo'
                ):
                    for anotacion_detail in anotacion.anotacionesdetail_set.exclude(
                        condicion__isnull=False
                    ).order_by('-encuentro_detail__indice'):
                        json_anotacion = {}
                        json_anotacion['equipo'] = anotacion_detail \
                            .encuentro_detail.equipos_temporadas.equipo.nombre

                        json_anotacion['puntaje'] = str(anotacion_detail.puntaje)
                        json_resultado['resultado']['juego_completo'].append(
                            json_anotacion
                        )

                if (
                    len(json_resultado['resultado']['primera_mita']) or
                    len(json_resultado['resultado']['juego_completo'])
                ):
                    message.append(json_resultado)

        return message

    def get_resulttable_by_deports(self, fecha, deporte):
        self.template_name = 'resulttable.html'

        message = []

        if fecha and self.sistema:
            encuentros_list = Encuentros.objects.filter(
                horajuego__range=(fecha + hora_cero, fecha + hora_23),
                jornada__sistema=self.sistema,
                status__codename__in=['status_habilitado', 'status_valido_no_terminado'],
            )

            if int(deporte):
                encuentros_list = encuentros_list.filter(
                    jornada__temporadas__torneo__deporte_id=deporte,
                )
        else:
            encuentros_list = Encuentros.objects.none()

        temporadas_objects = encuentros_list.values_list('jornada__temporadas_id', flat=True)
        temporadas = list(set(temporadas_objects))

        context = {}
        context['head'] = {}
        context['head']['sistema'] = SistemaJuego.objects.get(pk=self.sistema).nombre
        if int(deporte):
            context['head']['deporte'] = Deportes.objects.get(pk=deporte).nombre
        else:
            context['head']['deporte'] = "Todos"

        context['head']['fecha'] = fecha

        context['consulta_new'] = []
        for temporada in temporadas_objects:
            resultado = False
            encuentros = encuentros_list.filter(
                jornada__temporadas_id=temporada
            )
            for encuentro in encuentros:
                resultado = encuentro.get_exists_resultados(
                    self.sistema_resultados
                )
                if resultado:
                    if encuentro.get_resultado(
                        self.sistema_resultados
                    ).status.codename in ['status_habilitado', 'status_valido_no_terminado']:
                        break
                    else:
                        resultado = False

            if resultado is False:
                try:
                    temporadas.remove(temporada)
                except Exception:
                    pass

        for temporada_pk in temporadas:
            temporada = Temporadas.objects.get(pk=temporada_pk)
            json_liga = {}
            json_liga['nombre'] = '{0} {1}'.format(
                temporada.torneo.nombre,
                temporada.nombre
            )
            json_liga['logo'] = temporada.torneo.logo
            json_liga['grupos'] = []
            json_liga['encuentros'] = []

            grupo_json = {}
            grupo_json['nombre'] = 'Participantes'
            grupo_json['modalidades'] = []
            json_liga['grupos'].append(grupo_json)
            for deporte_grupo in Deportes_Grupos.objects.filter(
                deporte=temporada.torneo.deporte,
            ).exclude(
                grupo__codename='referencia'
            ).order_by('grupo__orden'):
                grupo_json = {}
                grupo_json['nombre'] = deporte_grupo.grupo.nombre
                grupo_json['modalidades'] = []
                modalidades_grupos_list = deporte_grupo.grupo.modalidades_grupos_set.all().exclude(
                    modalidad__codename__in=['empate', 'games']
                )
                for modalidad_grupo in modalidades_grupos_list.all(
                ).order_by('modalidad__orden'):
                    grupo_json['modalidades'].append(
                        modalidad_grupo.modalidad.modalidad)

                json_liga['grupos'].append(grupo_json)

            for obj in encuentros_list.filter(
                jornada__temporadas_id=temporada.id
            ):
                try:
                    resultado = obj.resultados_set.get(
                        sistema=self.sistema_resultados
                    )

                    if resultado.status.codename in ['status_habilitado', 'status_valido_no_terminado']:
                        pass
                    else:
                        resultado = None

                except Resultados.DoesNotExist:
                    resultado = None

                if resultado is not None:
                    json_encuentro = {}
                    json_encuentro['hora'] = obj.horajuego
                    json_encuentro['equipos'] = []

                    anotaciones = Anotaciones.objects.filter(
                        resultado=resultado,
                    ).order_by('grupo__orden')

                    json_externo = []

                    for equipo in obj.encuentrosdetail_set.all().order_by('-indice'):
                        json_interno = []
                        td_object = {}
                        td_object['row'] = 1
                        td_object['puntaje'] = equipo.equipos_temporadas.equipo.nombre
                        json_interno.append(td_object)

                        for anotacion in anotaciones:
                            if anotacion.grupo.codename != 'combinadas':
                                # Condicion de ganador
                                detail = AnotacionesDetail.objects.filter(
                                    anotacion=anotacion,
                                    encuentro_detail=equipo,
                                    condicion__isnull=True
                                )[0]
                                td_object = {}
                                td_object['row'] = 1
                                if detail.puntaje is None:
                                    td_object['puntaje'] = ''
                                else:
                                    td_object['puntaje'] = detail.puntaje
                                json_interno.append(td_object)
                                # Condicion alta/baja
                                td_object = {}
                                td_object['row'] = 2
                                if anotacion.anotacionesdetail_set.filter(
                                    encuentro_detail__isnull=True
                                ).order_by('-condicion').exists():
                                    for detail in anotacion.anotacionesdetail_set.filter(
                                        encuentro_detail__isnull=True
                                    ).order_by('-condicion'):
                                        if detail.puntaje is None:
                                            td_object['puntaje'] = ''
                                        else:
                                            td_object['puntaje'] = str(detail.puntaje)
                                else:
                                    td_object['puntaje'] = ''
                                json_interno.append(td_object)
                                # Condicion Runline
                                td_object = {}
                                td_object['row'] = 1
                                if anotacion.anotacionesdetail_set.filter(
                                    encuentro_detail=equipo,
                                    condicion__isnull=False
                                ).order_by('-condicion').exists():
                                    for detail in anotacion.anotacionesdetail_set.filter(
                                        encuentro_detail=equipo,
                                        condicion__isnull=False
                                    ).order_by('-condicion'):
                                        if detail.puntaje is not None:
                                            if detail.puntaje > 0:
                                                text = "+" + str(detail.puntaje)
                                            else:
                                                text = detail.puntaje
                                        else:
                                            text = ''
                                        td_object['puntaje'] = text
                                else:
                                    td_object['puntaje'] = ''
                                json_interno.append(td_object)
                            else:
                                # SuperRunline
                                td_object = {}
                                td_object['row'] = 1
                                try:
                                    detail = AnotacionesDetail.objects.get(
                                        anotacion=anotacion,
                                        encuentro_detail=equipo,
                                        condicion__isnull=False
                                    )
                                    if detail.puntaje is not None:
                                        if detail.puntaje > 0:
                                            text = "+" + str(detail.puntaje)
                                        else:
                                            text = detail.puntaje
                                    else:
                                        text = ''
                                    td_object['puntaje'] = text
                                except Exception:
                                    td_object['puntaje'] = ''
                                json_interno.append(td_object)
                                details = AnotacionesDetail.objects.filter(
                                    anotacion=anotacion,
                                    condicion__isnull=False,
                                    encuentro_detail__isnull=True
                                ).order_by('id')
                                for detail in details:
                                    td_object = {}
                                    td_object['row'] = 2
                                    if detail.get_label_customize() is None:
                                        td_object['puntaje'] = ''
                                    else:
                                        td_object['puntaje'] = detail.get_label_customize()
                                    json_interno.append(td_object)
                        json_externo.append(json_interno)
                    json_encuentro['resultados'] = json_externo
                    json_liga['encuentros'].append(json_encuentro)
            context['consulta_new'].append(json_liga)

        # Renderizar plantilla
        template = loader.get_template(self.template_name)
        cont = Context({
            'consulta_new': context['consulta_new'],
            'head': context['head'],
            'sistema_resultados': self.sistema_resultados,
        })
        rendered = template.render(cont)
        message = rendered.replace('\n', '')

        return message


class DatosJuegos(object):
    """
        Esta clase de usa para consultar toda la data de juegos,
        por las taquillas
    """

    def __init__(self, session, kwargs):
        super(DatosJuegos, self).__init__()
        self.session = session
        self.session_id = self.session.pk
        self.sistema_juego = kwargs['sistema_']
        self.sistema_logros = kwargs['sistema_logros']
        self.comercializadora = kwargs['comercializadora']

        self.fecha = now().date()
        self.fecha_hora = now()

        fecha_str_init = self.fecha_hora.strftime(FORMAT_STR_DATE_REPORTS)
        if DEBUG:
            fecha_str_fin = (self.fecha_hora + timedelta(days=30)).strftime(FORMAT_STR_DATE_REPORTS)
        else:
            fecha_str_fin = fecha_str_init

        self.fecha_range = (fecha_str_init + hora_cero, fecha_str_fin + hora_23)

        self.key_cache_sistema = '{0}_{1}'.format(
            self.sistema_juego.pk,
            self.sistema_logros.pk,
        )

        self.status_habilitado = Status.get_status_by_codename('status_habilitado')
        self.status_pendiente = Status.get_status_by_codename('status_pendiente')

    def get_querry_notification(self):
        if self.sistema_juego.pk == self.sistema_logros.pk:
            querry_set = EventNotification.objects.filter(
                sistema=self.sistema_juego.pk
            )
        else:
            querry_set = EventNotification.objects.filter(
                sistema__in=[self.sistema_juego.pk, self.sistema_logros.pk]
            )
        return querry_set

    def get_update(self):
        querry_set = self.get_querry_notification().filter(
            in_production=True
        ).order_by('-date_production')

        try:
            return querry_set[0].date_production.strftime(FORMAT_STR_DATETIME_SECONDS)
        except Exception:
            return ''

    def get_notifications_lost(self, pk_origin, data_origin):
        notificaciones = self.get_querry_notification().filter(
            pk_origin=pk_origin,
            data_origin=data_origin,
        )

        return self.process_notifications(notificaciones)

    def get_notifications(self, data_fecha_old, data_fecha_new):
        fecha_old = now().strptime(data_fecha_old, FORMAT_STR_DATETIME_SECONDS)
        fecha_new = now().strptime(data_fecha_new, FORMAT_STR_DATETIME_SECONDS)

        notificaciones = self.get_querry_notification().filter(
            in_production=True,
            # Sumamos un segundo a la fecha de inicio para no bajar actualizaciones ya descargadas
            # Sumamos un segundo a la fecha de fin, para abarcar error de redondeo
            date_production__range=(fecha_old + timedelta(seconds=1), fecha_new + timedelta(seconds=1))
        ).order_by('data_origin')

        return self.process_notifications(notificaciones)

    def process_notifications(self, notificaciones):
        deportes_exclude_exists = self.get_deportes_exclude_exists()
        if deportes_exclude_exists:
            deportes_restri = self.get_deportes_exclude()

        message = []
        for obj in notificaciones.only('data_origin', 'pk_origin', 'data'):
            valid = True
            if deportes_exclude_exists:
                if obj.data_origin == 1 and obj.pk_origin in deportes_restri:
                    valid = False
                elif obj.data_origin > 1 and 'deporte_id' in obj.data and obj.data['deporte_id'] in deportes_restri:
                    # Todas las demas notificaciones
                    valid = False

            if valid:
                message.append(
                    {
                        'data_origin': obj.data_origin,
                        'pk_origin': obj.pk_origin,
                        'data': obj.data,
                    }
                )

        return message

    def get_deportes_exclude_exists(self):
        return self.comercializadora.get_restrictions_ventas().filter(
            deporte__isnull=False,
            grupo__isnull=True,
            modalidad__isnull=True,
        ).exists()

    def get_deportes_exclude(self):
        return self.comercializadora.get_restrictions_ventas().filter(
            deporte__isnull=False,
            grupo__isnull=True,
            modalidad__isnull=True,
        ).values_list('deporte_id', flat=True)

    def get_juegos_all(self):
        # generar cache
        deportes_exclude_exists = self.get_deportes_exclude_exists()
        if deportes_exclude_exists:
            message = None
        else:
            message = cache.get('all_{0}'.format(self.key_cache_sistema))

        if not message or DEBUG:
            update = self.fecha_hora.strftime(FORMAT_STR_DATETIME_SECONDS)
            respuesta = self.get_juegos_filter(deporte_id=None)
            respuesta['fecha'] = update
            if not deportes_exclude_exists:
                cache.set(
                    'all_{0}'.format(self.key_cache_sistema),
                    respuesta,
                    CACHES_CONF_TIME['getJuegos']['all']
                )
            return respuesta
        else:
            return message

    def get_juegos_filter(self, deporte_id):
        message = self.get_deportes(deporte_id=deporte_id)
        equipos = {}
        grupos = {}

        self.keys_system_vec = [self.sistema_juego.pk, ]
        if self.sistema_juego.pk != self.sistema_logros.pk:
            self.keys_system_vec.append(self.sistema_logros.pk)

        for deporte in message:
            cache_temporadas = cache.get(
                'all_{0}_{1}'.format(self.key_cache_sistema, deporte)
            )

            if not cache_temporadas or DEBUG:
                cache_temporadas = {
                    'equipos': {},
                    'grupos': {},
                    'temporadas': self.get_torneos_temporadas(deporte)
                }

                for temporada in cache_temporadas['temporadas']:
                    cache_temporadas['temporadas'].get(
                        temporada
                    )['jornadas'] = self.get_jornadas(temporada)

                    for jornada in cache_temporadas['temporadas'].get(
                        temporada
                    )['jornadas']:
                        cache_temporadas['temporadas'].get(
                            temporada
                        )['jornadas'].get(
                            jornada
                        )['encuentros'] = self.get_encuentros(jornada)

                        for encuentro in cache_temporadas['temporadas'].get(
                            temporada
                        )['jornadas'].get(jornada)['encuentros']:

                            cache_temporadas['equipos'] = self.get_equipos(
                                encuentro=encuentro,
                                message=cache_temporadas['equipos']
                            )

                            encuentro_obj = cache_temporadas['temporadas'].get(temporada)['jornadas'].get(jornada)[
                                'encuentros'].get(encuentro)

                            if encuentro_obj.get('grupo_id'):
                                cache_temporadas['grupos'] = self.get_grupos(
                                    grupo_id=encuentro_obj.get('grupo_id'),
                                    message=cache_temporadas['grupos']
                                )

                            encuentro_obj['jugadas'] = self.get_jugadas(encuentro)

                cache.set(
                    'all_{0}_{1}'.format(self.key_cache_sistema, deporte),
                    cache_temporadas,
                    CACHES_CONF_TIME['getJuegos']['all'],
                )

            message.get(deporte)['temporadas'] = cache_temporadas['temporadas']
            equipos = self.merge_equipos(
                equipos,
                cache_temporadas.pop('equipos'),
            )
            grupos = self.merge_grupos(
                grupos,
                cache_temporadas.pop('grupos'),
            )

        return {'deportes': message, 'equipos': equipos, 'grupos': grupos}

    def get_deportes(self, deporte_id=None):
        message = {}

        deportes_exclude = self.get_deportes_exclude()

        if deporte_id:
            deportes = Deportes.objects.filter(
                pk=deporte_id
            ).exclude(
                pk__in=deportes_exclude
            ).values_list('pk', flat=True)
        else:
            deportes = Deportes.objects.all().exclude(
                pk__in=deportes_exclude
            ).values_list('pk', flat=True)

        for obj_pk in deportes:
            validate = Jugadas.objects.filter(
                status_id=self.status_pendiente.pk,
                valor_americano__isnull=False,

                encuentros_modalidad__encuentro__horajuego__range=self.fecha_range,
                encuentros_modalidad__encuentro__status_id=self.status_habilitado.pk,
                encuentros_modalidad__encuentro__horacierre__gte=self.fecha_hora,

                encuentros_modalidad__encuentro__jornada__temporadas__torneo__deporte_id=obj_pk,
                encuentros_modalidad__encuentro__jornada__temporadas__status_id=self.status_habilitado.pk,
                encuentros_modalidad__encuentro__jornada__status_id=self.status_habilitado.pk,
                encuentros_modalidad__encuentro__jornada__temporadas__fechafin__gte=self.fecha,
                encuentros_modalidad__encuentro__jornada__fechafin__gte=self.fecha,
                encuentros_modalidad__encuentro__jornada__sistema_id=self.sistema_juego.pk,
            ).distinct(
                'encuentros_modalidad__encuentro_id'
            ).values_list(
                'encuentros_modalidad__encuentro_id', flat=True
            )
            count = validate.count()

            if count > 0:
                message_interno = {'count_juegos': count}
                message['{0}'.format(obj_pk)] = message_interno

        return message

    def get_torneos_temporadas(self, deporte):
        message = {}

        temporadas = Temporadas.objects.filter(
            torneo__deporte_id=deporte,
            status_id=self.status_habilitado.pk,
            fechafin__gte=self.fecha,
            jornadas__encuentros__horajuego__range=self.fecha_range,
            jornadas__encuentros__horacierre__gt=self.fecha_hora,
            jornadas__encuentros__status_id=self.status_habilitado.pk,
            jornadas__status_id=self.status_habilitado.pk,
            jornadas__sistema_id=self.sistema_juego.pk,
            jornadas__fechafin__gt=self.fecha,
        ).values_list('pk', flat=True).distinct()

        for obj_pk in temporadas:
            # se validad esto primero xq no tiene sentido armar el json y
            # luego decir q no hay data :)
            validate = Jugadas.objects.filter(
                status_id=self.status_pendiente.pk,
                valor_americano__isnull=False,
                encuentros_modalidad__encuentro__jornada__temporadas_id=obj_pk,
                encuentros_modalidad__encuentro__horajuego__range=self.fecha_range,
                encuentros_modalidad__encuentro__horacierre__gt=self.fecha_hora,
                encuentros_modalidad__encuentro__status_id=self.status_habilitado.pk,
            )
            if validate.exists():
                message_interno = cache.get(
                    'temporada_json_event{0}'.format(obj_pk)
                )
                if not message_interno:
                    message_interno = Temporadas.objects.get(
                        pk=obj_pk
                    ).set_cache()
                message['{0}'.format(obj_pk)] = message_interno

        return message

    def get_jornadas(self, temporada):
        message = {}

        jornadas = Jornadas.objects.filter(
            Q(parley=True) | Q(quiniela=True) | Q(apuestasimple=True)
        ).filter(
            sistema_id=self.sistema_juego.pk,
            temporadas_id=temporada,
            status_id=self.status_habilitado.pk,
            fechafin__gt=self.fecha,
            encuentros__horajuego__range=self.fecha_range,
            encuentros__horacierre__gt=self.fecha_hora,
            encuentros__status_id=self.status_habilitado.pk,
        ).values_list('pk', flat=True).distinct()

        for obj_pk in jornadas:
            validate = Jugadas.objects.filter(
                status_id=self.status_pendiente.pk,
                valor_americano__isnull=False,
                encuentros_modalidad__encuentro__jornada_id=obj_pk,
                encuentros_modalidad__encuentro__horajuego__range=self.fecha_range,
                encuentros_modalidad__encuentro__horacierre__gt=self.fecha_hora,
                encuentros_modalidad__encuentro__status_id=self.status_habilitado.pk,
            )
            if validate.exists():
                message_interno = cache.get(
                    'jornadas_json_event{0}'.format(obj_pk)
                )
                if not message_interno:
                    message_interno = Jornadas.objects.get(
                        pk=obj_pk
                    ).set_cache()
                message['{0}'.format(obj_pk)] = message_interno

        return message

    def get_encuentros(self, jornada):
        message = {}
        encuentros = Encuentros.objects.filter(
            jornada_id=jornada,
            horajuego__range=self.fecha_range,
            horacierre__gte=self.fecha_hora,
            status_id=self.status_habilitado.pk,
        ).values_list('pk', flat=True)

        for obj_pk in encuentros:
            validate = Jugadas.objects.filter(
                status_id=self.status_pendiente.pk,
                valor_americano__isnull=False,
                encuentros_modalidad__encuentro_id=obj_pk,
            )
            if validate.exists():
                message_interno = cache.get(
                    'encuentros_json_event{0}'.format(obj_pk)
                )
                if not message_interno:
                    message_interno = Encuentros.objects.get(
                        pk=obj_pk
                    ).set_cache()
                message['{0}'.format(obj_pk)] = message_interno
        return message

    def get_jugadas(self, encuentro):
        message = cache.get(
            'encuentros_jugadas_all_json_event_key{0}_{1}'.format(encuentro, self.key_cache_sistema)
        )

        if not message or DEBUG:
            message = Encuentros.objects.get(
                pk=encuentro
            ).get_cache_jugadas()

            for grupo_key in message.keys():
                var_delete_encuentro_modalidad = []
                for encuentro_modalidad_key in message[grupo_key]['encuentro_modalidad']:
                    if message[grupo_key]['encuentro_modalidad'][
                            encuentro_modalidad_key]['sistema'] in self.keys_system_vec:
                        var_delete_jugadas = []
                        for jugada_key in message[grupo_key]['encuentro_modalidad'][
                                encuentro_modalidad_key]['jugadas']:
                            if message[grupo_key]['encuentro_modalidad'][encuentro_modalidad_key][
                                    'jugadas'][jugada_key]['sistema'] not in self.keys_system_vec:
                                var_delete_jugadas.append(jugada_key)
                        for key_delete in var_delete_jugadas:
                            del message[grupo_key]['encuentro_modalidad'][
                                encuentro_modalidad_key]['jugadas'][key_delete]
                    else:
                        var_delete_encuentro_modalidad.append(encuentro_modalidad_key)
                for key_delete in var_delete_encuentro_modalidad:
                    del message[grupo_key]['encuentro_modalidad'][key_delete]

            cache.set(
                'encuentros_jugadas_all_json_event_key{0}_{1}'.format(encuentro, self.key_cache_sistema),
                message,
                CACHES_CONF_TIME['getJuegos']['jugadas']
            )
        return message

    def get_equipos(self, encuentro, message={}):

        equipos = EncuentrosDetail.objects.filter(
            encuentro_id=encuentro
        ).values_list('equipos_temporadas__equipo_id', flat=True)

        for obj_pk in equipos:
            if '{0}'.format(obj_pk) not in message:
                message_interno = cache.get(
                    'equipos_json_event{0}'.format(
                        obj_pk
                    )
                )
                if not message_interno:
                    message_interno = Equipos.objects.get(
                        pk=obj_pk
                    ).set_cache()

                message[
                    '{0}'.format(obj_pk)
                ] = message_interno

        return message

    def merge_equipos(self, equipos, copy):
        if len(equipos) == 0:
            return copy
        else:
            for key in copy.keys():
                if not equipos.get(key):
                    equipos[key] = copy[key]
            return equipos

    def get_grupos(self, grupo_id, message={}):
        if '{0}'.format(grupo_id) not in message:
            message_interno = cache.get(
                'grupos_juego_json_event{0}'.format(
                    grupo_id
                )
            )
            if not message_interno:
                message_interno = GruposJuego.objects.get(
                    pk=grupo_id
                ).set_cache()

            message[
                '{0}'.format(grupo_id)
            ] = message_interno

        return message

    def merge_grupos(self, grupos, copy):
        if len(grupos) == 0:
            return copy
        else:
            for key in copy.keys():
                if not grupos.get(key):
                    grupos[key] = copy[key]
            return grupos
