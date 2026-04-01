# -*- coding: utf-8 -*-

from datetime import timedelta

from admin_asterisco7.settings import DEBUG
from admin_comercializacion.models import Bancas, Bloques, Operadoras
from admin_juego.models import (
    Condiciones, TipoProducto, TipoProducto_Grupos, Sorteo, EventNotification, apuesta,
    JugadasInformativas, SistemaJuego,
)
from admin_lib.util_forms import FORMAT_STR_DATE_FORM, WidgetCustomizeForms
from admin_status.models import Status
from django import forms
from django.core.cache import cache
from django.db.models import Q
from django.utils.timezone import now


class EncuentrosLogrosCreateUpdateForm(WidgetCustomizeForms, forms.ModelForm):
    """
    Formulario dinamico para asignar logros,
    en base a las modalidades disponibles en cada
    encuentro
    """
    class Meta:
        model = Sorteo
        exclude = [
            'jornada',
            'grupo',
            'status',
            'horajuego',
            'horacierre',
            'pk_clone',
        ]

    def __init__(self, *args, **kwargs):
        """
        Se crea la data necesaria vacia inicialmente
        en caso de no existir, para generar los feields
        y poder cargar los datos
        """
        super(EncuentrosLogrosCreateUpdateForm, self).__init__(*args, **kwargs)
        self.tabindex = 1
        deporte = self.instance.jornada.temporadas.torneo.deporte
        filter_indice = deporte.get_filter_orden_equipos()

        self.add_runline_loose = deporte.runline_positivo
        self.runline_loose_default = False
        self.view.get_object_sistema_logros()
        add_resalt = ' input-logro-resalt'

        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=deporte
        ).order_by('grupo__orden'):
            grupo_id = deporte_grupo.grupo.id
            modalidad_grupo_list = deporte_grupo.grupo.modalidades_grupos_set.all()
            for modalidad_grupo in modalidad_grupo_list.order_by('modalidad__orden'):

                if modalidad_grupo.deporte_restriccion.filter(
                    pk=self.instance.jornada.temporadas.torneo.deporte.pk
                ).exists():
                    continue

                encuentro_modalidad = SorteoModalidades.get_carefully(
                    kwargs={
                        'encuentro': self.instance,
                        'deporte_grupo': deporte_grupo,
                        'modalidad_grupo': modalidad_grupo,
                    },
                    sistemajuego=self.view.object_sistema_juego,
                    sistemalogros=self.view.object_sistema_logros,
                )

                if encuentro_modalidad.modalidad_grupo.modalidad.etiqueta_ref:
                    try:
                        rango = RestriccionesSorteo.objects.get(
                            deporte=encuentro_modalidad.deporte_grupo.deporte,
                            grupo=encuentro_modalidad.deporte_grupo.grupo,
                            modalidad=encuentro_modalidad.modalidad_grupo.modalidad
                        )
                        rango_str = 'Rango valido [{0} | {1}]'.format(
                            rango.min_ref,
                            rango.max_ref
                        )
                    except RestriccionesSorteo.DoesNotExist:
                        rango_str = ''

                    ref_encuentromodalidad_name = 'ref_encuentromodalidad_{0}' \
                                                  ''.format(
                                                      encuentro_modalidad.pk
                                                  )

                    self.fields[ref_encuentromodalidad_name] = forms.CharField(
                        required=False,
                        max_length=10,
                        help_text='{0} : Etiqueta de referencia para la modalidad {1}'
                        ''.format(
                            deporte_grupo.grupo.nombre,
                            encuentro_modalidad.modalidad_grupo.modalidad.modalidad
                        )
                    )
                    add_class_resalt = ''
                    if encuentro_modalidad.sistema_id != self.view.object_sistema_juego.pk:
                        add_class_resalt = add_resalt

                    self.customize(
                        field=ref_encuentromodalidad_name,
                        validation='[+-]?[0-9]+[,]?[0-9]*',
                        valor=encuentro_modalidad.etiqueta_ref,
                        validate='{0}-{1}-{2}'.format(
                            deporte_grupo.deporte.id,
                            deporte_grupo.grupo.id,
                            encuentro_modalidad.modalidad_grupo.modalidad.id
                        ),
                        rango=rango_str,
                        add_class=add_class_resalt
                    )

                condiciones_list = encuentro_modalidad.modalidad_grupo.modalidad.condiciones_set
                for condicion in condiciones_list.all().order_by('orden'):

                    if condicion.equipo:

                        encuentro_detail_list = self.instance.encuentrosdetail_set.all()
                        for encuentro_detail in encuentro_detail_list.order_by(filter_indice):

                            if condicion.tipo == 4:
                                """
                                verificamos nuevamente que sea
                                una condicion de Informativa
                                """
                                jugada_info = JugadasInformativas.get_carefully(
                                    kwargs={
                                        'detalle_encuentro': encuentro_detail,
                                        'encuentros_modalidad': encuentro_modalidad,
                                        'condicion': condicion,
                                    },
                                    sistemajuego=self.view.object_sistema_juego,
                                    sistemalogros=self.view.object_sistema_logros,
                                )

                                para = encuentro_detail.equipos_temporadas.equipo.nombre
                                encuentro_ref_name_0 = 'encuentro_ref_{0}-0'.format(
                                    jugada_info.pk
                                )
                                self.fields[encuentro_ref_name_0] = forms.CharField(
                                    required=False,
                                    max_length=100,
                                    label='Nombre',
                                    help_text='{0}: modalidad {1} - {2} '
                                    ': Nombre para {3}'.format(
                                        deporte_grupo.grupo.nombre,
                                        condicion.modalidad.modalidad,
                                        condicion.nombre,
                                        para
                                    )
                                )

                                add_class_resalt = ''
                                if jugada_info.sistema_id != self.view.object_sistema_juego.pk:
                                    add_class_resalt = add_resalt

                                self.customize(
                                    field=encuentro_ref_name_0,
                                    valor=jugada_info.ref_principal,
                                    add_class=add_class_resalt
                                )
                                self.fields[encuentro_ref_name_0].widget.attrs['list'] = '' \
                                    'modalidad-{0}-infornacion_list'.format(
                                        modalidad_grupo.modalidad.pk
                                )

                                encuentro_ref_name_1 = 'encuentro_ref_{0}-1'.format(
                                    jugada_info.pk
                                )
                                self.fields[encuentro_ref_name_1] = forms.CharField(
                                    required=False,
                                    max_length=100,
                                    label='Ref',
                                    help_text='{0}: modalidad {1} - {2} '
                                    ' : Orientacion, Ganados/Perdidos'
                                    ' y Efectividad para {3}'.format(
                                        deporte_grupo.grupo.nombre,
                                        condicion.modalidad.modalidad,
                                        condicion.nombre,
                                        para
                                    )
                                )
                                self.customize(
                                    field=encuentro_ref_name_1,
                                    valor=jugada_info.ref_other_1,
                                    add_class=add_class_resalt,
                                )

                            else:

                                jugada = apuesta.get_carefully(
                                    kwargs={
                                        'detalle_encuentro': encuentro_detail,
                                        'encuentros_modalidad': encuentro_modalidad,
                                        'condicion': condicion,
                                    },
                                    sistemajuego=self.view.object_sistema_juego,
                                    sistemalogros=self.view.object_sistema_logros,
                                )

                                if jugada.indice != encuentro_detail.indice:
                                    jugada.indice = encuentro_detail.indice
                                    if jugada.status is None:
                                        """solo entra cuando se crea"""
                                        jugada.status = Status.get_status_by_codename(
                                            codename='status_eliminado'
                                        )
                                    jugada.save()

                                add_class = ''
                                add_class_resalt = ''
                                if jugada.sistema_id != self.view.object_sistema_juego.pk:
                                    add_class_resalt = add_resalt
                                    add_class += add_class_resalt

                                if condicion.etiqueta_ref:

                                    try:
                                        rango = RestriccionesSorteo.objects.get(
                                            deporte=deporte_grupo.deporte,
                                            grupo=deporte_grupo.grupo,
                                            condicion=condicion
                                        )
                                        rango_str = ' Rango valido [{0}|{1}]'.format(
                                            rango.min_ref,
                                            rango.max_ref
                                        )
                                    except RestriccionesSorteo.DoesNotExist:
                                        rango_str = ''

                                    ref_logro_name = 'ref_logro_{0}'.format(
                                        jugada.pk
                                    )

                                    if rango.min_ref == rango.max_ref:
                                        CHOICES = (('+' + rango.min_ref, '+' + rango.min_ref),
                                                   ('-' + rango.max_ref, '-' + rango.max_ref,))
                                        self.fields[ref_logro_name] = forms.ChoiceField(
                                            widget=forms.RadioSelect,
                                            choices=CHOICES,
                                            required=False,
                                            label='',
                                            help_text='{0}: ingrese la referencia'
                                            ' del logro de modalidad: '
                                            '{1} condicion {2} '
                                            'para {3}'.format(
                                                deporte_grupo.grupo.nombre,
                                                encuentro_modalidad.modalidad_grupo
                                                .modalidad.modalidad,
                                                condicion.nombre,
                                                encuentro_detail.equipos_temporadas.equipo.nombre
                                            )
                                        )

                                    else:
                                        self.fields[ref_logro_name] = forms.CharField(
                                            required=False,
                                            max_length=10,
                                            label='',
                                            help_text='{0}: ingrese la referencia'
                                            ' del logro de modalidad: '
                                            '{1} condicion {2} '
                                            'para {3}'.format(
                                                deporte_grupo.grupo.nombre,
                                                encuentro_modalidad.modalidad_grupo
                                                .modalidad.modalidad,
                                                condicion.nombre,
                                                encuentro_detail.equipos_temporadas.equipo.nombre
                                            )
                                        )

                                    if self.add_runline_loose:
                                        if (encuentro_modalidad.modalidad_grupo.grupo.codename in [
                                                'juego_completo', 'medio_juego'] and
                                                encuentro_modalidad.modalidad_grupo.modalidad.codename == 'runline'):
                                            add_class += ' runline_loose'

                                    """
                                    if (
                                        encuentro_modalidad.modalidad_grupo.modalidad.codename ==
                                        'super_runline'
                                            ):
                                        validateextra = None
                                    else:
                                        validateextra = '{0}'.format(
                                                    encuentro_detail.equipos_temporadas.equipo.id
                                                )
                                    """
                                    validateextra = '{0}'.format(
                                                    encuentro_detail.equipos_temporadas.equipo.id
                                    )
                                    self.customize(
                                        field=ref_logro_name,
                                        validation='[+-]?[0-9]+[,]?[0-9]*',
                                        valor=jugada.valor_etq_ref,
                                        validate='{0}-{1}-{2}'.format(
                                            deporte_grupo.deporte.id,
                                            deporte_grupo.grupo.id,
                                            encuentro_modalidad.modalidad_grupo.modalidad.id,
                                        ),
                                        validateextra=validateextra,
                                        rango=rango_str,
                                        add_class=add_class_resalt
                                    )

                                try:
                                    rango = RestriccionesSorteo.objects.get(
                                        deporte=deporte_grupo.deporte,
                                        grupo=deporte_grupo.grupo,
                                        min_ref='logro'
                                    )
                                    rango_str = 'Rango valido [({0},-100),(100,{1})]'.format(
                                        rango.max_logro_favorito,
                                        rango.max_logro_no_favorito
                                    )
                                except RestriccionesSorteo.DoesNotExist:
                                    rango_str = 'Rango valido [(-1000,-100),(100,1000)]'

                                logro_name = 'logro_{0}'.format(
                                    jugada.pk
                                )
                                self.fields[logro_name] = forms.CharField(
                                    required=True,
                                    label='',
                                    help_text='{0}: ingrese el logro de '
                                    '{1} condicion {2} para '
                                    '{3}'.format(
                                        deporte_grupo.grupo.nombre,
                                        encuentro_modalidad.modalidad_grupo.modalidad.modalidad,
                                        condicion.nombre,
                                        encuentro_detail.equipos_temporadas.equipo.nombre
                                    )
                                )
                                self.customize(
                                    field=logro_name,
                                    validation='[+-]?[0-9]+',
                                    valor=jugada.valor_americano,
                                    validate=grupo_id,
                                    validateextra='{0}-{1}'.format(
                                        grupo_id,
                                        encuentro_modalidad.modalidad_grupo.modalidad.id
                                    ),
                                    equipo='{0}'.format(
                                        encuentro_detail.equipos_temporadas.equipo.id
                                    ),
                                    rango=rango_str,
                                    add_class=add_class,
                                )

                                # Verificamos si ya hay logros con referencias positivas
                                # para activar la bandera
                                if self.add_runline_loose:
                                    if jugada.valor_etq_ref:
                                        ref = float(jugada.valor_etq_ref.replace(',', '.'))
                                        if ref > 0 and jugada.valor_americano > 0:
                                            self.runline_loose_default = True
                    else:
                        for indice in range(1, condicion.tipo + 1):
                            jugada = apuesta.get_carefully(
                                kwargs={
                                    'encuentros_modalidad': encuentro_modalidad,
                                    'condicion': condicion,
                                    'indice': indice,
                                },
                                sistemajuego=self.view.object_sistema_juego,
                                sistemalogros=self.view.object_sistema_logros,
                            )

                            if jugada.status is None:
                                """solo entra cuando se crea"""
                                jugada.status = Status.get_status_by_codename(
                                    codename='status_eliminado'
                                )
                                jugada.save()

                            para = jugada.get_pertenece()
                            add_class_resalt = ''
                            if jugada.sistema_id != self.view.object_sistema_juego.pk:
                                add_class_resalt = add_resalt

                            if condicion.etiqueta_ref:

                                try:
                                    rango = RestriccionesSorteo.objects.get(
                                        deporte=deporte_grupo.deporte,
                                        grupo=deporte_grupo.grupo,
                                        condicion=condicion
                                    )
                                    rango_str = 'Rango valido [{0}|{1}]'.format(
                                        rango.min_ref,
                                        rango.max_ref
                                    )
                                except RestriccionesSorteo.DoesNotExist:
                                    rango_str = ''

                                ref_logro_name_other = 'ref_logro_{0}'.format(
                                    jugada.pk
                                )
                                self.fields[ref_logro_name_other] = forms.CharField(
                                    required=False,
                                    max_length=10,
                                    label='',
                                    help_text='{0}: ingrese la referencia'
                                    ' del logro de modalidad '
                                    '{1} condicion {2} {3}'.format(
                                        deporte_grupo.grupo.nombre,
                                        encuentro_modalidad.modalidad_grupo.modalidad.modalidad,
                                        condicion.nombre,
                                        para
                                    )
                                )

                                self.customize(
                                    field=ref_logro_name_other,
                                    validation='[+-]?[0-9]+[,]?[0-9]*',
                                    valor=jugada.valor_etq_ref,
                                    rango=rango_str,
                                    add_class=add_class_resalt,
                                )

                            try:
                                rango = RestriccionesSorteo.objects.get(
                                    deporte=deporte_grupo.deporte,
                                    grupo=deporte_grupo.grupo,
                                    min_ref='logro'
                                )
                                rango_str = 'Rango valido [({0},-100),(100,{1})]'.format(
                                    rango.max_logro_favorito,
                                    rango.max_logro_no_favorito
                                )
                            except RestriccionesSorteo.DoesNotExist:
                                rango_str = 'Rango valido [(-1000,-100),(100,1000)]'

                            logro_name_other = 'logro_{0}'.format(
                                jugada.pk
                            )
                            self.fields[logro_name_other] = forms.CharField(
                                required=True,
                                label='',
                                help_text='{0}: ingrese el logro '
                                'de modalidad {1} condicion {2} {3}'.format(
                                    deporte_grupo.grupo.nombre,
                                    encuentro_modalidad.modalidad_grupo.modalidad.modalidad,
                                    condicion.nombre,
                                    para
                                )
                            )
                            self.customize(
                                field=logro_name_other,
                                validation='[+-]?[0-9]+',
                                valor=jugada.valor_americano,
                                validate=grupo_id,
                                validateextra='{0}-{1}'.format(
                                    grupo_id,
                                    encuentro_modalidad.modalidad_grupo.modalidad.id
                                ),
                                equipo='',
                                rango=rango_str,
                                add_class=add_class_resalt
                            )

        self.valid_runline_loose = False
        if self.add_runline_loose:
            self.valid_runline_loose = True
            self.fields['runline_loose'] = forms.BooleanField(
                label='Runline [+] libre',
                help_text='Solo seleccione este campo si desea asignar runline de forma libre,'
                'sin restricciones de signos',
                required=False,
                initial=self.runline_loose_default,
            )

    def customize(
        self,
        field,
        validation=None,
        valor='',
        validate='',
        validateextra='',
        rango='',
        equipo='',
        add_class=''
    ):

        if validation is not None:
            self.fields[field].widget.attrs['pattern'] = validation
        if self.fields[field].required:
            self.fields[field].widget.attrs['required'] = ''

        self.fields[field].widget.attrs['title'] = self.fields[field].help_text + rango
        self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

        if valor is not None:
            if isinstance(valor, int):
                self.fields[field].initial = valor if valor <= 0 else str('+') + str(valor)
            else:
                self.fields[field].initial = valor
        else:
            if field.find('encuentro_ref_') >= 0:
                self.fields[field].initial = valor
            else:
                self.fields[field].initial = 0

        self.fields[field].widget.attrs['class'] = ''

        if field.find('encuentro_ref_') >= 0:
            self.fields[field].widget.attrs['class'] = 'input-referencia-encuentro'
        elif field.find('ref_encuentromodalidad') >= 0:
            self.fields[field].widget.attrs['class'] = 'input-etiqueta modalidad-validate-' \
                                                       '{0}'.format(
                validate
            )
            self.fields[field].widget.attrs['onkeyup'] = 'validar_modalidad(' + field + ')'
            self.fields[field].widget.attrs['onclick'] = 'remove_error(' + field + ')'
        elif field.find('ref_logro') >= 0:
            if validateextra is None:
                self.fields[field].widget.attrs['class'] = 'input-etiqueta condicion-' \
                                                           'validate-{0} super'.format(
                    validate
                )
                self.fields[field].widget.attrs['onkeyup'] = 'validar_condicion(' + field + ')'
                self.fields[field].widget.attrs['onclick'] = 'remove_error(' + field + ')'
            else:
                self.fields[field].widget.attrs['class'] = 'input-etiqueta condicion-' \
                                                           'validate-{0} equipo-{1}'.format(
                    validate,
                    validateextra
                )
                self.fields[field].widget.attrs['onkeyup'] = 'validar_condicion(' + field + ')'
                self.fields[field].widget.attrs['onclick'] = 'remove_error(' + field + ')'
        else:
            self.fields[field].widget.attrs['class'] = 'input-logro grupo-' \
                                                       'validate-{0} ' \
                                                       'grupo-equipo-{1}'.format(
                validateextra,
                equipo
            )

            self.fields[field].widget.attrs['onkeyup'] = 'validar_grupo(' \
                                                         '{0},{1})'.format(
                field,
                validate
            )

        if add_class:
            self.fields[field].widget.attrs['class'] += ' {0}'.format(add_class)

        self.fields[field].widget.attrs['tabindex'] = self.tabindex
        self.tabindex += 1

    def save(self, commit=True, *args, **kwargs):
        super(EncuentrosLogrosCreateUpdateForm, self).save(commit=False, *args, **kwargs)

        if self.view.object_sistema_logros.notificacion_automatica:
            fecha_ini_notification = now()
            cache.set(
                '{0}_{1}'.format('block_event', self.view.object_sistema_logros.pk),
                True,
            )

        generate_cache_grupos = []
        generate_notifications = False
        if self.instance.horajuego.date() == now().date():
            generate_notifications = True

        if generate_notifications is False and DEBUG is True:
            if self.instance.horajuego.date() <= (now().date() + timedelta(days=30)):
                generate_notifications = True

        deporte = self.instance.jornada.temporadas.torneo.deporte
        filter_indice = deporte.get_filter_orden_equipos()
        key_sistema_juego = '{0}_{1}_{2}'.format(
            self.view.object_sistema_juego.pk,
            self.view.object_sistema_logros.pk,
            self.instance.horajuego.strftime(FORMAT_STR_DATE_FORM)
        )

        exists_change = False

        for deporte_grupo in TipoProducto_Grupos.objects.filter(
            deporte=deporte
        ).order_by('grupo__orden'):

            cambio_exists_por_grupo = False
            modalidad_grupo_list = deporte_grupo.grupo.modalidades_grupos_set.all()

            for modalidad_grupo in modalidad_grupo_list.order_by('modalidad__orden'):

                if modalidad_grupo.deporte_restriccion.filter(
                    pk=self.instance.jornada.temporadas.torneo.deporte.pk
                ).exists():
                    continue

                encuentro_modalidad = SorteoModalidades.get_carefully(
                    kwargs={
                        'encuentro': self.instance,
                        'deporte_grupo': deporte_grupo,
                        'modalidad_grupo': modalidad_grupo,
                    },
                    sistemajuego=self.view.object_sistema_juego,
                    sistemalogros=self.view.object_sistema_logros,
                )

                force_generate = False

                if encuentro_modalidad.modalidad_grupo.modalidad.etiqueta_ref:
                    ref_encuentromodalidad_name = 'ref_encuentromodalidad_{0}'.format(
                        encuentro_modalidad.pk
                    )

                    if (
                            encuentro_modalidad.etiqueta_ref !=
                            self.cleaned_data[ref_encuentromodalidad_name]
                    ):

                        if (
                                encuentro_modalidad.etiqueta_ref is None and
                                str(self.cleaned_data[ref_encuentromodalidad_name]) == '0'
                        ):
                            """no se agrega"""
                            pass

                        else:

                            if encuentro_modalidad.sistema_id != self.view.object_sistema_logros.pk:
                                encuentro_modalidad = encuentro_modalidad.create_heir(
                                    sistemalogros=self.view.object_sistema_logros
                                )
                                force_generate = True

                            encuentro_modalidad.etiqueta_ref = self.cleaned_data[
                                ref_encuentromodalidad_name
                            ]
                            encuentro_modalidad.save(update_fields=['etiqueta_ref', 'updated_at'])
                            exists_change = True
                            if generate_notifications:
                                encuentro_modalidad.broadcast(
                                    sistema=encuentro_modalidad.sistema
                                )
                            cambio_exists_por_grupo = True

                condiciones_list = encuentro_modalidad.modalidad_grupo.modalidad.condiciones_set
                for condicion in condiciones_list.all().order_by('orden'):
                    jugadas_verificacion_favoritos = []

                    if condicion.equipo:
                        encuentro_detail_list = self.instance.encuentrosdetail_set.all()
                        for encuentro_detail in encuentro_detail_list.order_by(filter_indice):

                            if condicion.tipo == 4:
                                """verificamos si es condicion informativa"""
                                jugada_info = JugadasInformativas.get_carefully(
                                    kwargs={
                                        'detalle_encuentro': encuentro_detail,
                                        'encuentros_modalidad': encuentro_modalidad,
                                        'condicion': condicion,
                                    },
                                    sistemajuego=self.view.object_sistema_juego,
                                    sistemalogros=self.view.object_sistema_logros,
                                )

                                encuentro_ref_name_0 = 'encuentro_ref_{0}-0'.format(
                                    jugada_info.pk
                                )
                                encuentro_ref_name_1 = 'encuentro_ref_{0}-1'.format(
                                    jugada_info.pk
                                )
                                if encuentro_ref_name_0 not in self.cleaned_data:
                                    encuentro_ref_name_0 = 'encuentro_ref_{0}-0'.format(
                                        jugada_info.origen_id
                                    )
                                    encuentro_ref_name_1 = 'encuentro_ref_{0}-1'.format(
                                        jugada_info.origen_id
                                    )

                                cp_encuentro_ref_name_0 = self.cleaned_data[encuentro_ref_name_0]
                                cp_encuentro_ref_name_1 = self.cleaned_data[encuentro_ref_name_1]

                                if (jugada_info.ref_principal != cp_encuentro_ref_name_0 or
                                        jugada_info.ref_other_1 != cp_encuentro_ref_name_1 or force_generate):

                                    if jugada_info.sistema_id != self.view.object_sistema_logros.pk:
                                        jugada_info = jugada_info.create_heir(
                                            encuentro_modalidad=jugada_info.encuentros_modalidad,
                                            sistemalogros=self.view.object_sistema_logros
                                        )

                                    jugada_info.ref_principal = self \
                                        .cleaned_data[encuentro_ref_name_0]

                                    jugada_info.ref_other_1 = self \
                                        .cleaned_data[encuentro_ref_name_1]

                                    jugada_info.save(update_fields=['ref_principal', 'ref_other_1', 'updated_at'])
                                    exists_change = True
                                    if generate_notifications:
                                        jugada_info.broadcast(
                                            sistema=jugada_info.sistema
                                        )

                            else:
                                jugada = apuesta.get_carefully(
                                    kwargs={
                                        'detalle_encuentro': encuentro_detail,
                                        'encuentros_modalidad': encuentro_modalidad,
                                        'condicion': condicion,
                                    },
                                    sistemajuego=self.view.object_sistema_juego,
                                    sistemalogros=self.view.object_sistema_logros,
                                )

                                logro_name = 'logro_{0}'.format(jugada.pk)
                                ref_logro_name = 'ref_logro_{0}'.format(jugada.pk)
                                if logro_name not in self.cleaned_data:
                                    logro_name = 'logro_{0}'.format(jugada.origen_id)
                                    ref_logro_name = 'ref_logro_{0}'.format(jugada.origen_id)

                                if (jugada.valor_americano != int(self.cleaned_data[logro_name]) or
                                        (
                                        condicion.etiqueta_ref and
                                        jugada.valor_etq_ref != self.cleaned_data[ref_logro_name]
                                ) or force_generate):

                                    if (jugada.valor_americano is None and
                                            int(self.cleaned_data[logro_name]) == 0):
                                        continue

                                    if jugada.sistema_id != self.view.object_sistema_logros.pk:
                                        jugada = jugada.create_heir(
                                            encuentro_modalidad=jugada.encuentros_modalidad,
                                            sistemalogros=self.view.object_sistema_logros
                                        )

                                    jugada.valor_americano = int(self.cleaned_data[logro_name])
                                    jugada.valor_europeo = self.set_convert_americano_europeo(
                                        jugada.valor_americano
                                    )
                                    update_fields = ['valor_americano', 'valor_europeo', 'updated_at']
                                    if jugada.valor_americano != 0:
                                        if jugada.status.codename == 'status_eliminado':
                                            jugada.status = Status.get_status_by_codename(
                                                codename='status_pendiente'
                                            )
                                            update_fields.append('status')
                                    else:
                                        jugada.status = Status.get_status_by_codename(
                                            codename='status_eliminado'
                                        )
                                        update_fields.append('status')

                                    if condicion.etiqueta_ref:
                                        jugada.valor_etq_ref = self.cleaned_data[ref_logro_name]
                                        update_fields.append('etiqueta_ref')

                                    jugada.save(update_fields=update_fields)
                                    jugadas_verificacion_favoritos.append(jugada)

                                # pregunta si el indice cambio y lo actualiza
                                if jugada.indice != encuentro_detail.indice:
                                    jugada.indice = encuentro_detail.indice
                                    jugada.save(update_fields=['indice', 'updated_at'])

                    else:
                        for indice in range(1, condicion.tipo + 1):
                            jugada = apuesta.get_carefully(
                                kwargs={
                                    'encuentros_modalidad': encuentro_modalidad,
                                    'condicion': condicion,
                                    'indice': indice,
                                },
                                sistemajuego=self.view.object_sistema_juego,
                                sistemalogros=self.view.object_sistema_logros,
                            )

                            logro_name = 'logro_{0}'.format(jugada.pk)
                            ref_logro_name = 'ref_logro_{0}'.format(jugada.pk)
                            if logro_name not in self.cleaned_data:
                                logro_name = 'logro_{0}'.format(jugada.origen_id)
                                ref_logro_name = 'ref_logro_{0}'.format(jugada.origen_id)

                            if (jugada.valor_americano != int(self.cleaned_data[logro_name]) or
                                    (
                                        condicion.etiqueta_ref and
                                        jugada.valor_etq_ref !=
                                        self.cleaned_data[ref_logro_name]
                            ) or force_generate):

                                if (
                                        (
                                            jugada.valor_americano is None and
                                            int(self.cleaned_data[logro_name]) == 0
                                        )):
                                    continue

                                if jugada.sistema_id != self.view.object_sistema_logros.pk:
                                    jugada = jugada.create_heir(
                                        encuentro_modalidad=jugada.encuentros_modalidad,
                                        sistemalogros=self.view.object_sistema_logros
                                    )

                                jugada.valor_americano = int(self.cleaned_data[logro_name])
                                jugada.valor_europeo = self.set_convert_americano_europeo(
                                    jugada.valor_americano
                                )

                                update_fields = ['valor_americano', 'valor_europeo', 'updated_at']
                                if jugada.valor_americano != 0:
                                    if jugada.status.codename == 'status_eliminado':
                                        jugada.status = Status.get_status_by_codename(
                                            codename='status_pendiente'
                                        )
                                        update_fields.append('status')
                                else:
                                    jugada.status = Status.get_status_by_codename(
                                        codename='status_eliminado'
                                    )
                                    update_fields.append('status')

                                if condicion.etiqueta_ref:
                                    jugada.valor_etq_ref = self.cleaned_data[ref_logro_name]
                                    update_fields.append('etiqueta_ref')

                                jugada.save(update_fields=update_fields)
                                jugadas_verificacion_favoritos.append(jugada)

                    if jugadas_verificacion_favoritos:

                        cambio_exists_por_grupo = True
                        if condicion.modalidad.codename == 'empate':
                            for jugada in jugadas_verificacion_favoritos:
                                jugada.favorito = None
                                jugada.save(update_fields=['favorito', ])
                                exists_change = True
                                if generate_notifications:
                                    jugada.broadcast(
                                        sistema=jugada.sistema
                                    )

                        elif condicion.etiqueta_ref:
                            for jugada in jugadas_verificacion_favoritos:
                                if float(jugada.valor_etq_ref.replace(',', '.')) < 0:
                                    jugada.favorito = True
                                else:
                                    jugada.favorito = False
                                jugada.save(update_fields=['favorito', ])
                                exists_change = True
                                if generate_notifications:
                                    jugada.broadcast(
                                        sistema=jugada.sistema
                                    )
                        else:
                            for jugada in jugadas_verificacion_favoritos:
                                if jugada.valor_americano < 0:
                                    jugada.favorito = True
                                else:
                                    jugada.favorito = False
                                jugada.save(update_fields=['favorito', ])
                                exists_change = True
                                if generate_notifications:
                                    jugada.broadcast(
                                        sistema=jugada.sistema
                                    )

            if cambio_exists_por_grupo:
                generate_cache_grupos.append(deporte_grupo)

        if exists_change:
            """
            Reinicia la cache para la lista de logros,
            esto de debe mejorar y utilizar la que ya esta procesada
            """

            for grupo in generate_cache_grupos:
                grupo.set_cache_by_encuentro(self.instance)

            # Lanza tambien las actualizaciones de los jugadores
            self.instance.set_cache_jugadas()

            cache.delete(
                'list_logros_deporte_{0}_{1}'.format(
                    self.instance.jornada.temporadas.torneo.deporte_id,
                    key_sistema_juego
                )
            )
            cache.delete(
                'list_logros_temporada_{0}_{1}'.format(
                    self.instance.jornada.temporadas_id,
                    key_sistema_juego
                )
            )
            cache.delete('list_logros_encuentro_{0}_{1}'.format(
                self.instance.pk,
                key_sistema_juego
            )
            )

            # Busca todas las cadenas inferiores y elimina la cache que ellas heredan
            cadena = self.view.object_comercializadora.get_object()
            bloques = []
            bancas = []
            if cadena.prefix_filter == 'operadora':
                bloques = Bloques.objects.filter(
                    operadora_id=cadena.pk,
                    is_logros=True
                )
                bancas = Bancas.objects.filter(
                    bloque__operadora_id=cadena.pk,
                    is_logros=True
                )
            else:
                if cadena.prefix_filter == 'bloque':
                    bancas = Bancas.objects.filter(
                        bloque_id=cadena.pk,
                        is_logros=True
                    )
            for cadena_exter in [bancas, bloques]:
                for cadena_inter in cadena_exter:
                    comercializadora = cadena_inter.get_comercializadora()
                    object_sistema_logros = SistemaJuego.objects \
                        .get_sistema_logros_by_comercializadora(
                            comercializadora
                        )
                    object_sistema_juego = SistemaJuego.objects \
                        .get_sistema_juego_by_comercializadora(
                            comercializadora
                        )
                    key_sistema_juego = '{0}_{1}'.format(
                        object_sistema_juego.pk,
                        object_sistema_logros.pk,
                        self.instance.horajuego.strftime(FORMAT_STR_DATE_FORM)
                    )
                    cache.delete(
                        'list_logros_deporte_{0}_{1}'.format(
                            self.instance.jornada.temporadas.torneo.deporte_id,
                            key_sistema_juego
                        )
                    )
                    cache.delete(
                        'list_logros_temporada_{0}_{1}'.format(
                            self.instance.jornada.temporadas_id,
                            key_sistema_juego
                        )
                    )
                    cache.delete('list_logros_encuentro_{0}_{1}'.format(
                        self.instance.pk,
                        key_sistema_juego
                    )
                    )

        if self.view.object_sistema_logros.notificacion_automatica:
            EventNotification.objects.filter(
                sistema=self.view.object_sistema_logros.pk,
                in_production=False,
                date_production__range=[fecha_ini_notification, now()]
            ).update(
                in_production=True
            )
            cache.delete('{0}_{1}'.format('block_event', self.view.object_sistema_logros.pk))

        if exists_change:
            self.instance.updated_at_logros = now()
            self.instance.save(update_fields=['updated_at_logros'])

    def set_convert_americano_europeo(self, logro):
        if logro < 0:
            return round(float(float(-(100 - float(logro))) / float(logro)), 2)
        elif logro > 0:
            return round(float(float((100 + float(logro))) / 100), 2)
        else:
            return logro

    def clean(self):
        cleaned_data = super(EncuentrosLogrosCreateUpdateForm, self).clean()

        logros = []
        referencias_modalidades = []
        referencias_condiciones = []
        for c_d in cleaned_data:
            if c_d.find('logro') == 0:
                var = c_d.split('_')
                logros.append(var[1])
            elif c_d.find('ref_encuentromodalidad') == 0:
                var = c_d.split('_')
                referencias_modalidades.append(var[2])
            elif c_d.find('ref_logro') == 0:
                var = c_d.split('_')
                referencias_condiciones.append(var[2])

        # Verifica rangos en los logros
        error = 0
        for l in logros:
            jugada = apuesta.objects.get(pk=l)
            try:
                rango = RestriccionesSorteo.objects.get(
                    deporte=jugada.encuentros_modalidad.deporte_grupo.deporte,
                    grupo=jugada.encuentros_modalidad.deporte_grupo.grupo,
                    min_ref='logro',
                    max_logro_no_favorito__isnull=False,
                    max_logro_favorito__isnull=False,
                )
            except RestriccionesSorteo.DoesNotExist:
                continue

            campo = int(cleaned_data['logro_' + str(l)])
            if campo > 0:
                if campo > int(rango.max_logro_no_favorito) or campo < 100:
                    self.fields['logro_' + str(l)].widget.attrs['class'] = '' \
                        'input-logro-error grupo-validate-{0}'.format(
                        rango.id
                    )
                    error = 1
            elif campo < 0:
                if campo < int(rango.max_logro_favorito) or campo > (-100):
                    self.fields['logro_' + str(l)].widget.attrs['class'] = ''\
                        'input-logro-error grupo-validate-{0}'.format(
                        rango.id
                    )
                    error = 1
        if error != 1:
            # Verifica rangos en los logros de encuentro modalidad
            for r in referencias_modalidades:
                encuentro_modalidad = SorteoModalidades.objects.get(pk=r)

                try:
                    rango = RestriccionesSorteo.objects.get(
                        deporte=encuentro_modalidad.deporte_grupo.deporte,
                        grupo=encuentro_modalidad.deporte_grupo.grupo,
                        modalidad=encuentro_modalidad.modalidad_grupo.modalidad,
                        min_ref__isnull=False,
                        max_ref__isnull=False,
                    )
                except RestriccionesSorteo.DoesNotExist:
                    continue

                campo = str(cleaned_data['ref_encuentromodalidad_' + str(r)])

                if campo:
                    campo = float(campo.replace(',', '.'))
                    menor = float(rango.min_ref.replace(',', '.'))
                    mayor = float(rango.max_ref.replace(',', '.'))
                    if (campo < menor or campo > mayor) and campo != 0:
                        self.fields['ref_encuentromodalidad_' + str(r)].widget.attrs['class'] = '' \
                            'input-etiqueta-error modalidad-validate-{0}-{1}-{2}'.format(
                            encuentro_modalidad.deporte_grupo.deporte.id,
                            encuentro_modalidad.deporte_grupo.grupo.id,
                            encuentro_modalidad.modalidad_grupo.modalidad.id
                        )
                        error = 1
        if error != 1:
            # Verifica rangos en las referencias condiciones
            for c in referencias_condiciones:
                jugada = apuesta.objects.get(pk=c)
                condicion = Condiciones.objects.get(
                    modalidad=jugada.encuentros_modalidad.modalidad_grupo.modalidad
                )
                try:
                    rango = RestriccionesSorteo.objects.get(
                        deporte=jugada.encuentros_modalidad.deporte_grupo.deporte,
                        grupo=jugada.encuentros_modalidad.deporte_grupo.grupo,
                        condicion=condicion,
                        min_ref__isnull=False,
                        max_ref__isnull=False,
                    )
                except RestriccionesSorteo.DoesNotExist:
                    continue

                campo = str(cleaned_data['ref_logro_' + str(c)])

                if campo:
                    campo = float(campo.replace(',', '.'))
                    menor = float(rango.min_ref.replace(',', '.'))
                    mayor = float(rango.max_ref.replace(',', '.'))
                    if campo > 0:
                        if (campo < menor or campo > mayor):
                            self.fields['ref_logro_' + str(c)].widget.attrs['class'] = '' \
                                'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                                    jugada.encuentros_modalidad.deporte_grupo.deporte.id,
                                    jugada.encuentros_modalidad.deporte_grupo.grupo.id,
                                    jugada.encuentros_modalidad.modalidad_grupo.modalidad.id
                            )
                            error = 1
                    elif campo < 0:
                        menor = (menor * -1)
                        mayor = (mayor * -1)
                        if (campo > menor or campo < mayor):
                            self.fields['ref_logro_' + str(c)].widget.attrs['class'] = '' \
                                'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                                    jugada.encuentros_modalidad.deporte_grupo.deporte.id,
                                    jugada.encuentros_modalidad.deporte_grupo.grupo.id,
                                    jugada.encuentros_modalidad.modalidad_grupo.modalidad.id
                            )
                            error = 1
        if error != 1:
            # Verifica que las condiciones sean correctas
            encuentros_modalidad = []
            for c in referencias_condiciones:
                jugada = apuesta.objects.get(pk=c)
                encuentros_modalidad.append(jugada.encuentros_modalidad)
                logro = str(cleaned_data['logro_' + str(c)])
                if logro != '0':
                    ref = str(cleaned_data['ref_logro_' + str(c)])
                    ref = float(ref.replace(',', '.'))
                    if ref == 0:
                        self.fields['ref_logro_' + str(c)].widget.attrs['class'] = '' \
                            'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                            jugada.encuentros_modalidad.deporte_grupo.deporte.id,
                            jugada.encuentros_modalidad.deporte_grupo.grupo.id,
                            jugada.encuentros_modalidad.modalidad_grupo.modalidad.id
                        )
                        error = 1
                    elif ref > 0 and int(logro) > 0:
                        logro_class = self.fields['logro_' + str(c)].widget.attrs['class']

                        # Los logros con runline libre sin excluidos
                        # en caso de que este activada la bandera
                        if logro_class.find('runline_loose') >= 0:
                            if cleaned_data.get('runline_loose'):
                                continue

                        self.fields['ref_logro_' + str(c)].widget.attrs['class'] = '' \
                            'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                            jugada.encuentros_modalidad.deporte_grupo.deporte.id,
                            jugada.encuentros_modalidad.deporte_grupo.grupo.id,
                            jugada.encuentros_modalidad.modalidad_grupo.modalidad.id
                        )
                        error = 1

        if error != 1:
            import math
            # Verifica restricciones en las referencias condiciones (Diferentes signos)
            encuentros_modalidad = list(set(encuentros_modalidad))
            for em in encuentros_modalidad:
                jugadas = apuesta.objects.filter(
                    encuentros_modalidad=em,
                    sistema=self.view.object_sistema_logros
                )
                if jugadas.count() != 2:
                    jugadas = apuesta.objects.filter(
                        encuentros_modalidad=em,
                        sistema=self.view.object_sistema_juego
                    )
                if jugadas.count() != 2:
                    continue

                name_ref0 = 'ref_logro_' + str(jugadas[0].pk)
                name_ref1 = 'ref_logro_' + str(jugadas[1].pk)

                if name_ref0 not in cleaned_data or name_ref1 not in cleaned_data:
                    continue

                ref0 = str(cleaned_data[name_ref0])
                ref1 = str(cleaned_data[name_ref1])
                if (ref0 != '0' and ref1 != '0') and (ref0 != '' and ref1 != ''):
                    ref0 = math.copysign(1, float(ref0.replace(',', '.')))
                    ref1 = math.copysign(1, float(ref1.replace(',', '.')))
                    if ref0 == ref1:
                        self.fields['ref_logro_' + str(jugadas[0].pk)].widget.attrs['class'] = '' \
                            'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                            jugadas[0].encuentros_modalidad.deporte_grupo.deporte.id,
                            jugadas[0].encuentros_modalidad.deporte_grupo.grupo.id,
                            jugadas[0].encuentros_modalidad.modalidad_grupo.modalidad.id
                        )
                        error = 1

        if error != 1:
            import math
            # Verifica restricciones en las referencias condiciones (Diferentes signos)
            encuentros_modalidad = list(set(encuentros_modalidad))
            for em in encuentros_modalidad:
                jugadas = apuesta.objects.filter(
                    encuentros_modalidad=em,
                    sistema=self.view.object_sistema_logros
                )
                if jugadas.count() != 2:
                    jugadas = apuesta.objects.filter(
                        encuentros_modalidad=em,
                        sistema=self.view.object_sistema_juego
                    )
                if jugadas.count() != 2:
                    continue

                name_ref0 = 'ref_logro_' + str(jugadas[0].pk)
                name_ref1 = 'ref_logro_' + str(jugadas[1].pk)

                if name_ref0 not in cleaned_data or name_ref1 not in cleaned_data:
                    continue

                ref0 = str(cleaned_data['ref_logro_' + str(jugadas[0].pk)])
                ref1 = str(cleaned_data['ref_logro_' + str(jugadas[1].pk)])
                if (ref0 != '0' and ref1 != '0') and (ref0 != '' and ref1 != ''):
                    ref0 = math.copysign(1, float(ref0.replace(',', '.')))
                    ref1 = math.copysign(1, float(ref1.replace(',', '.')))
                    if ref0 == ref1:
                        self.fields['ref_logro_' + str(jugadas[0].pk)].widget.attrs['class'] = '' \
                            'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                            jugadas[0].encuentros_modalidad.deporte_grupo.deporte.id,
                            jugadas[0].encuentros_modalidad.deporte_grupo.grupo.id,
                            jugadas[0].encuentros_modalidad.modalidad_grupo.modalidad.id
                        )
                        error = 1

        if error != 1:
            import math
            # Verifica condiciones por equipo
            for detail in self.instance.encuentrosdetail_set.all():
                jugadas = apuesta.objects.filter(
                    detalle_encuentro=detail,
                    encuentros_modalidad__modalidad_grupo__modalidad__codename__in=['runline', 'super_runline'],
                    sistema=self.view.object_sistema_logros,
                )
                if not jugadas.exists():
                    jugadas = apuesta.objects.filter(
                        detalle_encuentro=detail,
                        encuentros_modalidad__modalidad_grupo__modalidad__codename__in=['runline', 'super_runline'],
                        sistema=self.view.object_sistema_juego,
                    )
                if jugadas.exists():
                    name_ref0 = 'ref_logro_' + str(jugadas[0].pk)
                    if name_ref0 not in cleaned_data:
                        continue

                    ref0 = str(cleaned_data[name_ref0])
                    if (ref0 != '0' and ref0 != ''):
                        ref0 = math.copysign(1, float(ref0.replace(',', '.')))
                        for jugada in jugadas[1:]:

                            name_ref1 = 'ref_logro_' + str(jugada.pk)
                            if name_ref1 not in cleaned_data:
                                continue

                            ref1 = str(cleaned_data['ref_logro_' + str(jugada.pk)])
                            if (ref1 != '0' and ref1 != ''):
                                ref1 = math.copysign(1, float(ref1.replace(',', '.')))
                                if ref0 != ref1:
                                    self.fields['ref_logro_' + str(jugada.pk)].widget.attrs['class'] = '' \
                                        'input-etiqueta-error condicion-validate-{0}-{1}-{2}'.format(
                                        jugada.encuentros_modalidad.deporte_grupo.deporte.id,
                                        jugada.encuentros_modalidad.deporte_grupo.grupo.id,
                                        jugada.encuentros_modalidad.modalidad_grupo.modalidad.id
                                    )
                                    error = 1

        if error == 1:
            raise forms.ValidationError('Error')
        return cleaned_data


