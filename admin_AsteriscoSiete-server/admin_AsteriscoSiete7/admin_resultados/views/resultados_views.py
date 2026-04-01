# -*- coding: utf-8 -*-

from datetime import timedelta

from admin_asterisco7.settings import CACHES_CONF_TIME
from admin_juego.models import TipoProducto_Grupos, Sorteo, Fechas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterDeportesFechaForm
from admin_lib.util_reverse import new_reverse
from admin_lib.util_views import MyViewBase
from admin_resultados.forms import EncuentrosResultadosCreateUpdateForm, FilterCadenaModeloJuegosResultados
from admin_resultados.models import Anotaciones, AnotacionesDetail, Resultados
from admin_resultados.task import Algorithms
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.timezone import now
from django.views.generic import ListView, UpdateView, View


class ResultadosView(MyViewBase):
    '''
    Clase base que define el modelo y queryset inicial
    '''
    model = Sorteo

    def get_queryset(self):
        '''
        En esta consulta queda validado a los encuentros que tiene acceso un usuario
        '''

        if self.get_profile().codename == 'userprofile_master':
            # si es un master tiene derecho a todo
            encuentros = Sorteo.objects.filter(
                horajuego__gte=(
                    now() -
                    timedelta(
                        days=Sorteo.maximo_dias_olgura)).date(),
                horajuego__lte=now(),
                exists_tickets=True,
            )

        else:
            # si es un usuario de cadena se hace el filtro respectivo por
            # el sistema de juego asociado
            encuentros = Sorteo.objects.filter(
                jornada__sistema=self.object_sistema_juego,
                horajuego__gte=(
                    now() -
                    timedelta(
                        days=Sorteo.maximo_dias_olgura)).date(),
                horajuego__lte=now(),
                exists_tickets=True,
            )

        return encuentros.select_related(
            'status',
            'jornada__temporadas__torneo__deporte',
        )


class ResultadosEncuentrosListView(ResultadosView, ListView):
    '''
    Clase que implementa el listar, aqui se añade un segundo nivel al
    queryset
    '''
    template_name = 'admin_resultados/resultados/encuentros_list.html'
    form_class = FilterDeportesFechaForm
    filter_form = None

    def get_queryset(self):
        '''
        Es este get_queryset se hace el respectivo filtro por
        los fields del formulario
        '''
        encuentros = super(ResultadosEncuentrosListView, self).get_queryset()

        if self.get_filter_form().is_valid():
            '''
            Es caso de ser valido el form se ejecutan los filtros
            '''
            fecha = strFecha(
                self.get_filter_form().cleaned_data['fecha']).getFecha()
            deporte = self.get_filter_form().cleaned_data['deporte']
            # torneo = self.get_filter_form().cleaned_data['torneo']
            encuentros = encuentros.filter(
                horajuego__range=(fecha + hora_cero, fecha + hora_23),
            )

            if deporte is not None:
                encuentros = encuentros.filter(
                    jornada__temporadas__torneo__deporte=deporte,
                )
        else:
            encuentros = Sorteo.objects.none()
        return encuentros.filter(
            status__codename__in=[
                'status_habilitado',
                'status_valido_no_terminado']
        )

    def get_context_data(self, **kwargs):
        context = super(
            ResultadosEncuentrosListView,
            self).get_context_data(
            **kwargs)

        count_resultados = 0
        sistema_resultados = self.get_object_sistema_resultados()

        for encuentro in context['object_list']:

            encuentro.resultado_object = encuentro.get_resultado(
                sistema_resultados=sistema_resultados
            )
            status_result = None
            if encuentro.resultado_object:
                if encuentro.resultado_object.status:
                    status_result = encuentro.resultado_object.status

                encuentro.resultado_exists = encuentro.get_exists_resultados(
                    sistema_resultados=sistema_resultados
                )

            if not status_result:
                status_result = encuentro.status
                encuentro.resultado_exists = 0

            if encuentro.resultado_exists == 0:
                if (status_result.codename == 'status_habilitado' or
                        status_result.codename == 'status_valido_no_terminado'):
                    encuentro.resultado_exists = 0
                    count_resultados += 1
                else:
                    encuentro.resultado_exists = 1
            else:
                encuentro.resultado_exists = 1

        mensaje = 'Hay {0} encuentros sin procesar resultados'.format(
            count_resultados)
        messages.warning(
            self.request,
            mensaje
        )

        context['QUERY_STRING'] = self.request.META['QUERY_STRING']

        return context


