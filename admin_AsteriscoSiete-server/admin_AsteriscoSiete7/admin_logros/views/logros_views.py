# -*- coding: utf-8 -*-
from admin_asterisco7.settings import CACHES_CONF_TIME
from admin_juego.models import (
    TipoProducto_Grupos, Sorteo, SorteoDetalle, apuesta, JugadasInformativas, SistemaJuego, Fechas,
)
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FORMAT_STR_DATE_FORM, FilterDeporteFechaForm
from admin_lib.util_reverse import new_reverse
from admin_lib.util_views import MyViewBase
from admin_logros.forms import EncuentrosLogrosCreateUpdateForm, FilterCadenaModeloJuegosLogros
from django.contrib import messages
from django.core.cache import cache
from django.urls import reverse
from django.utils.timezone import now
from django.views.generic import ListView, UpdateView


class LogrosView(MyViewBase):
    """
    Clase base que define el modelo y queryset inicial
    """
    model = Sorteo

    def get_queryset(self):
        """
        En esta consulta queda validado a los encuentros que tiene
        acceso un usuario
        """
        if self.get_profile().codename == 'userprofile_master':
            """si es un master tiene derecho a todo"""
            encuentros = Sorteo.objects.all().exclude(
                horajuego__lt=now()
            )

        else:
            """
            si es un usuario de cadena se hace el filtro respectivo por
            el sistema de juego asociado
            """
            encuentros = Sorteo.objects.filter(
                jornada__sistema_id=self.object_sistema_juego.pk
            ).exclude(
                horajuego__lt=now()
            )

        return encuentros.select_related(
            'status',
            'jornada__temporadas__torneo__deporte',
        )


class LogrosListView(LogrosView, ListView):
    """
    Clase que implementa el listar, aqui se añade un segundo nivel al
    queryset
    """
    template_name = 'admin_logros/jugadas/jugadas_list.html'
    form_class = FilterDeporteFechaForm
    filter_form = None

    def get_queryset(self):
        """
        Es este get_queryset se hace el respectivo filtro por
        los fields del formulario
        """
        encuentros = super(LogrosListView, self).get_queryset()
        if self.get_filter_form().is_valid():
            """
            Es caso de ser valido el form se ejecutan los filtros
            """
            fecha = strFecha(self.get_filter_form().cleaned_data['fecha']).getFecha()
            deporte = self.get_filter_form().cleaned_data['deporte']

            encuentros = encuentros.filter(
                horajuego__range=(fecha + hora_cero, fecha + hora_23),
                jornada__temporadas__torneo__deporte=deporte
            )
        else:
            encuentros = Sorteo.objects.none()

        return encuentros


