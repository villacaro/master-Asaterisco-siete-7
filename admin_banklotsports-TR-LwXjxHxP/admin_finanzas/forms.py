# -*- coding: utf-8 -*-

from admin_finanzas.models import Comercializadora, Cuenta, DiaTrabajo, Movimiento, TipoMovimiento
from admin_lib.util_forms import WidgetCustomizeForms
from django import forms
from django.template import defaultfilters
from django.utils.timezone import now


class CuentaForm(WidgetCustomizeForms, forms.ModelForm):

    class Meta:
        model = Cuenta
        fields = '__all__'

    def clean_numero(self):
        numero = self.cleaned_data.get('numero')
        if numero:
            if numero.isdigit() is False:
                raise forms.ValidationError('Este Campo debe ser númerico')
            elif len(numero) < 4:
                raise forms.ValidationError(
                    'Este Campo debe al menos 4 digitos')
        return numero

    def save(self, commit=True, *args, **kwargs):
        if not self.instance.pk:
            self.instance.comercializadora = self.view.object_comercializadora
        super(CuentaForm, self).save(*args, **kwargs)
        return self.instance


class ComercializadoraSaldoInicialForm(WidgetCustomizeForms, forms.ModelForm):

    nombre = forms.CharField(
        max_length=100,
        label='Cadena '
    )

    class Meta:
        model = Comercializadora
        fields = [
            'nombre',
            'saldo_inicial',
            'saldo_fecha'
        ]

    def __init__(self, *args, **kwargs):
        super(ComercializadoraSaldoInicialForm, self).__init__(*args, **kwargs)
        self.fields['saldo_fecha'].widget.attrs['required'] = ''
        self.fields['saldo_inicial'].widget.attrs['required'] = ''
        self.fields['saldo_fecha'].required = True
        self.fields['saldo_inicial'].required = True

        if self.instance.pk:
            self.fields['nombre'].widget.attrs['readonly'] = 'readonly'
            self.fields['nombre'].initial = self.instance
            self.fields['nombre'].label = self.instance.get_object(
            ).get_verbose_name()

    def save(self, commit=True, *args, **kwargs):
        super(
            ComercializadoraSaldoInicialForm,
            self).save(
            commit=False,
            *args,
            **kwargs)

        if not self.instance.resumen_personalizado:
            self.instance.resumen_personalizado = True
            self.instance.resumen_personalizado_comer = self.view.object_comercializadora
            self.instance.save(update_fields=[
                'resumen_personalizado',
                'resumen_personalizado_comer',
                'updated_at',
            ]
            )

        self.instance.set_saldo_inicial()
        return self.instance


class ComercializadoraSaldoInicialRegisterForm(
        WidgetCustomizeForms, forms.Form):

    comercializadora = forms.ModelChoiceField(
        queryset=Comercializadora.objects.none(),
        empty_label='Seleccione una {0}'.format(
            Comercializadora._meta.verbose_name),
        required=True,
    )
    saldo_inicial = forms.DecimalField(
        label='Saldo',
        help_text='Ingrese el saldo inicial de la comercializadora',
        required=True,
        min_value=0,
        initial=0,
    )
    saldo_fecha = forms.DateField(
        label='Fecha del saldo inicial (*)',
        required=True,
    )

    class Meta:
        fields = [
            'comercializadora',
            'saldo_inicial',
            'saldo_fecha',
        ]

    def __init__(self, *args, **kwargs):
        super(
            ComercializadoraSaldoInicialRegisterForm,
            self).__init__(
            *args,
            **kwargs)
        self.fields[
            'comercializadora'].queryset = self.view.object_comercializadora.get_offspring()

        self.fields['comercializadora'].queryset = self.fields['comercializadora'] \
            .queryset.filter(
                resumen_personalizado_comer_id=None
        ).exclude(
                pk__in=list(self.view.object_comercializadora.get_offspring_level1().values_list(
                    'pk', flat=True
                ))
        )

        for comer_asoc in self.view.object_comercializadora.comercializadora_set.all():
            keys = comer_asoc.get_exclude_resumen_personalizado_kwargs()
            for key in keys.keys():
                self.fields['comercializadora'].queryset = self.fields['comercializadora'].queryset.exclude(
                    ** {
                        key: keys[key]
                    }
                )

        self.fields['saldo_fecha'].initial = self.view \
            .object_comercializadora.get_dia_trabajo().dia.fecha


class DiaTrabajoForm(WidgetCustomizeForms, forms.Form):

    fecha = forms.DateField(
        label='Nuevo dia de trabajo (*)',
        required=True
    )

    def clean_fecha(self):
        fecha = self.cleaned_data.get('fecha')
        if fecha:
            dia_trabajo = self.view.object_comercializadora.get_dia_trabajo()
            if dia_trabajo:
                if fecha > dia_trabajo.dia.fecha:
                    raise forms.ValidationError(
                        'No se puede avanzar a un dia de trabajo superior '
                        'al dia de trabajo actual'
                    )

        return fecha