class ResultadosPremiarView(MyViewBase, View):

    def get_success_url(self):

        messages.info(
            self.request,
            '¡Enhorabuena! la premiación para el Encuentro {} a iniciado'.format(
                self.encuentro)
        )
        return reverse(
            'admin_resultados_encuentros_resultados_list_edit'
        ) + '?{}'.format(self.request.META['QUERY_STRING'])

    def get(self, request, encuentro):
        self.encuentro = get_object_or_404(Sorteo, pk=encuentro)

        sistema_resultados = self.get_object_sistema_resultados()

        self.resultado = Resultados.get_or_create_or_flush(
            encuentro=encuentro,
            sistema=sistema_resultados
        )

        if self.object_user.superuser is False and self.resultado.processed is True:
            raise Http404('Object does not exist.')

        if (self.resultado.status.codename == 'status_habilitado' or
                self.resultado.status.codename == 'status_valido_no_terminado'):

            # =============================================================
            #   Se arma el kwargs para el filtro de tickets, este depende
            #   Del sistema de juego usado

            object_sistema = sistema_resultados.comercializadora.get_object()
            kwargs_async = {}
            key = 'ticket__{0}'.format(
                object_sistema.get_prefix_kwargs_by_level_tickets())
            kwargs_async[key] = object_sistema.pk

            if object_sistema.user_type_codename == 'userprofile_operadora':
                # se exluyen todas bancas y multibancas con derecho a resultados activado
                # en la operadora seleccionada

                # filtrando bancas sin resultados
                kwargs_async[key.replace(
                    '__bloque__operadora_id', '__is_resultados')] = False

                # filtrando bloques sin resultados
                kwargs_async[key.replace(
                    '__operadora_id', '__is_resultados')] = False

                # filtrando bancas sin sistemas de juego
                kwargs_async[key.replace(
                    '__bloque__operadora_id', '__is_sistema_juego')] = False

                # filtrando bloques sin sistema de juego
                kwargs_async[key.replace(
                    '__operadora_id', '__is_sistema_juego')] = False

            elif object_sistema.user_type_codename == 'userprofile_bloque':
                # Se exluyen todas las bancas con derecho a resultados activado
                # en la multibanca seleccionada

                # filtrando bancas sin resultados
                kwargs_async[key.replace(
                    '__bloque_id', '__is_resultados')] = False

                # filtrando bancas sin sistemas de juego
                kwargs_async[key.replace(
                    '__bloque_id', '__is_sistema_juego')] = False

            Algorithms.delay(
                *(),
                **{
                    'encuentro': self.encuentro.pk,
                    'sistema_resultados': sistema_resultados.pk,
                    'filter_cadena': kwargs_async
                }
            )
            self.resultado.processed = True
            self.resultado.save(update_fields=['processed'])

        return HttpResponseRedirect(self.get_success_url())


