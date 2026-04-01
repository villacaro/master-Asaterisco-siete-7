# -*- coding: utf-8 -*-

from admin_finanzas.models import Comercializadora
from admin_lib.util_forms import WidgetCustomizeForms
from admin_permisologia.models import Groups, Permissions
from admin_status.models import Status, StatusDetail
from admin_users.models import UserProfile, Users
from django import forms
from django.utils.timezone import now


class FilterByProfileForm(WidgetCustomizeForms, forms.Form):
    """
    Formulario dedicado a general un filtro, un selector de tipos de usuario
    """

    profile = forms.ModelChoiceField(
        queryset=UserProfile.objects.none(),
        required=True,
        empty_label='Seleccione un {0}'.format(UserProfile._meta.verbose_name)
    )

    def __init__(self, *args, **kwargs):
        """
        Genera las opciones disponibles en el formulario
        """
        super(FilterByProfileForm, self).__init__(*args, **kwargs)
        superuser = self.view.object_user.superuser
        if not superuser:
            if self.view.object_comercializadora:

                superuser = getattr(
                    self.view.object_comercializadora.get_object(),
                    'permissions_create_user',
                    None
                )
        if superuser:
            self.fields["profile"].queryset = UserProfile.objects.only('pk', 'nombre').filter(
                content_type__gte=self.view.get_profile().content_type
            )
        else:
            self.fields["profile"].queryset = UserProfile.objects.only('pk', 'nombre').filter(
                content_type__gt=self.view.get_profile().content_type
            )


class FilterByProfileAndComerForm(FilterByProfileForm):
    """
    Formulario que hereda de FilterByProfileForm y agrega un filtro de comercializadora
    """
    comercializadora = forms.ModelChoiceField(
        queryset=Comercializadora.objects.none(),
        required=False,
        empty_label='Seleccione una {0}'.format(
            Comercializadora._meta.verbose_name
        )
    )

    def __init__(self, *args, **kwargs):
        """
        Genera las opciones disponibles en el formulario
        """
        super(FilterByProfileAndComerForm, self).__init__(*args, **kwargs)
        self.fields["profile"].required = False
        """
        Filtramos las comercializadoras disponibles para el user creador
        """
        if self.view.object_user.profile.codename == 'userprofile_master':
            from admin_status.models import Status
            status_eliminado = Status.get_status_by_codename('status_eliminado').pk
            self.fields['comercializadora'].queryset = Comercializadora.objects.filter(
                taquilla__isnull=True
            ).exclude(bloque__status_id=status_eliminado)\
                .exclude(banca__status_id=status_eliminado)\
                .exclude(distribuidor__status_id=status_eliminado)\
                .exclude(agencia__status_id=status_eliminado)
        else:
            comercializadoras_user = self.view.object_user.get_user_comercializadoras()
            self.fields['comercializadora'].queryset = comercializadoras_user

            for comercializadora in comercializadoras_user:

                self.fields['comercializadora'].queryset |= comercializadora.get_offspring(
                    profile=self.view.get_profile()
                )

                if comercializadora.get_type().content_type >= self.view.object_user.profile.content_type:
                    self.fields['comercializadora'].queryset |= self.view \
                        .object_user.comercializadora.filter(
                            pk=comercializadora.pk
                    )

        self.fields["comercializadora"].queryset = self.fields["comercializadora"] \
            .queryset.distinct()


