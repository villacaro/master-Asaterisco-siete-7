# -*- coding: utf-8 -*-
from django import forms
from django.core.exceptions import ObjectDoesNotExist

from .models import ClientFiles, ClientIPAddress, ClientStatus, ClientVersion


class ClientVersionAdminForm(forms.ModelForm):

    class Meta:
        model = ClientVersion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientVersionAdminForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = ClientStatus.objects.filter(content_type=2)

    def save(self, commit=True, *args, **kwargs):
        super(ClientVersionAdminForm, self).save(commit=False, *args, **kwargs)
        if self.instance.status.equals_by_codename('client_status_vs_active'):  # Si la versión que edito es activa
            try:
                version = ClientVersion.objects.get(status_id=4)  # Status de versión activa
                version.set_status_by_status_codename("client_status_vs_inactive")
                # Coloca no disponible el archivo client de esa versión
                ClientFiles.set_files_status(version, "client_status_file_unavailable")
            except ObjectDoesNotExist:
                pass
        # Coloca disponible el archivo client de la versión activa
        ClientFiles.set_files_status(self.instance.version, "client_status_file_available")
        self.instance.save()
        return self.instance


class ClientIPAddressAdminForm(forms.ModelForm):

    class Meta:
        model = ClientIPAddress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientIPAddressAdminForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = ClientStatus.objects.filter(content_type=1)


class ClientFilesAdminForm(forms.ModelForm):

    class Meta:
        model = ClientFiles
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(ClientFilesAdminForm, self).__init__(*args, **kwargs)
        self.fields['status'].queryset = ClientStatus.objects.filter(content_type=3)

    def save(self, commit=True, *args, **kwargs):
        super(ClientFilesAdminForm, self).save(commit=False, *args, **kwargs)
        self.instance.save()
        self.instance.crc = "{0}".format(self.instance.getcrc())
        self.instance.save(update_fields=['crc'])
        return self.instance