class ResultadosCreateUpdateView(ResultadosView, UpdateView):
    '''
    Aqui se crean y editan los resultados de todos los encuentros
    '''
    form_class = EncuentrosResultadosCreateUpdateForm
    template_name = 'admin_resultados/resultados/resultados_form.html'
    proceso = 'Creación'

    def form_valid(self, form):
        '''
        Aqui solo se verifica si el el encuentro ya tenia logros,
        para poder mostrar un mensaje
        en el get_success_url bien identificado
        '''
        sistema_resultados = self.get_object_sistema_resultados()
        if self.object.get_exists_resultados(
            sistema_resultados=sistema_resultados
        ):
            self.proceso = 'Actualización'

        return super(ResultadosCreateUpdateView, self).form_valid(form)

    def get_success_url_filter_form(self):
        '''
        Devuelve los filtros equivalentes
        '''
        return '?deporte={0}&fecha={1}'.format(
            self.object.jornada.temporadas.torneo.deporte.pk,
            strFecha(self.object.horajuego).getFecha()
        )

    def get_success_url(self):

        messages.info(self.request, '¡Enhorabuena! {0} de resultados'
                                    ' exitosa para el Encuentro {1} '.format(
                                        self.proceso, self.object)
                      )

        return reverse(
            'admin_resultados_encuentros_resultados_list_edit'
        ) + self.get_success_url_filter_form()

    def get_context_data(self, **kwargs):
        context = super(
            ResultadosCreateUpdateView,
            self).get_context_data(
            **kwargs)

        context['grupos'] = []
        context['grupos_option'] = []
        sistema_resultados = self.get_object_sistema_resultados()

        resultado = Resultados.objects.get(
            encuentro=self.object,
            sistema=sistema_resultados
        )

        deporte = self.object.jornada.temporadas.torneo.deporte
        filter_indice = deporte.get_filter_orden_equipos()

        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=deporte
        ).exclude(
            grupo__codename='referencia'
        ).select_related('grupo').order_by('grupo__orden'):

            anotaciones = Anotaciones.objects.get(
                resultado=resultado,
                grupo=deporte_grupo.grupo
            )

            json_grupos = {}
            json_grupos['grupo'] = deporte_grupo.grupo.nombre
            json_grupos['resultados'] = []

            if deporte_grupo.grupo.codename == 'combinadas':
                grupos = deporte_grupo.grupo.modalidades_grupos_set.all().select_related('modalidad')
                for modalidad_grupo in grupos.order_by('modalidad__orden'):

                    if modalidad_grupo.deporte_restriccion.filter(
                        pk=deporte.pk
                    ).exists():
                        continue
                    condiciones = modalidad_grupo.modalidad.condiciones_set.all().select_related('modalidad')
                    for condicion in condiciones.order_by('orden'):

                        if (condicion.modalidad.codename == 'h+c+e' or
                                condicion.modalidad.codename == 'anota_1ro' or
                                condicion.modalidad.codename == 'si/no'):

                            anotacion = AnotacionesDetail.objects.get(
                                anotacion=anotaciones,
                                condicion=condicion
                            )
                            json_resultado = {}
                            json_resultado['field'] = context['form'][
                                'resultado_' + str(anotacion.pk)
                            ]
                            json_resultado[
                                'indice'] = condicion.modalidad.orden
                            json_grupos['resultados'].append(json_resultado)

            else:
                for equipo in self.object.encuentrosdetail_set.all().order_by(filter_indice):
                    anotacion = AnotacionesDetail.objects.get(
                        anotacion=anotaciones,
                        encuentro_detail=equipo,
                        condicion__isnull=True
                    )
                    json_resultado = {}
                    json_resultado['field'] = context['form'][
                        'resultado_' + str(anotacion.pk)]
                    json_resultado['indice'] = equipo.indice
                    json_grupos['resultados'].append(json_resultado)

            if len(json_grupos['resultados']):
                context['grupos'].append(json_grupos)

                context['grupos_option'].append(
                    ['code-grupo-{0}'.format(deporte_grupo.grupo.pk),
                     deporte_grupo.grupo.nombre]
                )

        return context

    # Revisar este trozo de codigo, dado que con el usuario pedro morles no
    # esta dejando cargar logros
    """
    def dispatch(self, request, *args, **kwargs):

        if kwargs.get('object_user').superuser is False:
            self.object = self.get_object()
            self.sistema_resultados = self.get_object_sistema_resultados()
            self.resultado = Resultados.get_or_create_or_flush(
                encuentro=self.object,
                sistema=self.sistema_resultados
            )
            if self.resultado.processed is True:
                raise Http404('Object does not exist.')

        return super(ResultadosCreateUpdateView, self).dispatch(request, *args, **kwargs)
    """


class ResultadosChangeView(ResultadosCreateUpdateView):

    def form_valid(self, form):
        sistema_resultados = self.get_object_sistema_resultados()
        resultado = Resultados.objects.get(
            encuentro=self.object,
            sistema=sistema_resultados
        )
        resultado.processed = False
        resultado.save(update_fields=['processed'])
        return super(ResultadosChangeView, self).form_valid(form)


