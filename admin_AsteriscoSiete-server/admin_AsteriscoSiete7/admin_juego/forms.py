# -*- coding: utf-8 -*-

from admin_apuestas.models import TicketsDetail
from admin_finanzas.models import Comercializadora
from admin_finanzas.task import AsyncSuspenderEncuentro, AsyncSuspenderJornada, AsyncSuspenderTemporada
from admin_juego.models import (
    # === Vocabulario Asterisco Siete (*7) ===
    OperadoraLoteria,       # Operadora (Zulia, Táchira, Cojedes) - ex-Deportes
    TipoProducto,           # Producto comercial (EL ARREJUNTAO, Triple...) - ex-Torneos
    TipoProducto_Grupos,    # M2M helper
    PeriodoSorteo,          # Período/Temporada de sorteos - ex-Temporadas
    Fechas,                 # Horarios/Jornadas de sorteo - ex-Jornadas
    Sorteo,                 # Sorteo/Encuentro
    SorteoDetalle,          # Detalle del sorteo
    ModalidadJuego,         # Modalidad de juego (Triple, Terminal, Animal) - ex-Equipos
    ModalidadApuesta,       # Tipo de apuesta - ex-Modalidades
    ModalidadJuego_Grupos,  # M2M helper
    ModalidadPeriodo,       # Período de modalidad
    GruposApuesta,          # Grupos de apuesta
    SistemaJuego,           # Sistema de juego
    Condiciones,            # Condiciones de juego
    RestriccionesSorteo,    # Restricciones del sorteo
    TipoNumeroSorteo,       # Tipos de números del sorteo - ex-JugadorTipo
    NumeroSorteo,           # Números del sorteo - ex-Jugador
    apuesta,                # Modelo de apuesta
    JugadasInformativas,    # Jugadas informativas
)
from admin_lib.util_forms import WidgetCustomizeForms
from admin_status.models import Status
from django import forms
from django.contrib import messages


class SistemaJuegoForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = SistemaJuego
        fields = [
            "nombre",
            "logo",
            "banner",
            "theme",
            "notificacion_automatica",
        ]


class DeportesForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = TipoProducto
        fields = '__all__'


