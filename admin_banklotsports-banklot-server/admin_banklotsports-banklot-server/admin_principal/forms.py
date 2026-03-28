# -*- coding: utf-8 -*-

from admin_lib.util_forms import WidgetCustomizeForms
from admin_users.models import Users
from django import forms


class AuthenticationForm(WidgetCustomizeForms, forms.Form):
    """
    Formulario para la autentificacion de los usuarios en el panel administrativo.
    """
    username = forms.CharField(max_length=100, label="Nombre de usuario ", required=True)
    password = forms.CharField(label="Contraseña ", widget=forms.PasswordInput, required=True)

    error_messages = {
        'invalid_login': "Combinación de credenciales incorrecta.",
        'inactive': "Usuario %(status)s.",
        'complete_form': "Todos los datos son obligatorios.",
        'no_foud_comer': "No se encontró ninguna comercializadora asociada, por favor contacte al administrador."
    }

    def clean(self):
        """
        En este metodo se verifica que los campos no esten vacios,
        luego se usa el metodo autenticiacion de Users,
        para validar la combinacion de credenciales.
        """
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user = Users.objects.authenticate(username=username, password=password)
            if self.user is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                )
            else:
                if (self.user.profile.codename != "userprofile_master" and
                        self.user.comercializadora.all().exists() is False):
                    raise forms.ValidationError(
                        self.error_messages['no_foud_comer'],
                        code='no_foud_comer',
                        params={'status': self.user.get_status().name, },
                    )
                else:
                    self.confirm_login_allowed(self.user)

        else:
            raise forms.ValidationError(
                self.error_messages['complete_form'],
                code='complete_form',
            )

        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        Se controla el status del usuario, para indicar si puede o no iniciar en el sistema
        """

        if user.get_status().codename != "status_activo":
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
                params={'status': user.get_status().name, },
            )