class UsersCreateForm(WidgetCustomizeForms, forms.ModelForm):
    """
    A form that creates a user, with no privileges, from the given username and
    password.
    """

    user = forms.RegexField(
        label='Nombre de usuario (*)',
        min_length=4,
        max_length=30, regex=r'^[a-zA-Z0-9_.-]+$',
        help_text='El usuario debe ser superior o igual a 6 caracteres, o como maximo 30, . '
        ' Acepta numeros y simbolos /_/./-',
        error_messages={
            'invalid': 'El usuario debe estar en minuscula y '
                       'solo acepta numeros y los siguientes  /_/./- caracteres.'
        }
    )

    password1 = forms.CharField(
        label='Contraseña (*)',
        widget=forms.PasswordInput
    )

    password2 = forms.CharField(
        label='Confirmar contraseña (*)',
        min_length=6,
        max_length=30,
        widget=forms.PasswordInput,
        help_text='Por favor confirme la contraseña.'
    )

    # Declaramos profile explicitamente con queryset=None para evitar que Django
    # intente construir el formfield durante la carga del modulo (antes de que
    # admin_permisologia.Profile este disponible). El queryset real se asigna en __init__.
    profile = forms.ModelChoiceField(
        queryset=None,
        required=True,
        label='Perfil de usuario (*)',
        empty_label='Seleccione un perfil',
    )

    error_messages = {
        'duplicate_username': 'El nombre de usario ingresado ya existe.',
        'password_mismatch': 'Las contraseñas no coinciden.',
    }

    class Meta:
        model = Users
        fields = ['profile', 'user', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UsersCreateForm, self).__init__(*args, **kwargs)
        # Inicializamos el queryset de profile aqui, cuando todos los modelos ya estan cargados
        self.fields['profile'].queryset = UserProfile.objects.none()
        """
        si es super usuario puede crear otros de su mismo nivel
        y luego solo se podran asociar las comercializadoras
        de dicho nivel asociadas al usuario, o en su defecto
        comercializadoras de niveles inferiores pero
        asociadas a las comercializadoras del usuario creador
        """

        superuser = self.view.object_user.superuser
        if not superuser:
            if self.view.object_comercializadora:

                superuser = getattr(
                    self.view.object_comercializadora.get_object(),
                    'permissions_create_user',
                    None
                )

        if superuser:
            self.fields['profile'].queryset = UserProfile.objects.filter(
                content_type__gte=self.view.get_profile().content_type
            )
        else:
            self.fields['profile'].queryset = UserProfile.objects.filter(
                content_type__gt=self.view.get_profile().content_type
            )

        if self.view.request.GET.get('ccadena'):
            self.view.kwargs['ccadena'] = self.view.request.GET.get('ccadena')
            cadena = Comercializadora.objects.get(
                pk=self.view.request.GET.get('ccadena'))
            self.fields['profile'].queryset = self.fields['profile'].queryset.filter(
                content_type__lte=cadena.get_object().get_type().content_type
            )

            self.fields['profile'].initial = UserProfile.objects.get(
                content_type=cadena.get_object().get_type().content_type
            )

    def clean_user(self):
        # Since User.username is unique, this check is redundant,
        # but it sets a nicer error message than the ORM. See #13147.
        user = self.cleaned_data['user']
        try:
            Users.objects.get(user=user)
        except Users.DoesNotExist:
            return user

        raise forms.ValidationError(
            self.error_messages['duplicate_username'],
            code='duplicate_username',
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(UsersCreateForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        user.user_ref = self.view.object_user
        if commit:
            user.save()
            StatusDetail.objects.create(
                status=Status.get_status_by_codename(codename='status_activo'),
                user=user
            )
        return user


class UsersUpdateForm(WidgetCustomizeForms, forms.ModelForm):
    perfil = forms.CharField(
        label='Perfil de usuario (*)'
    )

    password2 = forms.CharField(
        label='Contraseña ',
        help_text='Si desea cambiar la contraseña selecione '
        '<a href="password"/><i class="icon-key-1" >'
        'este formulario</i></a>'
    )

    class Meta:
        model = Users
        fields = [
            'perfil',
            'user',
            'password2',
            'superuser',
            'comercializadora',
            'groups',
            'user_permissions',
        ]

        widgets = {
            # 'comercializadora': forms.widgets.CheckboxSelectMultiple(),
            'user_permissions': forms.widgets.CheckboxSelectMultiple(),
            'groups': forms.widgets.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(UsersUpdateForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['readonly'] = ''
        self.fields['perfil'].widget.attrs['readonly'] = ''
        self.fields['password2'].initial = '*****************'
        self.fields['password2'].widget.attrs['readonly'] = ''
        self.fields['perfil'].initial = self.instance.profile.nombre

        self.fields['comercializadora'].label = 'Ente de cadena (*)'

        if self.view.request.GET.get('ccadena'):
            cadena = Comercializadora.objects.get(
                pk=self.view.request.GET.get('ccadena'),
            )
            self.initial['comercializadora'] = [cadena.pk]

        """
        filtramos los permisos, en caso de editarse el mismo usuario,
        los mismo se deshabilitan
        """
        if self.view.object_user.pk == self.instance.pk:
            del self.fields['superuser']
            del self.fields['groups']
            del self.fields['user_permissions']

        else:
            if self.view.object_user.superuser is False:
                """
                eliminamos la el campo de super usuario del formulario
                es mas seguro eliminarlo aqui que enviarlo como hiden
                """
                del self.fields['superuser']

                """
                filtramos los grupos y permisos deacuerdo a los asignados al usuario
                que se encuentra editando
                """
                self.fields['groups'].queryset = self.view.object_user.get_query_set_groups(
                    comercializadora=self.view.object_comercializadora
                )
                self.fields['user_permissions'].queryset = self.view.object_user \
                    .get_query_set_permissions(
                        comercializadora=self.view.object_comercializadora
                )
            else:
                """
                si es super usuario, los permisos se habilitan deacuerdo con el
                perfil iniciado
                """

                self.fields['user_permissions'].queryset = Permissions.objects.filter(
                    profiles__codename=self.view.get_profile().codename
                ).distinct()

                self.fields['groups'].queryset = Groups.objects.filter(
                    permissions__profiles__codename=self.view.get_profile().codename
                ).distinct()

            self.fields['user_permissions'].queryset = self.fields['user_permissions'].queryset.filter(
                profiles__in=[self.instance.profile]
            )

        """
        filtramos las comercializadoras disponibles para el user creador
        """
        if self.view.object_user.profile.codename == 'userprofile_master':
            from admin_status.models import Status
            status_eliminado = Status.get_status_by_codename('status_eliminado').pk
            self.fields['comercializadora'].queryset = Comercializadora.objects.filter(
                taquilla__isnull=True
            ).exclude(bloque__status_id=status_eliminado)\
                .exclude(banca__status_id=status_eliminado)\
                .exclude(distribuidor__status_id=status_eliminado)\
                .exclude(agencia__status_id=status_eliminado)
        else:
            comercializadoras_user = self.view.object_user.get_user_comercializadoras()
            self.fields['comercializadora'].queryset = comercializadoras_user

            for comercializadora in comercializadoras_user:
                self.fields['comercializadora'].queryset |= comercializadora.get_offspring(
                    profile=self.view.get_profile()
                )

                if comercializadora.get_type().content_type >= self.view.object_user.profile.content_type:
                    self.fields['comercializadora'].queryset |= self.view \
                        .object_user.comercializadora.filter(
                            pk=comercializadora.pk
                    )

        self.fields['comercializadora'].queryset = self.fields['comercializadora'] \
            .queryset.distinct()

    def save(self, commit=True, *args, **kwargs):
        if self.view.object_user.pk == self.instance.pk:
            return super(UsersUpdateForm, self).save(commit=True, *args, **kwargs)
        else:
            self.instance.cache_clear(clear_permisos=True)
            return super(UsersUpdateForm, self).save(commit=True, *args, **kwargs)


class CustomizationUsersForm(WidgetCustomizeForms, forms.ModelForm):
    perfil = forms.CharField(
        label='Perfil de usuario (*)'
    )

    status = forms.ModelChoiceField(
        queryset=Status.objects.filter(
            content_type=1
        ).exclude(
            codename='status_activo_sin_venta'
        ).order_by('name'),
        required=True,
        help_text='Seleccione un estatus para el usuario'
    )

    class Meta:
        model = Users
        fields = [
            'perfil',
            'user',
            'status',
            'etiqueta',
            'email',
        ]

    def __init__(self, *args, **kwargs):
        super(CustomizationUsersForm, self).__init__(*args, **kwargs)
        self.fields['status'].initial = self.instance.get_status()
        self.fields['user'].widget.attrs['readonly'] = ''
        self.fields['perfil'].widget.attrs['readonly'] = ''
        self.fields['perfil'].initial = self.instance.profile.nombre

    def clean_email(self):
        """
        Descarta un correo vacio, en caso de no existir devuelve un None
        """
        email = self.cleaned_data['email']
        if email:
            return email
        else:
            return None

    def save(self, commit=True, *args, **kwargs):
        status_old = self.instance.get_status()
        status_new = self.cleaned_data['status']
        if status_old.codename != status_new.codename:
            self.instance.statusdetail_set.filter(
                enddate=None
            ).update(enddate=now())

            StatusDetail.objects.create(
                status=status_new,
                user=self.instance
            )
        return super(CustomizationUsersForm, self).save(commit=True, *args, **kwargs)


class SetPasswordForm(WidgetCustomizeForms, forms.ModelForm):
    """

    Con este formulario se edita la contraseña de cualquier usuario
    """
    error_messages = {
        'password_mismatch': 'Las contraseñas no coinciden.',
    }
    new_password1 = forms.CharField(
        label='Nueva contraseña (*)',
        widget=forms.PasswordInput
    )
    new_password2 = forms.CharField(
        label='Confirmar contraseña (*)',
        widget=forms.PasswordInput,
        min_length=6,
        max_length=30
    )
    perfil = forms.CharField(
        label='Perfil de usuario (*)'
    )

    class Meta:
        model = Users
        fields = [
            'perfil',
            'user',
            'new_password1',
            'new_password2'
        ]

    def __init__(self, *args, **kwargs):
        super(SetPasswordForm, self).__init__(*args, **kwargs)
        self.fields['user'].widget.attrs['readonly'] = ''
        self.fields['perfil'].widget.attrs['readonly'] = ''
        if self.instance.pk:
            self.fields['perfil'].initial = self.instance.profile.nombre

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',
                )
        return password2

    def save(self, commit=True):
        """
        Actualiza la contraseña del usuario
        """
        self.instance.set_password(self.cleaned_data['new_password1'])
        if commit:
            self.instance.save(clear_session=False, update_fields=['password'])
        return self.instance


class PasswordChangeForm(SetPasswordForm):
    """
    Este formulario utiliza un formulario base, añadiendo
    solo una confirmacion de contraseña anterior.
    """
    error_messages = dict(SetPasswordForm.error_messages, **{
        'password_incorrect': 'Contraseña incorrecta. '
        'Por favor vuelva a intentarlo.',
    })
    old_password = forms.CharField(
        label='Contraseña anterior (*)',
        widget=forms.PasswordInput
    )

    class Meta:
        model = Users
        fields = [
            'perfil',
            'user',
            'old_password',
            'new_password1',
            'new_password2'
        ]

    def __init__(self, *args, **kwargs):
        super(PasswordChangeForm, self).__init__(*args, **kwargs)
        self.instance = self.view.object_user
        self.fields['user'].initial = self.instance.user
        self.fields['perfil'].initial = self.instance.profile.nombre

    def clean_old_password(self):
        """
        Validates that the old_password field is correct.
        """
        old_password = self.cleaned_data['old_password']
        if not self.instance.check_password(old_password):
            raise forms.ValidationError(
                self.error_messages['password_incorrect'],
                code='password_incorrect',
            )
        return old_password