class ResultadosLoadListView(MyViewBase, ListView):
    '''
    Se listan todos los resultados de los encuentros
    '''
    template_name = 'admin_resultados/resultados/print_resultados_list.html'
    model = Sorteo
    form_class = FilterCadenaModeloJuegosResultados
    filter_form = None

    def get_queryset(self):
        '''
        Es este get_queryset se hace el respectivo filtro por
        los fields del formulario
        '''

        if self.get_profile().codename == 'userprofile_master':
            # si es un master tiene derecho a todo
            encuentros = Sorteo.objects.all()

        else:
            # si es un usuario de cadena se hace el filtro respectivo por
            # el sistema de juego asociado
            encuentros = Sorteo.objects.filter(
                jornada__sistema=self.object_sistema_juego,
            )

        encuentros = encuentros.filter(
            status__codename__in=[
                'status_habilitado',
                'status_valido_no_terminado']
        )

        if self.get_filter_form().is_valid():
            '''
            Es caso de ser valido el form se ejecutan los filtros
            '''
            fecha = strFecha(
                self.get_filter_form().cleaned_data['fecha']).getFecha()
            deporte = self.get_filter_form().cleaned_data['deporte']

            operadora = self.get_filter_form().cleaned_data.get('operadora')
            bloque = self.get_filter_form().cleaned_data.get('bloque')
            banca = self.get_filter_form().cleaned_data.get('banca')

            if banca:
                comercializadora = banca.get_comercializadora()
            elif bloque:
                comercializadora = bloque.get_comercializadora()
            elif operadora:
                comercializadora = operadora.get_comercializadora()
            else:
                comercializadora = self.object_comercializadora

            self.sistema_resultados = self.get_object_sistema_resultados(
                comercializadora=comercializadora
            )

            encuentros = encuentros.filter(
                horajuego__range=(fecha + hora_cero, fecha + hora_23),
            )

            if deporte is not None:
                encuentros = encuentros.filter(
                    jornada__temporadas__torneo__deporte=deporte,
                )
        else:
            encuentros = Sorteo.objects.none()

        return encuentros

    def get_context_data(self, **kwargs):
        context = super(ResultadosLoadListView, self).get_context_data(
            **kwargs
        )

        deporte = None
        if self.get_filter_form().is_valid():
            deporte = self.get_filter_form().cleaned_data['deporte']
            fecha = self.get_filter_form().cleaned_data['fecha']

        if deporte is not None:
            filtro_deporte = deporte.nombre
        else:
            filtro_deporte = 'Deporte'

        context['consulta'] = []
        context['grupos'] = []

        context['consulta_new'] = []

        if context['object_list']:

            temporadas_objects = context['object_list'].values_list(
                'jornada__temporadas_id', flat=True)

            grupos_json = {}

            for temporada in Fechas.objects.select_related(
                    'torneo').filter(pk__in=list(set(temporadas_objects))).order_by('torneo__nombre'):

                temporada_add = False
                json_liga = {}
                json_liga['nombre'] = '{0} {1}'.format(
                    temporada.torneo.nombre,
                    temporada.nombre
                )
                json_liga['logo'] = temporada.torneo.logo
                json_liga['encuentros'] = []

                if str(temporada.torneo.deporte_id) not in grupos_json:
                    json_liga['grupos'] = []
                    grupo_json = {}
                    grupo_json['nombre'] = 'Participantes'
                    grupo_json['modalidades'] = []
                    json_liga['grupos'].append(grupo_json)
                    for deporte_grupo in TipoProducto_Grupos.objects.filter(
                            deporte=temporada.torneo.deporte_id).exclude(
                            grupo__codename='referencia').order_by('grupo__orden').select_related('grupo'):
                        grupo_json = {}
                        grupo_json['nombre'] = deporte_grupo.grupo.nombre
                        grupo_json['modalidades'] = []
                        modalidades_grupos_list = deporte_grupo.grupo.modalidades_grupos_set.all().exclude(
                            modalidad__codename__in=['empate', 'games']
                        )
                        for modalidad_grupo in modalidades_grupos_list.select_related('modalidad__modalidad').all(
                        ).order_by('modalidad__orden'):
                            grupo_json['modalidades'].append(
                                modalidad_grupo.modalidad.modalidad)

                        json_liga['grupos'].append(grupo_json)
                    grupos_json[str(temporada.torneo.deporte_id)
                                ] = json_liga['grupos']
                else:
                    json_liga['grupos'] = grupos_json[
                        str(temporada.torneo.deporte_id)]

                for obj in context['object_list'].filter(
                        jornada__temporadas_id=temporada.id).only('pk', 'horajuego'):

                    resultado_exists = obj.get_exists_resultados(
                        self.sistema_resultados
                    )
                    if not resultado_exists:
                        continue

                    resultado = obj.get_resultado(
                        self.sistema_resultados
                    )

                    if resultado and resultado.status.codename not in [
                            'status_habilitado', 'status_valido_no_terminado']:
                        continue

                    if resultado is not None:
                        temporada_add = True
                        json_encuentro = {}
                        json_encuentro['hora'] = obj.horajuego
                        json_encuentro['equipos'] = []

                        anotaciones = Anotaciones.objects.filter(
                            resultado=resultado,
                        ).select_related('grupo').order_by('grupo__orden')

                        json_externo = []

                        for equipo in obj.encuentrosdetail_set.all().select_related(
                                'equipos_temporadas__equipo').order_by('-indice'):
                            json_interno = []
                            td_object = {}
                            td_object['row'] = 1
                            td_object[
                                'puntaje'] = equipo.equipos_temporadas.equipo.nombre
                            json_interno.append(td_object)

                            for anotacion in anotaciones:
                                if anotacion.grupo.codename != 'combinadas':

                                    td_object = {}
                                    td_object['row'] = 1
                                    td_object['puntaje'] = ''

                                    # Condicion de ganador
                                    for detail in AnotacionesDetail.objects.only('puntaje').filter(
                                            anotacion=anotacion, encuentro_detail=equipo,
                                            condicion__isnull=True, puntaje__isnull=False):
                                        td_object['puntaje'] = detail.puntaje
                                    json_interno.append(td_object)

                                    # Condicion alta/baja
                                    td_object = {}
                                    td_object['row'] = 2
                                    td_object['puntaje'] = ''
                                    for detail in AnotacionesDetail.objects.only('puntaje').filter(
                                            anotacion=anotacion, encuentro_detail__isnull=True,
                                            puntaje__isnull=False):
                                        td_object['puntaje'] = detail.puntaje
                                    json_interno.append(td_object)

                                    # Condicion Runline
                                    td_object = {}
                                    td_object['row'] = 1
                                    td_object['puntaje'] = ''
                                    for detail in AnotacionesDetail.objects.only('puntaje').filter(
                                            anotacion=anotacion, encuentro_detail=equipo,
                                            condicion__isnull=False, puntaje__isnull=False):
                                        if detail.puntaje > 0:
                                            td_object['puntaje'] = '+' + \
                                                str(detail.puntaje)
                                        else:
                                            td_object[
                                                'puntaje'] = detail.puntaje
                                    json_interno.append(td_object)

                                else:

                                    # SuperRunline
                                    td_object = {}
                                    td_object['row'] = 1
                                    # Condicion de ganador
                                    for detail in AnotacionesDetail.objects.only('puntaje').filter(
                                            anotacion=anotacion, encuentro_detail=equipo,
                                            puntaje__isnull=False):
                                        if detail.puntaje > 0:
                                            td_object['puntaje'] = '+' + \
                                                str(detail.puntaje)
                                        else:
                                            td_object[
                                                'puntaje'] = detail.puntaje
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
                                            td_object[
                                                'puntaje'] = detail.get_label_customize()
                                        json_interno.append(td_object)

                            json_externo.append(json_interno)
                        json_encuentro['resultados'] = json_externo
                        json_liga['encuentros'].append(json_encuentro)
                if temporada_add:
                    context['consulta_new'].append(json_liga)

            var_cache = {
                'titulo': 'Reporte - Lista de resultados',
                'fecha': strFecha(fecha).getFecha(),
                'deporte': filtro_deporte,
                'consulta': context['consulta_new'],
                'sistema_resultados': self.sistema_resultados,
                'template_name': 'admin_resultados/resultados/print_resultados_pdf.html',
            }

            import re
            if self.object_sistema_juego is not None:
                sistema = self.sistema_resultados.get_lower_ascci()
            else:
                sistema = 'todo'

            context['cache_key'] = re.sub(
                '--',
                '-',
                '{0}-{1}-{2}-generate-{3}-{4}'.format(
                    sistema,
                    var_cache['deporte'].lower(),
                    var_cache['fecha'],
                    now().strftime('%Y-%m-%d-%H-%M'),
                    self.object_user
                )
            )

            cache.set(
                context['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_resultados']
            )
        return context


