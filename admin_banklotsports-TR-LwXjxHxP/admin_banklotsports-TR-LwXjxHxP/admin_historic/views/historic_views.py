# -*- coding: utf-8 -*-
from admin_banklotsports.settings import FORMAT_STR_DATE_3
from admin_historic.models import SessionsDetail
from admin_historic.process_audit import (
    AdminComercializacionProcess, AdminJuegoProcess, AdminResultadoProcess, ProcessModelGeneric,
)
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_icons import Icons
from admin_lib.util_views import MyViewBase
from admin_users.views.users_views import UsersDetailView
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.views.generic import ListView


class HistoricUsersDetailDetailView(UsersDetailView):
    model = SessionsDetail
    template_name = 'admin_historic/sessionsdetail/sessionsdetail_detail.html'

    def get_object(self, queryset=None):
        return self.object_user

    def get_context_data(self, **kwargs):
        """
        Se añade al context data el form reference al filtro de sessiones del usuario
        """
        context = super(HistoricUsersDetailDetailView,
                        self).get_context_data(**kwargs)
        context['is_detail_detail'] = True

        try:
            obj = SessionsDetail.objects.get(
                pk=self.kwargs['pk'],
                ref__isnull=False)

            app = obj.get_app()
            model = obj.get_model()
            context['object_session'] = obj
            if app == 'admin_juego':
                process = AdminJuegoProcess()
                if model == 'encuentros':
                    context['object_session_refs'] = process.process_encuentros(
                        context['object_session'])
                else:
                    process = ProcessModelGeneric()
                    context['object_session_refs'] = process.process(context['object_session'])

            elif app == 'admin_resultados':
                process = AdminResultadoProcess()
                if model == 'resultados':
                    context['object_session_refs'] = process.process_resultados(
                        context['object_session']
                    )
            elif app == 'admin_comercializacion':
                if model == 'factorriesgo':
                    process = AdminComercializacionProcess()
                    context['object_session_refs'] = process.process_factorriesgo(
                        context['object_session'])
                else:
                    process = ProcessModelGeneric()
                    context['object_session_refs'] = process.process(context['object_session'])
            elif app == 'admin_permisologia':
                if model == 'permissionssalesrestrictions':
                    process = AdminComercializacionProcess()
                    context['object_session_refs'] = process.process_permissionssalesrestrictions(
                        context['object_session'])
                else:
                    process = ProcessModelGeneric()
                    context['object_session_refs'] = process.process(context['object_session'])
            else:
                process = ProcessModelGeneric()
                context['object_session_refs'] = process.process(context['object_session'])

            '''
            elif context['object_session'].get_app() == "admin_comercializacion":
                process = AdminComercializacionProcess()
                if model == 'bloques':
                    context['object_session_refs'] = process.process_comercializacion(
                        context['object_session']
                    )
            '''
        except SessionsDetail.DoesNotExist:
            from django.http import Http404
            raise Http404
        return context


class HistoricAccountDetailDetailView(HistoricUsersDetailDetailView):
    template_name = 'admin_historic/sessionsdetail/sessionsdetail_detail.html'


class HistoricAppModelRefView(MyViewBase, ListView):
    model = SessionsDetail

    def get_queryset(self):
        """
        Se prefiltran los procesos deacuerco a los datos del kwargs
        """
        if self.request.GET.get('app'):
            ref_prefix = '{0}.{1}.{2}'.format(
                self.request.GET.get('app'),
                self.request.GET.get('model').lower(),
                self.request.GET.get('ref'),
            )

            queryset = SessionsDetail.objects.filter(ref_related=ref_prefix)\
                .exclude(ref__startswith='admin_juego.jugadas')\
                .exclude(ref__startswith='admin_juego.encuentrosdetail')\
                .exclude(ref__startswith='admin_juego.encuentrosmodalidades')\
                .exclude(ref__startswith='admin_resultados.anotaciones')\
                .exclude(ref__startswith='admin_resultados.anotacionesdetail')\
                .exclude(ref__startswith='admin_resultados.resultadosrestric')

            queryset |= SessionsDetail.objects.filter(ref=ref_prefix)

            return queryset.order_by('-created_at')
        return SessionsDetail.objects.none()


class HistoricAppModelRefDetailView(HistoricUsersDetailDetailView):
    model = SessionsDetail


class HistoricAppModelRefDatatableView(HistoricAppModelRefView, BaseDatatableView):
    order_columns = None

    def get_initial_queryset(self):
        self.opcions_url = [
            'admin_historic_app_model_ref_detail$' + Icons.doc_text_inv,
        ]
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            opcions = '---'
            user = ''
            comer = ''
            ip = ''
            if item.session:
                user = '{0}'.format(item.session.user)
                comer = '{0}'.format(item.session.get_comercializadora())
                ip = item.session.ip,

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
                "<span title={0}><i class='icon-clock'><i>{1}</span>".format(
                    naturaltime(item.created_at),
                    item.created_at.strftime(FORMAT_STR_DATE_3)
                ),
                user,
                comer,
                item.userprocess.name,
                ip,
                opcions
            ])
        return json_data
