# -*- coding: utf-8 -*-

from admin_comercializacion.models import Bancas, Bloques, Operadoras
from admin_finanzas.task import AsyncSuspenderEncuentro
from admin_juego.models import Condiciones, TipoProducto, TipoProducto_Grupos, Sorteo, apuesta
from admin_lib.util_forms import FORMAT_STR_DATE_FORM, WidgetCustomizeForms
from admin_resultados.models import Anotaciones, AnotacionesDetail, Resultados, ResultadosRestric
from admin_status.models import Status
from django import forms
from django.db.models import Q
from django.utils.timezone import now


class EncuentrosResultadosCreateUpdateForm(WidgetCustomizeForms, forms.ModelForm):
    '''
    Formulario dinamico para asignar resutados,
    en base a las modalidades disponibles en cada
    encuentro
    '''

    status_result = forms.ModelChoiceField(
        queryset=Status.objects.only('pk', 'name', 'codename').filter(content_type=2),
        required=True,
        empty_label='Seleccione un {0}'.format(Status._meta.verbose_name)
    )

    restric_result = forms.MultipleChoiceField(
        required=False,
        label='ModalidadJuego a excluir'
    )

    class Meta:
        model = Sorteo
        exclude = ['jornada', 'grupo', 'horajuego', 'horacierre', 'status', 'pk_clone']

    def __init__(self, *args, **kwargs):
        super(EncuentrosResultadosCreateUpdateForm, self).__init__(*args, **kwargs)
        '''
        Se crea la data necesaria vacia inicialmente
        en caso de no existir, para generar los fields
        y poder cargar los datos
        '''

        self.sistema_resultados = self.view.get_object_sistema_resultados()

        self.pk_habilitado = ' status{0}'.format(
            self.fields['status_result'].queryset.get(
                codename='status_habilitado'
            ).pk
        )

        self.pk_valido_no_terminado = ' status{0}'.format(
            self.fields['status_result'].queryset.get(
                codename='status_valido_no_terminado'
            ).pk
        )

        self.resultado = Resultados.get_or_create_or_flush(
            encuentro=self.instance,
            sistema=self.sistema_resultados)

        self.status_old = self.resultado.status
        self.fields['status_result'].initial = self.resultado.status
        deporte = self.instance.jornada.temporadas.torneo.deporte

        self.fields['restric_result'].initial = []
        self.CHOICES_RESTRIC = []
        self.pk_modalidad_ganador = None
        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=deporte
        ).select_related('grupo').order_by('grupo__orden'):
            grupo_vec = ['', []]
            grupo_vec[0] = deporte_grupo.grupo.nombre

            abr = ''
            for name in deporte_grupo.grupo.nombre.split(' '):
                abr += name[0]
            for modalidad_grupo in deporte_grupo.grupo \
                    .modalidades_grupos_set.all()\
                    .select_related('modalidad').order_by('modalidad__orden'):

                if modalidad_grupo.deporte_restriccion.filter(
                    pk=deporte.pk
                ).exists():
                    continue
                option = [
                    '{0}_{1}'.format(
                        deporte_grupo.grupo_id,
                        modalidad_grupo.modalidad_id
                    ),
                    '{0} - {1}'.format(abr, modalidad_grupo.modalidad.modalidad)
                ]

                if self.pk_modalidad_ganador is None:
                    if modalidad_grupo.modalidad.codename == 'ganador':
                        self.pk_modalidad_ganador = modalidad_grupo.modalidad_id

                if self.resultado.resultadosrestric_set.filter(
                        grupo_id=deporte_grupo.grupo_id,
                        modalidad_id=modalidad_grupo.modalidad_id).exists():
                    self.fields['restric_result'].initial += option

                grupo_vec[1].append(
                    option
                )

            if len(grupo_vec[1]):
                self.CHOICES_RESTRIC.append(grupo_vec)

        self.fields['restric_result'].choices = self.CHOICES_RESTRIC

        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=deporte
        ).exclude(
            grupo__codename='referencia'
        ).select_related('grupo').order_by('grupo__orden'):

            anotaciones = Anotaciones.get_or_create_or_flush(
                resultado=self.resultado,
                grupo=deporte_grupo.grupo
            )[0]

            if deporte_grupo.grupo.codename == 'combinadas':
                grupos = deporte_grupo.grupo.modalidades_grupos_set.all()
                for modalidad_grupo in grupos.order_by('modalidad__orden'):

                    if modalidad_grupo.deporte_restriccion.filter(
                        pk=self.instance.jornada.temporadas.torneo.deporte.pk
                    ).exists():
                        continue

                    for condicion in modalidad_grupo.modalidad \
                            .condiciones_set.all().select_related('modalidad').order_by('orden'):

                        if (condicion.modalidad.codename == 'h+c+e' or
                                condicion.modalidad.codename == 'anota_1ro' or
                                condicion.modalidad.codename == 'si/no'):

                            anotacion = AnotacionesDetail.get_or_create_or_flush(
                                anotacion=anotaciones,
                                condicion=condicion
                            )[0]

                            if condicion.modalidad.codename == 'h+c+e':
                                self.fields['resultado_' + str(anotacion.pk)] = forms.IntegerField(
                                    required=False,
                                    label=condicion.modalidad.modalidad,
                                    help_text='Ingrese resultado individual para grupo '
                                    ' ' + deporte_grupo.grupo.nombre + ', modalidad '
                                    ' ' + condicion.modalidad.modalidad + ', condicion '
                                    ' ' + condicion.nombre
                                )
                                self.customize(
                                    field='resultado_' + str(anotacion.pk),
                                    validation='[+-]?[0-9]+',
                                    obj_valor=anotacion,
                                    obj_grupo=deporte_grupo.grupo,
                                    obj_modalidad=condicion.modalidad,
                                )
                            else:
                                self.fields['resultado_' + str(anotacion.pk)] = forms.ChoiceField(
                                    widget=forms.RadioSelect(),
                                    required=False,
                                    label='Seleccione ' + condicion.nombre,
                                    help_text='Ingrese resultado individual para grupo '
                                    ' ' + deporte_grupo.grupo.nombre + ', modalidad '
                                    ' ' + condicion.modalidad.modalidad + ', condicion '
                                    ' ' + condicion.nombre
                                )

                                choices = []
                                for i, parse in enumerate(condicion.nombre.split('/')):
                                    choices.append((i + 1, parse))

                                self.fields['resultado_' + str(anotacion.pk)].choices = choices
                                self.customize(
                                    field='resultado_' + str(anotacion.pk),
                                    obj_valor=anotacion,
                                    obj_grupo=deporte_grupo.grupo,
                                    obj_modalidad=condicion.modalidad,
                                )

            else:
                for equipo in self.instance.encuentrosdetail_set.all()\
                        .select_related('equipos_temporadas__equipo').order_by('indice'):
                    anotacion = AnotacionesDetail.get_or_create_or_flush(
                        anotacion=anotaciones,
                        encuentro_detail=equipo
                    )[0]
                    self.fields['resultado_' + str(anotacion.pk)] = forms.IntegerField(
                        required=False,
                        label=equipo.equipos_temporadas.equipo.nombre,
                        help_text='Ingrese el resultado para procesamiento automatico de '
                        ' ' + deporte_grupo.grupo.nombre + ' para '
                        ' ' + equipo.equipos_temporadas.equipo.nombre
                    )

                    self.customize(
                        field='resultado_' + str(anotacion.pk),
                        validation='[0-9]+',
                        obj_valor=anotacion,
                        obj_grupo=deporte_grupo.grupo,
                    )

    def customize(self, field, validation=None, obj_valor=None, obj_grupo=None, obj_modalidad=None):
        self.fields[field].widget.attrs['class'] = 'status'
        if validation is not None:
            self.fields[field].widget.attrs['pattern'] = validation
        if self.fields[field].required:
            self.fields[field].widget.attrs['required'] = ''
        self.fields[field].widget.attrs['placeholder'] = self.fields[field].label
        self.fields[field].widget.attrs['title'] = self.fields[field].help_text

        if isinstance(self.fields[field], forms.IntegerField):
            self.fields[field].widget.attrs['class'] += ' input-resultado'
            if obj_grupo:
                self.fields[field].widget.attrs['class'] += ' code-grupo code-grupo-{0}'.format(
                    obj_grupo.pk
                )

        self.fields[field].widget.attrs['class'] += self.pk_habilitado
        # Agregando clases para manejar la edicion de del estatus dinamico
        if obj_grupo:
            if obj_grupo.codename == 'juego_completo':
                self.fields[field].widget.attrs['class'] += self.pk_valido_no_terminado
            elif obj_grupo.codename == 'combinadas':
                if obj_modalidad:
                    if obj_modalidad.codename == 'anota_1ro' or obj_modalidad.codename == 'si/no':
                        self.fields[field].widget.attrs['class'] += self.pk_valido_no_terminado
                    else:
                        if self.resultado.status.codename == 'status_valido_no_terminado':
                            obj_valor.puntaje = None
                            obj_valor.save()

            else:
                if self.resultado.status.codename == 'status_valido_no_terminado':
                    obj_valor.puntaje = None
                    obj_valor.save()

        if obj_grupo:
            if obj_modalidad:
                self.fields[field].widget.attrs['class'] += ' field-{0}-{1}'.format(
                    obj_grupo.pk,
                    obj_modalidad.pk
                )
            # Este codigo tambien oculta los input
            '''
            elif self.pk_modalidad_ganador:
                self.fields[field].widget.attrs['class'] += ' field-{0}-{1}'.format(
                    obj_grupo.pk,
                    self.pk_modalidad_ganador
                )
            '''

        self.fields[field].initial = obj_valor.puntaje

    def save(self, commit=True, *args, **kwargs):
        self.resultado.status = self.cleaned_data.get('status_result')
        self.resultado.updated_at = now()
        self.resultado.save(update_fields=['updated_at', 'status'])

        restric_result = self.cleaned_data.get('restric_result')
        for restric_str in restric_result:
            restric = restric_str.split('_')
            if self.resultado.resultadosrestric_set.filter(
                    grupo_id=restric[0], modalidad_id=restric[1]).exists() is False:
                ResultadosRestric.objects.create(
                    resultado=self.resultado,
                    grupo_id=restric[0],
                    modalidad_id=restric[1],
                )
        # Eliminando grupos y modalidades no asociados
        for restric_object in self.resultado.resultadosrestric_set.all():
            if '{0}_{1}'.format(restric_object.grupo_id, restric_object.modalidad_id) not in restric_result:
                restric_object.delete()

        # =============================================================
        #   Se arma el kwargs para el filtro de tickets, este depende
        #   Del sistema de juego usado

        object_sistema = self.sistema_resultados.comercializadora.get_object()
        kwargs_async = {}
        key = 'ticket__{0}'.format(object_sistema.get_prefix_kwargs_by_level_tickets())
        kwargs_async[key] = object_sistema.pk

        if object_sistema.user_type_codename == 'userprofile_operadora':
            # se exluyen todas bancas y multibancas con derecho a resultados activado
            # en la operadora seleccionada

            # filtrando bancas sin resultados
            kwargs_async[key.replace('__bloque__operadora_id', '__is_resultados')] = False

            # filtrando bloques sin resultados
            kwargs_async[key.replace('__operadora_id', '__is_resultados')] = False

            # filtrando bancas sin sistemas de juego
            kwargs_async[key.replace('__bloque__operadora_id', '__is_sistema_juego')] = False

            # filtrando bloques sin sistema de juego
            kwargs_async[key.replace('__operadora_id', '__is_sistema_juego')] = False

        elif object_sistema.user_type_codename == 'userprofile_bloque':
            # Se exluyen todas las bancas con derecho a resultados activado
            # en la multibanca seleccionada

            # filtrando bancas sin resultados
            kwargs_async[key.replace('__bloque_id', '__is_resultados')] = False

            # filtrando bancas sin sistemas de juego
            kwargs_async[key.replace('__bloque_id', '__is_sistema_juego')] = False

        elif object_sistema.user_type_codename == 'userprofile_banca':
            # Se filtra solo por la banca a la que pertenece el sistema de juego
            pass
        # =============================================================
        if self.status_old.codename == 'status_habilitado' or self.status_old.codename == 'status_valido_no_terminado':
            if self.resultado.status.codename == 'status_inhabilitado':
                AsyncSuspenderEncuentro.delay(
                    *(),
                    **{
                        'encuentro': self.instance.pk,
                        'filter_cadena': kwargs_async
                    }
                )

        if (self.resultado.status.codename != 'status_habilitado' and
                self.resultado.status.codename != 'status_valido_no_terminado'):
            return self.instance

        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=self.instance.jornada.temporadas.torneo.deporte
        ).exclude(
            grupo__codename='referencia'
        ).select_related('grupo').order_by('grupo__orden'):

            anotaciones = Anotaciones.objects.get(
                resultado=self.resultado,
                grupo=deporte_grupo.grupo)

            if deporte_grupo.grupo.codename == 'combinadas':
                grupos = deporte_grupo.grupo.modalidades_grupos_set.all()
                for modalidad_grupo in grupos.select_related('modalidad').order_by('modalidad__orden'):

                    if modalidad_grupo.deporte_restriccion.filter(
                        pk=self.instance.jornada.temporadas.torneo.deporte.pk
                    ).exists():
                        continue

                    for condicion in modalidad_grupo.modalidad \
                            .condiciones_set.all().select_related('modalidad').order_by('orden'):

                        if (condicion.modalidad.codename == 'h+c+e' or
                                condicion.modalidad.codename == 'anota_1ro' or
                                condicion.modalidad.codename == 'si/no'):

                            anotacion = AnotacionesDetail.objects.get(
                                anotacion=anotaciones,
                                condicion=condicion
                            )
                            anotacion.puntaje = self.cleaned_data.get(
                                'resultado_' + str(anotacion.pk))
                            if anotacion.puntaje is None or anotacion.puntaje == '':
                                anotacion.puntaje = None
                            anotacion.referencia = self.save_combinadas(anotacion)
                            anotacion.save()
                    self.save_runline(anotaciones, 'super_runline')
            else:
                puntaje_total = 0
                for equipo in self.instance.encuentrosdetail_set.all().order_by('indice'):
                    anotacion = AnotacionesDetail.objects.get(
                        anotacion=anotaciones,
                        encuentro_detail=equipo,
                        condicion__isnull=True
                    )
                    anotacion.puntaje = self.cleaned_data.get('resultado_' + str(anotacion.pk))
                    if anotacion.puntaje is None or anotacion.puntaje == '':
                        anotacion.puntaje = None
                        puntaje_total = None
                    else:
                        puntaje_total += anotacion.puntaje
                    anotacion.save()

                self.save_altabaja(puntaje_total, anotaciones)
                self.save_runline(anotaciones, 'runline')

        return self.instance

    def save_combinadas(self, anotaciondetail):
        codename = 'anota_1ro'
        referencia = ''

        process = True
        if self.resultado.resultadosrestric_set.filter(
            grupo_id=anotaciondetail.anotacion.grupo_id,
            modalidad__codename=codename
        ).exists():
            process = False

        if process:
            if anotaciondetail.puntaje is not None:
                if anotaciondetail.condicion.modalidad.codename == codename:
                    jugadas = apuesta.objects.filter(
                        encuentros_modalidad__encuentro_id=anotaciondetail.anotacion.resultado.encuentro_id,
                        encuentros_modalidad__modalidad_grupo__grupo_id=anotaciondetail.anotacion.grupo_id,
                        condicion__modalidad__codename=codename
                    ).select_related('detalle_encuentro__equipos_temporadas__equipo')

                    if jugadas.exists():
                        for jugada in jugadas:
                            if int(jugada.indice) == int(anotaciondetail.puntaje):
                                referencia = jugada.detalle_encuentro.equipos_temporadas.equipo.nombre
                                break
        return referencia

    def save_altabaja(self, puntaje, anotacion):
        codename = 'alta/baja'
        condicion = Condiciones.objects.get(
            modalidad__codename=codename
        )

        process = True
        if self.resultado.resultadosrestric_set.filter(
            grupo_id=anotacion.grupo_id,
            modalidad_id=condicion.modalidad_id
        ).exists():
            process = False

        jugadas = apuesta.objects.filter(
            encuentros_modalidad__encuentro_id=anotacion.resultado.encuentro_id,
            encuentros_modalidad__modalidad_grupo__grupo_id=anotacion.grupo_id,
            condicion__modalidad__codename=codename
        )

        anotacions = AnotacionesDetail.get_or_create_or_flush(
            anotacion=anotacion,
            condicion=condicion
        )[0]

        referencia = ''
        if process:
            anotacions.puntaje = puntaje
            if puntaje is not None:
                if jugadas.exists():
                    encuentros_modalidad = jugadas[0].encuentros_modalidad
                    if encuentros_modalidad.etiqueta_ref is not None:
                        ref = encuentros_modalidad.etiqueta_ref.replace(' ', '')
                        if ref:
                            ref = float(ref.replace(',', '.'))
                            if ref > puntaje:
                                referencia = '(Baja)'
                            elif ref < puntaje:
                                referencia = '(Alta)'

        anotacions.referencia = referencia
        anotacions.save(update_fields=['referencia', 'puntaje'])

    def save_runline(self, anotacion, codename):
        condicion = Condiciones.objects.get(
            modalidad__codename=codename
        )

        process = True
        if self.resultado.resultadosrestric_set.filter(
            grupo_id=anotacion.grupo_id,
            modalidad_id=condicion.modalidad_id
        ).exists():
            process = False

        jugadas = apuesta.objects.filter(
            encuentros_modalidad__encuentro=anotacion.resultado.encuentro,
            encuentros_modalidad__modalidad_grupo__grupo=anotacion.grupo,
            condicion__modalidad__codename=codename,
            origen=None
        )
        if process and anotacion.resultado.encuentro.status.codename != 'status_valido_no_terminado':
            if jugadas.exists():

                if codename == 'super_runline':
                    anotacion_copia = anotacion.resultado.anotaciones_set.get(
                        grupo__codename='juego_completo'
                    )

                    anotacionesdetail = anotacion_copia.anotacionesdetail_set.all().exclude(
                        condicion__modalidad__codename='alta/baja'
                    )
                elif codename == 'runline':
                    anotacionesdetail = anotacion.anotacionesdetail_set.all().exclude(
                        condicion__isnull=False
                    )

                puntaje = 0
                referencia = True

                puntajes = []
                for jugada in jugadas:
                    if jugada.valor_etq_ref:
                        puntaje = anotacionesdetail.get(
                            encuentro_detail=jugada.detalle_encuentro,
                            condicion__isnull=True
                        ).puntaje
                        if puntaje:
                            puntajes.append(puntaje)
                    else:
                        referencia = False
                        anotacions = AnotacionesDetail.get_or_create_or_flush(
                            anotacion=anotacion,
                            encuentro_detail=jugada.detalle_encuentro,
                            condicion=condicion)[0]
                        anotacions.puntaje = None
                        anotacions.save()

                if referencia is True and len(puntajes) == 2:
                    runlines = [0, 0]
                    if puntajes[0] > puntajes[1]:
                        runlines[0] = puntajes[0] - puntajes[1]
                        runlines[1] = puntajes[1] - puntajes[0]
                    elif puntajes[1] > puntajes[0]:
                        runlines[0] = puntajes[0] - puntajes[1]
                        runlines[1] = puntajes[1] - puntajes[0]

                    i = 0
                    for jugada in jugadas:
                        if jugada.valor_etq_ref:
                            anotacion_puntaje = AnotacionesDetail.get_or_create_or_flush(
                                anotacion=anotacion,
                                encuentro_detail=jugada.detalle_encuentro,
                                condicion=condicion)[0]
                            anotacion_puntaje.puntaje = runlines[i]
                            anotacion_puntaje.save()
                            i += 1
        else:
            for jugada in jugadas:
                anotacions = AnotacionesDetail.get_or_create_or_flush(
                    anotacion=anotacion,
                    encuentro_detail=jugada.detalle_encuentro,
                    condicion=condicion)[0]
                anotacions.puntaje = None
                anotacions.save()


