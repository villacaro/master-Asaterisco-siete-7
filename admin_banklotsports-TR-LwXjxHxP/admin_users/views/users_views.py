# -*- coding: utf-8 -*-

from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_icons import Icons
from admin_lib.util_views import MyViewBase
from admin_users.forms import (
    CustomizationUsersForm, FilterByProfileAndComerForm, PasswordChangeForm, SetPasswordForm, UsersCreateForm,
    UsersUpdateForm,
)
from admin_users.models import UserProfile, Users
from django.core.urlresolvers import reverse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from django.views.generic.edit import FormView


class UsersView(MyViewBase):
    """
    Clase base para manipular usuarios
    """
    model = Users

    def get_queryset(self):
        """
        En esta consulta queda validado que un usuario no puede
        verse a si mismo, ni tampoco usuarios con privilegios superiores.
        """
        superuser = self.object_user.superuser

        users = Users.objects.all()
        if not superuser:
            users = users.exclude(pk=self.object_user.pk)
            if self.object_comercializadora:

                superuser = getattr(
                    self.object_comercializadora.get_object(),
                    "permissions_create_user",
                    None
                )

        if superuser:
            users = users.filter(
                profile__content_type__gte=self.get_profile().content_type)
        else:
            users = users.filter(
                profile__content_type__gt=self.get_profile().content_type)

        if self.object_user.superuser:
            """
            si es superuser se agrega su propio usuario al querry set
            """
            users |= Users.objects.filter(pk=self.object_user.pk)

        return users

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        get = ""
        if self.request.GET.get("ccadena"):
            get = "&ccadena={0}".format(self.request.GET.get("ccadena"))
        return "?profile={0}".format(self.object.profile_id) + get


class UsersCreateView(UsersView, CreateView):
    """
    Clase usada para crear los usuarios, hereda de la vista generica de creacion
    y de la clase generica de usuario donde se define el modelos y el formulario
    """
    form_class = UsersCreateForm

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        return reverse("admin_users_users_update", kwargs={'pk': self.object.pk})


