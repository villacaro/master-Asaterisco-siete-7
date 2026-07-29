# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_comercializacion.models import (
    AgenciaDataDefault, Agencias, Bancas, Bloques, Cupos, Distribuidores, EventNotificationCadena, Operadoras,
    Porcentajes, Preferences, TaquillaDataDefault, Taquillas, TipoPorcentajes, TypePreferences, UsuariosTaquilla,
    choices_cancel_ticket, choices_frecuencia_monto_alquiler, choices_frecuencia_queda, types_notification_cadena,
)
from admin_datamart.task import ObtenerPorcentaje
from admin_juego.models import TipoProducto, SistemaJuego
from admin_lib.util_fechas import Funs as funs_dates
from admin_lib.util_forms import BaseFilterCadenaComercializacionForm, WidgetCustomizeForms
from admin_profiles.models import Direcciones, Estados, Municipios, Parroquias
from admin_status.models import Status, TaquillaStatusDetail
from admin_users.models import Users
from django import forms
from django.core.cache import cache
from django.db.models import Q
from django.forms.formsets import BaseFormSet
from django.utils.timezone import now


class ManualDeUsuario_ValidationEstra(object):

    def __init__(self, *args, **kwargs):
        super(ManualDeUsuario_ValidationEstra, self).__init__(*args, **kwargs)

        self.fields['telefono'].widget.attrs['instrucciones'] = []
        self.fields['telefono'].widget.attrs['instrucciones'].append(
            'El telefono debe contener 12 digitos.'
        )
        self.fields['telefono'].widget.attrs['instrucciones'].append(
            'Ejemplo: XXXX-XXXXXXX.'
        )

        self.fields['rif'].widget.attrs['instrucciones'] = []
        self.fields['rif'].widget.attrs['instrucciones'].append(
            'El rif debe cumplir con algunos de los siguientes formatos'
        )
        self.fields['rif'].widget.attrs['instrucciones'].append(
            'Ejemplo: R-XXXXXXXX-X.'
        )
        self.fields['rif'].widget.attrs['instrucciones'].append(
            'Donde R, puede ser: V (venezolano), J (juridido) o E (extranjero)'
        )

        self.fields['estado'].widget.attrs['instrucciones'] = []
        self.fields['estado'].widget.attrs['instrucciones'].append(
            'Para ingresar una dirección debe llenar todos los campos'
        )

        self.fields['email'].widget.attrs['instrucciones'] = []
        self.fields['email'].widget.attrs['instrucciones'].append(
            'Una dirección de correo electronica validad debe contener @'
        )
        self.fields['email'].widget.attrs['instrucciones'].append(
            'Ejemplo: example@dominio.com'
        )

    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono')

        if telefono != '' and telefono is not None:
            if len(telefono) < 12:
                raise forms.ValidationError(
                    'Asegúrese de que este valor tiene al menos 12 caracteres'
                    '(actualmente tiene ' + str(len(telefono)) + ').'
                )
            else:
                if telefono.find('-') != 4:
                    raise forms.ValidationError(
                        'Introduzca un valor valido.'
                    )
        else:
            telefono = None
        return telefono

    def clean_rif(self):
        rif = self.cleaned_data.get('rif')
        if rif != '' and rif is not None:

            if rif.find('-') >= 0:
                rif_ = rif.split('-')
                if rif_[0].isalpha() is False or rif_[1].isdigit() is False:
                    raise forms.ValidationError('Introduzca un valor valido.')
            else:
                raise forms.ValidationError('Introduzca un valor valido.')
        else:
            rif = None
        return rif

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email:
            return email
        else:
            return None


class DatosGenericosForm(forms.ModelForm):
    estado = forms.ModelChoiceField(
        help_text='Seleccione el estado de ubicación',
        required=False,
        queryset=Estados.objects.filter(
            pais__nombre='Venezuela'
        )
    )
    ciudad = forms.ChoiceField(
        label='Ciudad ',
        help_text='Seleccione la ciudad de ubicación',
        required=False,
    )
    municipio = forms.ModelChoiceField(
        help_text='Seleccione el municipio de ubicación',
        required=False,
        queryset=Municipios.objects.select_related('estado').all()
    )
    parroquia = forms.ModelChoiceField(
        help_text='Seleccione la Parroquia de ubicación',
        required=False,
        queryset=Parroquias.objects.select_related('municipio__estado').all()
    )

    direccion_ = forms.CharField(
        label='Direccion ',
        help_text='Seleccione la dirección de ubicación',
        required=False
    )

    error_messages = {
        'campo_requerido': 'El campo %(campo)s es obligatorio.',
    }

    def __init__(self, *args, **kwargs):
        super(DatosGenericosForm, self).__init__(*args, **kwargs)
        self.fields['ciudad'].choices = [('', '---------')]
        self.fields['ciudad'].choices += [(usr.pk, usr.capital) for usr in Municipios.objects.all()]
        if self.instance.direccion:
            self.fields['direccion_'].initial = self.instance.direccion.direccion
            if self.instance.direccion.parroquia:
                self.fields['parroquia'].initial = self.instance.direccion.parroquia.id

            if self.instance.direccion.municipio:
                self.fields['municipio'].initial = self.instance.direccion.municipio.id
                self.fields['ciudad'].initial = self.instance.direccion.municipio.id

            if self.instance.direccion.estado:
                self.fields['estado'].initial = self.instance.direccion.estado.id

        self.fields['status'].queryset = Status.objects.filter(
            content_type=1
        ).order_by('name')

        try:
            self.fields['status'].initial = Status.objects.filter(
                content_type=1
            ).order_by('name')[0]
        except Exception:
            pass

    def clean_nombre(self):
        nombre = self.cleaned_data.get('nombre')
        if nombre is None or nombre == '':
            return None
        else:
            return nombre.upper()

    def clean_resumen_automatic(self):
        resumen_automatic = self.cleaned_data.get('resumen_automatic')
        if self.instance.resumen_automatic != resumen_automatic:
            comercializadora = self.instance.get_comercializadora()
            profile = comercializadora.get_type_codename()
            users = Users.objects.filter(comercializadora__id=comercializadora.pk)
            for user in users:
                cache.delete("menu_{0}_{1}".format(user.pk, profile))
        return resumen_automatic

    def save(self, commit=True, *args, **kwargs):
        super(DatosGenericosForm, self).save(commit=False, *args, **kwargs)

        estado = self.cleaned_data.get('estado')
        municipio = self.cleaned_data.get('municipio')
        parroquia = self.cleaned_data.get('parroquia')
        direccions = self.cleaned_data.get('direccion_')

        if self.instance.direccion:

            self.instance.direccion.parroquia = parroquia
            self.instance.direccion.municipio = municipio
            self.instance.direccion.estado = estado
            self.instance.direccion.direccion = direccions

            self.instance.direccion.save()

        else:
            direccion = Direcciones(
                direccion=direccions,
                municipio=municipio,
                parroquia=parroquia,
                estado=estado
            )
            if not direccions and not municipio and not parroquia and not estado:
                direccion.audit_save = False
            direccion.save()

            self.instance.direccion = direccion

        self.instance.save()
        self.create_data_global()

        return self.instance

    def create_data_global(self, object=None):
        """
        Este metodo aplica los cupos y los porcentajes,
        en caso de venir el object inicializado, los datos se
        procesaran para el, o en su defecto si es nulo, para la
        instancia actual
        """

        if not object:
            object = self.instance

        object.create_data_global()


