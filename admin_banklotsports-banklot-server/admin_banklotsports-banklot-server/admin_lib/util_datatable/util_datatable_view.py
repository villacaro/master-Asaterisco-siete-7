# -*- coding: utf-8 -*-

from admin_lib.util_icons import VerboseIcons
from admin_lib.util_reverse import new_reverse
from django.contrib import messages

from .util_mixins import JSONResponseView


class DatatableMixin(object):
    """ JSON data for datatables
    """
    model = None
    columns = []
    order_columns = []
    footer_columns = []
    start = 0
    max_display_length = 100
    filter_search = None
    ordenar = True
    pagin_process = True

    # max limit of records returned, do not allow to kill our server by huge
    # sets of data

    def initialize(*args, **kwargs):
        pass

    def get_order_columns(self):
        """ Return list of columns used for ordering
        """
        return self.order_columns

    def get_columns(self):
        """ Returns the list of columns that are returned in the result set
        """
        return self.columns

    def render_column(self, row, column):
        """ Renders a column on a row
        """
        if hasattr(row, 'get_%s_display' % column):
            # It's a choice field
            text = getattr(row, 'get_%s_display' % column)()
        else:
            try:
                text = getattr(row, column)
            except AttributeError:
                obj = row
                for part in column.split('.'):
                    if obj is None:
                        break
                    obj = getattr(obj, part)

                text = obj

        if hasattr(row, 'get_absolute_url'):
            return '<a href="%s">%s</a>' % (row.get_absolute_url(), text)
        else:
            return text

    def ordering(self, qs):
        """ Get parameters from the request and prepare order by clause
        """
        request = self.request
        # Number of columns that are used in sorting
        try:
            i_sorting_cols = int(request.REQUEST.get('iSortingCols', 0))
        except ValueError:
            i_sorting_cols = 0

        order = []
        order_columns = self.get_order_columns()
        for i in range(i_sorting_cols):
            # sorting column
            try:
                i_sort_col = int(request.REQUEST.get('iSortCol_%s' % i))
            except ValueError:
                i_sort_col = 0

            # sorting order
            s_sort_dir = request.REQUEST.get('sSortDir_%s' % i)

            sdir = '-' if s_sort_dir == 'desc' else ''

            sortcol = order_columns[i_sort_col]
            if isinstance(sortcol, list):
                for sc in sortcol:
                    order.append('%s%s' % (sdir, sc))
            else:
                order.append('%s%s' % (sdir, sortcol))
        if order and self.ordenar:
            return qs.order_by(*order)
        return qs

    def paging(self, qs):
        """ Paging
        """
        limit = min(int(self.request.REQUEST.get(
            'iDisplayLength', 10)), self.max_display_length)
        # if pagination is disabled ("bPaginate": false)
        if limit == -1:
            return qs
        self.start = int(self.request.REQUEST.get('iDisplayStart', 0))
        offset = self.start + limit
        return qs[self.start:offset]

    def get_initial_queryset(self):
        if not self.model:
            raise NotImplementedError(
                "Need to provide a model or implement get_initial_queryset!")
        return self.model.objects.all()

    def filter_queryset(self, qs):
        """
        qs_params = None
        search = self.request.GET.get('sSearch', None)
        if search and self.filter_search:
            filters = {}
            q = Q()
            for key in self.filter_search:
                filters = {}
                filters[key+"__icontains"] = search
                q = q | Q( ** filters )
            qs_params = qs_params | q if qs_params else q
            qs = qs.filter(qs_params)
        """
        return qs

    def prepare_footeresults(self, qs):
        """
        data = []
        for item in qs:
            data.append([item])
        return data
        """
        return []

    def get_opcions(self, pk, tipo=None):
        opcions = ""
        opcions += "<div class='btn-group btn-group-73'>"

        if tipo is None:
            for url in self.opcions_url:
                url = url.split("$")
                if len(url) == 2:
                    opcions += "<a class='btn btn-xs btn-ico btn-default' href='" + \
                        new_reverse(self, url[0], kwargs={'pk': pk}) + "'>"
                    opcions += "<i title='" + \
                        VerboseIcons.get(url[1], '') + \
                        "' class='" + url[1] + "'></i></a>"
                elif len(url) == 3:
                    opcions += "<a class='btn btn-xs btn-ico btn-default' href='" + \
                        new_reverse(self, url[0], kwargs={
                                    'pk': pk}) + url[2] + "'>"
                    opcions += "<i title='" + \
                        VerboseIcons.get(url[1], '') + \
                        "' class='" + url[1] + "'></i></a>"
        else:
            for url in self.opcions_url:
                url = url.split("$")
                opcions += "<a class='btn btn-xs btn-ico btn-default' href='" + \
                    new_reverse(self, url[0], kwargs={
                                'pk': pk, 'type': tipo}) + "'>"
                opcions += "<i title='" + \
                    VerboseIcons.get(url[1], '') + \
                    "' class='" + url[1] + "'></i></a>"
        return opcions

    def get_urls(self, content, clase, **parameters):
        urls = "<div class='btn-group btn-group-74'>"
        for url in self.opcions_url:
            url = url.split("$")
            if len(url) == 2:
                urls += "<a class='" + clase + "' href='" + \
                    new_reverse(self, url[0], kwargs=parameters) + "'>"
                urls += "<i title='" + \
                    VerboseIcons.get(url[1], '') + "' class='" + \
                    url[1] + "'></i>" + content + "</a>"
            elif len(url) == 3:
                urls += "<a class='" + clase + "' href='" + \
                    new_reverse(
                        self, url[0], kwargs=parameters) + url[2] + "'>"
                urls += "<i title='" + \
                    VerboseIcons.get(url[1], '') + "' class='" + \
                    url[1] + "'></i>" + content + "</a>"
        urls += "</div>"
        return urls

    def get_context_data(self, *args, **kwargs):
        request = self.request
        self.initialize(*args, **kwargs)

        qs = self.get_initial_queryset()

        qs = self.filter_queryset(qs)

        # number of records after filtering
        if self.pagin_process:
            try:
                self.total_display_records = qs.count()
            except Exception:
                self.total_display_records = len(qs)

        aaFooter = self.prepare_footeresults(qs)

        search = self.request.GET.get('sSearch', None)

        if self.order_columns:
            qs = self.ordering(qs)

        if len(search) == 0 and self.pagin_process:
            qs = self.paging(qs)

        # prepare output data
        aaData = self.prepare_results(qs, self.start)

        if len(search) > 1:
            aaDataCopy = aaData
            aaData = []
            for data in aaDataCopy:
                if any(search.lower() in str(s).lower() for s in data):
                    aaData.append(data)

            self.total_display_records = len(aaData)

        ret = {
            'sEcho': int(request.REQUEST.get('sEcho', 0)),
            'iTotalRecords': self.total_display_records,
            'iTotalDisplayRecords': self.total_display_records,
            'aaData': aaData,
            'aaFooter': aaFooter
        }

        mensajes = messages.get_messages(self.request)
        if mensajes:

            send_mensajes = []
            for mensaje in mensajes:
                send_mensaje = {}
                send_mensaje['message'] = str(mensaje)
                send_mensaje['tags'] = str(mensaje.tags)
                send_mensajes.append(send_mensaje)

            ret['messages'] = send_mensajes
        else:
            ret['messages'] = []

        return ret


class BaseDatatableView(DatatableMixin, JSONResponseView):

    def dispatch(self, request, *args, **kwargs):
        """
        Inicializa los objetos de la clase, apenas se invoca la vista
        """
        if "object_session" in kwargs:
            self.object_comercializadora = kwargs.pop(
                "object_comercializadora")
            self.object_user = kwargs.pop("object_user")

        return super(BaseDatatableView, self).dispatch(request, *args, **kwargs)