class LogrosCreateUpdateView(LogrosView, UpdateView):
    """
    Aqui se crean y editan los resultados de todos los encuentros
    """
    form_class = EncuentrosLogrosCreateUpdateForm
    template_name = 'admin_logros/jugadas/jugadas_form.html'
    proceso = 'Creación'

    def form_valid(self, form):
        """
        Aqui solo se verifica si el el encuentro ya tenia logros,
        para poder mostrar un mensaje
        en el get_success_url bien identificado
        """
        if self.object.get_exists_logros():
            self.proceso = 'Actualización'

        return super(LogrosCreateUpdateView, self).form_valid(form)

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return '?deporte={0}&fecha={1}'.format(
            self.object.jornada.temporadas.torneo.deporte.pk,
            strFecha(self.object.horajuego).getFecha()
        )

    def get_success_url(self):
        self.object = self.get_object()
        messages.info(
            self.request,
            '¡Enhorabuena! {0} de logros'
            ' exitosa para el Encuentro {1} '.format(
                self.proceso,
                self.object
            )
        )
        return reverse(
            'admin_logros_encuentros_list_edit'
        ) + self.get_success_url_filter_form()

    def get_context_data(self, **kwargs):
        context = super(LogrosCreateUpdateView, self).get_context_data(**kwargs)

        context['rangos_grupo'] = []
        context['rangos_modalidad'] = []
        context['rangos_condicion'] = []
        context['grupos'] = []
        context['modalidades_data_list'] = []
        max_position = 0

        deporte = self.object.jornada.temporadas.torneo.deporte
        filter_indice = deporte.get_filter_orden_equipos()
        self.get_object_sistema_logros()

        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=deporte
        ).order_by('grupo__orden'):
            grupo_json = {}
            """
            #################Rangos logros##################
            """
            try:
                referencia = RestriccionesSorteo.objects.get(
                    deporte=deporte_grupo.deporte,
                    grupo=deporte_grupo.grupo,
                    min_ref='logro'
                )
            except Exception:
                referencia = 0

            if referencia:
                rangos_json = {}
                try:
                    rango = RestriccionesSorteo.objects.get(
                        deporte=deporte_grupo.deporte,
                        grupo=deporte_grupo.grupo,
                        min_ref='logro'
                    )
                    rangos_json['logro_favorito'] = int(rango.max_logro_favorito)
                    rangos_json['logro_no_favorito'] = int(rango.max_logro_no_favorito)
                    rangos_json['grupo'] = deporte_grupo.grupo.id
                except RestriccionesSorteo.DoesNotExist:
                    pass
                context['rangos_grupo'].append(rangos_json)
            ################################################

            grupo_json['grupo'] = deporte_grupo.grupo.nombre
            grupo_json['modalidades'] = []
            modalidades_grupos_list = deporte_grupo.grupo.modalidades_grupos_set.all()
            for modalidad_grupo in modalidades_grupos_list.order_by('modalidad__orden'):

                if modalidad_grupo.deporte_restriccion.filter(
                    pk=self.object.jornada.temporadas.torneo.deporte.pk
                ).exists():
                    continue

                modalidad_json = {}
                modalidad_json['nombre'] = modalidad_grupo.modalidad.modalidad

                if deporte_grupo.grupo.codename == 'referencia':
                    json_data_list = {}
                    json_data_list['name'] = 'modalidad-{0}-infornacion_list'.format(
                        modalidad_grupo.modalidad.pk
                    )
                    json_data_list['data'] = JugadasInformativas.objects.filter(
                        encuentros_modalidad__modalidad_grupo__modalidad=modalidad_grupo.modalidad
                    ).distinct('ref_principal')

                    context['modalidades_data_list'].append(json_data_list)

                encu_moda = SorteoModalidades.get_carefully(
                    kwargs={
                        'encuentro': self.object,
                        'deporte_grupo': deporte_grupo,
                        'modalidad_grupo': modalidad_grupo,
                    },
                    sistemajuego=self.object_sistema_juego,
                    sistemalogros=self.object_sistema_logros,
                )

                if encu_moda.modalidad_grupo.modalidad.etiqueta_ref:
                    modalidad_json['ref'] = context['form'][
                        'ref_encuentromodalidad_{0}'.format(
                            encu_moda.pk
                        )
                    ]
                    """
                    ######Rangos referencia modalidad##################
                    """
                    if RestriccionesSorteo.objects.filter(
                        deporte=deporte_grupo.deporte,
                        grupo=deporte_grupo.grupo,
                        modalidad=encu_moda.modalidad_grupo.modalidad
                    ).exists():

                        rangos_json = {}

                        rango = RestriccionesSorteo.objects.get(
                            deporte=deporte_grupo.deporte,
                            grupo=deporte_grupo.grupo,
                            modalidad=encu_moda.modalidad_grupo.modalidad
                        )

                        rangos_json['min'] = rango.min_ref
                        rangos_json['max'] = rango.max_ref
                        rangos_json['grupo'] = deporte_grupo.grupo.id
                        rangos_json['deporte'] = deporte_grupo.deporte.id
                        rangos_json['modalidad'] = encu_moda.modalidad_grupo.modalidad.id

                        context['rangos_modalidad'].append(rangos_json)

                modalidad_json['jugadas'] = []
                condiciones_list = encu_moda.modalidad_grupo.modalidad.condiciones_set
                for condicion in condiciones_list.all().order_by('orden'):

                    if condicion.equipo:
                        modalidad_json['espacio'] = self.object.encuentrosdetail_set.all().count()
                        encuentrosdetail_list = self.object.encuentrosdetail_set.all()
                        for encuent_deta in encuentrosdetail_list.order_by(filter_indice):

                            if condicion.tipo == 4:
                                """#verificamos nuevamente que sea una condicion de Informativa"""

                                jugada_info = JugadasInformativas.get_carefully(
                                    kwargs={
                                        'detalle_encuentro': encuent_deta,
                                        'encuentros_modalidad': encu_moda,
                                        'condicion': condicion,
                                    },
                                    sistemajuego=self.object_sistema_juego,
                                    sistemalogros=self.object_sistema_logros,
                                )

                                jugada_json = {}
                                jugada_json['extra'] = True
                                jugada_json['jugada'] = []
                                str_encuentro_ref_0 = 'encuentro_ref_{0}-0'.format(jugada_info.pk)
                                str_encuentro_ref_1 = 'encuentro_ref_{0}-1'.format(jugada_info.pk)

                                jugada_json['jugada'].append(
                                    context['form'][str_encuentro_ref_0]
                                )
                                jugada_json['jugada'].append(
                                    context['form'][str_encuentro_ref_1]
                                )
                                jugada_json['position'] = len(modalidad_json['jugadas'])
                                modalidad_json['jugadas'].append(jugada_json)

                            else:
                                jugada = apuesta.get_carefully(
                                    kwargs={
                                        'detalle_encuentro': encuent_deta,
                                        'encuentros_modalidad': encu_moda,
                                        'condicion': condicion,
                                    },
                                    sistemajuego=self.object_sistema_juego,
                                    sistemalogros=self.object_sistema_logros,
                                )

                                jugada_json = {}
                                jugada_json['extra'] = False
                                jugada_json['jugada'] = context['form']['logro_' + str(jugada.pk)]

                                if condicion.etiqueta_ref:
                                    jugada_json['ref'] = context['form']['ref_logro_' + str(
                                        jugada.pk
                                    )]
                                    """
                                    #########Rangos referencia condicion############
                                    """
                                    if RestriccionesSorteo.objects.filter(
                                        deporte=deporte_grupo.deporte,
                                        grupo=deporte_grupo.grupo,
                                        condicion=condicion
                                    ).exists():

                                        rangos_json = {}
                                        rango = RestriccionesSorteo.objects.get(
                                            deporte=deporte_grupo.deporte,
                                            grupo=deporte_grupo.grupo,
                                            condicion=condicion
                                        )

                                        rangos_json['min'] = rango.min_ref
                                        rangos_json['max'] = rango.max_ref
                                        rangos_json['grupo'] = deporte_grupo.grupo.id
                                        rangos_json['deporte'] = deporte_grupo.deporte.id
                                        rangos_json['modalidad'] = encu_moda.modalidad_grupo.modalidad.id
                                        context['rangos_condicion'].append(rangos_json)

                                jugada_json['position'] = len(modalidad_json['jugadas'])
                                modalidad_json['jugadas'].append(jugada_json)
                    else:
                        modalidad_json['espacio'] = condicion.tipo
                        for indice in range(1, condicion.tipo + 1):

                            jugada = apuesta.get_carefully(
                                kwargs={
                                    'encuentros_modalidad': encu_moda,
                                    'condicion': condicion,
                                    'indice': indice,
                                },
                                sistemajuego=self.object_sistema_juego,
                                sistemalogros=self.object_sistema_logros,
                            )

                            jugada_json = {}
                            jugada_json['extra'] = False
                            jugada_json['jugada'] = context['form']['logro_' + str(jugada.pk)]
                            if condicion.etiqueta_ref:
                                jugada_json['ref'] = context['form']['ref_logro_' + str(jugada.pk)]
                            jugada_json['position'] = len(modalidad_json['jugadas'])
                            modalidad_json['jugadas'].append(jugada_json)

                        if condicion.tipo < self.object.encuentrosdetail_set.all().count():
                            for other in range(
                                condicion.tipo,
                                self.object.encuentrosdetail_set.all().count()
                            ):
                                jugada_json_vacia = {}
                                jugada_json_vacia['extra'] = ''
                                jugada_json_vacia['jugada'] = ''
                                jugada_json_vacia['ref'] = ''
                                jugada_json_vacia['position'] = len(modalidad_json['jugadas'])
                                modalidad_json['jugadas'].append(jugada_json_vacia)

                grupo_json['modalidades'].append(modalidad_json)

                if max_position < len(modalidad_json['jugadas']):
                    max_position = len(modalidad_json['jugadas'])

            context['grupos'].append(grupo_json)

        context['cicle_position'] = []

        for i in range(0, max_position):
            if i == 0:
                context['cicle_position'].append(i)
                context['cicle_position'].append(max_position)
            else:
                context['cicle_position'].append(i)

        context['equipos'] = []
        for equipo in context['object'].encuentrosdetail_set.all().order_by(filter_indice):
            json_equipo = {}
            json_equipo['nombre'] = equipo.equipos_temporadas.equipo.nombre
            json_equipo['logo'] = equipo.equipos_temporadas.equipo.logo
            json_equipo['position'] = len(context['equipos'])
            context['equipos'].append(json_equipo)
        return context


