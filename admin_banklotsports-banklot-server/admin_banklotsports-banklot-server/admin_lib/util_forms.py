# -*- coding: utf-8 -*-

from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Operadoras
from admin_juego.models import Deportes, Equipos, Jugador, JugadorTipo, Temporadas, Torneos
from django import forms
from django.utils.timezone import now

FORMAT_STR_DATE_FORM = '%Y-%m-%d'


class WidgetCustomizeForms(object):
    '''
    Clase base para la personalizacion de los formularios
    '''

    def __init__(self, *args, **kwargs):
        '''
        En caso de venir en el kwargs la variable view se agrega como
        atributo y se elimina del kwargs
        '''
        try:
            self.view = kwargs.pop('view')
        except Exception:
            pass
        super(WidgetCustomizeForms, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            # recorre todos los fields
            if field.help_text:
                # anexa como title la ayuda descrita
                if not field.widget.attrs.get('title'):
                    field.widget.attrs['title'] = field.help_text

            field_type = type(field)
            if field_type in (
                forms.ChoiceField, forms.TypedChoiceField,
                forms.MultipleChoiceField, forms.ModelChoiceField,
                forms.ModelMultipleChoiceField
            ):
                # si son atributos de seleccion usa la clase chosen

                if not type(field.widget) in (
                        forms.widgets.CheckboxSelectMultiple,
                        forms.widgets.RadioSelect):
                    field.widget.attrs['class'] = 'select-chosen'
                    field.widget.attrs['data-placeholder'] = '...'

                if not field.label:
                    atr_add = ''
                    if field.required:
                        atr_add = ' (*)'
                    if field_type == forms.ModelChoiceField:
                        field.label = field.queryset.model._meta.verbose_name + atr_add
                    elif field_type == forms.ModelMultipleChoiceField:
                        field.label = field.queryset.model._meta.verbose_name_plural + atr_add
            else:
                # en caso contrario se verifica si existe un label
                if field.label:
                    pos = field.label.find('(*)')
                    # conprobamos que tenga el * de requerido o que sea requerido
                    if pos >= 0:
                        field.widget.attrs['required'] = ''
                    elif field.required is True:
                        field.widget.attrs['required'] = ''
                        pos = len(field.label)
                        field.label += ' (*)'

                    # por ultimo agrega el placeholder con el label sin el *
                    field.widget.attrs['placeholder'] = field.label[:pos]


class FilterDeporteForm(WidgetCustomizeForms, forms.Form):
    '''
    Formulario creado especificamente para filtrar por deporte
    '''
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.only('pk', 'nombre').all(),
        required=True,
        empty_label='Seleccione un {0}'.format(Deportes._meta.verbose_name)
    )


class FilterTorneoForm(FilterDeporteForm):
    '''
    Formulario creado especificamente para filtrar por deporte y torneo
    '''
    torneo = forms.ModelChoiceField(
        queryset=Torneos.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione una {0}'.format(Torneos._meta.verbose_name)
    )

    def __init__(self, *args, **kwargs):
        super(FilterTorneoForm, self).__init__(*args, **kwargs)
        self.fields["deporte"].required = False
        if kwargs["view"].request.GET.get("deporte"):
            self.fields["torneo"].queryset = Torneos.objects.filter(
                deporte_id=kwargs["view"].request.GET.get("deporte")
            ).only("nombre")


class FilterEquipoForm(FilterTorneoForm):
    '''
    Formulario creado especificamente para filtrar por deporte, torneo y equipo
    '''
    equipo = forms.ModelChoiceField(
        queryset=Equipos.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(Equipos._meta.verbose_name)
    )

    def __init__(self, *args, **kwargs):
        super(FilterEquipoForm, self).__init__(*args, **kwargs)
        if kwargs["view"].request.GET.get("equipo"):
            self.fields["equipo"].queryset = Equipos.objects.filter(
                pk=kwargs["view"].request.GET.get("equipo")
            )
        elif kwargs["view"].request.GET.get("torneo"):
            self.fields["equipo"].queryset = Equipos.objects.filter(
                equiposligas__liga_id=kwargs["view"].request.GET.get("torneo")
            ).only("nombre").distinct()

        elif kwargs["view"].request.GET.get("deporte"):
            self.fields["equipo"].queryset = Equipos.objects.filter(
                deporte_id=kwargs["view"].request.GET.get("deporte")
            ).only("nombre")


