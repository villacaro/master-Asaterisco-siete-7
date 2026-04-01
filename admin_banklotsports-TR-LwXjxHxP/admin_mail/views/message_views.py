# -*- coding: utf-8 -*-
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_reverse import new_reverse
from admin_lib.util_views import MyViewBase
from admin_mail.forms import FilterMailsForm, MessageForm
from admin_mail.models import Message, MessageComer
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import naturaltime
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView


class MessajeView(MyViewBase):
    model = MessageComer

    def get_queryset(self):
        """
        Se prefiltran los grupos a los cuales tiene acceso el usuario
        """
        return self.model.objects.filter(
            comercializadora=self.object_comercializadora
        )


class MessajeCreateView(MyViewBase, CreateView):
    model = Message
    form_class = MessageForm


class MessajeDeleteView(MessajeView, DeleteView):

    def get_success_url_force(self):
        return reverse(
            'admin_mail_message_list_{0}'.format(
                self.object.get_tray_group_display().lower()
            )
        )

    def get_object(self):
        try:
            pk = self.request.POST.get('delete', None)
            if pk is None:
                pk = self.request.POST.get('archive', None)
            return MessageComer.objects.get(
                pk=pk
            )
        except MessageComer.DoesNotExist:
            from django.http import Http404
            raise Http404

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.tray_group == MessageComer.TRAY_GROUP_RECYCLE:
            if 'delete' in self.request.POST:
                return super(MyViewBase, self).delete(self, request, *args, **kwargs)

        if self.object.tray_group == MessageComer.TRAY_GROUP_SENT:
            url_name = 'admin_mail_message_list'
        else:
            url_name = 'admin_mail_message_list_{0}'.format(
                self.object.get_tray_group_display().lower()
            )

        if 'archive' in self.request.POST:
            self.object.tray_group = MessageComer.TRAY_GROUP_ARCHIVED
        else:
            self.object.tray_group = MessageComer.TRAY_GROUP_RECYCLE

        self.object.save(update_fields=['tray_group'])
        messages.warning(
            request,
            '¡El mensaje se a movido a {0}'
            ''.format(
                self.object.get_tray_group_display().lower()
            )
        )
        return HttpResponseRedirect(
            reverse(
                url_name
            )
        )


class MessajeDetailView(MessajeView, DetailView):

    def get_object(self):
        self.object = super(MessajeDetailView, self).get_object()
        if self.object.read is False:
            self.object.read = True
            self.object.save(update_fields=['read'])
        return self.object


class MessajeListView(MessajeView, ListView):

    def get_queryset(self):
        """
        Se prefiltran los grupos a los cuales tiene acceso el usuario
        """
        queryset = super(MessajeListView, self).get_queryset()

        if self.request.GET.get('priority'):
            queryset = queryset.filter(
                message__priority=self.request.GET.get('priority')
            )

        return queryset.filter(
            tray_group=self.filtro_list
        ).select_related(
            'message'
        )

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(MessajeListView, self).get_context_data(**kwargs)
        context['name_url_data_table'] = new_reverse(self, self.name_url_data_table)
        context['form'] = FilterMailsForm()

        return context


class BaseDatatableView(BaseDatatableView):
    # Modelo de la lista
    model = MessageComer
    # Orden del filtro
    order_columns = ['-message__send_at']
    # Fields de busqueda
    filter_search = 'message__subject'

    opcions_url = [
    ]

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []

        add_color = 'link'
        for x, item in enumerate(qs):
            add = ''
            if item.read is False:
                add = add_color

            priority = ''
            if item.message.priority == Message.PRIORITY_HIGH:
                priority = 'tag-red'
            elif item.message.priority == Message.PRIORITY_MEDIUM:
                priority = 'tag-yellow'
            else:
                priority = 'tag-green'

            json_data.append([
                (x + 1 + acarreo),
                '<a class="f show label {2}" href="{0}">{1}</a>'.format(
                    new_reverse(self, 'admin_mail_message_detail', kwargs={'pk': item.pk}),
                    item.message.subject,
                    add,
                ),
                '<i title="{0}" class="icon-clock"><i>{1}'.format(
                    item.message.send_at,
                    naturaltime(item.message.send_at)
                ),
                '<span class="tag {0}">{1}</span>'.format(
                    priority,
                    item.message.get_priority_display()
                ),
                self.get_opcions(item)
            ])
        return json_data

    def get_opcions(self, item):
        opcions = ''
        opcions += '<div class="btn-group btn-group-73">'
        opcions += ''
        class_css = 'btn btn-xs btn-ico btn-default'
        if item.get_tray_diff_archived():
            opcions += '<button id="_delete" type="submit" value="{0}" name="archive" class=" {1}">'.format(
                item.pk,
                class_css
            )
            opcions += '<i class="icon-save"></i>'
            opcions += '</button>'

        opcions += '<button id="_delete" type="submit" value="{0}" name="delete" class=" {1}">'.format(
            item.pk,
            class_css
        )
        opcions += '<i class="icon-delete"></i>'
        opcions += '</button>'

        opcions += '</div>'

        return opcions


class MessajeRecibidosListView(MessajeListView):
    filtro_list = MessageComer.TRAY_GROUP_RECEIVED
    name_url_data_table = 'admin_mail_message_list_recibidos_datatables'


class MessajeRecibidosListDatatableView(MessajeRecibidosListView, BaseDatatableView):
    pass


class MessajeEnviadosListView(MessajeListView):
    filtro_list = MessageComer.TRAY_GROUP_SENT
    name_url_data_table = 'admin_mail_message_list_enviados_datatables'


class MessajeEnviadosListDatatableView(MessajeEnviadosListView, BaseDatatableView):
    pass


class MessajeArchivadosListView(MessajeListView):
    filtro_list = MessageComer.TRAY_GROUP_ARCHIVED
    name_url_data_table = 'admin_mail_message_list_archivados_datatables'


class MessajeArchivadosListDatatableView(MessajeArchivadosListView, BaseDatatableView):
    pass


class MessajePapeleraListView(MessajeListView):
    filtro_list = MessageComer.TRAY_GROUP_RECYCLE
    name_url_data_table = 'admin_mail_message_list_papelera_datatables'


class MessajePapeleraListDatatableView(MessajePapeleraListView, BaseDatatableView):
    pass
