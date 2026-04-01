# -*- coding: utf-8 -*-

from admin_apuestas.models import Tickets
from admin_asterisco7.settings import REDIS_DB
from admin_finanzas.models import Comercializadora
from admin_lib.util_forms import WidgetCustomizeForms
from admin_status.models import Status
from django import forms
from django.db.models import Q


class BuscarTicketForm(WidgetCustomizeForms, forms.Form):
    """
    Formulario para gestionar grupos de usuarios
    """

    code_ticket = forms.IntegerField(
        min_value=0,
        label="N° de ticket ",
        help_text="Ingrese el número del ticket",
        required=False
    )

    error_messages = {
        'code_ticket': "Ticket no encontrado",
        'relate_ticket': "El ticket no pertenece a su comercializadora",
    }

    def __init__(self, *args, **kwargs):
        super(BuscarTicketForm, self).__init__(*args, **kwargs)

    def clean_code_ticket(self):
        code_ticket = self.cleaned_data.get('code_ticket')
        try:
            ticket = Tickets.objects.get(pk=code_ticket)
            self.verificate_comercializacion(ticket)
        except Tickets.DoesNotExist:
            raise forms.ValidationError(
                self.error_messages['code_ticket'],
                code='code_ticket',
            )
        return code_ticket

    def verificate_comercializacion(self, ticket):

        if self.view.set_execute_function_by_profile(
            **{"prefix": "is_related",
               "instance": self,
               "ticket": ticket,
               }
        ) is True:
            return

        raise forms.ValidationError(
            self.error_messages['relate_ticket'],
            code='relate_ticket',
        )

    def is_related_userprofile_master(self, **kwargs):
        """
        Puesto que es el master accede a todo
        """
        return True

    def is_related_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        return self.view.object_comercializadora.get_object() == \
            kwargs["ticket"].user.taquilla.agencia.distribuidores.banca.bloque.operadora

    def is_related_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        return self.view.object_comercializadora.get_object() == \
            kwargs["ticket"].user.taquilla.agencia.distribuidores.banca.bloque

    def is_related_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """
        return self.view.object_comercializadora.get_object() == \
            kwargs["ticket"].user.taquilla.agencia.distribuidores.banca

    def is_related_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        return self.view.object_comercializadora.get_object() == \
            kwargs["ticket"].user.taquilla.agencia.distribuidores

    def is_related_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una agencia
        """
        return self.view.object_comercializadora.get_object() == \
            kwargs["ticket"].user.taquilla.agencia


KEYS_CODENAME = {
    'bet_taquilla': 'WS_MAINTENANCE_BET',
    'pay_taquilla': 'WS_MAINTENANCE_PAY',
    'connection_taquilla': 'WS_MAINTENANCE_GLOBAL',
    'connection_panel': 'PANEL_MAINTENANCE_GLOBAL',
}


class SistemForm(WidgetCustomizeForms, forms.Form):
    """
    Formulario para las opciones de contigencia del sistema
    """
    bet_taquilla = forms.BooleanField(
        label='Venta en taquilla', required=False)
    pay_taquilla = forms.BooleanField(
        label='Pago de tickets en taquilla', required=False)
    connection_taquilla = forms.BooleanField(
        label='Conexión en taquilla', required=False)
    connection_panel = forms.BooleanField(
        label='Conexión en panel', required=False)

    def __init__(self, *args, **kwargs):
        super(SistemForm, self).__init__(*args, **kwargs)
        if self.view.get_profile().codename != 'userprofile_master':
            del self.fields['connection_panel']
            for key in self.fields.keys():
                access = self.get_access(KEYS_CODENAME[key], self.view.object_comercializadora)
                self.fields[key].initial = access[0]
                if access[0] is False and access[1] is True:
                    self.fields[key].widget.attrs['disabled'] = True
        else:
            for key in self.fields.keys():
                key_redis = '{0}'.format(KEYS_CODENAME[key])
                value = REDIS_DB.get(key_redis)
                if value:
                    if int(value) == 0:
                        self.fields[key].initial = False
                    else:
                        self.fields[key].initial = True
                else:
                    self.fields[key].initial = True

    def get_access(self, key, comercializadora):
        access = True
        parent = False
        if REDIS_DB.get(key) == b'0':
            access = False
            parent = True
        else:
            origen = comercializadora.get_origen()
            if origen:
                while origen:
                    key_redis = '{0}-{1}'.format(key, origen.id)
                    value = REDIS_DB.get(key_redis)
                    if value == b'0':
                        access = False
                        parent = True
                        break
                    origen = origen.get_origen()
            else:
                key_redis = '{0}-{1}'.format(key, comercializadora.id)
                value = REDIS_DB.get(key_redis)
                if value == b'0':
                    access = False
        return [access, parent]


class ComercializadorasForm(WidgetCustomizeForms, forms.Form):
    """
    Formulario para restaurar comercializadoras
    """
    comercializadora = forms.ModelChoiceField(
        required=True,
        queryset=Comercializadora.objects.all(),
        empty_label='Todas las comercializadoras eliminadas'
    )

    def __init__(self, *args, **kwargs):
        super(ComercializadorasForm, self).__init__(*args, **kwargs)
        status = Status.get_status_by_codename('status_eliminado')
        self.fields['comercializadora'].queryset = Comercializadora.objects.filter(
            Q(operadora__status=status) |
            Q(bloque__status=status) |
            Q(banca__status=status) |
            Q(distribuidor__status=status) |
            Q(agencia__status=status) |
            Q(taquilla__usuariostaquilla__status=status)
        )

        def label_from_instance(obj):
            comercializadora = obj.get_object()
            label = ''
            if comercializadora.prefix_filter != 'taquilla':
                label = comercializadora._meta.verbose_name + ': ' + comercializadora.nombre.split('_delete_')[0]
            else:
                label = comercializadora._meta.verbose_name + ': ' + comercializadora.taquilla.split('_delete_')[0]

            origen = comercializadora.get_origen()
            while origen:
                label += ' | {}: {} '.format(
                    origen._meta.verbose_name,
                    origen.nombre.split('_delete_')[0]
                )
                origen = origen.get_origen()
                if not origen:
                    break

            return label

        self.fields['comercializadora'].label_from_instance = label_from_instance