class FilterTemporadaForm(FilterTorneoForm):
    '''
    Formulario creado especificamente para filtrar por deporte, torneo y temporada
    '''
    temporada = forms.ModelChoiceField(
        queryset=Temporadas.objects.filter(fechafin__gte=now().date()),
        required=False,
        empty_label="Seleccione una temporada"
    )


class FilterDeporteRangoFechaForm(WidgetCustomizeForms, forms.Form):
    '''
    Formulario creado especificamente para filtrar por deporte y por rando de fechas
    '''
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.only('pk', 'nombre').all(),
        label=Deportes._meta.verbose_name + ' (*)',
        required=True,
        empty_label='Seleccione un {0}'.format(Deportes._meta.verbose_name)
    )
    torneo = forms.ModelChoiceField(
        queryset=Torneos.objects.only('pk', 'nombre').all(),
        label=Torneos._meta.verbose_name,
        required=False,
        empty_label='Seleccione una {0}'.format(Torneos._meta.verbose_name)
    )
    fecha_inicio = forms.DateField(
        label='Fecha inicio ',
        required=True,
    )
    fecha_fin = forms.DateField(
        label='Fecha fin ',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FilterDeporteRangoFechaForm, self).__init__(*args, **kwargs)
        self.fields['fecha_inicio'].initial = now().strftime(FORMAT_STR_DATE_FORM)
        self.fields['fecha_fin'].initial = self.fields['fecha_inicio'].initial

    def clean(self):
        # valido que si no viene fecha, se renderize otra vez el form
        if not self.data.get('fecha_inicio'):
            self.is_bound = False

        deporte = self.data.get('deporte')
        torneo = self.data.get('torneo')
        if deporte:
            self.fields['torneo'].queryset = Torneos.objects.filter(deporte=deporte)
            if torneo:
                self.fields['torneo'].initial = torneo
        return self.cleaned_data


