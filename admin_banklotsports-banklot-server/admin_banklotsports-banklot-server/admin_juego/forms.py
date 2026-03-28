# -*- coding: utf-8 -*-

from admin_apuestas.models import TicketsDetail
from admin_finanzas.models import Comercializadora
from admin_finanzas.task import AsyncSuspenderEncuentro, AsyncSuspenderJornada, AsyncSuspenderTemporada
from admin_juego.models import (
    Condiciones, Deportes, Deportes_Grupos, Encuentros, EncuentrosDetail, EncuentrosModalidades, Equipos,
    EquiposTemporadas, GruposApuestas, GruposJuego, Jornadas, Jugadas, JugadasInformativas, Jugador, JugadorTipo,
    Modalidades, Modalidades_Grupos, RestriccionesReferencias, SistemaJuego, Temporadas, Torneos,
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
        model = Deportes
        fields = '__all__'


class TorneosForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = Torneos
        fields = [
            'deporte',
            'nombre',
            'logo',
            'fondoweb',
            'por_jornadas',
            'por_grupos'
        ]

    def __init__(self, *args, **kwargs):
        super(TorneosForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields["deporte"]


class JornadasForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.all(),
        help_text="Seleccione un deporte para la jornada",
        required=True,
    )
    liga = forms.ModelChoiceField(
        queryset=Torneos.objects.all(),
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
        model = Jornadas
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
            self.fields["liga"].queryset = Torneos.objects.filter(
                por_jornadas=True
            )
            self.fields['temporadas'].queryset = Temporadas.objects.filter(
                torneo__por_jornadas=True
            )

    def save(self, commit=True, *args, **kwargs):
        super(JornadasForm, self).save(commit=True, *args, **kwargs)

        if self.create:
            self.instance.sistema = self.view.object_sistema_juego
            self.instance.save(update_fields=["sistema"])

            horajuego = self.cleaned_data['horajuego']
            if horajuego is not None:
                equipos_afiliados = EquiposTemporadas.objects.filter(
                    temporada=self.instance.temporadas
                )
                for obj in equipos_afiliados:
                    encuentro = Encuentros(
                        horajuego=horajuego,
                        horacierre=horajuego,
                        status=self.instance.status,
                        jornada=self.instance
                    )
                    encuentro.save()
                    detalle_encuentro = EncuentrosDetail(
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
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.all(),
        help_text="Seleccione un deporte para la liga",
        required=True
    )
    parley = forms.BooleanField(
        label="Permite la venta de parley? ",
        help_text="Seleccione este campo solo "
        "si la temporada admite venta de parley",
        required=False
    )
    quiniela = forms.BooleanField(
        label="Permite la venta de quiniela? ",
        help_text="Seleccione este campo solo si la "
        "temporada admite venta de quiniela",
        required=False
    )
    apuestasimple = forms.BooleanField(
        label="Permite la venta de apuesta simple? ",
        help_text="Seleccione este campo solo si la "
        "temporada admite venta de apuesta simple",
        required=False
    )
    status_old = None

    class Meta:
        model = Temporadas
        fields = [
            'deporte',
            'torneo',
            'status',
            'nombre',
            'fechaini',
            'fechafin',
            'parley',
            'quiniela',
            'apuestasimple'
        ]

    def __init__(self, *args, **kwargs):
        super(TemporadasForm, self).__init__(*args, **kwargs)

        self.fields['status'].queryset = Status.objects.filter(content_type=2)

        if self.instance.pk:
            self.status_old = self.instance.status

            fields_names = ["deporte", "torneo"]

            if self.instance.torneo.por_jornadas is False:
                jornada = self.get_jornada()
                for field in ["parley", "quiniela", "apuestasimple"]:
                    self.fields[field].initial = getattr(
                        jornada,
                        field,
                        False
                    )

            for field in fields_names:
                """
                recorre los filds a ocultar
                """
                del self.fields[field]
        else:
            for field in ["parley", "quiniela", "apuestasimple"]:
                self.fields[field].widget.attrs["class"] = "invisible"

    def clean_fechafin(self):
        fecha_ini = self.cleaned_data.get('fechaini')
        fecha_fin = self.cleaned_data.get('fechafin')
        if fecha_ini is not None:
            if fecha_ini > fecha_fin:
                raise forms.ValidationError(
                    "Debe ser mayor a la fecha de inicio"
                )
            else:
                temporadas_filter = Temporadas.objects.filter(
                    torneo=self.cleaned_data.get('torneo'),
                    fechafin__gte=fecha_ini,
                )

                if temporadas_filter.exists():
                    self._errors["torneo"] = "Ya hay temporadas creadas en el mismo rango de fechas, para esta liga."

        return fecha_fin

    def get_jornada(self, update=False):
        """Obtiene las jornadas de una temporada.

        Rertorna una jornada en caso de der una temporada afiliada un
        un torneo que no es por jornada
        """
        if not self.instance.torneo.por_jornadas:
            if hasattr(self, "cleaned_data"):
                parley = self.cleaned_data["parley"]
                quiniela = self.cleaned_data["quiniela"]
                apuestasimple = self.cleaned_data["apuestasimple"]
            else:
                parley = False
                quiniela = False
                apuestasimple = False

            try:

                try:
                    jornada = Jornadas.objects.get(
                        temporadas=self.instance,
                        sistema_id=self.view.object_sistema_juego
                    )
                except Jornadas.MultipleObjectsReturned:
                    messages.warning(
                        self.view.request,
                        "Se han detectato una actividad inusual, "
                        "esta temporada no es por jornadas, pero existen "
                        "varias registradas, dirijase a eliminarlas y solo "
                        "dejar una, o en su defecto cambiar la liga para que "
                        "sea por jornadas."
                    )
                    return None

                if update:
                    jornada.jornada = self.instance.nombre
                    jornada.status = self.instance.status
                    jornada.fechaini = self.instance.fechaini
                    jornada.fechafin = self.instance.fechafin
                    jornada.parley = parley
                    jornada.quiniela = quiniela
                    jornada.apuestasimple = apuestasimple
                    jornada.save()

            except Jornadas.DoesNotExist:
                jornada = Jornadas.objects.create(
                    jornada=self.instance.nombre,
                    status=self.instance.status,
                    temporadas=self.instance,
                    fechaini=self.instance.fechaini,
                    fechafin=self.instance.fechafin,
                    parley=parley,
                    quiniela=quiniela,
                    apuestasimple=apuestasimple,
                    sistema=self.view.object_sistema_juego
                )
            return jornada
        else:
            return None

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

        self.get_jornada(update=True)

        return self.instance


class GruposJuegoForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.all(),
        required=True,
        help_text="Seleccione un deporte para el grupo"
    )
    torneo = forms.ModelChoiceField(
        queryset=Torneos.objects.filter(por_grupos=True),
        required=True,
        help_text="Seleccione una liga para el grupo"
    )

    class Meta:
        model = GruposJuego
        fields = [
            "deporte",
            "torneo",
            "temporada",
            "nombre",
            "orden",
        ]

    def __init__(self, *args, **kwargs):
        super(GruposJuegoForm, self).__init__(*args, **kwargs)

        if self.instance.pk:
            for field in ["deporte", "torneo", "temporada"]:
                del self.fields[field]


class EquiposForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = Equipos
        fields = '__all__'


class JugadorTipoForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = JugadorTipo
        fields = '__all__'


class JugadorForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.all(),
        help_text="Seleccione un deporte para el jugador",
        required=False
    )

    class Meta:
        model = Jugador
        fields = ['deporte', 'tipo', 'nombre', 'lateralidad', 'foto']

    def __init__(self, *args, **kwargs):
        super(JugadorForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields["deporte"]
            del self.fields["tipo"]

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if not self.instance.pk:
            if Jugador.objects.filter(
                nombre=nombre,
                tipo_id=self.instance.tipo_id
            ).exists():
                raise forms.ValidationError(
                    'El nombre {0} ya se encuentra registrado para el tipo {1}'.format(nombre, self.instance.tipo)
                )
        return nombre


class EncuentrosForm(WidgetCustomizeForms, forms.ModelForm):
    deporte = forms.ModelChoiceField(
        queryset=Deportes.objects.only('pk', 'nombre').all(),
        required=True,
        help_text="Seleccione un deporte para el encuentro"
    )
    liga = forms.ModelChoiceField(
        queryset=Torneos.objects.only('pk', 'nombre').all(),
        required=True,
        help_text="Seleccione una liga para el encuentro"
    )
    temporada = forms.ModelChoiceField(
        queryset=Temporadas.objects.only('pk', 'nombre').all(),
        required=True,
        help_text="Seleccione una temporada para el encuentro"
    )
    status_old = None

    class Meta:
        model = Encuentros
        fields = [
            'deporte',
            'liga',
            'temporada',
            'jornada',
            'grupo',
            'status',
            'horajuego',
            'horacierre'
        ]

    def __init__(self, *args, **kwargs):
        super(EncuentrosForm, self).__init__(*args, **kwargs)
        self.fields["jornada"].queryset = Jornadas.objects.only('pk', 'jornada').filter(
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
            self.fields["liga"].queryset = Torneos.objects.only('pk', 'nombre').filter(
                deporte=self.view.request.POST.get('deporte')
            )
            if not self.view.request.POST.get('temporada'):
                self.fields["temporada"].queryset = Temporadas.objects.none()

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
                    jornada = Jornadas.get_or_create_or_flush(
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
                    jornada = Jornadas.get_or_create_or_flush(
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
            for deporte_grupo in Deportes_Grupos.objects.filter(
                    deporte=self.instance.jornada.temporadas.torneo.deporte
            ):
                for modalidad_grupo in deporte_grupo.grupo \
                        .modalidades_grupos_set.all():
                    if modalidad_grupo.deporte_restriccion.filter(
                        pk=self.instance.jornada.temporadas.torneo.deporte.pk
                    ).exists():
                        continue
                    encuentro_modalidad = EncuentrosModalidades.objects.get_or_create(
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
                                    jugada = Jugadas.objects.get_or_create(
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
                                jugada = Jugadas.objects.get_or_create(
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
        model = GruposApuestas
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
            Deportes_Grupos.objects.get_or_create(
                deporte=deporte,
                grupo=self.instance
            )
        for deporte in self.instance.deporte.all():
            if deporte not in self.cleaned_data["deporte"]:
                try:
                    deporte_old = Deportes_Grupos.objects.get(
                        deporte=deporte,
                        grupo=self.instance
                    )
                    deporte_old.delete()
                except Deportes_Grupos.DoesNotExist:
                    pass
        return self.instance


class ModalidadesForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = Modalidades
        fields = '__all__'
        widgets = {
            'grupo': forms.widgets.CheckboxSelectMultiple(),
            'restriction': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ModalidadesForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields["restriction"] \
                .queryset = Modalidades.objects.all().exclude(
                pk=self.instance.pk
            )

    def save(self, commit=True, *args, **kwargs):
        super(ModalidadesForm, self).save(commit=False, *args, **kwargs)

        self.instance.codename = self.instance \
            .modalidad.replace(" ", "_").lower()

        self.instance.save()

        for grupo in self.cleaned_data["grupo"]:
            """guardo"""
            Modalidades_Grupos.objects.get_or_create(
                modalidad=self.instance,
                grupo=grupo
            )

        for grupo in self.instance.grupo.all():
            if grupo not in self.cleaned_data["grupo"]:
                grupo_old = Modalidades_Grupos.objects.get(
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
        model = Modalidades_Grupos
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
        model = RestriccionesReferencias
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

        if isinstance(self.view.object, Modalidades):

            modalidad_grupos = Modalidades_Grupos.objects.filter(
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
                        existe = RestriccionesReferencias.objects.get(
                            grupo=mg.grupo,
                            deporte=gd.deporte,
                            modalidad=self.view.object
                        )
                        self.fields[name + "_min"].initial = existe.min_ref
                        self.fields[name + "_max"].initial = existe.max_ref
                    except RestriccionesReferencias.DoesNotExist:
                        pass

                    self.fields[name + "_min"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'
                    self.fields[name + "_max"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'

        elif isinstance(self.view.object, Condiciones):
            modalidad_grupos = Modalidades_Grupos.objects.filter(
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
                        existe = RestriccionesReferencias.objects.get(
                            grupo=mg.grupo,
                            deporte=gd.deporte,
                            condicion=self.view.object
                        )
                        self.fields[name + "_min"].initial = existe.min_ref
                        self.fields[name + "_max"].initial = existe.max_ref
                    except RestriccionesReferencias.DoesNotExist:
                        pass

                    self.fields[name + "_min"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'
                    self.fields[name + "_max"] \
                        .widget.attrs["pattern"] = '[0-9]+[,]?[0-9]*'

        elif isinstance(self.view.object, GruposApuestas):
            grupo_deportes = Deportes_Grupos.objects.filter(
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
                    existe = RestriccionesReferencias.objects.get(
                        grupo=self.view.object,
                        deporte=gd.deporte,
                        min_ref='logro'
                    )
                    self.fields[name + "_maxnofavorito"] \
                        .initial = existe.max_logro_no_favorito
                    self.fields[name + "_maxfavorito"] \
                        .initial = existe.max_logro_favorito
                except RestriccionesReferencias.DoesNotExist:
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
