# -*- coding: utf-8 -*-
from datetime import timedelta

from admin_comercializacion.models import EventNotificationCadena, types_notification_cadena
from admin_juego.forms import EncuentrosForm, EncuentrosRestrictionForm
from admin_juego.models import (
    Sorteo, SorteoDetalle, ModalidadJuego, ModalidadPeriodo, Fechas,
)
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterDeporteRangoFechaForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from admin_permisologia.models import PermissionsSales
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class EncuentrosView(MyViewBase):
    model = Sorteo
    form_class = EncuentrosForm

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return '?deporte={0}&torneo={1}&fecha_inicio={2}&fecha_fin={2}'.format(
            self.object.jornada.temporadas.torneo.deporte.pk,
            self.object.jornada.temporadas.torneo.pk,
            strFecha(self.object.horajuego).getFecha(),
            strFecha(self.object.horajuego).getFecha()
        )

    def get_queryset(self):
        """
        En esta consulta queda validado a los encuentros que tiene
        acceso un usuario
        """

        if self.get_profile().codename == 'userprofile_master':
            # si es un master tiene derecho a todo
            encuentros = Sorteo.objects.all()
        else:
            # si es un usuario de cadena se hace el filtro respectivo por
            # el sistema de juego asociado
            encuentros = Sorteo.objects.filter(
                jornada__sistema=self.object_sistema_juego
            )

        return encuentros.select_related(
            'status',
            'jornada__temporadas__torneo__deporte',
        )


