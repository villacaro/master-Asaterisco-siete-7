# -*- coding: utf-8 -*-

from admin_banklotsports.settings import ACCESO_URL, INDEX_URL
from admin_lib.util_views import MyViewBase
from admin_principal.forms import AuthenticationForm
from admin_users.models import Users
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import TemplateView
from django.views.generic.edit import FormView


class PrincipalLoginView(MyViewBase, FormView):
    """
    Clase encargada de procesar el login.
    """
    template_name = 'home/login.html'
    form_class = AuthenticationForm
    info_menu = False
    info_user = False

    def get_context_data(self, **kwargs):
        context = super(PrincipalLoginView, self).get_context_data(**kwargs)
        context['error'] = self.request.GET.get('error')
        return context

    def form_valid(self, form):
        """
        Al ser valido el formulario, se procede a iniciar la session
        y redirigir a la vista deseada.
        """

        Users.objects.login(username=form.cleaned_data.get('username'),
                            request=self.request
                            )

        if self.request.GET.get('next'):
            return HttpResponseRedirect(self.request.GET.get('next'))
        else:
            return HttpResponseRedirect(INDEX_URL)

        return super(PrincipalLoginView, self).form_valid(form)


class PrincipalView(MyViewBase, TemplateView):
    """
    Clase encargada de generar el index del sistema
    """
    template_name = 'home/index.html'


class PrincipalLogoutView(PrincipalView):
    """
    Clase encargada de relizar el logout de los usuarios
    """

    def get(self, request, *args, **kwargs):
        """
        Por get simplemente se deslogea el usuario conectado y se redirige
        al login, si la session a finalizado
        """
        if not request.META.get('HTTP_X_REQUESTED_WITH'):
            # Si esta variable llega es ajax, sino, es una peticion
            # normal y ejecuta el post
            return self.post(request, *args, **kwargs)

        if self.object_session.check_seccion() is False:
            self.object_user.logout(False)
            return HttpResponse(1, content_type='application/html')
        else:
            return HttpResponse(0, content_type='application/html')

    def post(self, request, *args, **kwargs):
        """
        Elimina la variable de session y procede a cerrar las sessiones,
        luego se verifica de donde proviene la peticion para retornar
        el HttpResponse adecuado.
        """
        try:
            request.session.flush()
        except Exception:
            pass

        self.object_user.logout()
        return HttpResponseRedirect(ACCESO_URL)


class PrincipalComercializadoraChangeListView(PrincipalView):
    """
    Clase encargada de hacer el cambio de comercializadora.
    """
    template_name = 'account_change_comercilizadora.html'


class PrincipalComercializadoraChangeProcessView(PrincipalView):
    """
    Clase encargada de hacer el cambio de comercializadora.
    """

    def get(self, request, *args, **kwargs):
        """
        Al realizar la peticion por get procedo reenviarla al post
        """
        return self.post(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Hace un login con el user iniciado y la comercializadora indicada,
        en caso de error se retorna un 404
        """

        try:
            try:
                request.session.flush()
            except Exception:
                pass
            Users.objects.login(username=self.object_user.user,
                                request=request,
                                id_comercializadora=kwargs.get('pk')
                                )
            return HttpResponseRedirect(INDEX_URL)
        except Exception:
            from django.http import Http404
            raise Http404