class LogrosListDetailView(LogrosView, ListView):
    model = Fechas
    template_name = 'admin_logros/jugadas/print_logros_list_detail.html'
    form_class = FilterCadenaModeloJuegosLogros
    filter_form = None
    is_consulta = False

    def get_queryset(self):
        """
        Es este get_queryset se hace el respectivo filtro por
        los fields del formulario
        """
        # precargamos el sistema de logros para el user actual
        self.get_object_sistema_logros()
        self.fecha = now().strftime(FORMAT_STR_DATE_FORM)

        if self.get_filter_form().is_valid():
            """
            Es caso de ser valido el form se ejecutan los filtros
            """
            cleaned_data = self.get_filter_form().cleaned_data
            self.is_consulta = True
            self.fecha = strFecha(cleaned_data['fecha']).getFecha()
            self.inicio = self.fecha + hora_cero
            self.fin = self.fecha + hora_23
            self.deporte = cleaned_data['deporte']

            if self.get_profile().codename == 'userprofile_master':
                """
                #si es un master tiene derecho a todo
                """
                temporadas = Fechas.objects.all()

            comercializadora = None
            for cadena in ['banca', 'bloque', 'operadora']:
                if cleaned_data.get(cadena):
                    comercializadora = cleaned_data.get(cadena).get_comercializadora()
                    break

            if comercializadora:
                self.object_sistema_logros = SistemaJuego.objects \
                    .get_sistema_logros_by_comercializadora(
                        comercializadora
                    )
                self.object_sistema_juego = SistemaJuego.objects \
                    .get_sistema_juego_by_comercializadora(
                        comercializadora
                    )

            if self.object_sistema_juego:
                temporadas = Fechas.objects.filter(
                    jornadas__sistema=self.object_sistema_juego
                )
                if self.deporte is not None:
                    temporadas = temporadas.filter(
                        torneo__deporte=self.deporte,
                    )

                temporadas = temporadas.distinct()
            else:
                temporadas = Fechas.objects.none()

        else:
            temporadas = Fechas.objects.none()

        return temporadas.order_by('torneo__deporte_id')

    def get_filter_form(self):
        """
        Retorna el formulario de la instanca,
        de ya estar inicializado devuelve el que esta en memoria
        """
        if self.filter_form is None:
            self.filter_form = self.form_class(self.request.GET, **self.get_form_kwargs())
        return self.filter_form

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(LogrosListDetailView, self).get_context_data(**kwargs)

        key_sistema_juego = '{0}_{1}_{2}'
        if self.object_sistema_juego:
            key_sistema_juego = key_sistema_juego.replace('{0}', '{0}'.format(self.object_sistema_juego.pk))
        if self.object_sistema_logros:
            key_sistema_juego = key_sistema_juego.replace('{1}', '{0}'.format(self.object_sistema_logros.pk))

        key_sistema_juego = key_sistema_juego.replace('{2}', '{0}'.format(self.fecha))

        context['ligas'] = None
        if context['object_list']:
            context['ligas'] = cache.get(
                'list_logros_deporte_{0}_{1}'.format(
                    self.deporte.pk if self.deporte is not None else 0,
                    key_sistema_juego
                )
            )
        else:
            context['is_consulta'] = self.is_consulta
            return context

        if not context['ligas']:
            """
            #################################################
            """
            json_ligas_list = []

            for temporada in context['object_list']:
                filter_indice = temporada.torneo.deporte.get_filter_orden_equipos()
                json_liga = cache.get('list_logros_temporada_{0}_{1}'.format(
                    temporada.pk,
                    key_sistema_juego
                )
                )

                if not json_liga:
                    json_liga = {}
                    json_liga['nombre'] = '{0} {1}'.format(
                        temporada.torneo.nombre,
                        temporada.nombre
                    )
                    json_liga['logo'] = temporada.torneo.logo
                    json_liga['encuentros'] = []

                    if self.get_profile().codename == 'userprofile_master':
                        jornadas_list = temporada.jornadas_set.all()

                    else:
                        jornadas_list = temporada.jornadas_set.filter(
                            sistema=self.object_sistema_juego
                        )

                    for jornada in jornadas_list:

                        for encuentro in jornada.encuentros_set.filter(
                            horajuego__range=(self.inicio, self.fin)
                        ):

                            json_encuentro = cache.get('list_logros_encuentro_{0}_{1}'.format(
                                encuentro.pk,
                                key_sistema_juego
                            )
                            )

                            if not json_encuentro:
                                if encuentro.get_exists_logros() is False:
                                    continue

                                json_encuentro = {}
                                json_encuentro['fecha_hora'] = encuentro.horajuego

                                json_encuentro['equipos'] = cache.get(
                                    'list_logros_encuentro_equipos_{0}_{1}'.format(
                                        encuentro.pk,
                                        key_sistema_juego
                                    )
                                )

                                if not json_encuentro['equipos']:
                                    json_encuentro['equipos'] = []
                                    encuentrosdetail_list = encuentro.encuentrosdetail_set.all()
                                    for equipo in encuentrosdetail_list.order_by(filter_indice):
                                        json_equipo = {
                                            'nombre': equipo.equipos_temporadas.equipo.nombre,
                                            'logo': equipo.equipos_temporadas.equipo.logo,
                                            'position': len(json_encuentro['equipos'])
                                        }
                                        json_encuentro['equipos'].append(json_equipo)

                                    cache.set(
                                        'list_logros_encuentro_equipos_{0}_{1}'.format(
                                            encuentro.pk,
                                            key_sistema_juego
                                        ),
                                        json_encuentro['equipos']
                                    )

                                json_encuentro['grupos'] = []

                                for jugador_tipo in TipoNumeroSorteo.objects.filter(
                                    deporte=self.deporte
                                ).order_by('nombre'):

                                    grupo_json = {}
                                    grupo_json['nombre'] = 'Jugadores'
                                    grupo_json['modalidades'] = []

                                    modalidad_json = {}
                                    modalidad_json['nombre'] = jugador_tipo.nombre
                                    modalidad_json['ref'] = ''

                                    modalidad_json['jugadas'] = []
                                    detalle_encuentros = SorteoDetalle.objects.filter(
                                        encuentro=encuentro,
                                        jugador__tipo=jugador_tipo
                                    ).order_by(filter_indice)

                                    for detalle_encuentro in detalle_encuentros:
                                        jugada_json = {
                                            'ref': '',
                                            'val': '({0}){1} {2}'.format(
                                                detalle_encuentro.jugador.lateralidad,
                                                detalle_encuentro.jugador.nombre,
                                                detalle_encuentro.referencia
                                            ),
                                            'position': len(modalidad_json['jugadas']),
                                            'pertenece': ''
                                        }
                                        modalidad_json['jugadas'].append(jugada_json)

                                    if detalle_encuentros:
                                        grupo_json['modalidades'].append(modalidad_json)
                                        json_encuentro['grupos'].append(grupo_json)

                                for deporte_grupo in TipoProducto_Grupos.objects.filter(
                                    deporte=encuentro.jornada.temporadas.torneo.deporte
                                ).order_by('grupo__orden'):

                                    grupo_json = {}
                                    if deporte_grupo.grupo.codename != 'referencia':
                                        grupo_json['nombre'] = deporte_grupo.grupo.nombre
                                    else:
                                        grupo_json['nombre'] = ''

                                    grupo_json['modalidades'] = []
                                    modalidades_grupos_list = deporte_grupo \
                                        .grupo.modalidades_grupos_set

                                    for modalidad_grupo in modalidades_grupos_list.all(
                                    ).order_by('modalidad__orden'):
                                        if modalidad_grupo.deporte_restriccion.filter(
                                            pk=encuentro.jornada
                                            .temporadas.torneo.deporte.pk
                                        ).exists():
                                            continue
                                        try:
                                            encu_moda = SorteoModalidades \
                                                .get_carefully(
                                                    kwargs={
                                                        'encuentro': encuentro,
                                                        'deporte_grupo': deporte_grupo,
                                                        'modalidad_grupo': modalidad_grupo,
                                                    },
                                                    sistemajuego=self.object_sistema_juego,
                                                    sistemalogros=self.object_sistema_logros,
                                                )

                                        except SorteoModalidades.DoesNotExist:
                                            continue

                                        modalidad_json = {}
                                        modalidad_json['nombre'] = '{0}'.format(
                                            modalidad_grupo.modalidad.modalidad
                                        )

                                        if (
                                            encu_moda.modalidad_grupo
                                            .modalidad.etiqueta_ref and
                                            encu_moda.etiqueta_ref
                                        ):
                                            modalidad_json['ref'] = '{0}'.format(
                                                encu_moda.etiqueta_ref
                                            )
                                        else:
                                            modalidad_json['ref'] = ''

                                        modalidad_json['jugadas'] = []
                                        condiciones_list = encu_moda.modalidad_grupo \
                                            .modalidad.condiciones_set

                                        for condicion in condiciones_list.all().order_by('orden'):

                                            if condicion.equipo:
                                                encuentrosdetail_list = encuentro \
                                                    .encuentrosdetail_set.all()
                                                for encuent_deta in encuentrosdetail_list.all(
                                                ).order_by(filter_indice):
                                                    if condicion.tipo == 4:
                                                        """
                                                        #verificamos nuevamente
                                                        #que sea una condicion de Informativa
                                                        """
                                                        try:
                                                            jugada = JugadasInformativas \
                                                                .get_carefully(
                                                                    kwargs={
                                                                        'detalle_encuentro': encuent_deta,
                                                                        'encuentros_modalidad': encu_moda,
                                                                        'condicion': condicion,
                                                                    },
                                                                    sistemajuego=self.object_sistema_juego,
                                                                    sistemalogros=self.object_sistema_logros,
                                                                )

                                                            jugada_json = {}

                                                            jugada_json['ref'] = ''
                                                            if (
                                                                    jugada.status.codename ==
                                                                    'status_pendiente'
                                                            ):
                                                                jugada_json['val'] = '{0}{1}' \
                                                                    .format(
                                                                        jugada.ref_principal,
                                                                        jugada.ref_other_1
                                                                )
                                                            else:
                                                                jugada_json['val'] = ''
                                                            """
                                                            #+'('+jugada.ref_other_2+','+jugada.ref_other_3+')'
                                                            """
                                                            jugada_json['pertenece'] = ''
                                                            """
                                                            #jugada.detalle_encuentro.equipos_temporadas.equipo.nombre
                                                            """
                                                            jugada_json['position'] = len(
                                                                modalidad_json['jugadas']
                                                            )
                                                            modalidad_json['jugadas'].append(
                                                                jugada_json
                                                            )

                                                        except JugadasInformativas.DoesNotExist:
                                                            pass
                                                    else:
                                                        try:
                                                            jugada = apuesta.get_carefully(
                                                                kwargs={
                                                                    'detalle_encuentro': encuent_deta,
                                                                    'encuentros_modalidad': encu_moda,
                                                                    'condicion': condicion,
                                                                },
                                                                sistemajuego=self.object_sistema_juego,
                                                                sistemalogros=self.object_sistema_logros,
                                                            )
                                                        except apuesta.DoesNotExist:
                                                            continue

                                                        jugada_json = {}
                                                        if (
                                                            condicion.etiqueta_ref and
                                                            jugada.valor_etq_ref
                                                        ):
                                                            jugada_json['ref'] = str(
                                                                jugada.valor_etq_ref
                                                            )
                                                        else:
                                                            jugada_json['ref'] = ''
                                                        if jugada.valor_americano:
                                                            jugada_json['val'] = str(
                                                                jugada.valor_americano
                                                            ) \
                                                                if jugada.valor_americano <= 0 \
                                                                else str('+') + str(
                                                                    jugada.valor_americano
                                                            )
                                                        else:
                                                            jugada_json['val'] = ''
                                                        jugada_json['pertenece'] = ''
                                                        """
                                                        #jugada.get_pertenece()
                                                        """
                                                        jugada_json['position'] = len(
                                                            modalidad_json['jugadas']
                                                        )
                                                        modalidad_json['jugadas'].append(
                                                            jugada_json
                                                        )
                                            else:
                                                for indice in range(1, condicion.tipo + 1):
                                                    try:
                                                        jugada = apuesta.get_carefully(
                                                            kwargs={
                                                                'encuentros_modalidad': encu_moda,
                                                                'condicion': condicion,
                                                                'indice': indice,
                                                            },
                                                            sistemajuego=self.object_sistema_juego,
                                                            sistemalogros=self.object_sistema_logros,
                                                        )
                                                    except apuesta.DoesNotExist:
                                                        continue

                                                    jugada_json = {}
                                                    if (
                                                        condicion.etiqueta_ref and
                                                        jugada.valor_etq_ref
                                                    ):
                                                        jugada_json['ref'] = str(
                                                            jugada.valor_etq_ref
                                                        )
                                                    else:
                                                        jugada_json['ref'] = ''

                                                    if jugada.valor_americano:
                                                        jugada_json['pertenece'] = jugada \
                                                            .get_pertenece()

                                                        if jugada.valor_americano <= 0:
                                                            jugada_json['val'] = str(
                                                                jugada.valor_americano
                                                            )
                                                        else:
                                                            jugada_json['val'] = str('+') + str(
                                                                jugada.valor_americano
                                                            )
                                                    else:
                                                        jugada_json['val'] = ''
                                                        jugada_json['pertenece'] = ''
                                                    jugada_json['position'] = len(
                                                        modalidad_json['jugadas']
                                                    )

                                                    modalidad_json['jugadas'].append(jugada_json)

                                                coun_encuetro_detail = encuentro \
                                                    .encuentrosdetail_set.all().count()

                                                if condicion.tipo < coun_encuetro_detail:
                                                    for other in range(
                                                        condicion.tipo,
                                                        coun_encuetro_detail
                                                    ):
                                                        jugada_json_vacia = {
                                                            'ref': '',
                                                            'val': '',
                                                            'pertenece': '',
                                                            'position': len(
                                                                modalidad_json['jugadas']
                                                            )
                                                        }
                                                        modalidad_json['jugadas'].append(
                                                            jugada_json_vacia
                                                        )

                                        grupo_json['modalidades'].append(
                                            modalidad_json
                                        )
                                    json_encuentro['grupos'].append(
                                        grupo_json
                                    )
                                cache.set(
                                    'list_logros_encuentro_{0}_{1}'.format(
                                        encuentro.pk,
                                        key_sistema_juego
                                    ),
                                    json_encuentro
                                )

                            json_liga['encuentros'].append(
                                json_encuentro
                            )

                    cache.set(
                        'list_logros_temporada_{0}_{1}'.format(
                            temporada.pk,
                            key_sistema_juego
                        ),
                        json_liga
                    )

                if len(json_liga['encuentros']):
                    json_ligas_list.append(
                        json_liga
                    )
            #################################################
            if context['object_list']:
                context['ligas'] = json_ligas_list
                cache.set(
                    'list_logros_deporte_{0}_{1}'.format(
                        self.deporte,
                        key_sistema_juego
                    ),
                    context['ligas']
                )

        if context['ligas']:
            var_cache = {
                'titulo': 'Reporte - Lista de logros',
                'fecha': self.fecha,
                'deporte': self.deporte.nombre if self.deporte is not None else 'Todos',
                'ligas': context['ligas'],
                'template_name': 'admin_logros/jugadas/print_logros_pdf.html',
            }

            import re
            if self.object_sistema_juego is not None:
                sistema = self.object_sistema_juego.get_lower_ascci()
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
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )
        context['is_consulta'] = self.is_consulta

        return context