FORMATO_CHOICES = (
    ('AM', 'Americano'),
    ('EU', 'Europeo'),
)


class CalculadoraForm(WidgetCustomizeForms, forms.Form):
    """
    formato = forms.ChoiceField(
        label='Formato',
        required=True,
        choices = FORMATO_CHOICES,
    )
    """
    apuesta = forms.IntegerField(
        label='Apuesta',
    )

    ganancia = forms.IntegerField(
        label='Ganancia',
    )

    total = forms.IntegerField(
        label='Total',
    )

    def __init__(self, *args, **kwargs):
        super(CalculadoraForm, self).__init__(*args, **kwargs)
        self.fields['ganancia'].widget.attrs['disabled'] = 'disabled'
        self.fields['total'].widget.attrs['disabled'] = 'disabled'
        for x in range(10):
            self.fields['logro_' + str(x + 1)] = forms.IntegerField(label='Logro ' + str(x + 1))
            self.fields['logro_' + str(x + 1)].widget.attrs['class'] = 'calculo'


class FilterCadenaModeloJuegosLogros(WidgetCustomizeForms, forms.Form):
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
            Q(is_logros=True) | Q(is_sistema_juego=True)
        ),
        empty_label='Seleccione una {0}'.format(Bloques._meta.verbose_name.title())
    )
    banca = forms.ModelChoiceField(
        required=False,
        queryset=Bancas.objects.only('pk', 'nombre').filter(
            Q(is_logros=True) | Q(is_sistema_juego=True)
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
        super(FilterCadenaModeloJuegosLogros, self).__init__(*args, **kwargs)

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