class EncuentrosResultadosListForm(WidgetCustomizeForms, forms.Form):
    '''
    Formulario creado especificamente para filtrar encuentos,
    por deporte y por fecha
    '''

    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.only('pk', 'nombre').all().order_by('nombre'),
        required=True,
        empty_label='Seleccione un {0}'.format(TipoProducto._meta.verbose_name)
    )

    fecha = forms.DateField(label='Fecha (*)', required=True)


class FilterCadenaModeloJuegosResultados(WidgetCustomizeForms, forms.Form):
    '''
    Formulario creado especificamente para filtrar por la cadena de comercializacion
    deportes y fecha en resultados
    '''
    operadora = forms.ModelChoiceField(
        required=False,
        queryset=Operadoras.objects.only('pk', 'nombre').all(),
        empty_label='Seleccione una {0}'.format(Operadoras._meta.verbose_name.title())
    )
    bloque = forms.ModelChoiceField(
        required=False,
        queryset=Bloques.objects.only('pk', 'nombre').filter(
            Q(is_resultados=True) | Q(is_sistema_juego=True)
        ),
        empty_label='Seleccione una {0}'.format(Bloques._meta.verbose_name.title())
    )
    banca = forms.ModelChoiceField(
        required=False,
        queryset=Bancas.objects.only('pk', 'nombre').filter(
            Q(is_resultados=True) | Q(is_sistema_juego=True)
        ),
        empty_label='Seleccione una {0}'.format(Bancas._meta.verbose_name.title())
    )
    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(TipoProducto._meta.verbose_name)
    )
    fecha = forms.DateField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FilterCadenaModeloJuegosResultados, self).__init__(*args, **kwargs)

        self.fields['fecha'].initial = now().strftime(FORMAT_STR_DATE_FORM)

        self.view.set_execute_function_by_profile(
            **{
                'prefix': 'filter',
                'instance': self
            }
        )

    def filter_userprofile_master(self, **kwargs):
        '''
        Puesto que es el master accede a todos los usuarios

        Si es master tiene acceso a todo
        '''
        pass

    def filter_userprofile_operadora(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en una operadora
        '''
        del self.fields['operadora']

        self.fields['bloque'].queryset = self.fields['bloque'].queryset.filter(
            operadora_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['banca'].queryset = self.fields['banca'].queryset.filter(
            bloque__operadora_id=self.view.object_comercializadora.get_object().pk
        )

    def filter_userprofile_bloque(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en un bloque
        '''
        del self.fields['operadora']
        del self.fields['bloque']

        self.fields['banca'].queryset = self.fields['banca'].queryset.filter(
            bloque_id=self.view.object_comercializadora.get_object().pk
        )

    def filter_userprofile_banca(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en una banca
        '''
        del self.fields['operadora']
        del self.fields['bloque']
        del self.fields['banca']

    def filter_userprofile_distribuidor(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en un distribuidor
        '''
        del self.fields['operadora']
        del self.fields['bloque']
        del self.fields['banca']

    def filter_userprofile_agencia(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en una agencia
        '''
        del self.fields['operadora']
        del self.fields['bloque']
        del self.fields['banca']

    def clean(self):
        # valido que si no viene fecha, se renderize otra vez el form
        if not self.data.get('fecha'):
            self.is_bound = False
        return self.cleaned_data