class LogrosDatatableView(LogrosListView, BaseDatatableView):
    model = Sorteo
    order_columns = ['horajuego']
    # Fields de busqueda
    filter_search = 'id'

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            equipos = ""
            tam = len(item.encuentrosdetail_set_order())
            for x, equipo in enumerate(item.encuentrosdetail_set_order()):
                equipos += "<span class='tag tag-blue'>{0}</span>".format(
                    equipo.equipos_temporadas.equipo
                )
                if x != (tam - 1):
                    equipos += "<span class='tag tag-nomargin'>vs.</span>"

            json_data.append([
                item.pk,
                "{0} - {1}".format(
                    item.horajuego.strftime("%I:%M %p"),
                    item.horajuego.strftime("%d/%m/%Y")
                ),
                equipos,
                "{0} - {1}".format(
                    item.jornada.temporadas.torneo.nombre,
                    item.jornada.temporadas.nombre,
                ),
                "<span class='tag tag-green'>{0}</span>".format(
                    item.jornada.temporadas.torneo.deporte
                ),
                item.status.name,
                "<a href='" + new_reverse(
                    self,
                    'admin_logros_ecuentros_create_update',
                    kwargs={'pk': item.pk}) + "' class='btn btn-extrasmall {0}''>Asignar logros</a>".format(
                    "btn-green" if item.get_exists_logros() else "btn-danger"
                )
            ])
        return json_data