class FilterDeporteFechaForm(WidgetCustomizeForms, forms.Form):
    '''
    Formulario creado especificamente para filtrar por deporte y por fecha
    '''
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(Deportes._meta.verbose_name)
    )
    torneo = forms.ModelChoiceField(
        queryset=Torneos.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione una {0}'.format(Torneos._meta.verbose_name)
    )
    fecha = forms.DateField(
        label='Fecha (*)',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FilterDeporteFechaForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = now().strftime(FORMAT_STR_DATE_FORM)

    def clean(self):
        # valido que si no viene fecha, se renderize otra vez el form
        if not self.data.get('fecha'):
            self.is_bound = False
        return self.cleaned_data


class FilterDeportesFechaForm(WidgetCustomizeForms, forms.Form):
    '''
    Formulario creado especificamente para filtrar por deporte y por fecha
    '''
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(Deportes._meta.verbose_name)
    )
    fecha = forms.DateField(
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FilterDeportesFechaForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = now().strftime(FORMAT_STR_DATE_FORM)

    def clean(self):
        # valido que si no viene fecha, se renderize otra vez el form
        if not self.data.get('fecha'):
            self.is_bound = False
        return self.cleaned_data


class FilterDeporteJugadoresForm(FilterDeporteForm):
    '''
    Formulario creado especificamente para filtrar por deporte y por fecha
    '''
    tipo = forms.ModelChoiceField(
        queryset=JugadorTipo.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(JugadorTipo._meta.verbose_name)
    )
    equipo = forms.ModelChoiceField(
        queryset=Equipos.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(Equipos._meta.verbose_name)
    )
    jugador = forms.ModelChoiceField(
        queryset=Jugador.objects.only('pk', 'nombre').all(),
        required=False,
        empty_label='Seleccione un {0}'.format(Jugador._meta.verbose_name)
    )

    def __init__(self, *args, **kwargs):
        super(FilterDeporteJugadoresForm, self).__init__(*args, **kwargs)

        if kwargs["view"].request.GET.get("equipo"):
            self.fields["jugador"].queryset = Jugador.objects.filter(
                equipos=kwargs["view"].request.GET.get("equipo")
            )

        if kwargs["view"].request.GET.get("deporte"):
            self.fields["tipo"].queryset = JugadorTipo.objects.filter(
                deporte_id=kwargs["view"].request.GET.get("deporte")
            )

            self.fields["equipo"].queryset = Equipos.objects.filter(
                deporte_id=kwargs["view"].request.GET.get("deporte")
            ).only("nombre")


class BaseFilterCadenaComercializacionForm(forms.Form):
    '''
    Formulario creado especificamente para filtrar por la cadena de comercializacion
    '''

    operadora = forms.ModelChoiceField(
        required=False,
        queryset=Operadoras.objects.only('pk', 'nombre', 'status_id').all(),
        empty_label='Todas las {0}'.format(Operadoras._meta.verbose_name_plural)
    )
    bloque = forms.ModelChoiceField(
        required=False,
        queryset=Bloques.objects.only('pk', 'nombre', 'status_id').all(),
        empty_label='Todas las {0}'.format(Bloques._meta.verbose_name_plural)
    )
    banca = forms.ModelChoiceField(
        required=False,
        queryset=Bancas.objects.only('pk', 'nombre', 'status_id').all(),
        empty_label='Todas las {0}'.format(Bancas._meta.verbose_name_plural)
    )
    distribuidor = forms.ModelChoiceField(
        required=False,
        queryset=Distribuidores.objects.only('pk', 'nombre', 'status_id').all(),
        empty_label='Todas los {0}'.format(Distribuidores._meta.verbose_name_plural)
    )
    agencia = forms.ModelChoiceField(
        required=False,
        queryset=Agencias.objects.only('pk', 'nombre', 'status_id', 'codigo').all(),
        empty_label='Todas los {0}'.format(Agencias._meta.verbose_name_plural)
    )

    def __init__(self, *args, **kwargs):
        super(BaseFilterCadenaComercializacionForm, self).__init__(*args, **kwargs)

        self.view.set_execute_function_by_profile(
            **{
                'prefix': 'filter',
                'instance': self
            }
        )

        if hasattr(self.view, 'model'):
            if isinstance(self.view.model(), Bancas):
                del self.fields['distribuidor']
                del self.fields['agencia']
            elif isinstance(self.view.model(), Distribuidores):
                del self.fields['agencia']

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

        self.fields['distribuidor'].queryset = self.fields['distribuidor'].queryset.filter(
            banca__bloque__operadora_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['agencia'].queryset = self.fields['agencia'].queryset.filter(
            distribuidores__banca__bloque__operadora_id=self.view.object_comercializadora.get_object().pk
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

        self.fields['distribuidor'].queryset = self.fields['distribuidor'].queryset.filter(
            banca__bloque_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['agencia'].queryset = self.fields['agencia'].queryset.filter(
            distribuidores__banca__bloque_id=self.view.object_comercializadora.get_object().pk
        )

    def filter_userprofile_banca(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en una banca
        '''
        del self.fields['operadora']
        del self.fields['bloque']
        del self.fields['banca']

        self.fields['distribuidor'].queryset = self.fields['distribuidor'].queryset.filter(
            banca_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['agencia'].queryset = self.fields['agencia'].queryset.filter(
            distribuidores__banca_id=self.view.object_comercializadora.get_object().pk
        )

    def filter_userprofile_distribuidor(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en un distribuidor
        '''
        del self.fields['operadora']
        del self.fields['bloque']
        del self.fields['banca']
        del self.fields['distribuidor']

        self.fields['agencia'].queryset = self.fields['agencia'].queryset.filter(
            distribuidores_id=self.view.object_comercializadora.get_object().pk
        )

    def filter_userprofile_agencia(self, **kwargs):
        '''
        Se realizan los filtros respectivos basandose en una agencia
        '''
        del self.fields['operadora']
        del self.fields['bloque']
        del self.fields['banca']
        del self.fields['distribuidor']
        del self.fields['agencia']

    def clean(self):
        '''
        Preinicializa los initial para llenas
        las dependencias hacia arriba de los filtros
        '''
        agencia = self.cleaned_data.get('agencia')
        if agencia:
            self.fields['agencia'].queryset = Agencias.objects.only(
                'pk', 'nombre', 'status_id', 'codigo').filter(
                distribuidores_id=agencia.distribuidores_id)
            self.fields['agencia'].initial = agencia

            if 'distribuidor' in self.fields:
                self.fields['distribuidor'].initial = agencia.distribuidores
                if 'banca' in self.fields:
                    self.fields['distribuidor'].queryset = Distribuidores.objects.only(
                        'pk', 'nombre', 'status_id').filter(banca_id=agencia.distribuidores.banca_id)
                    self.fields['banca'].initial = agencia.distribuidores.banca
                    if 'bloque' in self.fields:
                        self.fields['banca'].queryset = Bancas.objects.only(
                            'pk', 'nombre', 'status_id').filter(
                            bloque_id=agencia.distribuidores.banca.bloque_id)
                        self.fields['bloque'].initial = agencia.distribuidores.banca.bloque
                        if 'operadora' in self.fields:
                            self.fields['bloque'].queryset = Bloques.objects.only(
                                'pk', 'nombre', 'status_id').filter(
                                operadora_id=agencia.distribuidores.banca.bloque.operadora_id)
                            self.fields['operadora'].initial = agencia.distribuidores.banca.bloque.operadora

        else:

            distribuidor = self.cleaned_data.get('distribuidor')
            if distribuidor:
                self.fields['distribuidor'].queryset = Distribuidores.objects.only(
                    'pk', 'nombre', 'status_id').filter(banca_id=distribuidor.banca_id)
                self.fields['distribuidor'].initial = distribuidor

                if 'agencia' in self.fields:
                    self.fields['agencia'].queryset = Agencias.objects.only(
                        'pk', 'nombre', 'status_id', 'codigo').filter(
                        distribuidores_id=distribuidor.pk)

                if 'banca' in self.fields:
                    self.fields['banca'].initial = distribuidor.banca
                    if 'bloque' in self.fields:
                        self.fields['banca'].queryset = Bancas.objects.only(
                            'pk', 'nombre', 'status_id').filter(
                            bloque_id=distribuidor.banca.bloque_id)
                        self.fields['bloque'].initial = distribuidor.banca.bloque
                        if 'operadora' in self.fields:
                            self.fields['bloque'].queryset = Bloques.objects.only(
                                'pk', 'nombre', 'status_id').filter(
                                operadora_id=distribuidor.banca.bloque.operadora_id)
                            self.fields['operadora'].initial = distribuidor.banca.bloque.operadora

            else:

                banca = self.cleaned_data.get('banca')
                if banca:
                    self.fields['banca'].queryset = Bancas.objects.only(
                        'pk', 'nombre', 'status_id').filter(bloque_id=banca.bloque_id)
                    self.fields['banca'].initial = banca
                    #
                    if 'distribuidor' in self.fields:
                        self.fields['distribuidor'].queryset = Distribuidores.objects.only(
                            'pk', 'nombre', 'status_id').filter(banca_id=banca.pk)
                    if 'agencia' in self.fields:
                        self.fields['agencia'].queryset = Agencias.objects.only(
                            'pk', 'nombre', 'status_id', 'codigo').filter(
                            distribuidores__banca=banca.pk)
                    #
                    if 'bloque' in self.fields:
                        self.fields['bloque'].initial = banca.bloque
                        if 'operadora' in self.fields:
                            self.fields['bloque'].queryset = Bloques.objects.only(
                                'pk', 'nombre', 'status_id').filter(
                                operadora=banca.bloque.operadora_id)
                            self.fields['operadora'].initial = banca.bloque.operadora

                else:

                    bloque = self.cleaned_data.get('bloque')
                    if bloque:
                        self.fields['bloque'].queryset = Bloques.objects.only(
                            'pk', 'nombre', 'status_id').filter(
                            operadora_id=bloque.operadora_id)
                        self.fields['bloque'].initial = bloque
                        #
                        if 'banca' in self.fields:
                            self.fields['banca'].queryset = Bancas.objects.only(
                                'pk', 'nombre', 'status_id').filter(bloque_id=bloque.pk)

                        if 'distribuidor' in self.fields:
                            self.fields['distribuidor'].queryset = Distribuidores.objects.only(
                                'pk', 'nombre', 'status_id').filter(banca__bloque_id=bloque.pk)

                        if 'agencia' in self.fields:
                            self.fields['agencia'].queryset = Agencias.objects.only(
                                'pk', 'nombre', 'status_id', 'codigo').filter(
                                distribuidores__banca__bloque_id=bloque.pk)
                        #
                        if 'operadora' in self.fields:
                            self.fields['operadora'].initial = bloque.operadora

                    else:
                        operadora = self.cleaned_data.get('operadora')
                        if operadora:
                            self.fields['operadora'].queryset = Operadoras.objects.only(
                                'pk', 'nombre', 'status_id').all()
                            self.fields['operadora'].initial = operadora

        self.is_bound = False
        return self.cleaned_data


class FilterCadenaComercializacionForm(
        WidgetCustomizeForms,
        BaseFilterCadenaComercializacionForm,
):
    pass


class FilterCadenaComercializacionSimpleForm(
        WidgetCustomizeForms,
        BaseFilterCadenaComercializacionForm,
):

    def __init__(self, *args, **kwargs):
        super(FilterCadenaComercializacionSimpleForm, self).__init__(*args, **kwargs)

        for field_name in self.fields:
            field = self.fields.get(field_name)
            field.empty_label = 'Seleccione ' + field.queryset.model._meta.verbose_name