class OperadoraForm(WidgetCustomizeForms, ManualDeUsuario_ValidationEstra, DatosGenericosForm):

    crear = forms.BooleanField(
        label='¿Desea crear una cadena completa automaticamente? ',
        help_text='Si desea crear una cadena automatica marque este campo',
        required=False
    )

    class Meta:
        model = Operadoras
        fields = [
            'nombre',
            'status',
            'resumen_automatic',
            'crear',
            'rif',
            'telefono',
            'email',
            'estado',
            'ciudad',
            'municipio',
            'parroquia',
            'direccion_'
        ]

    def __init__(self, *args, **kwargs):
        super(OperadoraForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            del self.fields['crear']

    def save(self, commit=True, *args, **kwargs):
        super(OperadoraForm, self).save(commit=False, *args, **kwargs)

        self.instance.save()
        comercializadora = self.instance.get_comercializadora()
        if not SistemaJuego.objects.filter(
                comercializadora=comercializadora
        ).exists():
            SistemaJuego.objects.create(
                comercializadora=self.instance.get_comercializadora(),
                nombre=self.instance.nombre
            )

        if self.cleaned_data.get('crear'):

            # ###BLOQUE####
            bloque = Bloques.objects.create(
                nombre='Bloque ' + self.instance.nombre,
                operadora=self.instance,
                status=self.instance.status
            )
            self.create_data_global(object=bloque)

            # ###BANCA####
            banca = Bancas.objects.create(
                nombre='Banca ' + self.instance.nombre,
                bloque=bloque,
                status=self.instance.status
            )
            self.create_data_global(object=banca)

            # ###DISTRIBUIDOR####
            distribuidor = Distribuidores.objects.create(
                nombre='Distribuidor ' + self.instance.nombre,
                banca=banca,
                status=self.instance.status
            )
            self.create_data_global(object=distribuidor)
            # ###AGENCIA####
            if AgenciaDataDefault.objects.all().exists():
                agencia = Agencias.objects.create(
                    nombre='Agencia ' + self.instance.nombre,
                    status=self.instance.status,
                    distribuidores=distribuidor,
                    num_taquillas=0,
                )
                self.create_data_global(object=agencia)

        return self.instance


class BloqueForm(WidgetCustomizeForms, ManualDeUsuario_ValidationEstra, DatosGenericosForm):

    class Meta:
        model = Bloques
        fields = [
            'nombre',
            'status',
            'resumen_automatic',
            'is_sistema_juego',
            'is_resultados',
            'permissions_create_user',
            'rif',
            'telefono',
            'email',
            'estado',
            'ciudad',
            'municipio',
            'parroquia',
            'direccion_'
        ]

    def __init__(self, *args, **kwargs):
        super(BloqueForm, self).__init__(*args, **kwargs)
        # self.fields['permissions_create_user'].widget.attrs['checked'] = 'checked'

    def clean(self):
        data = self.cleaned_data

        if not self.instance.operadora:

            self.instance.operadora = self.view.object_sistema_juego.comercializadora.get_object()

            if Bloques.objects.filter(
                    nombre=data['nombre'],
                    operadora=self.instance.operadora
            ).exists():
                raise forms.ValidationError(
                    'Ya se encuentra una multi banca registrada con dicho nombre'
                )
        else:
            if Bloques.objects.filter(
                    nombre=data.get('nombre'),
                    operadora=self.instance.operadora
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra una multi banca registrada con dicho nombre'
                )

        return data

    def save(self, commit=True, *args, **kwargs):
        super(BloqueForm, self).save(commit=True, *args, **kwargs)
        self.create_data_global()
        self.instance.save_sistema_juego()
        return self.instance


class BancaForm(WidgetCustomizeForms, ManualDeUsuario_ValidationEstra, DatosGenericosForm):

    class Meta:
        model = Bancas
        fields = [
            'bloque',
            'nombre',
            'status',
            'modelo_negocio',
            'resumen_automatic',
            'is_sistema_juego',
            'is_resultados',
            'permissions_create_user',
            'rif',
            'telefono',
            'email',
            'estado',
            'ciudad',
            'municipio',
            'parroquia',
            'direccion_'
        ]

    def __init__(self, *args, **kwargs):
        super(BancaForm, self).__init__(*args, **kwargs)
        # self.fields['permissions_create_user'].widget.attrs['checked'] = 'checked'

        if self.instance.pk:
            if 'bloque' in self.fields:
                del self.fields['bloque']
            del self.fields['modelo_negocio']
        else:

            if self.view.get_profile().codename == 'userprofile_operadora':
                self.fields['bloque'].queryset = Bloques.objects.filter(
                    operadora=self.view.object_comercializadora.get_object()
                )

            else:
                if 'bloque' in self.fields:
                    del self.fields['bloque']

    def clean(self):
        data = self.cleaned_data

        if not self.instance.bloque:

            if self.view.get_profile().codename == 'userprofile_bloque':
                data['bloque'] = self.view.object_comercializadora.get_object()

            bloque = data.get('bloque')
            if not bloque:
                raise forms.ValidationError(
                    self.error_messages['campo_requerido'],
                    code='campo_requerido',
                    params={'campo': 'Bloque', },
                )

            if Bancas.objects.filter(
                nombre=data['nombre'],
                bloque=data['bloque']
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra una banca registrada con dicho nombre'
                )
        else:
            if Bancas.objects.filter(
                nombre=data.get('nombre'),
                bloque=self.instance.bloque
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra una banca registrada con dicho nombre'
                )

        return data

    def save(self, commit=True, *args, **kwargs):

        super(BancaForm, self).save(commit=False, *args, **kwargs)

        self.instance.save()
        self.create_data_global()

        self.instance.save_sistema_juego()

        return self.instance


class DistribuidorForm(
        WidgetCustomizeForms, BaseFilterCadenaComercializacionForm,
        ManualDeUsuario_ValidationEstra, DatosGenericosForm):

    class Meta:
        model = Distribuidores
        fields = [
            'bloque',
            'banca',
            'nombre',
            'status',
            'resumen_automatic',
            'rif',
            'telefono',
            'email',
            'estado',
            'ciudad',
            'municipio',
            'parroquia',
            'direccion_'
        ]

    def __init__(self, *args, **kwargs):
        super(DistribuidorForm, self).__init__(*args, **kwargs)

        del self.fields['distribuidor']

        if self.instance.pk:
            if 'bloque' in self.fields:
                del self.fields['bloque']
            if 'banca' in self.fields:
                del self.fields['banca']
        else:
            if 'banca' in self.fields:
                self.fields['banca'].label += ' (*)'
                self.fields['banca'].required = True

    def clean(self):
        data = self.cleaned_data

        if not self.instance.banca:
            if self.view.get_profile().codename == 'userprofile_banca':
                data['banca'] = self.view.object_comercializadora.get_object()

            banca = data.get('banca')
            if not banca:
                raise forms.ValidationError(
                    self.error_messages['campo_requerido'],
                    code='campo_requerido',
                    params={'campo': 'Banca', },
                )

            if Distribuidores.objects.filter(
                nombre=data['nombre'],
                banca=data['banca']
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra un distribuidor registrado con dicho nombre'
                )
        else:
            if Distribuidores.objects.filter(
                nombre=data.get('nombre'),
                banca=self.instance.banca
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra un distribuidor registrado con dicho nombre'
                )

        return data

    def save(self, commit=True, *args, **kwargs):
        super(DistribuidorForm, self).save(commit=False, *args, **kwargs)

        self.instance.save()
        self.create_data_global()

        return self.instance


class AgenciaForm(
        WidgetCustomizeForms, BaseFilterCadenaComercializacionForm,
        ManualDeUsuario_ValidationEstra, DatosGenericosForm):

    create = True
    taquilla_master_check = forms.BooleanField(
        label='¿Crear taquilla master ? ',
        help_text='Seleccione si desea crear la taquilla master para ese sitema',
        required=False,
    )
    num_taquillas = forms.ChoiceField(
        label='Número de taquillas (*) ',
        help_text='Seleccione el numero de taquillas que desea crear automaticamente',
        required=True,
    )

    class Meta:
        model = Agencias
        fields = [
            'bloque',
            'banca',
            'distribuidor',
            'num_taquillas',
            'taquilla_master_check',
            'nombre',
            'status',
            'codigo',
            'resumen_automatic',
            'rif',
            'telefono',
            'email',
            'estado',
            'ciudad',
            'municipio',
            'parroquia',
            'direccion_'
        ]

    def __init__(self, *args, **kwargs):

        super(AgenciaForm, self).__init__(*args, **kwargs)

        del self.fields['agencia']

        if self.instance.pk:
            self.create = False
            if 'bloque' in self.fields:
                del self.fields['bloque']
            if 'banca' in self.fields:
                del self.fields['banca']
            if 'distribuidor' in self.fields:
                del self.fields['distribuidor']
            del self.fields['num_taquillas']
            del self.fields['taquilla_master_check']

        else:
            if 'distribuidor' in self.fields:
                self.fields['distribuidor'].label += ' (*)'
                self.fields['distribuidor'].required = True

            choices_num_taquillas = []
            for i in range(0, 4):
                nuevo = []
                nuevo.append(i)
                nuevo.append(str(i) + ' taquilla(s)')
                choices_num_taquillas.append(nuevo)
            self.fields['num_taquillas'].choices = choices_num_taquillas
            self.fields['num_taquillas'].widget.attrs['class'] = 'select-chosen'
            self.fields['num_taquillas'].widget.attrs['data-placeholder'] = '...'
            self.fields['taquilla_master_check'].widget.attrs['disabled'] = 'disabled'

    def clean(self):
        data = self.cleaned_data

        if not self.instance.distribuidores:
            if self.view.get_profile().codename == 'userprofile_distribuidor':
                data['distribuidor'] = self.view.object_comercializadora.get_object()

            """
            Como en la agencia el campo de distribuidor
            se llama es distribuidores lo copiamos
            """
            data['distribuidores'] = data.get('distribuidor')

            distribuidor = self.data.get('distribuidor')
            if not distribuidor:
                if self.view.get_profile().codename != 'userprofile_distribuidor':
                    raise forms.ValidationError(
                        self.error_messages['campo_requerido'],
                        code='campo_requerido',
                        params={'campo': 'Distribuidor', },
                    )

            if Agencias.objects.filter(
                nombre=data['nombre'],
                distribuidores=data['distribuidor']
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra un centro de apuesta registrado con dicho nombre'
                )

            self.instance.distribuidores = data.get('distribuidor')

        else:
            if Agencias.objects.filter(
                nombre=data.get('nombre'),
                distribuidores=self.instance.distribuidores
            ).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(
                    'Ya se encuentra un centro de apuesta registrado con dicho nombre'
                )

        return data

    def save(self, commit=True, *args, **kwargs):
        modo_alquiler = False
        if (self.instance.distribuidores.banca
                .modelo_negocio_codenames['codename_negocio_alquiler'] ==
                self.instance.distribuidores.banca.modelo_negocio):
            modo_alquiler = True
        super(AgenciaForm, self).save(commit=False, *args, **kwargs)

        if self.create:
            taquilla_default = TaquillaDataDefault.objects.all()
            if taquilla_default.exists():
                taquilla_default = taquilla_default[0]

                is_master = True
                for x in range(1, int(self.instance.num_taquillas) + 1):
                    taquilla = Taquillas.objects.create(
                        taquilla='Taquilla ' + str(x),
                        agencia=self.instance,
                        modo_alquiler=modo_alquiler,
                        is_taquilla_master=is_master
                    )

                    if x == 1 and self.cleaned_data.get('taquilla_master_check'):
                        is_master = False

                    taquilla.create_comercializadora_and_dimension()

                    usuariotaquilla = UsuariosTaquilla(
                        user=taquilla_default.user_name + str(x),
                        taquilla=taquilla
                    )

                    usuariotaquilla.set_password(taquilla_default.passwd)
                    usuariotaquilla.save()

                    TaquillaStatusDetail.objects.create(
                        usuariotaquilla=usuariotaquilla,
                        startdate=now(),
                        status=Status.get_status_by_codename(codename='status_instalacion')
                    )

        self.create_data_global()
        return self.instance


class TaquillaForm(
        WidgetCustomizeForms, BaseFilterCadenaComercializacionForm, forms.ModelForm):

    num_taquilla = forms.IntegerField(
        label='Agregar taquilla # (*)',
        help_text='Numero consecutivo generado automáticamente'
    )

    class Meta:
        model = Taquillas
        fields = [
            'bloque',
            'banca',
            'distribuidor',
            'agencia',
            'num_taquilla',
            'is_taquilla_master',
        ]

    def __init__(self, *args, **kwargs):
        super(TaquillaForm, self).__init__(*args, **kwargs)
        self.fields['num_taquilla'].widget.attrs['readonly'] = ''

        if 'agencia' in self.fields:
            self.fields['agencia'].label += ' (*)'
            self.fields['agencia'].required = True

    def save(self, commit=True, *args, **kwargs):

        if not self.instance.agencia:
            if self.view.get_profile().codename == 'userprofile_agencia':
                self.instance.agencia = self.view.object_comercializadora.get_object()

        if not self.instance.pk:
            if (self.instance.agencia.distribuidores.banca.
                    modelo_negocio_codenames['codename_negocio_alquiler'] ==
                    self.instance.agencia.distribuidores.banca.modelo_negocio):
                    # crea taquilla en modo alquiler
                self.instance.modo_alquiler = True

        super(TaquillaForm, self).save(commit=False, *args, **kwargs)

        self.instance.taquilla = 'Taquilla {0}'.format(
            self.cleaned_data['num_taquilla']
        )
        self.instance.save()
        self.instance.create_comercializadora_and_dimension()

        taquilla_default = TaquillaDataDefault.objects.all()[0]

        status = Status.get_status_by_codename(codename='status_instalacion')
        usuariotaquilla = UsuariosTaquilla.objects.create(
            user='{0}{1}'.format(
                taquilla_default.user_name,
                self.cleaned_data['num_taquilla'],
            ),
            status=status,
            taquilla=self.instance
        )

        TaquillaStatusDetail.objects.create(
            usuariotaquilla=usuariotaquilla,
            startdate=now(),
            status=status
        )

        usuariotaquilla.set_password(taquilla_default.passwd)
        usuariotaquilla.save()

        self.instance.agencia.num_taquillas = self.cleaned_data['num_taquilla']
        self.instance.agencia.save()

        return self.instance


class UpdateTaquillaForm(WidgetCustomizeForms, forms.ModelForm):
    status = forms.ModelChoiceField(
        help_text='Seleccione un estatus para la taquilla',
        required=False,
        queryset=Status.objects.filter(
            Q(content_type=3) | Q(codename='status_bloqueado')
        ).exclude(
            codename='status_instalacion'
        )
    )
    user = forms.CharField(
        label='Usuario (*)',
        help_text='Usuario, este campo no se puede editar'
    )

    class Meta:
        model = Taquillas
        fields = [
            'user',
            'status',
            'is_taquilla_master',
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateTaquillaForm, self).__init__(*args, **kwargs)

        self.usuariotaquilla = self.instance.get_user()
        self.fields['status'].initial = self.usuariotaquilla.get_status()

        self.fields['user'].widget.attrs['readonly'] = True
        self.fields['user'].initial = self.usuariotaquilla

        self.is_taquilla_master = self.instance.is_taquilla_master
        if not self.instance.modo_alquiler:
            pass
        else:
            if self.view.get_profile().codename != 'userprofile_operadora':
                pass

    def save(self, commit=True, *args, **kwargs):
        super(UpdateTaquillaForm, self).save(commit=False, *args, **kwargs)

        if self.is_taquilla_master != self.instance.is_taquilla_master:
            # Lanza la notificacion unicamente cuando cambia
            EventNotificationCadena.objects.create(
                **{
                    'taquilla': self.instance.pk,
                    'data_origin': types_notification_cadena['preferencia'][0],
                    'data': {
                        'master': 1 if self.instance.is_taquilla_master else 0
                    }
                }
            )

        self.instance.save()
        status_old = self.usuariotaquilla.get_status()

        if self.cleaned_data['status']:
            if status_old.pk != self.cleaned_data['status'].pk:

                self.usuariotaquilla.taquillastatusdetail_set.filter(
                    enddate=None
                ).update(enddate=now())

                status_new = TaquillaStatusDetail.objects.create(
                    usuariotaquilla=self.usuariotaquilla,
                    status=self.cleaned_data['status'],
                    startdate=now()
                )
                self.usuariotaquilla.status = self.cleaned_data['status']

                if status_new.status.codename == 'status_reinstalacion':
                    taquilla_default = TaquillaDataDefault.objects.all()[0]
                    self.usuariotaquilla.set_password(taquilla_default.passwd)
                    self.usuariotaquilla.save(update_fields=['password', 'status', 'updated_at'])
                else:
                    self.usuariotaquilla.save(update_fields=['status', 'updated_at'])

        return self.instance


class CuposForm(WidgetCustomizeForms, forms.ModelForm):
    label = forms.CharField()

    class Meta:
        model = Cupos
        fields = [
            'label',
            'monto_diario',
            'monto_premio'
        ]

    def __init__(self, *args, **kwargs):
        super(CuposForm, self).__init__(*args, **kwargs)

        if self.instance is not None:
            self.fields['label'].widget.attrs['readonly'] = True
            self.object = self.instance.get_object()
            self.fields['label'].initial = self.object
            self.fields['label'].label = self.object.get_verbose_name()
        else:
            self.object = None

    def get_monto_maximo(self, get):
        if self.object:
            kwargs = {}
            origen = self.object.get_origen()
            if origen:
                kwargs[origen.user_type_codename.split('_')[1]] = origen
                kwargs['fecha_fin'] = None
                cupo_origen = Cupos.objects.filter(**kwargs)
                if cupo_origen.exists():
                    if get == 'venta':
                        return cupo_origen[0].monto_diario
                    elif get == 'premio':
                        return cupo_origen[0].monto_premio
        return None

    def clean_monto_diario(self):
        monto_diario = self.cleaned_data.get('monto_diario')
        montomax = self.get_monto_maximo('venta')
        if montomax:
            if montomax < monto_diario:
                raise forms.ValidationError(
                    'El cupo ingresado debe ser menor o igual a {0}'.format(montomax)
                )

        return monto_diario

    def clean_monto_premio(self):
        monto_premio = self.cleaned_data.get('monto_premio')
        montomax = self.get_monto_maximo('premio')
        if montomax:
            if montomax < monto_premio:
                raise forms.ValidationError(
                    'El cupo ingresado debe ser menor o igual a {0}'.format(montomax)
                )

        return monto_premio

    def save(self, commit=False, *args, **kwargs):
        self.instance.fecha_fin = now()
        self.instance.save(update_fields=['fecha_fin', 'updated_at'])

        kwargs = {}
        kwargs[self.instance.get_object().prefix_filter] = self.instance.get_object()
        kwargs['fecha_inicio'] = now()
        kwargs['monto_diario'] = self.cleaned_data['monto_diario']
        kwargs['monto_premio'] = self.cleaned_data['monto_premio']

        cupo = Cupos(
            **kwargs
        )
        cupo.audit_save = False
        cupo.save()

        return self.instance


class UpdatePorcentajeForm(WidgetCustomizeForms, forms.Form):

    def __init__(self, *args, **kwargs):
        super(UpdatePorcentajeForm, self).__init__(*args, **kwargs)

        self.object = self.view.get_object()

        self.fields['form_object'] = forms.CharField(
            required=False,
            max_length=140,
            initial=self.object,
            label=self.object.get_verbose_name()
        )

        self.fields['form_object'].widget.attrs['readonly'] = 'True'
        validation_num_porcentaje = '[0-9]+[,]?[0-9]*'
        # Saco el tipo de cadena
        ptype = self.object.get_class_name()
        if ptype == 'bloques':
            bloques = Porcentajes.objects.filter(
                bloque=self.object,
                fecha_fin=None
            )
            bancas = None
            distribuidores = None
            agencias = None
            sucesor = bloques
        elif ptype == 'bancas':
            bancas = Porcentajes.objects.filter(
                banca=self.object,
                fecha_fin=None
            )
            bloques = Porcentajes.objects.filter(
                bloque=self.object.bloque,
                fecha_fin=None
            )
            distribuidores = None
            agencias = None
            sucesor = bancas
        elif ptype == 'distribuidores':
            bloques = Porcentajes.objects.filter(
                bloque=self.object.banca.bloque,
                fecha_fin=None
            )
            bancas = Porcentajes.objects.filter(
                banca=self.object.banca,
                fecha_fin=None
            )
            distribuidores = Porcentajes.objects.filter(
                distribuidor=self.object,
                fecha_fin=None
            )
            agencias = None
            sucesor = distribuidores
        elif ptype == 'agencias':
            bloques = Porcentajes.objects.filter(
                bloque=self.object.distribuidores.banca.bloque,
                fecha_fin=None
            )
            bancas = Porcentajes.objects.filter(
                banca=self.object.distribuidores.banca,
                fecha_fin=None
            )
            distribuidores = Porcentajes.objects.filter(
                distribuidor=self.object.distribuidores,
                fecha_fin=None
            )
            agencias = Porcentajes.objects.filter(
                agencia=self.object,
                fecha_fin=None
            )
            sucesor = agencias

        for porcentaje in self.get_porcentajes_types():

            if sucesor.filter(tipo=porcentaje).exists():
                porcentaje_value = sucesor.get(tipo=porcentaje)
            else:
                porcentaje_value = None

            if ptype != 'bloques':
                self.fields['max_' + porcentaje.codename] = forms.DecimalField(
                    required=False,
                    min_value=0,
                    max_value=100,
                    decimal_places=1,
                    localize=True,
                    label='%'
                )

                if sucesor.filter(tipo=porcentaje).exists():
                    self.fields['max_' + porcentaje.codename].initial = sucesor.get(
                        tipo=porcentaje
                    ).get_porcentaje_maximo_float()
                else:
                    self.fields['max_' + porcentaje.codename].initial = '0'
                self.fields['max_' + porcentaje.codename].widget.attrs['readonly'] = 'True'

            if bloques is not None:
                self.fields['bloques_' + porcentaje.codename] = forms.DecimalField(
                    required=False,
                    min_value=0,
                    max_value=100,
                    decimal_places=1,
                    localize=True,
                    label='%',
                    help_text='Asignar porcentaje de ' + str(porcentaje.nombre)
                )

                if ptype == 'bloques':
                    if bloques.filter(tipo=porcentaje).exists():
                        self.fields['bloques_' + porcentaje.codename].initial = bloques.get(
                            tipo=porcentaje
                        ).get_porcentaje_float()

                    self.fields[
                        'bloques_' + porcentaje.codename].widget.attrs['pattern'] = validation_num_porcentaje
                    self.fields['bloques_' + porcentaje.codename].required = True

                else:
                    if porcentaje_value:
                        self.fields['bloques_' +
                                    porcentaje.codename].initial = porcentaje_value.get_bloque_porc()
                        self.fields['bloques_' +
                                    porcentaje.codename].widget.attrs['readonly'] = 'True'

            if bancas is not None:
                self.fields['bancas_' + porcentaje.codename] = forms.DecimalField(
                    required=False,
                    min_value=0,
                    max_value=100,
                    decimal_places=1,
                    localize=True,
                    label='%',
                    help_text='Asignar porcentaje de ' + str(porcentaje.nombre)
                )
                if porcentaje.codename == 'porcentaje_comision':
                    self.fields['bancas_' + porcentaje.codename + '_relacion'] = forms.BooleanField(
                        help_text='Relación entre el padre en ' + str(porcentaje.nombre),
                        required=False
                    )

                    self.fields['bancas_' + porcentaje.codename + '_relacion'].widget.attrs['title'] = \
                        self.fields['bancas_' + porcentaje.codename + '_relacion'].help_text

                if ptype == 'bancas':
                    if bancas.filter(tipo=porcentaje).exists():
                        self.fields['bancas_' + porcentaje.codename] \
                            .initial = bancas.get(tipo=porcentaje).get_porcentaje_float()
                        if porcentaje.codename == 'porcentaje_comision':
                            self.fields['bancas_' + porcentaje.codename + '_relacion'].initial = \
                                bancas.get(tipo=porcentaje).relacion

                    self.fields[
                        'bancas_' + porcentaje.codename].widget.attrs['pattern'] = validation_num_porcentaje
                    self.fields['bancas_' + porcentaje.codename].required = True

                else:
                    if porcentaje_value:
                        self.fields['bancas_' +
                                    porcentaje.codename].initial = porcentaje_value.get_banca_porc()
                        self.fields['bancas_' +
                                    porcentaje.codename].widget.attrs['readonly'] = 'True'
                        if porcentaje.codename == 'porcentaje_comision':
                            self.fields['bancas_' + porcentaje.codename +
                                        '_relacion'].initial = porcentaje_value.relacion
                            self.fields['bancas_' + porcentaje.codename +
                                        '_relacion'].widget.attrs['disabled'] = 'disabled'

            if distribuidores is not None:
                self.fields['distribuidores_' + porcentaje.codename] = forms.DecimalField(
                    required=False,
                    min_value=0,
                    max_value=100,
                    decimal_places=1,
                    localize=True,
                    label='%',
                    help_text='Asignar porcentaje de ' + str(porcentaje.nombre)
                )

                if porcentaje.codename == 'porcentaje_comision':
                    self.fields['distribuidores_' + porcentaje.codename + '_relacion'] = forms.BooleanField(
                        help_text='Relación entre el padre en ' + str(porcentaje.nombre),
                        required=False
                    )

                    self.fields['distribuidores_' + porcentaje.codename + '_relacion'].widget.attrs['title'] = \
                        self.fields['distribuidores_' + porcentaje.codename + '_relacion'].help_text

                if ptype == 'distribuidores':
                    if distribuidores.filter(tipo=porcentaje).exists():
                        self.fields['distribuidores_' + porcentaje.codename].initial = \
                            distribuidores.get(tipo=porcentaje).get_porcentaje_float()
                        if porcentaje.codename == 'porcentaje_comision':
                            self.fields['distribuidores_' + porcentaje.codename + '_relacion'].initial = \
                                distribuidores.get(tipo=porcentaje).relacion

                    self.fields['distribuidores_' +
                                porcentaje.codename].widget.attrs['pattern'] = validation_num_porcentaje
                    self.fields['distribuidores_' + porcentaje.codename].required = True

                else:
                    if porcentaje_value:
                        self.fields[
                            'distribuidores_' + porcentaje.codename].initial = porcentaje_value.get_distribuidor_porc()
                        self.fields['distribuidores_' +
                                    porcentaje.codename].widget.attrs['readonly'] = 'True'
                        if porcentaje.codename == 'porcentaje_comision':
                            self.fields['distribuidores_' + porcentaje.codename +
                                        '_relacion'].initial = porcentaje_value.relacion
                            self.fields['distribuidores_' + porcentaje.codename +
                                        '_relacion'].widget.attrs['disabled'] = 'disabled'

            if agencias is not None:
                self.fields['agencias_' + porcentaje.codename] = forms.DecimalField(
                    required=False,
                    min_value=0,
                    max_value=100,
                    decimal_places=1,
                    localize=True,
                    label='%',
                    help_text='Asignar porcentaje de ' + str(porcentaje.nombre)
                )

                if agencias.filter(tipo=porcentaje).exists():
                    self.fields['agencias_' + porcentaje.codename].initial = \
                        agencias.get(tipo=porcentaje).get_porcentaje_float()

                self.fields['agencias_' +
                            porcentaje.codename].widget.attrs['pattern'] = validation_num_porcentaje
                self.fields['agencias_' + porcentaje.codename].required = True

    def get_porcentajes_types(self):
        return TipoPorcentajes.objects.all().order_by('orden')

    def get_porcentaje_arriba(self, object_, tipo, ptype):
        if ptype == 'bancas':
            return round(object_.get(tipo=tipo).bloque_porc * 100, 1)
        if ptype == 'distribuidores':
            return round(object_.get(tipo=tipo).banca_porc * 100, 1)
        if ptype == 'agencias':
            return round(object_.get(tipo=tipo).distribuidor_porc * 100, 1)
        return 0


class FactorRiesgoRowForm(WidgetCustomizeForms, forms.Form):
    porcentaje = forms.DecimalField(
        label=' ',
        help_text='Factor aplicado a la regla',
        required=False,
        min_value=0,
    )

    def __init__(self, *args, **kwargs):
        super(FactorRiesgoRowForm, self).__init__(*args, **kwargs)
        """Se Generan de esta forma para poder hacer los min y mas dinamicos"""

        min_value = 1
        max_value = 9999

        origen = self.object_comer.get_object()
        min_value = float(origen.get_preference_value_by_codename('preference_amount_min'))
        max_value = float(origen.get_preference_value_by_codename('preference_amount_max'))

        self.fields['rango_inicial'] = forms.DecimalField(
            label='Min ',
            help_text='Rango inicial para la regla',
            required=False,
            min_value=min_value,
            max_value=max_value,
        )
        self.fields['rango_final'] = forms.DecimalField(
            label='Max ',
            help_text='Rango final para la regla',
            required=False,
            min_value=min_value,
            max_value=max_value,
        )


class FactorRiesgoForm(BaseFormSet):

    def clean(self):
        super(FactorRiesgoForm, self).clean()
        for form in self.forms:

            procesar = True
            no_value = 0
            for label in ['rango_inicial', 'rango_final', 'porcentaje']:
                if not form.cleaned_data.get(label):
                    no_value += 1
                    procesar = False

            if no_value < 3:
                for label in ['rango_inicial', 'rango_final', 'porcentaje']:
                    if not form.cleaned_data.get(label):
                        form._errors[label] = 'Este campo es obligatorio.'
                        procesar = False

            if procesar:
                rango_inicial = form.cleaned_data.get('rango_inicial')
                rango_final = form.cleaned_data.get('rango_final')

                if rango_inicial and rango_final:
                    if rango_inicial > rango_final:
                        form._errors['rango_inicial'] = 'El rango inicial debe ser menor al final.'

                for form_2 in self.forms:
                    if (form.prefix != form_2.prefix):
                        rango_inicial_2 = form_2.cleaned_data.get('rango_inicial')
                        if rango_inicial_2:
                            if (rango_inicial_2 >= rango_inicial and
                                    rango_inicial_2 <= rango_final):
                                form_2._errors['rango_inicial'] = 'Rangos en conflicto'
                                form_2._errors['rango_final'] = 'Rangos en conflicto'
                                form._errors['rango_inicial'] = 'Rangos en conflicto'
                                form._errors['rango_final'] = 'Rangos en conflicto'


class PermissionsSalesForm(WidgetCustomizeForms, forms.Form):
    nombre = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(PermissionsSalesForm, self).__init__(*args, **kwargs)
        self.object = self.view.get_object()
        comercializadora = self.object.get_comercializadora()

        self.fields['nombre'].initial = self.object
        self.fields['nombre'].label = self.object.get_verbose_name()
        self.fields['nombre'].widget.attrs['readonly'] = True

        deportes = TipoProducto.objects.only('pk', 'nombre').all().order_by('orden')
        for deporte in deportes:
            self.fields[str(deporte.pk)] = forms.BooleanField(label=deporte.nombre, required=False)

            if comercializadora.get_permissions_sales(deporte.id):
                pass
            else:
                self.fields[str(deporte.pk)].widget.attrs['checked'] = 'checked'
            self.fields[str(deporte.pk)].widget.attrs['class'] = 'deportes'


class PermissionsSalesRestrictionsForm(WidgetCustomizeForms, forms.Form):
    deporte = forms.ModelChoiceField(
        required=True,
        queryset=TipoProducto.objects.all().only('nombre'),
        empty_label='Seleccione un deporte'
    )


class PreferencesForm(WidgetCustomizeForms, forms.Form):

    def __init__(self, *args, **kwargs):
        group = None
        if kwargs.get('group'):
            group = kwargs.pop('group')
        super(PreferencesForm, self).__init__(*args, **kwargs)
        from admin_comercializacion.views.preferencias_views import validate_model_bussiness

        self.object = self.view.get_object()
        self.comercializadora = self.object.get_comercializadora()
        self.type = self.object.user_type_codename
        self.distribute = False
        self.heredity = False
        self.divide = 2
        if self.type == 'userprofile_distribuidor':
            self.distribute = True
            self.divide = 3

        # Si no hay un grupo evalua todas las preferencias
        if group:
            preferences = TypePreferences.objects.filter(
                group_id=group.id,
            ).order_by('order').only('name', 'codename', 'edit', 'comparison', 'type_data', 'distribute')
            # Si es el formulario de finanzas, verifica los modelos de negocio
            if group.codename == 'group_finance':
                preferences = validate_model_bussiness(self.object, preferences)
        else:
            preferences = TypePreferences.objects.all()\
                .order_by('order')\
                .only('name', 'codename', 'edit', 'comparison', 'type_data', 'distribute')
            preferences = validate_model_bussiness(self.object, preferences)
        ################################################

        # Se recorren las preferencias para armar el formulario
        for preference in preferences:
            # Excluye las preferencias que no tengan el permiso de comercializacion
            if self.type not in preference.profile.all().values_list('codename', flat=True):
                continue

            # Creacion del campo del formulario de la preferencia
            if preference.edit:
                self.fields[preference.codename] = forms.CharField(
                    label=preference.name + ' ',
                    required=False
                )
            else:
                choices = []
                if preference.codename == 'preference_amount_rental_frequency':
                    choices = choices_frecuencia_monto_alquiler
                elif preference.codename == 'preference_queda_frequency':
                    choices = choices_frecuencia_queda
                elif preference.codename == 'preference_cancel_ticket':
                    choices = choices_cancel_ticket

                self.fields[preference.codename] = forms.ChoiceField(
                    label=preference.name + ' ',
                    required=False,
                    choices=choices,
                )

                self.fields[preference.codename].widget.attrs['class'] = 'select-chosen'
                self.fields[preference.codename].widget.attrs['data-placeholder'] = '...'

            self.fields[preference.codename].widget.attrs['disabled'] = True
            self.fields[preference.codename].initial = self.get_value_initial(preference)

            # Si es una preferencia distribuible y esta en el nivel distribuidor
            if self.type == 'userprofile_distribuidor':
                self.fields['distribute-' + preference.codename] = forms.BooleanField(
                    required=False
                )
                if preference.distribute is False:
                    self.fields['distribute-' + preference.codename].widget = forms.HiddenInput()
                else:
                    self.fields['distribute-' +
                                preference.codename].initial = self.get_value_distribute(preference)
                    self.fields['distribute-' +
                                preference.codename].widget.attrs['class'] = 'distribute'
                self.fields['distribute-' + preference.codename].widget.attrs['disabled'] = True

            # Creacion del campo de la herencia
            self.fields['heredity-' + preference.codename] = forms.BooleanField(
                required=False
            )
            if preference.heredity is False:
                self.fields['heredity-' + preference.codename].widget = forms.HiddenInput()
            else:
                self.heredity = True
                self.fields['heredity-' + preference.codename].initial = preference.heredity
            self.fields['heredity-' + preference.codename].widget.attrs['disabled'] = True

            # Creacion del campo de edicion de la preferencia
            self.fields[preference.codename + '.'] = forms.BooleanField(
                required=False
            )
            self.fields[preference.codename + '.'].widget.attrs['onchange'] = 'HabilitarDesabilitar("{0}")'.format(
                preference.codename
            )
            self.fields[preference.codename + '.'].widget.attrs['id'] = preference.codename

    def get_value_initial(self, preference):
        """
            Lectura del valor inicial de la preferencia
        """
        value = self.object.get_preference_value_by_codename(preference.codename)

        if preference.comparison != TypePreferences.comparison_codenames['codename_free']:
            if preference.type_data == TypePreferences.comparison_type['codename_decimal']:
                return self.view.get_encode_valor(value)
            elif preference.type_data == TypePreferences.comparison_type['codename_int']:
                return int(Decimal(value))
        else:
            return value

    def get_value_distribute(self, preference):
        preference_comer = Preferences.objects.only('distribute').filter(
            comercializacion_id=self.comercializadora,
            typepreference_id=preference.id
        )

        if preference_comer:
            return preference_comer[0].distribute
        else:
            return False

    def clean(self):
        cleaned_data = super(PreferencesForm, self).clean()

        participacion_porc = ObtenerPorcentaje(
            codename='porcentaje_participacion',
            cadena=self.object,
            fecha=now()
        )
        libre = True if participacion_porc == 1 else False

        for item in cleaned_data:
            if '.' in item or 'distribute' in item:
                continue

            if cleaned_data.get('{0}.'.format(item)) is True:
                if cleaned_data.get(item):
                    self.fields[item].initial = cleaned_data.get(item)
                    preference = TypePreferences.objects.get(codename=item)

                    # Checkeo del tipo de dato de la preferencia
                    if preference.type_data == TypePreferences.comparison_type['codename_decimal']:
                        value = self.view.check_decimal(cleaned_data.get(item))
                    elif preference.type_data == TypePreferences.comparison_type['codename_int']:
                        value = self.view.check_int(cleaned_data.get(item))
                    else:
                        value = cleaned_data.get(item)

                    if item == 'preference_queda_frequency':
                        old_value = self.get_value_initial(preference)
                        if old_value != value:
                            raise_disable = False
                            raise_message = ''
                            if old_value == 'frecuencia_semanal':
                                raise_disable = funs_dates.is_first_week_of_month()
                                raise_message = 'la primera semana del mes'
                            elif old_value == 'frecuencia_quincenal':
                                if value == 'frecuencia_semanal':
                                    raise_disable = funs_dates.is_first_week_of_fortnight()
                                    raise_message = 'la primera semana de la quincena'
                                elif value == 'frecuencia_mensual':
                                    raise_disable = funs_dates.is_first_fortnight_of_month()
                                    raise_message = 'la primera quincena del mes'
                            elif old_value == 'frecuencia_mensual':
                                if value == 'frecuencia_semanal':
                                    raise_disable = funs_dates.is_first_week_of_month()
                                    raise_message = 'la primera semana del mes'
                                elif value == 'frecuencia_quincenal':
                                    raise_disable = funs_dates.is_first_fortnight_of_month()
                                    raise_message = 'la primera quincena del mes'

                            if raise_disable is False:
                                self._errors[item] = self.error_class(
                                    [
                                        'Este campo, solo puede editarse en {}'.format(raise_message)
                                    ]
                                )

                    # Si en el checkeo devolvio otro tipo de dato, continua con las validaciones
                    if isinstance(value, str) \
                            and preference.type_data != TypePreferences.comparison_type['codename_string']:
                        self._errors[item] = self.error_class(
                                    [
                                        'Este campo tiene un formato incorrecto.'
                                    ]
                        )
                        continue
                    elif not isinstance(value, str):
                        # Validacion de las preferencias del padre
                        if preference.comparison != TypePreferences.comparison_codenames['codename_free']:

                            # Si tiene participacion no entra a la validaciones del padre
                            if libre:
                                continue

                            # Buscar si hay una preferencia de un comercializador padre
                            if self.type != 'userprofile_bloque':
                                value_limit = Decimal(self.object.get_origen().get_preference_value_by_codename(
                                    preference.codename
                                ))

                            # Verificar limites del padre
                            if preference.comparison == TypePreferences.comparison_codenames['codename_min']:
                                if value < value_limit:
                                    self._errors[item] = self.error_class(
                                        [
                                            'Este campo tiene que ser mayor o igual a {0}'.format(
                                                value_limit)
                                        ]
                                    )
                            elif preference.comparison == TypePreferences.comparison_codenames['codename_max']:
                                if value > value_limit:
                                    self._errors[item] = self.error_class(
                                        [
                                            'Este campo tiene que ser menor o igual a {0}'.format(
                                                value_limit)
                                        ]
                                    )
                else:
                    self.fields[item].initial = cleaned_data.get(item)
                    self._errors[item] = self.error_class(
                        [
                            'Este campo debe tener un valor'
                        ]
                    )
        self.is_bound = False
        return cleaned_data