class MovimientoForm(WidgetCustomizeForms, forms.ModelForm):

    ref_auto = forms.CharField(
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Movimiento
        exclude = ['user', 'dia']

        widgets = {
            'observacion': forms.widgets.Textarea(
                attrs={
                    'rows': 5,
                }
            ),
        }

    def __init__(self, *args, **kwargs):
        super(MovimientoForm, self).__init__(*args, **kwargs)
        self.fields['fecha'].initial = now()

        self.fields['comercializadora'].queryset = self.view \
            .object_comercializadora.get_offspring_level1()

        def label_from_instance(obj):
            return '{0}'.format(obj.get_object())

        self.fields[
            'comercializadora'].label_from_instance = label_from_instance

        if self.fields['comercializadora'].queryset.exists():
            self.fields['comercializadora'].label = self. \
                fields['comercializadora'].queryset[
                    0].get_object().get_verbose_name() + ' (*)'

        self.fields['cuenta'].queryset = Cuenta.objects.filter(
            comercializadora=self.view.object_comercializadora
        )

        self.fields['tipo'].queryset = TipoMovimiento.objects.filter(
            codename__in=self.view.tipo
        ).order_by('nombre')

        cantidad = self.fields['tipo'].queryset.count()

        if cantidad == 1:
            self.fields['tipo'].initial = self.fields['tipo'].queryset[0]
            self.fields['tipo'].widget = forms.HiddenInput()
        elif cantidad > 1:
            self.fields['tipo'].widget = forms.RadioSelect()
            self.fields['tipo'].choices = (
                (obj.pk, str(obj).replace('Ajuste', '')) for obj in self.fields['tipo'].queryset.all()
            )
            self.fields['tipo'].initial = self.fields['tipo'].queryset[0]
            self.fields['tipo'].widget.attrs[
                'class'] = 'radio_select_movimientos'

        # Buscando codigo automatico para movimientos
        codigo_ref = Movimiento.objects.filter(
            tipo__codename__in=self.view.tipo,
            cuenta__tipocuenta__codigo='C.E',
            dia=self.view.object_comercializadora.get_dia_trabajo().dia,
            user=self.view.object_user
        )
        self.fields['ref_auto'].initial = '{1}-{0}'.format(
            codigo_ref.count() + 1,
            self.view.object_user.user[0].upper()
        )

        self.fields['ref_auto'].widget.attrs['class'] = ''
        for cuenta in self.fields['cuenta'].queryset.filter(
            tipocuenta__codigo='C.E'
        ):
            self.fields['ref_auto'].widget.attrs[
                'class'] += ' c-e-{0}'.format(cuenta.pk)

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto:
            if monto <= 0:
                raise forms.ValidationError(
                    'Este Campo debe ser un número positivo')
        return monto

    def save(self, commit=True, *args, **kwargs):
        self.instance.user = self.view.object_user
        self.instance.dia = self.view.object_comercializadora.get_dia_trabajo().dia
        if (self.instance.tipo.codename == 'tipo_ajuste_pagar' or
                self.instance.tipo.codename == 'tipo_deposito'):
            self.instance.monto = self.instance.monto * (-1)

        super(MovimientoForm, self).save(commit=True, *args, **kwargs)
        return self.instance


class FilterMesesForm(WidgetCustomizeForms, forms.Form):

    filter_fecha = forms.ChoiceField(
        label='Periodo (*)',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        super(FilterMesesForm, self).__init__(*args, **kwargs)

        self.fields['filter_fecha'].widget.attrs[
            'class'] += ' filter_movimientos'

        self.inicializar_fechas(
            list(DiaTrabajo.objects.filter(
                comercializadora=self.view.object_comercializadora
            ).values_list(
                'dia__fecha', flat=True
            ).distinct('dia__fecha').order_by('-dia__fecha'))
        )

    def inicializar_fechas(self, fechas=[]):
        data = ()
        diccionario = {}
        for obj in fechas:
            fecha = obj.strftime('%Y-%m')
            if str(fecha) in diccionario:
                pass
            else:
                diccionario[str(fecha)] = True

                verbose_date = defaultfilters.date(
                    obj, 'F - Y'
                ).capitalize()
                data += ((fecha, verbose_date),)

        self.fields['filter_fecha'].choices = data
        del diccionario
        del data


class FilterMesesSuperiorForm(WidgetCustomizeForms, forms.Form):

    filter_fecha = forms.ChoiceField(
        label='Periodo (*)',
        required=True,
    )

    def __init__(self, *args, **kwargs):
        fechas = kwargs.pop('fechas')
        super(FilterMesesSuperiorForm, self).__init__(*args, **kwargs)

        self.fields['filter_fecha'].widget.attrs[
            'class'] += ' filter_movimientos'

        self.inicializar_fechas(
            fechas
        )

    def inicializar_fechas(self, fechas=[]):
        data = ()
        diccionario = {}
        for obj in fechas:
            fecha = obj.strftime('%Y-%m')
            if str(fecha) in diccionario:
                pass
            else:
                diccionario[str(fecha)] = True

                verbose_date = defaultfilters.date(
                    obj, 'F - Y'
                ).capitalize()
                data += ((fecha, verbose_date),)

        self.fields['filter_fecha'].choices = data
        del diccionario
        del data


class MovimientoFilterForm(FilterMesesForm):

    filter_cuenta = forms.ModelChoiceField(
        required=False,
        queryset=Cuenta.objects.none(),
        empty_label='Todas las cuentas'
    )

    def __init__(self, *args, **kwargs):
        super(MovimientoFilterForm, self).__init__(*args, **kwargs)

        self.fields['filter_cuenta'].queryset = Cuenta.objects.filter(
            comercializadora=self.view.object_comercializadora
        )

        self.fields['filter_cuenta'].widget.attrs[
            'class'] += ' filter_movimientos'
