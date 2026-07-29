# -*- coding: utf-8 -*-
from datetime import datetime as datetime_date

from admin_apuestas.models import Tickets, TicketsDetail
from admin_asterisco7.settings import CACHES_CONF_TIME, FORMAT_STR_DATETIME
from admin_comercializacion.task import AsyncProcessInvokeMethod
from admin_finanzas.models import Comercializadora
from admin_juego.models import SistemaJuego
from admin_lib.util_funtions import FiltersCadenaCsv
from admin_lib.util_json import JsonDumps
from admin_status.models import Status
from django.contrib import messages
from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.cache import cache
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.timezone import now
from django.views.generic import DeleteView, DetailView, View


class MyViewBaseDetailView(DetailView):

    def get_context_data(self, **kwargs):
        context = super(MyViewBaseDetailView, self).get_context_data(**kwargs)
        app = self.model().__module__.split('.')[0]
        var_cache = {
            'email': self.object_user.email,
            'object': self.object,
            'template_name': '{0}/{1}/{2}_detail_email.html'.format(
                app,
                self.object.prefix_filter_plural,
                self.object.prefix_filter
            ),
            'reverse': reverse(
                '{0}_{1}_detail'.format(
                    app,
                    self.object.prefix_filter_plural
                ),
                kwargs={'pk': self.object.pk}
            ),
        }

        context['cache_key'] = '{0}-{1}-{2}-generate'.format(
            self.object,
            now().strftime(FORMAT_STR_DATETIME),
            self.object_user
        )
        cache.set(
            context['cache_key'],
            var_cache,
            CACHES_CONF_TIME[app]['print_detail']
        )
        return context


class MyViewBaseDeleteView(DeleteView):

    def delete(self, request, *args, **kwargs):
        app = self.model().__module__.split('.')[0]
        model = self.model().__class__.__name__.lower()

        concat_delete = '_delete_{0}'.format(
            now().strftime(FORMAT_STR_DATETIME))
        self.object = self.get_object()
        name = self.object.nombre
        self.object.nombre += concat_delete
        self.object.status = Status.get_status_by_codename('status_eliminado')
        self.object.save(update_fields=['nombre', 'status', 'updated_at'])

        kwargs_async = {
            'session_id': '{0}'.format(self.object_session.pk),
            'parametros': {
                'concat_delete': concat_delete,
            },
        }
        kwargs_async['parametros'][
            'filter'] = self.object.prefix_filter + '_id'
        kwargs_async['parametros']['id'] = self.object.pk

        # Invocando proceso asyncrono que ejecutara la funcion
        AsyncProcessInvokeMethod.func_delay(
            MyViewBaseDeleteView.AsyncProcessInvokeMethodDelete,
            kwargs_async
        )

        if isinstance(self.model()._meta.verbose_name, str):
            verbose = self.model()._meta.verbose_name
        else:
            verbose = model

        messages.warning(
            self.request,
            '¡Enhorabuena! {0} {1} '
            'Esta siendo eliminada, esto solo llevara unos segundos!'.format(
                verbose,
                name
            )
        )

        return HttpResponseRedirect(
            reverse('{0}_{1}_list'.format(app, model)) +
            self.get_success_url_filter_form()
        )

    @staticmethod
    def AsyncProcessInvokeMethodDelete(kwargs):
        messaje = []
        kwargs_filter = {}
        kwargs_filter[kwargs.get('filter')] = kwargs.get('id')
        comercializadora = Comercializadora.objects.get(
            **kwargs_filter).get_object()
        status = Status.get_status_by_codename('status_eliminado')

        class deleteObj(object):

            def __init__(self, concat_delete):
                super(deleteObj, self).__init__()
                self.i_objects = 0
                self.concat_delete = concat_delete

            def delete_comer(self, comer):
                self.i_objects += 1
                if comer.prefix_filter == 'taquilla':
                    comer.set_new_status(status.codename)
                else:
                    comer.status = status
                    comer.nombre += self.concat_delete
                    comer.save(
                        update_fields=[
                            'nombre',
                            'status',
                            'updated_at'])
                    for comer_of in comer.get_offspring():
                        self.delete_comer(comer_of)

        obj_delete = deleteObj(kwargs.get('concat_delete'))
        for comer in comercializadora.get_offspring():
            obj_delete.delete_comer(comer)

        messaje.append('Objetos eliminados: {0}'.format(obj_delete.i_objects))
        return messaje