class TorneosForm(WidgetCustomizeForms, forms.ModelForm):
    """
    Form para crear/editar un Producto de Lotería (EL ARREJUNTAO, Triple Táchira, etc.)
    Vocabulario Asterisco Siete (*7):
      - loteria      → operadora a la que pertenece (era 'deporte')
      - fondo_pantalla → imagen de fondo para kioscos (era 'fondoweb')
      - por_horarios → venta por horas de sorteo (era 'por_jornadas')
      - por_modalidades → agrupa Triple/Terminal/Animalitos (era 'por_grupos')
    """

    class Meta:
        model = TipoProducto
        fields = [
            'deporte',   # FK a LOTERIA (operadora)
            'nombre',
            'logo',
            'fondoweb',  # => se migrará a fondo_pantalla
            'por_jornadas',   # => se migrará a por_horarios
            'por_grupos',     # => se migrará a por_modalidades
        ]

    def __init__(self, *args, **kwargs):
        super(TorneosForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields["deporte"]


class JornadasForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.all(),
        help_text="Seleccione un deporte para la jornada",
        required=True,
    )
    liga = forms.ModelChoiceField(
        queryset=TipoProducto.objects.all(),
        help_text="Seleccione una liga para la jornada",
        required=True,
    )
    horajuego = forms.DateTimeField(
        label="Fecha y hora ",
        widget=forms.DateInput(attrs={'class': 'invisible'}),
        help_text="Ingrese la fecha y hora de los encuentros "
        "a generar automaticamente",
        required=False
    )

    status_old = None

    class Meta:
        model = Fechas
        fields = [
            'deporte',
            'liga',
            'temporadas',
            'status',
            'jornada',
            'fechaini',
            'fechafin',
            'parley',
            'quiniela',
            'count_encuentros',
            'monto_inicial',
            'valor',
            'apuestasimple',
            'horajuego'
        ]

    def __init__(self, *args, **kwargs):
        super(JornadasForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Status.objects.filter(content_type=2)

        if self.instance.pk:
            self.create = False
            self.status_old = self.instance.status
            for fields in ["deporte", "liga", "temporadas", "horajuego"]:
                del self.fields[fields]
        else:
            self.create = True
            self.fields["liga"].queryset = TipoProducto.objects.filter(
                por_jornadas=True
            )
            self.fields['temporadas'].queryset = Fechas.objects.filter(
                torneo__por_jornadas=True
            )

    def save(self, commit=True, *args, **kwargs):
        super(JornadasForm, self).save(commit=True, *args, **kwargs)

        if self.create:
            self.instance.sistema = self.view.object_sistema_juego
            self.instance.save(update_fields=["sistema"])

            horajuego = self.cleaned_data['horajuego']
            if horajuego is not None:
                equipos_afiliados = ModalidadPeriodo.objects.filter(
                    temporada=self.instance.temporadas
                )
                for obj in equipos_afiliados:
                    encuentro = Sorteo(
                        horajuego=horajuego,
                        horacierre=horajuego,
                        status=self.instance.status,
                        jornada=self.instance
                    )
                    encuentro.save()
                    detalle_encuentro = SorteoDetalle(
                        encuentro=encuentro,
                        equipos_temporadas=obj,
                        indice=1
                    )
                    detalle_encuentro.save()

        if self.status_old is not None:
            if (
                    self.status_old.codename == "status_habilitado" and
                    self.instance.status.codename == "status_inhabilitado"
            ):
                AsyncSuspenderJornada.delay(
                    *(), **{"jornada": self.instance.pk, }
                )

        return self.instance

    def clean_fechafin(self):
        fecha_ini = self.cleaned_data.get('fechaini')
        fecha_fin = self.cleaned_data.get('fechafin')
        if fecha_ini is not None:
            if fecha_ini > fecha_fin:
                raise forms.ValidationError(
                    "Debe ser mayor o igual a la fecha de inicio"
                )
        return fecha_fin

    def clean_horajuego(self):
        fecha_hora = self.cleaned_data.get('horajuego')

        fecha_ini = self.cleaned_data.get('fechaini')
        fecha_fin = self.cleaned_data.get('fechafin')

        if fecha_hora is not None:
            if fecha_ini > fecha_hora.date() or fecha_fin < fecha_hora.date():
                raise forms.ValidationError(
                    "Esta fecha debe estar comprendida entre "
                    "la fecha de inicio y la fecha de fin de la jornada"
                )
        return fecha_hora


class TemporadasForm(WidgetCustomizeForms, forms.ModelForm):
    """
    Formulario para la gestión de Períodos/Fechas de Sorteo.
    Vocabulario Asterisco Siete (*7):
      - deporte  → TipoProducto (Lotería / Animalitos)
      - torneo   → Producto activo dentro del TipoProducto
      - nombre   → Nombre del período (ej. "Enero 2025")
      - fechaini / fechafin → Rango de vigencia del período
      - status   → Estado del período (Abierto / Cerrado)
    """
    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.all(),
        label='Tipo de Producto (*)',
        help_text='Seleccione el tipo de lotería o animalitos',
        required=True
    )
    status_old = None

    class Meta:
        # PeriodoSorteo = ex-Temporadas: tiene nombre, torneo (FK a TipoProducto),
        # fechaini, fechafin, status
        model = PeriodoSorteo
        fields = [
            'deporte',   # campo virtual del form (no del modelo)
            'torneo',    # FK a TipoProducto
            'status',
            'nombre',
            'fechaini',
            'fechafin',
        ]

    def __init__(self, *args, **kwargs):
        super(TemporadasForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Status.objects.filter(content_type=2)

        if self.instance.pk:
            self.status_old = self.instance.status
            # Al editar ocultamos deporte y torneo (ya están fijos)
            for field in ["deporte", "torneo"]:
                if field in self.fields:
                    del self.fields[field]

    def clean_fechafin(self):
        fecha_ini = self.cleaned_data.get('fechaini')
        fecha_fin = self.cleaned_data.get('fechafin')
        if fecha_ini is not None:
            if fecha_ini > fecha_fin:
                raise forms.ValidationError(
                    "Debe ser mayor o igual a la fecha de inicio"
                )
            else:
                # Valida que no haya solapamiento de períodos para el mismo tipo de producto
                torneo = self.cleaned_data.get('torneo')
                if torneo:
                    solapados = Fechas.objects.filter(
                        torneo=torneo,
                        fechafin__gte=fecha_ini,
                        fechaini__lte=fecha_fin,
                    ).exclude(pk=self.instance.pk if self.instance.pk else None)
                    if solapados.exists():
                        self._errors["torneo"] = (
                            "Ya existen períodos de sorteo en el mismo rango de fechas."
                        )
        return fecha_fin

    def save(self, commit=True, *args, **kwargs):
        super(TemporadasForm, self).save(commit=True, *args, **kwargs)

        if self.status_old is not None:
            if (
                    self.status_old.codename == "status_habilitado" and
                    self.instance.status.codename == "status_inhabilitado"
            ):
                AsyncSuspenderTemporada.delay(
                    *(), **{"temporada": self.instance.pk, }
                )

        return self.instance


class GruposJuegoForm(WidgetCustomizeForms, forms.ModelForm):
    """
    Form para Grupos de Apuesta.
    Vocabulario Asterisco Siete (*7):
      - deporte → TipoProducto operadora (campo virtual del form)
      - torneo  → TipoProducto producto (campo virtual del form)
      - nombre  → Nombre del grupo de apuesta
      - orden   → Prioridad de impresión
    """
    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.all(),
        required=True,
        label='Tipo de Producto (*)',
        help_text='Seleccione el tipo de lotería o animalitos'
    )
    torneo = forms.ModelChoiceField(
        queryset=TipoProducto.objects.filter(por_grupos=True),
        required=True,
        label='Producto (*)',
        help_text='Seleccione el producto para el grupo'
    )

    class Meta:
        model = GruposApuesta
        fields = [
            "deporte",
            "torneo",
            "nombre",
            "orden",
        ]

    def __init__(self, *args, **kwargs):
        super(GruposJuegoForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            for field in ["deporte", "torneo"]:
                if field in self.fields:
                    del self.fields[field]



class EquiposForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = ModalidadJuego
        fields = '__all__'


class JugadorTipoForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = TipoNumeroSorteo
        fields = '__all__'


class JugadorForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.all(),
        help_text="Seleccione un deporte para el jugador",
        required=False
    )

    class Meta:
        model = NumeroSorteo
        fields = ['deporte', 'tipo', 'nombre', 'lateralidad', 'foto']

    def __init__(self, *args, **kwargs):
        super(JugadorForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields["deporte"]
            del self.fields["tipo"]

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not self.instance.pk:
            if NumeroSorteo.objects.filter(
                nombre=nombre,
                tipo_id=self.instance.tipo_id
            ).exists():
                raise forms.ValidationError(
                    'El nombre {0} ya se encuentra registrado para el tipo {1}'.format(nombre, self.instance.tipo)
                )
        return nombre


class EncuentrosForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=TipoProducto.objects.only('pk', 'nombre').all(),
        required=True,
        help_text="Seleccione un deporte para el encuentro"
    )
    liga = forms.ModelChoiceField(
        queryset=TipoProducto.objects.only('pk', 'nombre').all(),
        required=True,
        help_text="Seleccione una liga para el encuentro"
    )
    temporada = forms.ModelChoiceField(
        queryset=Fechas.objects.only('pk', 'nombre').all(),
        required=True,
        help_text="Seleccione una temporada para el encuentro"
    )
    status_old = None

    class Meta:
        model = Sorteo
        # Vocabulario Asterisco Siete (*7) — pendiente renombrar en el modelo:
        #   loteria     = jornada    (período/fecha que gestiona el sorteo)
        #   tipo_jugada = grupo      (modalidad: Triple, Animalito, etc.)
        #   hora_ejecucion = horajuego  (hora exacta del sorteo)
        #   hora_bloqueo   = horacierre (5 min antes = cierre de tickets)
        #   estatus_sorteo = status
        #   resultado      = marcador
        #   logro          = monto del premio pagado (factor × apuesta)
        fields = [
            'deporte',
            'liga',
            'temporada',
            'jornada',
            'grupo',
            'status',
            'horajuego',
            'horacierre',
        ]


    def __init__(self, *args, **kwargs):
        super(EncuentrosForm, self).__init__(*args, **kwargs)
        self.fields["jornada"].queryset = Fechas.objects.only('pk', 'jornada').filter(
            sistema_id=self.view.object_sistema_juego.pk
        )

        self.fields["grupo"].required = False
        self.fields["grupo"].queryset = self.fields["grupo"].queryset.only('pk', 'nombre')

        self.fields["status"].queryset = Status.objects.only('pk', 'name').filter(
            content_type=2
        )

        self.fields["jornada"].required = False

        if self.instance.pk:
            self.status_old = self.instance.status
            for fields in ["deporte", "liga", "temporada"]:
                del self.fields[fields]
            del self.fields["jornada"]

        if self.view.request.POST.get('deporte'):
            self.fields["liga"].queryset = TipoProducto.objects.only('pk', 'nombre').filter(
                deporte=self.view.request.POST.get('deporte')
            )
            if not self.view.request.POST.get('temporada'):
                self.fields["temporada"].queryset = Fechas.objects.none()

    def check_apuestas(self):
        exists = False
        if self.instance.pk:
            kwargs = {}
            kwargs[self.instance.get_prefix_kwargs_by_level_tickets_details()] = self.instance.pk
            exists = TicketsDetail.objects.filter(**kwargs).exists()
        return exists

    def clean_horajuego(self):
        horajuego = self.cleaned_data.get('horajuego')
        if self.check_apuestas():
            if horajuego > self.instance.horajuego:
                raise forms.ValidationError(
                    "Una vez se registren ventas la hora del encuentro no "
                    "puede modificarse a un valor mayor del original."
                )
        return horajuego

    def clean_horacierre(self):
        hora_juego = self.cleaned_data.get('horajuego')
        hora_cierre = self.cleaned_data.get('horacierre')

        if hora_juego is not None and hora_cierre is not None:
            if hora_cierre >= hora_juego:
                raise forms.ValidationError(
                    "La fecha y hora de cierre "
                    "del encuentro debe ser "
                    "menor a la fecha y hora"
                    "de inicio del juego"
                )
        return hora_cierre

    def clean_jornada(self):
        """
        Se crea la jornada automaticamente en caso de ser un torneo
        sin las miamas. en caso contrario se devuelve un error
        """
        jornada = self.cleaned_data.get("jornada")
        if not jornada:
            temporada = self.cleaned_data.get("temporada")
            if temporada:
                if not temporada.torneo.por_jornadas:
                    jornada = Fechas.get_or_create_or_flush(
                        temporada=temporada,
                        sistemajuego=self.view.object_sistema_juego,
                    )
                else:
                    raise forms.ValidationError(
                        "Este campo es obligatorio"
                    )
        return jornada

    def clean(self):
        jornada = self.cleaned_data.get("jornada")
        if not jornada:
            temporada = self.cleaned_data.get("temporada")
            if temporada:
                if not temporada.torneo.por_jornadas:
                    jornada = Fechas.get_or_create_or_flush(
                        temporada=temporada,
                        sistemajuego=self.view.object_sistema_juego,
                    )
        super(EncuentrosForm, self).clean()
        return self.cleaned_data

    def save(self, commit=True, *args, **kwargs):
        super(EncuentrosForm, self).save(commit=False, *args, **kwargs)

        if self.status_old is not None:
            if (
                    self.status_old.codename == "status_habilitado" and
                    self.instance.status.codename == "status_inhabilitado"
            ):
                AsyncSuspenderEncuentro.delay(
                    *(), **{"encuentro": self.instance.pk, }
                )
        else:
            sistema_logro = self.instance.jornada.sistema
            for deporte_grupo in TipoProducto_Grupos.objects.filter(
                    deporte=self.instance.jornada.temporadas.torneo.deporte
            ):
                for modalidad_grupo in deporte_grupo.grupo \
                        .modalidades_grupos_set.all():
                    if modalidad_grupo.deporte_restriccion.filter(
                        pk=self.instance.jornada.temporadas.torneo.deporte.pk
                    ).exists():
                        continue
                    encuentro_modalidad = SorteoModalidades.objects.get_or_create(
                        encuentro=self.instance,
                        deporte_grupo=deporte_grupo,
                        modalidad_grupo=modalidad_grupo,
                        sistema=sistema_logro,
                    )[0]

                    for condicion in encuentro_modalidad.modalidad_grupo \
                            .modalidad.condiciones_set.all().order_by("orden"):
                        if condicion.equipo:
                            for encuentro_detail in self.instance \
                                    .encuentrosdetail_set.all() \
                                    .order_by("-indice"):
                                if condicion.tipo == 4:
                                    """
                                    verificamos nuevamente que sea una
                                    condicion de Informativa
                                    """
                                    JugadasInformativas.objects.get_or_create(
                                        detalle_encuentro=encuentro_detail,
                                        encuentros_modalidad=encuentro_modalidad,
                                        condicion=condicion,
                                        sistema=sistema_logro,
                                    )
                                else:
                                    jugada = apuesta.objects.get_or_create(
                                        detalle_encuentro=encuentro_detail,
                                        encuentros_modalidad=encuentro_modalidad,
                                        condicion=condicion,
                                        sistema=sistema_logro,
                                    )[0]
                                    jugada.indice = encuentro_detail.indice
                                    if jugada.status is None:
                                        """solo entra cuando se crea"""
                                        jugada.status = Status.get_status_by_codename(
                                            codename="status_eliminado"
                                        )
                                    jugada.save()
                        else:
                            for indice in range(1, condicion.tipo + 1):
                                jugada = apuesta.objects.get_or_create(
                                    encuentros_modalidad=encuentro_modalidad,
                                    condicion=condicion,
                                    indice=indice,
                                    sistema=sistema_logro,
                                )[0]
                                if jugada.status is None:
                                    jugada.status = Status.get_status_by_codename(
                                        codename="status_eliminado"
                                    )
                                    jugada.save()
        return self.instance


class GruposApuestasForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = GruposApuesta
        fields = '__all__'
        widgets = {
            'deporte': forms.widgets.CheckboxSelectMultiple(),
        }

    def save(self, commit=True, *args, **kwargs):
        super(GruposApuestasForm, self).save(commit=False, *args, **kwargs)
        self.instance.codename = self.instance.nombre.replace(" ", "_").lower()
        self.instance.save()

        for deporte in self.cleaned_data["deporte"]:
            """guardo"""
            TipoProducto_Grupos.objects.get_or_create(
                deporte=deporte,
                grupo=self.instance
            )
        for deporte in self.instance.deporte.all():
            if deporte not in self.cleaned_data["deporte"]:
                try:
                    deporte_old = TipoProducto_Grupos.objects.get(
                        deporte=deporte,
                        grupo=self.instance
                    )
                    deporte_old.delete()
                except TipoProducto_Grupos.DoesNotExist:
                    pass
        return self.instance


class ModalidadesForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = ModalidadJuego
        fields = '__all__'
        widgets = {
            'grupo': forms.widgets.CheckboxSelectMultiple(),
            'restriction': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ModalidadesForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["restriction"] \
                .queryset = ModalidadJuego.objects.all().exclude(
                pk=self.instance.pk
            )

    def save(self, commit=True, *args, **kwargs):
        super(ModalidadesForm, self).save(commit=False, *args, **kwargs)

        self.instance.codename = self.instance \
            .modalidad.replace(" ", "_").lower()

        self.instance.save()

        for grupo in self.cleaned_data["grupo"]:
            """guardo"""
            ModalidadJuego_Grupos.objects.get_or_create(
                modalidad=self.instance,
                grupo=grupo
            )

        for grupo in self.instance.grupo.all():
            if grupo not in self.cleaned_data["grupo"]:
                grupo_old = ModalidadJuego_Grupos.objects.get(
                    modalidad=self.instance,
                    grupo=grupo
                )
                grupo_old.delete()

        """
        como la tabla intermedia no esta definida esta es la manera de hacerlo
        """
        for restriction in self.cleaned_data["restriction"]:
            """guardo"""
            self.instance.restriction.add(restriction)
        for restriction in self.instance.restriction.all():
            if restriction not in self.cleaned_data["restriction"]:
                self.instance.restriction.remove(restriction)

        return self.instance


class CondicionesForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = Condiciones
        fields = [
            'modalidad',
            'tipo',
            'etiqueta_ref',
            'nombre',
            'orden'
        ]

    def __init__(self, *args, **kwargs):
        super(CondicionesForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            del self.fields["modalidad"]

    def save(self, commit=True, *args, **kwargs):
        super(CondicionesForm, self).save(commit=False, *args, **kwargs)
        self.instance.save()
        self.instance.equipo = True if self.instance.tipo == 0 \
            or self.instance.tipo == 4 else False

        self.instance.save(update_fields=["equipo"])
        return self.instance


class Modalidades_GruposForm(forms.ModelForm):
    nombre_grupo = forms.CharField(
        max_length=100,
        label="Grupo de Modalidad "
    )

    class Meta:
        model = ModalidadJuego_Grupos
        fields = [
            "nombre_grupo",
            "deporte_restriccion"
        ]

        widgets = {
            'deporte_restriccion': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(Modalidades_GruposForm, self).__init__(*args, **kwargs)
        self.fields["nombre_grupo"].initial = self.instance.grupo
        self.fields["nombre_grupo"].widget.attrs["readonly"] = ""
        self.fields["deporte_restriccion"] \
            .queryset = self.instance.grupo.deporte.all()


class RestriccionesReferenciasForm(WidgetCustomizeForms, forms.ModelForm):
    label = forms.CharField(
        max_length=100,
        required=False,
    )

    class Meta:
        model = RestriccionesSorteo
        exclude = [
            'deporte',
            'grupo',
            'modalidad',
            'condicion',
            'min_ref',
            'max_ref'
        ]

    def __init__(self, *args, **kwargs):
        super(RestriccionesReferenciasForm, self).__init__(*args, **kwargs)

        if isinstance(self.view.object, ModalidadJuego):

            modalidad_grupos = ModalidadJuego_Grupos.objects.filter(
                modalidad_id=self.view.object.pk
            )
            for mg in modalidad_grupos:
                for gd in mg.grupo.deportes_grupos_set.all():
                    if mg.deporte_restriccion.filter(
                        pk=gd.deporte.id
                    ).exists():
                        continue

                    name = "{0}_{1}".format(
                        mg.grupo.id,
                        gd.deporte.id
                    )

                    self.fields[name + "_min"] = forms.CharField(
                        required=False,
                        max_length=100
                    )
                    self.fields[name + "_max"] = forms.CharField(
                        required=False,
                        max_length=100
                    )
                    self.fields[name + "_min"] \
                        .widget.attrs['class'] = 'input-logro min'
                    self.fields[name + "_max"] \
                        .widget.attrs['class'] = 'input-logro max'

                    try:
                        existe = RestriccionesSorteo.objects.get(
                            grupo=mg.grupo,
                            deporte=gd.deporte,
                            modalidad=self.view.object
                        )
                        self.fields[name + "_min"].initial = existe.min_ref
                        self.fields[name + "_max"].initial = existe.max_ref
                    except RestriccionesSorteo.DoesNotExist:
                        pass

                    self.fields[name + "_min"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'
                    self.fields[name + "_max"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'

        elif isinstance(self.view.object, Condiciones):
            modalidad_grupos = ModalidadJuego_Grupos.objects.filter(
                modalidad=self.view.object.modalidad
            )
            for mg in modalidad_grupos:
                for gd in mg.grupo.deportes_grupos_set.all():
                    if mg.deporte_restriccion.filter(
                        pk=gd.deporte.id
                    ).exists():
                        continue

                    name = "{0}_{1}".format(
                        mg.grupo.id,
                        gd.deporte.id
                    )

                    self.fields[name + "_min"] = forms.CharField(
                        required=False,
                        max_length=100
                    )
                    self.fields[name + "_max"] = forms.CharField(
                        required=False,
                        max_length=100
                    )
                    self.fields[name + "_min"] \
                        .widget.attrs['class'] = 'input-logro min'
                    self.fields[name + "_max"] \
                        .widget.attrs['class'] = 'input-logro max'

                    try:
                        existe = RestriccionesSorteo.objects.get(
                            grupo=mg.grupo,
                            deporte=gd.deporte,
                            condicion=self.view.object
                        )
                        self.fields[name + "_min"].initial = existe.min_ref
                        self.fields[name + "_max"].initial = existe.max_ref
                    except RestriccionesSorteo.DoesNotExist:
                        pass

                    self.fields[name + "_min"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'
                    self.fields[name + "_max"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'

        elif isinstance(self.view.object, GruposApuesta):
            grupo_deportes = TipoProducto_Grupos.objects.filter(
                grupo=self.view.object
            )
            for gd in grupo_deportes:
                name = "{0}_{1}".format(self.view.object.id, gd.deporte.id)
                self.fields[name + "_maxnofavorito"] = forms.CharField(
                    required=False,
                    max_length=100
                )
                self.fields[name + "_maxfavorito"] = forms.CharField(
                    required=False,
                    max_length=100
                )

                self.fields[name + "_maxnofavorito"] \
                    .widget.attrs['class'] = 'input-logro'

                self.fields[name + "_maxfavorito"] \
                    .widget.attrs['class'] = 'input-logro'
                try:
                    existe = RestriccionesSorteo.objects.get(
                        grupo=self.view.object,
                        deporte=gd.deporte,
                        min_ref='logro'
                    )
                    self.fields[name + "_maxnofavorito"] \
                        .initial = existe.max_logro_no_favorito
                    self.fields[name + "_maxfavorito"] \
                        .initial = existe.max_logro_favorito
                except RestriccionesSorteo.DoesNotExist:
                    pass

                self.fields[name + "_maxnofavorito"] \
                    .widget.attrs["pattern"] = '[+]?[0-9]+'

                self.fields[name + "_maxfavorito"].widget \
                    .attrs["pattern"] = '[-]{1}[0-9]+'

        self.fields["label"].initial = "{0}".format(self.view.object)
        self.fields["label"].label = self.view.object._meta.verbose_name
        self.fields["label"].widget.attrs["readonly"] = ""

    def clean(self):
        super(RestriccionesReferenciasForm, self).clean()
        cleaned_data = self.cleaned_data

        vals = []
        for c_d in cleaned_data:
            if c_d.find('min') >= 0:
                var = c_d.split('_')
                vals.append(str(var[0] + "_" + var[1]))

        for v in vals:
            if cleaned_data[v + "_min"] and cleaned_data[v + "_max"]:
                menor = float(str(cleaned_data[v + "_min"]).replace(",", "."))
                mayor = float(str(cleaned_data[v + "_max"]).replace(",", "."))
                if menor > mayor:
                    raise forms.ValidationError(
                        "Rangos invalidos",
                        code='range_invalid',
                    )

        return cleaned_data


class EncuentrosRestrictionForm(WidgetCustomizeForms, forms.Form):

    comercializadora = forms.ModelMultipleChoiceField(
        queryset=Comercializadora.objects.none(),
        required=False,
        label="Ente de cadena"
    )

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance')
        super(EncuentrosRestrictionForm, self).__init__(*args, **kwargs)

        if self.view.object_comercializadora.get_type().codename == "userprofile_master":
            self.fields["comercializadora"].queryset = Comercializadora.objects.filter(
                taquilla__isnull=True
            )
        else:
            self.fields["comercializadora"].queryset = self.view.object_comercializadora.get_offspring(
                profile=self.view.object_comercializadora.get_type(),
            )