class ResultadosDatatableView(ResultadosEncuentrosListView, BaseDatatableView):
    model = Resultados
    order_columns = ['horajuego']
    # Fields de busqueda
    filter_search = 'id'

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        sistema_resultados = self.get_object_sistema_resultados()
        for x, item in enumerate(qs):
            if item.get_exists_logros():

                equipos = ''
                tam = len(item.encuentrosdetail_set_order())
                for x, equipo in enumerate(item.encuentrosdetail_set_order()):
                    equipos += '<span class="tag tag-blue">{0}</span>'.format(
                        equipo.equipos_temporadas.equipo
                    )

                    if x != (tam - 1):
                        equipos += '<span class="tag tag-nomargin">vs.</span>'

                json_data.append([
                    item.pk,
                    '{0} - {1}'.format(
                        item.horajuego.strftime('%I:%M %p'),
                        item.horajuego.strftime('%d/%m/%Y')
                    ),
                    equipos,
                    '{0} - {1}'.format(
                        item.jornada.temporadas.torneo.nombre,
                        item.jornada.temporadas.nombre,
                    ),
                    '<span class="tag tag-green">{0}</span>'.format(
                        item.jornada.temporadas.torneo.deporte
                    ),
                    '<a href="' + new_reverse(
                        self,
                        'admin_resultados_ecuentros_resultados_create_update',
                        kwargs={
                            "pk": item.pk
                        }
                    ) + ' class="btn {0}">Asignar resultado</a>'.format(
                        'btn-success' if item.get_exists_resultados(
                            sistema_resultados=sistema_resultados) else 'btn-danger'
                    )
                ])

        return json_data