class UsersListView(UsersView, ListView):
    """
    Clase usada para listar los usuarios
    """

    filter_form = None
    form_class = FilterByProfileAndComerForm

    def filter_userprofile_master(self, **kwargs):
        """
        Puesto que es el master accede a todos los usuarios
        """
        return Users.objects.filter(profile_id=kwargs.get('profile').pk)

    def filter_userprofile_operadora(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una operadora
        """
        users = Users.objects.filter(profile_id=kwargs.get('profile').pk)
        if kwargs.get('profile').codename == 'userprofile_operadora':
            users = users.filter(
                comercializadora__operadora=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_bloque':
            users = users.filter(
                comercializadora__bloque__operadora=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_banca':
            users = users.filter(
                comercializadora__banca__bloque__operadora=self.object_comercializadora
                .get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_distribuidor':
            users = users.filter(
                comercializadora__distribuidor__banca__bloque__operadora=self
                .object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_agencia':
            users = users.filter(
                comercializadora__agencia__distribuidores__banca__bloque__operadora=self
                .object_comercializadora.get_object()
            )

        return users

    def filter_userprofile_bloque(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un bloque
        """
        users = Users.objects.filter(profile_id=kwargs.get('profile').pk)
        if kwargs.get('profile').codename == 'userprofile_bloque':
            users = users.filter(
                comercializadora__bloque=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_banca':
            users = users.filter(
                comercializadora__banca__bloque=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_distribuidor':
            users = users.filter(
                comercializadora__distribuidor__banca__bloque=self
                .object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_agencia':
            users = users.filter(
                comercializadora__agencia__distribuidores__banca__bloque=self
                .object_comercializadora.get_object()
            )

        return users

    def filter_userprofile_banca(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una banca
        """

        users = Users.objects.filter(profile_id=kwargs.get('profile').pk)
        if kwargs.get('profile').codename == 'userprofile_banca':
            users = users.filter(
                comercializadora__banca=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_distribuidor':
            users = users.filter(
                comercializadora__distribuidor__banca=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_agencia':
            users = users.filter(
                comercializadora__agencia__distribuidores__banca=self
                .object_comercializadora.get_object()
            )

        return users

    def filter_userprofile_distribuidor(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en un distribuidor
        """
        users = Users.objects.filter(profile_id=kwargs.get('profile').pk)
        if kwargs.get('profile').codename == 'userprofile_distribuidor':
            users = users.filter(
                comercializadora__distribuidor=self.object_comercializadora.get_object()
            )

        elif kwargs.get('profile').codename == 'userprofile_agencia':
            users = users.filter(
                comercializadora__agencia__distribuidores=self.object_comercializadora.get_object()
            )

        return users

    def filter_userprofile_agencia(self, **kwargs):
        """
        Se realizan los filtros respectivos basandose en una agencia
        """
        users = Users.objects.filter(profile_id=kwargs.get('profile').pk)
        if kwargs.get('profile').codename == 'userprofile_agencia':
            users = users.filter(
                comercializadora__agencia=self.object_comercializadora.get_object()
            )

        return users

    def get_queryset(self):
        self.profile = None

        profile = self.request.GET.get('profile')
        comercializadora = self.request.GET.get('comercializadora')

        if profile is not None and profile != '':
            users = super(UsersListView, self).get_queryset()

            self.profile = UserProfile.get_userprofile_by_pk(profile)
            users = self.set_execute_function_by_profile(
                **{
                    'profile': self.profile,
                    'prefix': 'filter',
                    'instance': self
                }
            ).exclude(pk=self.object_user.pk)

            users |= Users.objects.filter(
                profile_id=self.profile.id,
                user_ref=self.object_user
            )

            if comercializadora is not None and comercializadora != '':
                users = users.filter(comercializadora=comercializadora)

            users = users.distinct('user')
        else:
            users = Users.objects.none()

        return users.only('user')


class UsersDeleteView(UsersView, DeleteView):
    relate_delete = True
    relate_delete_validate = True


class UsersDetailView(UsersView, DetailView):
    pass


class UsersUpdateView(UsersView, UpdateView):
    form_class = UsersUpdateForm

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        if self.object.pk == self.object_user.pk:
            return reverse("admin_users_users_account")
        else:
            return None


class UsersCustomizeView(UsersView, UpdateView):
    form_class = CustomizationUsersForm


class UsersUpdatePasswordView(UsersView, UpdateView):
    form_class = SetPasswordForm


class UsersChangePasswordView(UsersView, FormView):
    form_class = PasswordChangeForm
    template_name = "admin_users/users/account_change_password.html"

    def form_valid(self, form):
        """
        Al validarse el cambio de contraseña se redirige a la vista de account
        """
        from django.http import HttpResponseRedirect
        from django.contrib import messages
        messages.info(
            self.request, "¡Enhorabuena! Contraseña actualizada con éxito!")
        form.save()
        return HttpResponseRedirect(reverse("admin_users_users_account"))


class UsersAccountView(UsersView, DetailView):
    template_name = "admin_users/users/account.html"

    def get_object(self, queryset=None):
        return self.object_user


class UsersDatatableView(UsersListView, BaseDatatableView):
    # Orden del filtro
    order_columns = None

    def get_initial_queryset(self):
        self.opcions_url = [
            'admin_users_users_detail$' + Icons.detail,
            'admin_users_users_update$' + Icons.update,
            'admin_users_users_delete$' + Icons.delete,
            'admin_users_users_customize$' + Icons.tag,
            'admin_users_users_update_password$' + Icons.exchange,
        ]
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []

        for x, item in enumerate(qs):
            comercializadoras = ''

            for comercializadora in item.get_query_comercializadoras_level(self.profile.codename)\
                    .only('id'):
                comercializadoras += '<span class="tag tag-blue">{0}</span> '\
                    .format(str(comercializadora.get_object()))

            keys = {
                'pk': item.pk
            }
            links = self.get_urls('', 'btn btn-xs btn-ico btn-default', **keys)
            json_data.append([
                (x + 1 + acarreo),
                item.user,
                item.get_status().name,
                comercializadoras,
                links,
            ])

        return json_data