class MyViewBase(object):
    """
    Clase usada como base en las distintas vistas.
    que sirve para generar informacion directa en los templates
    sin necesidad de definirla en el context_data.

    atributos:
        info_system: si esta en true se envia automaticamente la informacion
                    del sistema en el context_data para renderisar en el
                    template

        info_menu: si esta en true se consulta el menu asociado a la session,
                    dicho menu cuenta con optimizaciones de cache y se genera en el
                    template base.

        info_user: si esta en true se consulta la info del usuario y se
            envia al template

        _profile: atributo con una instanca del profile referente a la
            instancia iniciada

        object_session: atributo con la instancia de la session iniciada

        object_user = atributo con la instancia del usuario

        object_comercializadora = atributo con la instancia de la comercializadora,
            activa

        object_sistema_juego = atributo con la instancia del sistema de
            juego asociado a la comercializadora activa

        object_sistema_resultados = atributo con la instancia del sistema de resultados
            asociado para la comercializadora activa

        object_sistema_logros = atributo con la instancia del sistema de los logros
            asociado para la comercializadora activa

        template_name: nombre de la plantilla, por defecto no esta definida

        relate_delete: atributo por defecto en None, al activarlo en alguna
        clase hija, se hara una consulta de todas la relaciones de los objetos
        hacia abajo al ser eliminados

        relate_delete_validate: en caso de estar activo verifica en el post
            si el objeto tiene relaciones y impide su eliminacion, por defecto
            esta en falso

        filter_form: atributo solo definido en las clases hijas,
            se usa generalmente en los listar, representa su formulario

        get_success_url_force: funcion no definida es caso de estarlo devuelve
            un url reversible

    """

    info_system = True
    info_menu = True
    info_user = True

    _profile = None

    object_session = None
    object_user = None
    object_user_ip = None
    object_comercializadora = None
    object_sistema_juego = None
    object_sistema_resultados = None
    object_sistema_logros = None

    template_name = None

    relate_delete = None
    relate_delete_validate = False

    def get_relate_sales(self):
        nodo = []
        if not hasattr(self, 'object'):
            self.object = self.get_object()

        if hasattr(self.object, 'get_prefix_kwargs_by_level_tickets'):
            kwargs = {}
            kwargs[self.object.get_prefix_kwargs_by_level_tickets()
                   ] = self.object.pk
            # Excluyo todos los tickets anulados
            nodo = [
                Tickets._meta.verbose_name_plural,
                Tickets.objects.filter(
                    **kwargs
                ).exclude(
                    status__codename__in=[
                        'status_anulado', 'status_anulado_automatico']
                ).count(),
            ]
        elif hasattr(self.object, 'get_prefix_kwargs_by_level_tickets_details'):
            kwargs = {}
            kwargs[self.object.get_prefix_kwargs_by_level_tickets_details()
                   ] = self.object.pk
            nodo = [
                TicketsDetail._meta.verbose_name_plural,
                TicketsDetail.objects.filter(**kwargs).count(),
            ]
        return nodo

    def get_relate(self):
        """
        Consulta todos los hijos relacionados con el
        objeto de la instancia actual
        """
        nodos = []
        self.object = self.get_object()
        for attr in dir(self.object):
            """
            recorre todos los atributos (que terminan en _set) ya que
            son relaciones hacia abajo, y al eliminar el objeto ellos
            tambien se eliminaran
            """
            if attr.endswith('_set'):
                model = None
                querryset = getattr(self.object, attr)
                if querryset.all().exists():
                    querry_one = querryset.all()[0]
                    if isinstance(querry_one._meta.verbose_name_plural, str):
                        model = querry_one._meta.verbose_name_plural
                    else:
                        model = querry_one.__class__.__name__
                    querry_count = querryset.all().count()
                    nodos.append([model, querry_count, ])

        nodo_venta = self.get_relate_sales()
        if nodo_venta:
            nodos.append(nodo_venta)
        return nodos

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(MyViewBase, self).get_context_data(**kwargs)

        if self.relate_delete:
            context['relate_delete'] = self.get_relate()

        if hasattr(self, 'filter_form'):
            context['form'] = self.get_filter_form()

        return context

    def get_template_names(self):
        """
        Obtiene el template asociado dependiendo del modelo
        definido en las clases hijas,
        o lo obtiene directamente del atributo definido
        """
        if self.template_name is None:
            tpl = super(MyViewBase, self).get_template_names()[0]
            app = self.model._meta.app_label
            mdl = self.model().__class__.__name__.lower()
            self.template_name = tpl.replace(app, '{0}/{1}'.format(app, mdl))
        return [self.template_name]

    def get_filter_form(self):
        """
        Retorna el formulario de la instancia,
        de ya estar inicializado devuelve el que esta en memoria
        """
        if self.filter_form is None:
            self.filter_form = self.form_class(
                self.request.GET,
                **self.get_form_kwargs()
            )
        return self.filter_form

    def get_form_kwargs(self):
        """
        Funcion usada para pasarle parametros en el kwargs al formulario
        """
        try:
            kwargs = super(MyViewBase, self).get_form_kwargs()
        except Exception:
            kwargs = {}

        kwargs.update({'view': self})

        return kwargs

    def get_profile(self):
        """
        Retorna el profile relacionado con la session instanciada
        """
        if self._profile is None:
            comercializadora = getattr(self, 'object_comercializadora', None) or self.kwargs.get('object_comercializadora')
            if comercializadora is None:
                user = self.kwargs['object_user']
                self._profile = user.profile
            else:
                self._profile = comercializadora.get_type()

        return self._profile

    def set_execute_function_by_profile(self, **kwargs):
        """
        Ejecuta la funcion de la instancia indicada,
        dependiendo de el profile de la session,
        con un prefijo indicado.
        """
        try:
            function = getattr(
                kwargs.get('instance'),
                '{0}_{1}'.format(
                    kwargs.get('prefix'),
                    self.get_profile().codename
                )
            )
            return function(**kwargs)
        except Exception:
            raise NotImplementedError(
                'la funcion {0}_{1} no esta implementada'.format(
                    kwargs.get('prefix'),
                    self.get_profile().codename
                )
            )

    def get_success_url_filter_form(self):
        """
        Este metodo debe implementarse en las clases hijas
        """
        return ''

    def get_next_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return ''

    def get_success_url(self):
        try:
            """
            en caso de algun error ejecuta el get_succe_url del padre
            """
            if self.request.method == 'POST':
                app = self.model().__module__.split('.')[0]
                model = self.model().__class__.__name__.lower()

                if isinstance(self.model()._meta.verbose_name, str):
                    verbose = self.model()._meta.verbose_name
                else:
                    verbose = model

                if self.object:
                    verbose_object = self.object
                else:
                    verbose_object = ''

                if '_delete' in self.request.POST:
                    messages.warning(
                        self.request,
                        '¡Enhorabuena! {0} {1} '
                        'ha sido eliminado con éxito!'.format(
                            verbose,
                            verbose_object
                        )
                    )

                    if hasattr(self, 'get_success_url_force'):
                        force = self.get_success_url_force()
                        if force:
                            return force + self.get_success_url_filter_form()

                    return reverse('{0}_{1}_list'.format(app, model)) + self \
                        .get_success_url_filter_form()

                messages.success(
                    self.request,
                    '¡Enhorabuena! {0} {1} '
                    'ha sido guardado con éxito!'.format(
                        verbose,
                        verbose_object
                    )
                )

                if hasattr(self, 'get_success_url_force'):
                    force = self.get_success_url_force()
                    if force:
                        return force + self.get_success_url_filter_form()

                if self.request.POST.get('next'):
                    return self.request.POST.get('next')
                elif self.request.POST['_save'] == '_save':
                    return reverse('{0}_{1}_list'.format(app, model)) + '' \
                        '' + self.get_success_url_filter_form()
                elif self.request.POST['_save'] == '_continue':
                    return reverse(
                        '{0}_{1}_update'.format(app, model),
                        kwargs={'pk': self.object.pk}
                    )
                elif self.request.POST['_save'] == '_addanother':
                    return reverse('{0}_{1}_create'.format(app, model))
                elif self.request.POST['_save'] == '_detail':
                    return reverse(
                        '{0}_{1}_detail'.format(app, model),
                        kwargs={'pk': self.object.pk}
                    )
        except Exception:
            raise
        return super(MyViewBase, self).get_success_url()

    def dispatch(self, request, *args, **kwargs):
        """
        Inicializa los objetos de la clase, apenas se invoca la vista
        """
        if 'object_session' in kwargs:
            self.object_session = kwargs.pop('object_session')
            self.object_user = kwargs.pop('object_user')
            self.object_user_ip = kwargs.pop('object_user_ip')
            self.object_comercializadora = kwargs.pop(
                'object_comercializadora')
            self.object_sistema_juego = kwargs.pop('object_sistema_juego')

        return super(MyViewBase, self).dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        Verifica si la bandera de proteccion esta activa,
        y verifica si hay dependencias para impedir la eliminacion
        """

        if self.relate_delete_validate:
            nodo_sales = self.get_relate_sales()
            if nodo_sales and nodo_sales[1]:
                app = self.model().__module__.split('.')[0]
                model = self.model().__class__.__name__.lower()

                if isinstance(self.model()._meta.verbose_name, str):
                    verbose = self.model()._meta.verbose_name
                else:
                    verbose = model

                messages.error(
                    request,
                    '¡El objeto de {0} {1} no se puede eliminar!, posee ventas asociadas'
                    ''.format(
                        verbose,
                        self.object
                    )
                )

                return HttpResponseRedirect(
                    reverse('{0}_{1}_list'.format(app, model)) +
                    self.get_success_url_filter_form()
                )

        return super(MyViewBase, self).delete(self, request, *args, **kwargs)

    def get_object_sistema_resultados(self, comercializadora=None):
        if not self.object_sistema_resultados:
            if comercializadora:
                self.object_sistema_resultados = SistemaJuego.objects \
                    .get_sistema_resultados_by_comercializadora(
                        comercializadora
                    )
            else:
                self.object_sistema_resultados = SistemaJuego.objects \
                    .get_sistema_resultados_by_comercializadora(
                        self.object_comercializadora
                    )
        return self.object_sistema_resultados

    def get_object_sistema_logros(self, comercializadora=None):
        if not self.object_sistema_logros:
            if comercializadora:
                self.object_sistema_logros = SistemaJuego.objects \
                    .get_sistema_logros_by_comercializadora(
                        comercializadora
                    )
            else:
                self.object_sistema_logros = SistemaJuego.objects \
                    .get_sistema_logros_by_comercializadora(
                        self.object_comercializadora
                    )
        return self.object_sistema_logros

    def get_exist_sistema_logro(self, comercializadora=None):
        """
        Retorna verdadero solo si la comercializadora tiene un sistema de logros propio,
        o hereda de una comercializadora padre
        """
        return self.object_sistema_juego.pk != self.get_object_sistema_logros(
            comercializadora)

    def get_object(self):
        """
        Utiliza cache por objeto en ram para no ejecutar la funcion varias veces
        """
        self.object = getattr(self, 'object', None)
        if not self.object:
            self.object = super(MyViewBase, self).get_object()
        return self.object


class ReportsBaseView(View):
    # Bandera que consulta el query completo
    all_query = False
    # Bandera que valida las columnas de negocio a mostrar
    valid_columns = True

    # Nombres de los urls de pdf y csv respectivamente
    pdf_url = None
    csv_url = None
    datatable_url = None

    # Bandera de aplicar filtros
    apply_filters_juego = True
    apply_filters_cadena = True

    # Atributos para la generacion del cache
    name_report = ''
    template_print = ''

    # Codename del reporte para generacion de keys
    codename_report = ''

    def dispatch(self, request, *args, **kwargs):
        self.get_parameters()
        self.get_pertenece()

        if request.GET.get('action') == 'get_titles':
            prefix = 'get_titles_for_{0}'.format(self.agrupado)
            if hasattr(self, prefix):
                titles = getattr(self, prefix)()
            else:
                raise
            return HttpResponse(
                content=JsonDumps(
                    list(
                        titles
                    )
                ),
                content_type='application/json'
            )

        elif request.GET.get('action') == 'get_pdf' or request.GET.get('action') == 'get_csv':

            self.all_query = True
            if request.GET.get('cache'):
                if cache.get(self.get_key_report()):
                    self.cache_key = cache.get(self.get_key_report())
                else:
                    self.execute_all_process()
            else:
                self.execute_all_process()

            name_url = ''
            if request.GET.get('action') == 'get_pdf':
                name_url = self.pdf_url
            elif request.GET.get('action') == 'get_csv':
                name_url = self.csv_url

            return HttpResponseRedirect(
                reverse(
                    name_url,
                    kwargs={'cache_key': self.cache_key}
                )
            )

        return super(ReportsBaseView, self).dispatch(request, *args, **kwargs)

    def get_parameters(self):
        # Filtros Fechas
        self.fecha_inicio = self.request.GET.get('fecha_inicio')
        self.fecha_fin = self.request.GET.get('fecha_fin')

        # Filtros Cadena
        self.operadora = self.request.GET.get('operadora')
        self.bloque = self.request.GET.get('bloque')
        self.banca = self.request.GET.get('banca')
        self.distribuidor = self.request.GET.get('distribuidor')
        self.agencia = self.request.GET.get('agencia')

        # Filtros Juego
        self.deporte = self.request.GET.get('deporte')
        self.temporada = self.request.GET.get('temporada')
        self.encuentro = self.request.GET.get('encuentro')
        self.grupo_modalidad = self.request.GET.get('grupo_modalidad')
        self.modalidad = self.request.GET.get('modalidad')

        # Filtros agrupado
        self.agrupado = self.request.GET.get('orden')
        self.codigo = self.request.GET.get('codigo')

        # Rango en formato Date
        self.ini = datetime_date.strptime(self.fecha_inicio, '%Y-%m-%d')
        if self.fecha_fin:
            self.fin = datetime_date.strptime(self.fecha_fin, '%Y-%m-%d')

    def get_pertenece(self):

        if self.agencia:
            self.pertenece = Comercializadora.objects.get(
                agencia_id=self.agencia).get_object()
        elif self.distribuidor:
            self.pertenece = Comercializadora.objects.get(
                distribuidor_id=self.distribuidor).get_object()
        elif self.banca:
            self.pertenece = Comercializadora.objects.get(
                banca_id=self.banca).get_object()
        elif self.bloque:
            self.pertenece = Comercializadora.objects.get(
                bloque_id=self.bloque).get_object()
        elif self.operadora:
            self.pertenece = Comercializadora.objects.get(
                operadora_id=self.operadora).get_object()
        else:
            self.pertenece = self.kwargs[
                'object_comercializadora'].get_object()

        if self.valid_columns:
            self.get_valid_columns()

    def get_valid_columns(self):

        # Bandera para las columnas a mostrar
        if self.pertenece.get_is_apply_comision():
            self.show_comision = True
        else:
            self.show_comision = False

        if self.pertenece.get_is_apply_regalia():
            self.show_regalia = True
        else:
            self.show_regalia = False

        if self.pertenece.get_is_apply_participacion():
            self.show_participacion = True
        else:
            self.show_participacion = False

        if self.pertenece.get_is_apply_queda():
            self.show_queda = True
        else:
            self.show_queda = False

    def apply_filter_juego(self):
        if self.encuentro:
            self.ventas = self.ventas.filter(
                juegos__encuentro_id=self.encuentro)
        elif self.temporada:
            self.ventas = self.ventas.filter(
                juegos__temporada_id=self.temporada)
        elif self.deporte:
            self.ventas = self.ventas.filter(juegos__deporte_id=self.deporte)

    def execute_query(self):
        prefix = 'apply_presentation_for_{0}'.format(self.agrupado)
        if hasattr(self, prefix):
            self.query = getattr(self, prefix)()
        else:
            raise

        prefix_title = 'get_titles_for_{0}'.format(self.agrupado)
        if hasattr(self, prefix_title):
            self.titles = getattr(self, prefix_title)()
        else:
            raise

        self.footer = self.query['totales']
        self.content = self.query['detalle']

    def execute_all_process(self):
        self.get_hecho_venta()

        if self.apply_filters_cadena:
            self.apply_filter_cadena()

        if self.apply_filters_juego:
            self.apply_filter_juego()

        self.execute_query()
        self.set_cache()

        cache.set(
            self.get_key_report(),
            self.cache_key,
            CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
        )

    def get_key_report(self):
        return '{0}-{1}-{2}'.format(
            self.codename_report,
            now().strftime('%Y-%m-%d-%H'),
            self.kwargs['object_user'],
        )

    def get_parameters_send_get(self):
        keys = ''
        # Filtros Fechas
        keys += '&fecha_inicio=' + self.request.GET.get('fecha_inicio', '')
        keys += '&fecha_fin=' + self.request.GET.get('fecha_fin', '')

        # Filtros Cadena
        keys += '&operadora=' + self.request.GET.get('operadora', '')
        keys += '&bloque=' + self.request.GET.get('bloque', '')
        keys += '&banca=' + self.request.GET.get('banca', '')
        keys += '&distribuidor=' + self.request.GET.get('distribuidor', '')
        keys += '&agencia=' + self.request.GET.get('agencia', '')

        # Filtros Juego
        keys += '&deporte=' + self.request.GET.get('deporte', '')
        keys += '&temporada=' + self.request.GET.get('temporada', '')
        keys += '&encuentro=' + self.request.GET.get('encuentro', '')
        keys += '&grupo_modalidad=' + \
            self.request.GET.get('grupo_modalidad', '')
        keys += '&modalidad=' + self.request.GET.get('modalidad', '')

        # Filtros agrupado
        keys += '&orden=' + self.request.GET.get('orden', '')

        # Selecctor de data procesada
        keys += '&data_process=' + self.request.GET.get('data_process', '')

        # Filtros otros
        if self.codigo:
            keys += '&codigo=' + self.request.GET.get('codigo', '')
        return keys

    def get_hecho_venta(self):
        """
            Función que decide de que HECHO(Datamart) consultar las ventas
        """
        raise NotImplementedError('La función no esta implementada')

    def apply_filter_cadena(self):

        if self.pertenece.prefix_filter == 'master':
            self.ventas = self.ventas.filter(
                comercializacion__operadora_id__in=list(
                    self.pertenece.get_offspring().values_list(
                        'pk', flat=True)),
                comercializacion__bloque_id__isnull=False
            )
        else:
            if self.agrupado == 'agencia':
                self.ventas = self.ventas.filter(
                    ** self.pertenece.get_kwargs_hijos_agencia_dimension_arco_comercializadora()
                )
            else:
                self.ventas = self.ventas.filter(
                    ** self.pertenece.get_kwargs_hijos_dimension_arco_comercializadora()
                )

    def set_cache(self):
        if self.fecha_fin:
            fechas = '{0}/{1}'.format(
                self.fecha_inicio,
                self.fecha_fin
            )
        else:
            fechas = '{0}/{1}'.format(
                self.fecha_inicio,
                self.fecha_inicio
            )

        var_cache = {
            'filters_cadena': FiltersCadenaCsv(self.request),
            'titulo': 'Reporte - {0}'.format(self.name_report),
            'fecha': fechas,
            'titles': self.titles,
            'content': self.content,
            'footer': self.footer,
            'comercializador': self.kwargs['object_comercializadora'].get_object().nombre,
            'agrupado': self.agrupado,
            'template_name': self.template_print,
        }

        if self.kwargs['object_sistema_juego'] is not None:
            sistema = self.kwargs['object_sistema_juego'].get_lower_ascci()
        else:
            sistema = 'todo'

        self.cache_key = 'generate_{0}_time_{1}_{2}_por_{3}_{4}_user_{5}'.format(
            var_cache['fecha'].replace('/', '_'),
            now().strftime('%Y-%m-%d-%H-%M'),
            sistema,
            self.pertenece.prefix_filter,
            self.pertenece,
            self.kwargs['object_user'],
        )

        cache.set(
            self.cache_key,
            var_cache,
            CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
        )

    def type_html_conf(self, _type, val, add_class=''):
        item = {}
        item['html'] = _type
        item['html'] = _type
        item['class'] = ' ' if _type else 'text-align-right '
        if _type is False:
            if val < 0:
                item['class'] += ' link-red'
            elif val > 0 and add_class != ' link-red':
                item['class'] += ' link-blue'
            elif val == 0:
                add_class = ''

        item['val'] = val
        item['class'] += add_class
        return item

    def prepare_results_for_venta(self, qs):
        json_data = []
        for x, pertenece in enumerate(qs):
            row = []
            for item in pertenece['pertenece']:
                if item['html']:
                    val = item['val']
                else:
                    if item['val'] == 0:
                        val = 0
                    else:
                        val = item['val']
                    val = '<div class="{0} no - pd" >{1}</div>'.format(
                        item['class'],
                        intcomma(val),
                    )
                row.append(val)
            json_data.append(row)
        return json_data

    def prepare_footer_for_venta(self):
        array = [
            reverse(
                self.datatable_url,
            ) + '?action=get_pdf' + self.get_parameters_send_get(),
            reverse(
                self.datatable_url,
            ) + '?action=get_csv' + self.get_parameters_send_get(),
        ]
        for x, item in enumerate(self.footer):
            try:
                val = intcomma(item)
            except Exception:
                val = item
            array.append(val)
        return array
