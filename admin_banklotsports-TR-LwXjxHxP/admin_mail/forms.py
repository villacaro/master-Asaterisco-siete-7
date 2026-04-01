# -*- coding: utf-8 -*-

from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Operadoras, Taquillas
from admin_lib.util_forms import WidgetCustomizeForms
from admin_mail.models import Message, MessageAdjunt, MessageComer, MessageSend
from admin_mail.task import AsyncSendMail
from django import forms


class FilterMailsForm(WidgetCustomizeForms, forms.Form):
    priority = forms.ChoiceField(
        label='Prioridad',
        required=False,
        choices=[['', 'Seleccione una opción']] + Message.PRIORITIES
    )


class MessageForm(WidgetCustomizeForms, forms.ModelForm,):
    """
    Formulario para crear mensajes
    """

    operadora = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Operadoras.objects.only('pk', 'nombre').all(),
    )
    bloque = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Bloques.objects.only('pk', 'nombre').all(),
    )
    banca = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Bancas.objects.only('pk', 'nombre').all(),
    )
    distribuidor = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Distribuidores.objects.only('pk', 'nombre').all(),
    )
    agencia = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Agencias.objects.only('pk', 'nombre').all(),
    )
    taquilla = forms.MultipleChoiceField(
        required=False,
    )

    option = forms.ChoiceField(
        choices=MessageSend.SEND_OPTIONS,
        required=True,
        initial=MessageSend.SEND_SIMPLE,
        label='Forma de envío',
        help_text='Simple: Solo comercializadoras seleccionadas. \n\n'
                  'Masivo: Nivel inferior de las comercializadoras seleccionadas.\n\n'
                  'Taquillas: Solo las taquillas de las comercializadoras seleccionadas.'
    )

    class Meta:
        model = Message
        fields = [
            'operadora',
            'bloque',
            'banca',
            'distribuidor',
            'agencia',
            'taquilla',
            'option',
            'subject',
            'body',
            'priority',
        ]

        widgets = {
        }

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        self.fields['option'].widget.attrs[
            'title'] = self.fields['option'].help_text
        getattr(
            self, 'filter_{0}'.format(
                self.view.get_profile().codename))(
            **{})

    def get_taquillas(self, **kwargs):

        choices_taquilla = []

        for taquilla in Taquillas.objects.all().filter(
                **kwargs).values_list('pk', 'taquilla', 'agencia__nombre'):
            choices_taquilla.append(
                (taquilla[0], '{0} - {1}'.format(taquilla[2], taquilla[1])))

        return choices_taquilla

    def filter_userprofile_master(self, **kwargs):
        """
        Puesto que es el master accede a todos los usuarios

        Si es master tiene acceso a todo
        """
        pass

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """

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

        self.fields['taquilla'].choices = self.get_taquillas(**{
            'agencia__distribuidores__banca__bloque__operadora_id':
            self.view.object_comercializadora.get_object().pk
        })

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """

        self.fields['operadora'].queryset = self.fields['operadora'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().operadora_id
        )

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

        self.fields['taquilla'].choices = self.get_taquillas(**{
            'agencia__distribuidores__banca__bloque_id':
            self.view.object_comercializadora.get_object().pk
        })

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """

        self.fields['operadora'].queryset = self.fields['operadora'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().bloque.operadora_id
        )

        self.fields['bloque'].queryset = self.fields['bloque'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().bloque_id
        )

        del self.fields['banca']

        self.fields['distribuidor'].queryset = self.fields['distribuidor'].queryset.filter(
            banca_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['agencia'].queryset = self.fields['agencia'].queryset.filter(
            distribuidores__banca_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['taquilla'].choices = self.get_taquillas(**{
            'agencia__distribuidores__banca_id':
            self.view.object_comercializadora.get_object().pk
        })

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """

        self.fields['operadora'].queryset = self.fields['operadora'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().banca.bloque.operadora_id
        )

        self.fields['bloque'].queryset = self.fields['bloque'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().banca.bloque_id
        )

        self.fields['banca'].queryset = self.fields['banca'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().banca_id
        )

        del self.fields['distribuidor']

        self.fields['agencia'].queryset = self.fields['agencia'].queryset.filter(
            distribuidores_id=self.view.object_comercializadora.get_object().pk
        )

        self.fields['taquilla'].choices = self.get_taquillas(**{
            'agencia__distribuidores_id':
            self.view.object_comercializadora.get_object().pk
        })

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una agencia
        """
        self.fields['operadora'].queryset = self.fields['operadora'].queryset.filter(
            pk=self.view.object_comercializadora.get_object(
            ).distribuidores.banca.bloque.operadora_id
        )

        self.fields['bloque'].queryset = self.fields['bloque'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().distribuidores.banca.bloque_id
        )

        self.fields['banca'].queryset = self.fields['banca'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().distribuidores.banca_id
        )

        self.fields['distribuidor'].queryset = self.fields['distribuidor'].queryset.filter(
            pk=self.view.object_comercializadora.get_object().distribuidores_id
        )

        del self.fields['agencia']

        self.fields['taquilla'].choices = self.get_taquillas(**{
            'agencia__id':
            self.view.object_comercializadora.get_object().pk
        })

    def save(self, commit=True, *args, **kwargs):
        self.instance.from_comercializadora = self.view.object_comercializadora
        super(MessageForm, self).save(commit=True, *args, **kwargs)

        MessageComer.objects.create(
            comercializadora=self.view.object_comercializadora,
            message=self.instance,
            read=True,
            tray_group=MessageComer.TRAY_GROUP_SENT
        )

        send = MessageSend.objects.create(
            message=self.instance,
            options=self.cleaned_data.get('option')
        )

        names = ['operadora', 'bloque', 'banca', 'distribuidor', 'agencia']

        _objects = []
        for name in names:
            if self.cleaned_data.get(name) is not None:
                for _object in self.cleaned_data.get(name):
                    _objects.append(_object)

        for _object in Taquillas.objects.filter(
                pk__in=self.cleaned_data.get('taquilla')):
            _objects.append(_object)

        if len(_objects) == 0:
            for _object in self.view.object_comercializadora.get_object().get_offspring():
                _objects.append(_object)

        for _object in _objects:
            send.to_comercializadora.add(
                _object.get_comercializadora()
            )

        for _file in self.view.request.FILES.getlist('files'):
            self.instance.adjunts.add(
                MessageAdjunt.objects.create(
                    adjunt=_file
                )
            )

        # Tarea asincrona que se encarga de enviar el mensaje
        task = AsyncSendMail()
        task.delay(
            *(),
            **{
                'message_send': send.pk
            }
        )
