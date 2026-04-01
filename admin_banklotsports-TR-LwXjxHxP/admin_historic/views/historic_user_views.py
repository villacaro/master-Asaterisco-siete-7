# -*- coding: utf-8 -*-

from admin_banklotsports.settings import FORMAT_STR_DATE_3
from admin_historic.forms import FechasAndModulosForm
from admin_historic.models import MODULES, SessionsDetail
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero
from admin_lib.util_icons import Icons
from admin_users.forms import FilterByProfileAndComerForm
from admin_users.views.users_views import UsersDetailView, UsersListView
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.db.models import Q


class HistoricUsersListView(UsersListView):
    """
    Clase usada para listar los usuarios, y poder visualizar su auditoria,
    hereda de UsersListView, donde se definio el queryset optimizado
    para ver solo los usuarios correspondientes.
    """
    form_class = FilterByProfileAndComerForm
    template_name = 'admin_historic/users/users_list.html'


class HistoricUsersDatatableView(HistoricUsersListView, BaseDatatableView):

    # Orden del filtro
    order_columns = None

    def get_initial_queryset(self):
        self.opcions_url = [
            'admin_historic_users_detail$' + Icons.folder_open,
        ]
        qs = self.get_queryset().only('user', 'last_login')
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            last_login = '........'
            detail = ''
            if item.sessions_set.exists():
                last_login = '<i class="icon-clock"><i>{0}'.format(
                    naturaltime(item.last_login))

                detail = ''
                keys = {'pk': item.pk, }
                detail = self.get_urls('', 'btn btn-xs btn-ico btn-default', **keys)

            comercializadoras = ''
            for comercializadora in item.get_query_comercializadoras_level(item.profile.codename).only('id'):
                comercializadoras += '<span class="tag tag-blue">{0}</span> '.format(
                    comercializadora.get_object()
                )

            json_data.append([
                (x + 1 + acarreo),
                item.user,
                item.get_status().name,
                comercializadoras,
                '<span title="{0}">{1}</span>'.format(
                    item.last_login,
                    last_login
                ),
                detail
            ])

        return json_data


class HistoricUsersDetailView(UsersDetailView):
    """
    clase usada para mostrar todos los detalles de la auditoria del usuario
    """
    filter_form = None
    form_class = FechasAndModulosForm
    template_name = 'admin_historic/users/users_detail.html'

    def get_list_sessions_detail(self):
        """
        Obtiene todo el detalle de una o muchas sessiones segun filtros
        """
        user = self.request.GET.get('user')
        fecha_inicio = self.request.GET.get('fecha_inicio') + hora_cero
        fecha_fin = self.request.GET.get('fecha_fin') + hora_23
        module = self.request.GET.get('tipo')

        queryset = SessionsDetail.objects.filter(
            session__user_id=user,
            created_at__range=(fecha_inicio, fecha_fin),
        ).exclude(
            ref__startswith='admin_juego.jugadas'
        ).exclude(
            ref__startswith='admin_juego.encuentrosdetail'
        ).exclude(
            ref__startswith='admin_juego.encuentrosmodalidades'
        ).exclude(
            ref__startswith='admin_resultados.anotaciones'
        ).exclude(
            ref__startswith='admin_resultados.anotacionesdetail'
        ).exclude(
            ref__startswith='admin_resultados.resultadosrestric'
        )

        if module in MODULES:
            subquery = Q()
            for modul in MODULES[module]:
                subquery |= Q(ref__startswith=modul)

            queryset = queryset.filter(
                subquery
            )

        if module == 'ms':
            queryset |= SessionsDetail.objects.filter(
                session__user_id=user,
                userprocess__codename__in=['process_login', 'process_logout'],
                created_at__range=(fecha_inicio, fecha_fin),
            )

        return queryset.order_by('-created_at').select_related('userprocess')

    def get_filter_form(self):
        """
        Retorna el formulario de la instancia,
        de ya estar inicializado devuelve el que esta en memoria
        """
        if self.filter_form is None:
            if self.request.method == 'POST':
                self.filter_form = self.form_class(self.request.POST,
                                                   **self.get_form_kwargs())
                if self.filter_form.is_valid():
                    pass

                self.fecha_inicio = self.filter_form.cleaned_data[
                    'fecha_inicio'] + hora_cero
                self.fecha_fin = self.filter_form.cleaned_data[
                    'fecha_fin'] + hora_23
            else:
                self.filter_form = self.form_class(**self.get_form_kwargs())
                fecha = self.filter_form.fields['fecha_inicio'].initial
                self.fecha_inicio = fecha + hora_cero
                self.fecha_fin = fecha + hora_23

        return self.filter_form


class HistoricAccountDetailView(HistoricUsersDetailView):

    def get_object(self, queryset=None):
        return self.object_user

    def get_context_data(self, **kwargs):
        """
        Se añade al context data una variable para indicar que url imprimir,
        ya que esta vista es para el usuario asociado y por la otra not
        podria acceder a sus datos directamente
        """
        context = super(HistoricAccountDetailView,
                        self).get_context_data(**kwargs)
        context['is_account'] = True
        return context


class HistoricUsersDetailDatatableView(HistoricUsersDetailView, BaseDatatableView):
    # Modelo de la lista
    model = SessionsDetail
    # Orden del filtro
    order_columns = ['-created_at']

    def get_initial_queryset(self):
        self.opcions_url = [
            'admin_historic_app_model_ref_detail$' + Icons.doc_text_inv,
        ]
        qs = self.get_list_sessions_detail()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            opcions = '---'

            if item.ref:
                keys = {
                    'app': item.get_app(),
                    'model': item.get_model(),
                    'ref': item.get_obj_id(),
                    'pk': item.pk,
                }
                content = item.json.get('object', '')
                opcions = self.get_urls(content, '', **keys)

            json_data.append([
                (x + 1 + acarreo),
                '<span title="{0}"><i class="icon-clock"><i>{1}</span>'.format(
                    naturaltime(item.created_at),
                    item.created_at.strftime(FORMAT_STR_DATE_3)
                ),
                item.get_module(),
                item.userprocess.name,
                opcions,
            ])
        return json_data