class EncuentrosCreateView(EncuentrosView, CreateView):
    errors_all = None

    def get_context_data(self, **kwargs):
        context = super(EncuentrosCreateView, self).get_context_data(**kwargs)
        context['errors_all'] = self.errors_all
        return context

    def post(self, request, *args, **kwargs):
        self.errors_all = ''

        equipos = self.request.POST.getlist('equipos')
        temporada = self.request.POST.get('temporada')
        horajuego = self.request.POST.get('horajuego')
        horajuego = now().strptime(horajuego, '%d/%m/%Y %H:%M')
        inicio = horajuego

        if not temporada or int(temporada) == 0:
            return super(EncuentrosCreateView, self).post(
                self, request, *args, **kwargs)

        if len(equipos) > 0:
            indices = {}
            jugadores = {}
            temporada = Fechas.objects.get(
                pk=temporada
            )

            referencias = False
            for obj in equipos:
                equipo = ModalidadJuego.objects.get(
                    pk=obj
                )

                if not equipo.equiposligas_set.filter(
                        liga_id=temporada.torneo_id):
                    self.errors_all = 'El equipo ' + \
                        equipo.nombre + \
                        ' no pertenece a la liga seleccionada.'
                    break

                equipo_temporada = ModalidadPeriodo.objects.get_or_create(
                    temporada=temporada,
                    equipo=equipo
                )[0]

                fin_1 = inicio - timedelta(hours=2)
                fin_2 = inicio + timedelta(hours=2)
                equipo_choques = SorteoDetalle.objects.filter(
                    equipos_temporadas=equipo_temporada,
                    encuentro__horajuego__range=(fin_1, fin_2),
                    encuentro__jornada__sistema=self.object_sistema_juego
                )

                if equipo_choques.exists():
                    self.errors_all = 'El equipo ' + \
                        equipo.nombre + \
                        ' ya tiene un juego ' \
                        'el mismo dia en un ' \
                        'intervalo de 2 horas'
                    break

                if str(self.request.POST.get('indice_' + str(obj))) in indices:
                    indices[str(self.request.POST.get(
                        'indice_' + str(obj)))] += 1
                else:
                    indices[str(self.request.POST.get(
                        'indice_' + str(obj)))] = 1

                try:
                    jugador = self.request.POST.get('jugador_' + str(obj))
                    jugador = SorteoDetalle.objects.filter(
                        jugador_id=jugador,
                        encuentro__horajuego__range=(inicio, fin_1),
                        encuentro__jornada__sistema=self.object_sistema_juego
                    )
                    if jugador.exists():
                        self.errors_all = 'El jugador ' + \
                                          jugador[0].jugador.nombre + \
                                          ' ya tiene un juego el mismo ' \
                                          ' dia en un intervalo de 2 horas'
                        break

                    jugador = self.request.POST.get('jugador_' + str(obj))
                    jugador = SorteoDetalle.objects.filter(
                        jugador_id=jugador,
                        encuentro__horajuego__range=(fin_2, inicio),
                        encuentro__jornada__sistema=self.object_sistema_juego
                    )
                    if jugador.exists():
                        self.errors_all = 'El jugador ' + \
                                          jugador[0].jugador.nombre + \
                                          ' ya tiene un juego el mismo '\
                                          'dia en un intervalo de 2 horas'
                        break

                    if str(self.request.POST.get(
                            'jugador_' + str(obj))) != '0':
                        if str(self.request.POST.get(
                                'jugador_' + str(obj))) in jugadores:
                            jugadores[str(self.request.POST.get(
                                'jugador_' + str(obj)))] += 1
                        else:
                            jugadores[str(self.request.POST.get(
                                'jugador_' + str(obj)))] = 1

                        referencia = self.request.POST.get(
                            'referencia_' + str(obj))
                        if referencia is None or referencia == '' and jugadores:
                            referencias = True

                except Exception:
                    pass

            jugadores_exist = NumeroSorteo.objects.filter(
                tipo__deporte_id=temporada.torneo.deporte_id
            )

            if jugadores_exist.exists():

                invalid_indice = False
                for indice in indices:
                    if indices[indice] > 1:
                        invalid_indice = True
                        break
                if invalid_indice:
                    self.errors_all = 'Los equipos deben ' + \
                                      'tener indices de posision distintos'
                else:
                    invalid_jugador = False
                    for jugador in jugadores:
                        if jugadores[jugador] > 1:
                            invalid_jugador = True
                            break

                    if invalid_jugador:
                        self.errors_all = 'Los equipos deben ' + \
                                          ' tener jugadores diferentes'
                    else:
                        if referencias:
                            self.errors_all = 'Las referencias de ' \
                                              'los jugadores son obligatorias'

        if self.errors_all:
            return super(EncuentrosCreateView, self).get(
                self, request, *args, **kwargs)
        else:
            if self.request.POST['_save'] == '_addanother':
                super(
                    EncuentrosCreateView,
                    self).post(
                    self,
                    request,
                    *
                    args,
                    **kwargs)
                return super(EncuentrosCreateView, self).get(
                    self, self.request, *args, **kwargs)
            else:
                return super(EncuentrosCreateView, self).post(
                    self, request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.save()

        equipos = self.request.POST.getlist('equipos')
        if len(equipos) > 0:
            for obj in equipos:
                equipo = ModalidadJuego.objects.get(
                    pk=obj
                )

                try:
                    equipo_temporada = ModalidadPeriodo.objects.get_or_create(
                        temporada=form.instance.jornada.temporadas,
                        equipo=equipo
                    )[0]
                except Exception:
                    equipo_temporada = ModalidadPeriodo.objects.get_or_update(
                        temporada=form.instance.jornada.temporadas,
                        equipo=equipo
                    )[0]

                indice = self.request.POST.get('indice_' + str(obj))
                try:
                    jugador = NumeroSorteo.objects.get(
                        pk=self.request.POST.get('jugador_' + str(obj))
                    )
                except Exception:
                    jugador = None
                referencia = self.request.POST.get('referencia_' + str(obj))
                SorteoDetalle.objects.create(
                    encuentro=form.instance,
                    equipos_temporadas=equipo_temporada,
                    indice=indice,
                    jugador=jugador,
                    referencia=referencia
                )

        # Solo se envian en la actualizacion
        # form.instance.set_cache_jugadres()

        return super(EncuentrosCreateView, self).form_valid(form)


class EncuentrosDeleteView(EncuentrosView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class EncuentrosDetailView(EncuentrosView, DetailView):

    def get_url_historic_result(self, encuentro, sistema):
        resultado = encuentro.get_resultado(sistema)
        if resultado:
            return reverse(
                'admin_historic_app_model_ref',
                kwargs={
                    'app': 'admin_resultados',
                    'model': 'resultados',
                    'ref': resultado.pk
                }
            )
        else:
            return False

    def get_object(self):
        objecto = super(EncuentrosDetailView, self).get_object()
        objecto.get_url_historic_result = self.get_url_historic_result(
            objecto, self.object_sistema_juego)
        return objecto


class EncuentrosListView(EncuentrosView, ListView):
    """
    Clase que implementa el listar, aqui se añade un segundo nivel al
    queryset
    """
    form_class = FilterDeporteRangoFechaForm
    filter_form = None

    def get_queryset(self):
        """
        Es este get_queryset se hace el respectivo filtro por
        los fields del formulario
        """
        encuentros = super(EncuentrosListView, self).get_queryset()
        if self.get_filter_form().is_valid():
            """
            Es caso de ser valido el form se ejecutan los filtros
            """
            fecha_inicio = strFecha(self.get_filter_form().cleaned_data[
                                    'fecha_inicio']).getFecha()
            fecha_fin = strFecha(
                self.get_filter_form().cleaned_data['fecha_fin']).getFecha()
            deporte = self.get_filter_form().cleaned_data['deporte']
            torneo = self.get_filter_form().cleaned_data['torneo']
            encuentros = encuentros.filter(
                horajuego__range=(
                    fecha_inicio + hora_cero,
                    fecha_fin + hora_23),
            )
            if torneo:
                encuentros = encuentros.filter(
                    jornada__temporadas__torneo=torneo
                )
            elif deporte:
                encuentros = encuentros.filter(
                    jornada__temporadas__torneo__deporte=deporte,
                )
        else:
            encuentros = Sorteo.objects.none()

        return encuentros


class EncuentrosUpdateView(EncuentrosView, UpdateView):
    errors_all = None

    def get_queryset(self):
        """
        En esta consulta queda validado a los encuentros que tiene
        acceso un usuario
        """

        encuentros = super(EncuentrosUpdateView, self).get_queryset()

        return encuentros.filter(
            horajuego__gte=(
                now() -
                timedelta(
                    days=Sorteo.maximo_dias_olgura)).date()
        )

    def get_context_data(self, **kwargs):
        context = super(EncuentrosUpdateView, self).get_context_data(**kwargs)
        equipos = SorteoDetalle.objects.select_related('equipos_temporadas__equipo').filter(
            encuentro_id=self.object.pk
        ).order_by('indice')
        equipos_array = []
        for equipo in equipos:
            equipo_json = {}
            equipo_json['pk'] = equipo.equipos_temporadas.equipo.pk
            equipo_json['nombre'] = equipo.equipos_temporadas.equipo.nombre
            equipo_json['logo'] = equipo.equipos_temporadas.equipo.logo
            equipo_json['indice'] = equipo.indice
            equipo_json['jugador'] = {}
            if equipo.jugador is not None:
                equipo_json['jugador'] = {
                    'pk': equipo.jugador.pk,
                    'nombre': equipo.jugador.get_label(),
                    'tipo': equipo.jugador.tipo.pk,
                    'tipo_nombre': equipo.jugador.tipo.nombre,
                }

                equipo_json['jugadores'] = TipoNumeroSorteo.objects.filter(
                    deporte_id=self.object.jornada.temporadas.torneo.deporte_id
                ).exclude(
                    pk=equipo.jugador.tipo.pk
                )

            else:
                jugadores_exist = NumeroSorteo.objects.filter(
                    tipo__deporte_id=self.object.jornada.temporadas.torneo.deporte_id
                )

                if jugadores_exist.exists():
                    equipo_json['jugador'] = {
                        'pk': 0,
                        'nombre': '',
                        'tipo': 0,
                        'tipo_nombre': '',
                    }
                    equipo_json['jugadores'] = TipoNumeroSorteo.objects.filter(
                        deporte_id=self.object.jornada.temporadas.torneo.deporte_id
                    )

            if equipo.referencia:
                equipo_json['referencia'] = equipo.referencia
            else:
                equipo_json['referencia'] = ''
            equipos_array.append(equipo_json)
        context['equipos'] = equipos_array

        indices = []
        for i, indice in enumerate(equipos):
            indices.append({'pk': (i + 1)})
        context['indices'] = indices

        context['errors_all'] = self.errors_all

        return context

    def post(self, request, *args, **kwargs):
        self.errors_all = ''

        self.object = self.get_object()

        equipos = self.request.POST.getlist('equipos')
        horajuego = self.request.POST.get('horajuego', )
        horajuego = now().strptime(horajuego, '%d/%m/%Y %H:%M')
        inicio = horajuego
        temporada = self.object.jornada.temporadas

        if len(equipos) > 0:
            indices = {}
            jugadores = {}
            referencias = False
            for obj in equipos:
                equipo = ModalidadJuego.objects.get(
                    pk=obj
                )
                equipo_temporada = ModalidadPeriodo.objects.get_or_create(
                    temporada=temporada,
                    equipo=equipo
                )[0]

                fin_1 = inicio - timedelta(hours=2)
                fin_2 = inicio + timedelta(hours=2)
                equipo_choques = SorteoDetalle.objects.filter(
                    equipos_temporadas=equipo_temporada,
                    encuentro__horajuego__range=(fin_1, fin_2),
                    encuentro__jornada__sistema=self.object_sistema_juego
                ).exclude(
                    encuentro_id=self.object.pk
                )

                if equipo_choques.exists():
                    self.errors_all = 'El equipo ' + \
                                      equipo.nombre + \
                                      ' ya tiene un juego ' + \
                                      'el mismo dia en un ' + \
                                      'intervalo de a 2 horas'
                    break

                try:
                    jugador = self.request.POST.get('jugador_' + str(obj))
                    jugador = SorteoDetalle.objects.filter(
                        jugador_id=jugador,
                        encuentro__horajuego__range=(inicio, fin_1),
                        encuentro__jornada__sistema=self.object_sistema_juego
                    ).exclude(
                        encuentro_id=self.object.pk
                    )
                    if jugador.exists():
                        self.errors_all = 'El jugador ' + \
                                          jugador[0].jugador.nombre + \
                                          ' ya tiene un juego el ' + \
                                          'mismo dia en un intervalo ' + \
                                          'de 2 horas'
                        break

                    jugador = self.request.POST.get('jugador_' + str(obj))
                    jugador = SorteoDetalle.objects.filter(
                        jugador_id=jugador,
                        encuentro__horajuego__range=(fin_2, inicio),
                        encuentro__jornada__sistema=self.object_sistema_juego
                    ).exclude(
                        encuentro_id=self.object.pk
                    )

                    if jugador.exists():
                        self.errors_all = 'El jugador ' + \
                                          jugador[0].jugador.nombre + \
                                          ' ya tiene un juego el ' + \
                                          'mismo dia en un ' + \
                                          'intervalo de 2 horas'
                        break

                    if str(self.request.POST.get(
                            'indice_' + str(obj))) in indices:
                        indices[str(self.request.POST.get(
                            'indice_' + str(obj)))] += 1
                    else:
                        indices[str(self.request.POST.get(
                            'indice_' + str(obj)))] = 1

                    if str(self.request.POST.get(
                            'jugador_' + str(obj))) != '0':
                        if str(self.request.POST.get(
                                'jugador_' + str(obj))) in jugadores:
                            jugadores[str(self.request.POST.get(
                                'jugador_' + str(obj)))] += 1
                        else:
                            jugadores[str(self.request.POST.get(
                                'jugador_' + str(obj)))] = 1

                        referencia = self.request.POST.get(
                            'referencia_' + str(obj))
                        if referencia is None or referencia == '':
                            referencias = True

                except Exception:
                    pass

            jugadores_exist = NumeroSorteo.objects.filter(
                tipo__deporte_id=temporada.torneo.deporte.pk
            )

            if jugadores_exist.exists():

                invalid_indice = False
                for indice in indices:
                    if indices[indice] > 1:
                        invalid_indice = True
                        break
                if invalid_indice:
                    self.errors_all = 'Los equipos ' + \
                                      'deben tener indices ' +\
                                      'de posision distintos'
                else:
                    invalid_jugador = False
                    for jugador in jugadores:
                        if jugadores[jugador] > 1:
                            invalid_jugador = True
                            break

                    if invalid_jugador:
                        self.errors_all = 'Los equipos deben ' + \
                                          'tener jugadores diferentes'
                    else:
                        if referencias:
                            self.errors_all = 'Las referencias ' + \
                                              'de los jugadores ' + \
                                              'son obligatoria'

        if self.errors_all:
            return super(EncuentrosUpdateView, self).get(
                self, request, *args, **kwargs)
        else:
            return super(EncuentrosUpdateView, self).post(
                self, request, *args, **kwargs)

    def form_valid(self, form):

        form.instance.save()

        equipos = self.request.POST.getlist('equipos')

        lanzar_actualizacion_jugadas = False

        if len(equipos) > 0:
            new_equipos = []
            for obj in equipos:
                equipo = ModalidadJuego.objects.get(
                    pk=obj
                )
                equipo_temporada = ModalidadPeriodo.objects.get_or_create(
                    temporada=form.instance.jornada.temporadas,
                    equipo=equipo
                )[0]

                indice = self.request.POST.get('indice_' + str(obj))
                try:
                    jugador = NumeroSorteo.objects.get(
                        pk=self.request.POST.get('jugador_' + str(obj))
                    )
                except Exception:
                    jugador = None

                referencia = self.request.POST.get('referencia_' + str(obj))
                detalle_encuentro = SorteoDetalle.objects.get_or_create(
                    encuentro=form.instance,
                    equipos_temporadas=equipo_temporada
                )[0]
                if lanzar_actualizacion_jugadas is False and detalle_encuentro.indice != indice:
                    lanzar_actualizacion_jugadas = True

                detalle_encuentro.indice = indice
                detalle_encuentro.jugador = jugador
                detalle_encuentro.referencia = referencia
                detalle_encuentro.save()

                new_equipos.append(
                    detalle_encuentro.pk
                )
            for old_detalle_encuentro in SorteoDetalle.objects.filter(
                encuentro=form.instance
            ).exclude(
                pk__in=new_equipos
            ):

                old_detalle_encuentro.delete()
        form.instance.save()

        if form.instance.get_exists_logros():
            # solo si hay jugadas se envia la info de el
            form.instance.set_cache_jugadres()

            if lanzar_actualizacion_jugadas:
                # si actualizar las jugadas en caso de que cambie el indice
                form.instance.set_cache_jugadas()

        return super(EncuentrosUpdateView, self).form_valid(form)


class EncuentrosRestrictionView(EncuentrosView, UpdateView):
    form_class = EncuentrosRestrictionForm
    template_name = 'admin_juego/encuentros/encuentros_restriction.html'

    def form_valid(self, form):
        comercializadoras = form.cleaned_data.get('comercializadora')

        json_encuentro = {}
        json_encuentro['pk'] = self.object.pk

        list_comercializadoras = list(
            comercializadoras.values_list(
                'id', flat=True))

        habilitados = PermissionsSales.objects.filter(
            encuentro_id=self.object.id,
        ).exclude(
            comercializadora_id__in=list_comercializadoras
        )

        for habilitado in habilitados:
            json_encuentro['action'] = 'add'

            kwargs_notificacion = {
                'data_origin': types_notification_cadena['encuentro'][0],
                'data': json_encuentro
            }

            kwargs_notificacion[
                habilitado.comercializadora.get_object().prefix_filter
            ] = habilitado.comercializadora.get_object().pk

            EventNotificationCadena.objects.create(
                **kwargs_notificacion
            )

        habilitados.delete()

        for comercializadora in comercializadoras:

            if not PermissionsSales.objects.filter(
                encuentro_id=self.object.id,
                comercializadora_id=comercializadora.id
            ).exists():

                json_encuentro['action'] = 'remove'

                PermissionsSales.objects.create(
                    encuentro=self.object,
                    comercializadora=comercializadora
                )

                kwargs_notificacion = {
                    'data_origin': types_notification_cadena['encuentro'][0],
                    'data': json_encuentro
                }

                kwargs_notificacion[
                    comercializadora.get_object().prefix_filter
                ] = comercializadora.get_object().pk

                EventNotificationCadena.objects.create(
                    **kwargs_notificacion
                )

        return HttpResponseRedirect(self.get_success_url())


class EncuentrosListbyTemporadaAjax(View):

    def dispatch(self, request, *args, **kwargs):

        fecha_inicio = request.REQUEST.get('fecha_inicio')
        fecha_fin = request.REQUEST.get('fecha_fin')

        my_kwargs = {}
        my_kwargs['jornada__temporadas_id'] = request.REQUEST['temporada']

        if len(fecha_inicio.split(' ')) == 1:
            my_kwargs['horajuego__range'] = (
                fecha_inicio + hora_cero, fecha_fin + hora_23
            )
        else:
            my_kwargs['horajuego__range'] = (
                fecha_inicio, fecha_fin
            )

        if kwargs['object_user'].profile.codename != 'userprofile_master':
            my_kwargs['jornada__sistema'] = kwargs['object_sistema_juego']

        encuentros = Sorteo.objects.filter(
            **my_kwargs
        )

        def label_from_instance_encuentros(obj):
            objFecha = strFecha(obj.horajuego)
            campo = '{0} Fecha: {1} {2} ModalidadJuego: '.format(
                obj.pk,
                objFecha.getFecha(),
                objFecha.getHora(),
            )
            for obj2 in obj.encuentrosdetail_set_order():
                nombre = obj2.equipos_temporadas.equipo.nombre
                campo = campo + ' - ' + nombre
            return campo

        result = []
        for obj in encuentros:
            result.append(
                {
                    'pk': obj.pk,
                    'nombre': label_from_instance_encuentros(obj)
                }
            )

        return HttpResponse(
            content=JsonDumps(
                result
            ),
            content_type='application/json'
        )


class EncuentrosDatatableView(EncuentrosListView, BaseDatatableView):
    model = Sorteo
    order_columns = ['horajuego']
    # Fields de busqueda
    filter_search = ['id', 'horajuego']

    opcions_url = [
        'admin_juego_' + model.prefix_filter_plural + '_detail/' + Icons.detail,
        'admin_juego_' + model.prefix_filter_plural + '_delete/' + Icons.delete,
    ]

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            if item.get_is_edit():
                self.opcions_url.append(
                    'admin_juego_' +
                    self.model.prefix_filter_plural +
                    '_update/' +
                    Icons.update,
                )

            equipos = ''
            tam = len(item.encuentrosdetail_set_order())
            for x, equipo in enumerate(item.encuentrosdetail_set_order()):
                equipos += '<span class="tag tag-light-green">{0}</span>'.format(
                    equipo.equipos_temporadas.equipo
                )
                if x != (tam - 1):
                    equipos += '<span class="tag tag-nomargin">vs.</span>'

            json_data.append([
                str(item.pk),
                '<span class="tag tag-nomarginup"><span>{0}</span></span>'.format(
                    item.horajuego.strftime('%d/%m/%Y')
                ),
                '<span class="tag tag-nomarginup"><span>{0}</span></span>'.format(
                    item.horajuego.strftime('%I:%M %p')
                ),
                equipos,
                '<span class="tag tag-nomarginup"><span class="tag tag-nomarginupb tag-blue">{0}</span>'
                '<span>{1} - {2}</span></span>'.format(
                    item.jornada.temporadas.torneo.nombre,
                    item.jornada.temporadas.nombre,
                    item.jornada.jornada
                ),
                '<span class="tag tag-green">{0}</span>'.format(
                    item.jornada.temporadas.torneo.deporte
                ),
                item.status.name,
                self.get_opcions(item.pk)
            ])
            if item.get_is_edit():
                self.opcions_url.pop(-1)

        return json_data
