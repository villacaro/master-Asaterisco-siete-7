# -*- coding: utf-8 -*-
import copy

from admin_comercializacion.forms import PermissionsSalesForm, PermissionsSalesRestrictionsForm
from admin_comercializacion.models import EventNotificationCadena, types_notification, types_notification_cadena
from admin_comercializacion.task import AsyncProcessInvokeMethod
from admin_comercializacion.views.agencias_views import AgenciasListView
from admin_comercializacion.views.bancas_views import BancasListView
from admin_comercializacion.views.bloques_views import BloquesListView
from admin_comercializacion.views.distribuidores_views import DistribuidoresListView
from admin_finanzas.models import Comercializadora
from admin_juego.models import TipoProducto, TipoProducto_Grupos, ModalidadJuego, ModalidadJuego_Grupos
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from admin_permisologia.models import PermissionsSales, PermissionsSalesRestrictions
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import DetailView
from django.views.generic.edit import FormView, View


class PermissionsSalesView(MyViewBase):
    model = PermissionsSales

    def get_model(self):
        try:
            from django.db.models import get_app
            return getattr(
                get_app('admin_comercializacion'),
                self.kwargs.get('type').capitalize()
            )
        except Exception:
            from django.http import Http404
            raise Http404

    def get_object(self):
        try:
            model = self.get_model()
            return model.objects.get(
                pk=self.kwargs.get('pk')
            )
        except Exception:
            from django.http import Http404
            raise Http404

    def get_success_url_force(self):
        return reverse(
            'admin_comercializacion_{0}_permisos_ventas_list'.format(
                self.object.get_class_name()
            )
        )

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return '?{0}={1}'.format(
            self.object.prefix_filter,
            self.object.pk
        )


class PermissionsSalesListView(MyViewBase):
    template_name = 'admin_comercializacion/permisos_ventas/permisos_ventas_list.html'


class BloquesPermissionsSalesListView(
        PermissionsSalesListView, BloquesListView):

    def get_context_data(self, **kwargs):
        context = super(
            BloquesPermissionsSalesListView,
            self).get_context_data(
            **kwargs)
        context['cadena'] = 'Bloques'
        return context


class BancasPermissionsSalesListView(PermissionsSalesListView, BancasListView):

    def get_context_data(self, **kwargs):
        context = super(
            BancasPermissionsSalesListView,
            self).get_context_data(
            **kwargs)
        context['cadena'] = 'Bancas'
        return context


class DistribuidoresPermissionsSalesListView(
        PermissionsSalesListView, DistribuidoresListView):

    def get_context_data(self, **kwargs):
        context = super(
            DistribuidoresPermissionsSalesListView,
            self).get_context_data(
            **kwargs)
        context['cadena'] = 'Distribuidores'
        return context


class AgenciasPermissionsSalesListView(
        PermissionsSalesListView, AgenciasListView):

    def get_context_data(self, **kwargs):
        context = super(
            AgenciasPermissionsSalesListView,
            self).get_context_data(
            **kwargs)
        context['cadena'] = 'Agencias'
        return context


class PermissionsSalesFormView(PermissionsSalesView, FormView):
    form_class = PermissionsSalesForm
    template_name = 'admin_comercializacion/permisos_ventas/permisos_ventas_form.html'

    def get_context_data(self, **kwargs):
        context = super(
            PermissionsSalesFormView,
            self).get_context_data(
            **kwargs)
        context['comercializadora'] = self.get_object(
        ).get_comercializadora().id
        return context

    def form_valid(self, form):
        self.object = self.get_object()

        datos = list(self.request.POST)
        datos.remove('nombre')
        datos.remove('csrfmiddlewaretoken')

        json = self.process_permissions_sales(self.object, datos)
        self.save_permissions(self.object, json)
        return super(PermissionsSalesFormView, self).form_valid(form)

    def process_permissions_sales(self, objecto, datos):
        comercializadora = objecto.get_comercializadora()

        deportes_list = []
        for check in datos:
            if check.find('grupo') < 0 and check.find('modalidad') < 0:
                deportes_list.append(check)

        deportes_check = TipoProducto.objects.only('pk').filter(pk__in=deportes_list)

        deportes_nocheck = TipoProducto.objects.only('pk').all().exclude(pk__in=deportes_list)

        # Agregando restricciones por deporte
        add_restriccions = []
        delete_restriccions = []
        for obj in deportes_nocheck:
            restriction = comercializadora.get_permissions_sales(obj.id, breaking=True)
            if restriction and restriction.parent is False:
                restriction.audit_save = False
                restriction.delete()
                notification = {}
                notification['deporte_id'] = obj.id
                notification['notification'] = True
                add_restriccions.append(notification)

            restriction = comercializadora.get_permissions_sales(obj.id)
            if not restriction:
                deporte = {}
                deporte['deporte_id'] = obj.id
                delete_restriccions.append(deporte)
                add_restriccions.append(deporte)

        # Eliminando restricciones por deporte
        for obj in deportes_check:
            restriction = comercializadora.get_permissions_sales(obj.id)
            if restriction:
                deporte = {}
                deporte['deporte_id'] = obj.id
                deporte['grupo__isnull'] = True
                deporte['modalidad__isnull'] = True
                if restriction.parent:
                    breaking = {}
                    breaking['deporte_id'] = obj.id
                    breaking['breaking'] = True
                    add_restriccions.append(breaking)
                delete_restriccions.append(deporte)

            grupos_list = []
            for check in datos:
                if check.find('grupo_' + str(obj.id)) == 0:
                    grupos_list.append(check.split('_')[2])

            if grupos_list:
                grupos_check = TipoProducto_Grupos.objects.select_related('grupo').filter(
                    deporte_id=obj.id, grupo_id__in=grupos_list)

                grupos_nocheck = TipoProducto_Grupos.objects.select_related('grupo').filter(
                    deporte_id=obj.id,
                ).exclude(
                    grupo_id__in=grupos_list
                )

                # Agregando restricciones por grupo
                for grupo in grupos_nocheck:
                    restriction = comercializadora.get_permissions_sales(
                        obj.id, grupo.grupo.id, breaking=True)
                    if restriction and restriction.parent is False:
                        restriction.audit_save = False
                        restriction.delete()
                        notification = {}
                        notification['deporte_id'] = obj.id
                        notification['grupo_id'] = grupo.grupo.id
                        notification['notification'] = True
                        add_restriccions.append(notification)

                    if not comercializadora.get_permissions_sales(obj.id, grupo.grupo.id):
                        grupo_rest = {}
                        grupo_rest['deporte_id'] = obj.id
                        grupo_rest['grupo_id'] = grupo.grupo.id
                        delete_restriccions.append(grupo_rest)
                        add_restriccions.append(grupo_rest)

                # Eliminando restricciones por grupo
                for grupo in grupos_check:
                    restriction = comercializadora.get_permissions_sales(obj.id, grupo.grupo.id)
                    if restriction:
                        grupo_rest = {}
                        grupo_rest['deporte_id'] = obj.id
                        grupo_rest['grupo_id'] = grupo.grupo.id
                        grupo_rest['modalidad__isnull'] = True
                        if restriction.parent:
                            breaking = {}
                            breaking['deporte_id'] = obj.id
                            breaking['grupo_id'] = grupo.grupo.id
                            breaking['breaking'] = True
                            add_restriccions.append(breaking)
                        delete_restriccions.append(grupo_rest)

                    modalidades_list = []
                    for check in datos:
                        if check.find('modalidad_' + str(obj.id) +
                                      '_' + str(grupo.grupo.id)) == 0:
                            modalidades_list.append(check.split('_')[3])

                    if modalidades_list:
                        modalidades_check = ModalidadJuego_Grupos.objects.select_related('modalidad')\
                            .filter(grupo_id=grupo.grupo.id, modalidad_id__in=modalidades_list)

                        modalidades_nocheck = ModalidadJuego_Grupos.objects.select_related('modalidad')\
                            .filter(grupo_id=grupo.grupo.id,)\
                            .exclude(modalidad_id__in=modalidades_list)

                        # Agregando restricciones por modalidad
                        for modalidad in modalidades_nocheck:
                            if modalidad.deporte_restriccion.filter(
                                pk=obj.id
                            ).exists():
                                continue

                            restriction = comercializadora.get_permissions_sales(
                                obj.id, grupo.grupo.id, modalidad.modalidad.id, breaking=True)
                            if restriction and restriction.parent is False:
                                restriction.audit_save = False
                                restriction.delete()
                                notification = {}
                                notification['deporte_id'] = obj.id
                                notification['grupo_id'] = grupo.grupo.id
                                notification['modalidad_id'] = modalidad.modalidad.id
                                notification['notification'] = True
                                add_restriccions.append(notification)

                            if not comercializadora.get_permissions_sales(
                                    obj.id, grupo.grupo.id, modalidad.modalidad.id):
                                modalidad_rest = {}
                                modalidad_rest['deporte_id'] = obj.id
                                modalidad_rest['grupo_id'] = grupo.grupo.id
                                modalidad_rest['modalidad_id'] = modalidad.modalidad.id
                                add_restriccions.append(modalidad_rest)

                        # Eliminando restricciones por modalidad
                        for modalidad in modalidades_check:
                            restriction = comercializadora.get_permissions_sales(
                                obj.id, grupo.grupo.id, modalidad.modalidad.id)
                            if restriction:
                                modalidad_rest = {}
                                modalidad_rest['deporte_id'] = obj.id
                                modalidad_rest['grupo_id'] = grupo.grupo.id
                                modalidad_rest['modalidad_id'] = modalidad.modalidad.id
                                if restriction.parent:
                                    breaking = {}
                                    breaking['deporte_id'] = obj.id
                                    breaking['grupo_id'] = grupo.grupo.id
                                    breaking['modalidad_id'] = modalidad.modalidad.id
                                    breaking['breaking'] = True
                                    add_restriccions.append(breaking)
                                delete_restriccions.append(modalidad_rest)

        json = {}
        json['add'] = add_restriccions
        json['delete'] = delete_restriccions
        return json

    def save_permissions(self, objecto, json):
        comercializadora = objecto.get_comercializadora()
        json_delete = copy.deepcopy(json['delete'])
        json_add = copy.deepcopy(json['add'])

        for delete in json_delete:
            delete['comercializadora_id'] = comercializadora.id
            delete['breaking'] = False
            permisos = PermissionsSales.objects.filter(**delete)
            for obj in permisos:
                obj.delete()

        for add in json_add:
            if add.get('notification'):
                continue
            add['comercializadora_id'] = comercializadora.id
            if add.get('breaking') is True:
                PermissionsSales.objects.create(**add)
            else:
                try:
                    add['breaking'] = True
                    breaking = PermissionsSales.objects.get(**add)
                    breaking.audit_save = False
                    breaking.delete()
                    add.pop('breaking')
                    PermissionsSales.objects.create(**add)
                except PermissionsSales.DoesNotExist:
                    add.pop('breaking')
                    PermissionsSales.objects.create(**add)

        for add in json_add:
            if add.get('breaking'):
                continue
            try:
                add['breaking'] = False
                json_delete.remove(add)
                add.pop('breaking')
            except Exception:
                pass

        # Guardando restricciones
        EventNotificationCadenaSend = []
        add_restriccions = []
        for add in json_add:
            if add.get('breaking'):
                continue
            elif add.get('breaking') is False:
                add.pop('breaking')
            if add.get('notification'):
                add.pop('notification')
            json_data = {}
            json_data['data'] = {}
            json_data['data']['action'] = 'add'

            if not add.get('grupo_id') and not add.get('modalidad_id'):
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['deporte'][0]
                json_data['data']['pk_origin'] = add.get('deporte_id')
                json_data['data']['data'] = add
            elif not add.get('modalidad_id'):
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['deporte_grupo'][0]
                json_data['data']['pk_origin'] = TipoProducto_Grupos.objects.only('pk').get(
                    deporte_id=add.get('deporte_id'),
                    grupo_id=add.get('grupo_id'),
                ).pk
                json_data['data']['data'] = add
            else:
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['grupo_modalidad'][0]
                json_data['data']['pk_origin'] = ModalidadJuego_Grupos.objects.only('pk').get(
                    grupo_id=add.get('grupo_id'),
                    modalidad_id=add.get('modalidad_id'),
                ).pk
                json_data['data']['data'] = add
            add_restriccions.append(json_data)

        for restriccions in add_restriccions:
            restriccions[objecto.prefix_filter] = objecto.pk
            restriccions['data_origin'] = types_notification_cadena[
                'permiso_venta'][0]
            EventNotificationCadenaSend.append(EventNotificationCadena(**restriccions))

        # Eliminando restricciones
        delete_restriccions = []
        for delete in json_delete:
            if delete.get('breaking', None):
                continue
            elif delete.get('breaking') is False:
                delete.pop('breaking')
            json_data = {}
            json_data['data'] = {}
            json_data['data']['action'] = 'delete'
            if delete.get('grupo__isnull') and delete.get('modalidad__isnull'):
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['deporte'][0]
                json_data['data']['pk_origin'] = delete.get('deporte_id')
                json_data['data']['data'] = delete
            elif not delete.get('grupo_id') and not delete.get('modalidad_id'):
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['deporte'][0]
                json_data['data']['pk_origin'] = delete.get('deporte_id')
                json_data['data']['data'] = delete
            elif delete.get('modalidad__isnull'):
                delete.pop('modalidad__isnull')
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['deporte_grupo'][0]
                json_data['data']['pk_origin'] = TipoProducto_Grupos.objects.only('pk').get(
                    deporte_id=delete.get('deporte_id'),
                    grupo_id=delete.get('grupo_id'),
                ).pk
                json_data['data']['data'] = delete
            else:
                json_data['data']['data_origin'] = types_notification[
                    'data_type_origin']['grupo_modalidad'][0]
                json_data['data']['pk_origin'] = ModalidadJuego_Grupos.objects.only('pk').get(
                    grupo_id=delete.get('grupo_id'),
                    modalidad_id=delete.get('modalidad_id'),
                ).pk
                json_data['data']['data'] = delete
            delete_restriccions.append(json_data)

        for restriccions in delete_restriccions:
            restriccions[objecto.prefix_filter] = objecto.pk
            restriccions['data_origin'] = types_notification_cadena[
                'permiso_venta'][0]
            EventNotificationCadenaSend.append(EventNotificationCadena(**restriccions))

        # El bulk_create genera un sql optimo que crea todos los objetos al
        # mismo tiempo
        EventNotificationCadena.objects.bulk_create(EventNotificationCadenaSend)

        ##########################################################################
        kwargs_async = {
            'session_id': '{0}'.format(self.object_session.pk),
            'parametros': {
                'comercializadora': comercializadora.id,
                'json': json,

            },
        }

        # Invocando proceso asyncrono que ejecutará la función
        AsyncProcessInvokeMethod.func_delay(
            PermissionsSalesFormView.delete_permissions, kwargs_async, delay=False)

    def delete_permissions(kwargs):
        comercializadora = Comercializadora.objects.only('id').get(
            pk=kwargs.get('comercializadora'))
        cont = 0
        childs = comercializadora.get_offspring().values_list('id', flat=True)
        for child in childs:
            permissions_comer = PermissionsSales.objects.only('id').filter(
                comercializadora_id=child)
            for permission_comer in permissions_comer:
                cont += 1
                permission_comer.audit_save = False
                permission_comer.delete()
        return ['{0} comercializadora(s) gestionada(s)'.format(cont)]


class PermissionsSalesDetailView(PermissionsSalesView, DetailView):
    template_name = 'admin_comercializacion/permisos_ventas/permisos_ventas_detail.html'

    def get_context_data(self, **kwargs):
        context = super(
            PermissionsSalesDetailView,
            self).get_context_data(
            **kwargs)
        # comercializadora = self.get_object().get_comercializadora()
        """
        context['deportes'] = []
        deportes = TipoProducto.objects.only('pk', 'nombre').all()

        for deporte in deportes:
            json_deporte = {}
            json_deporte['nombre'] = deporte.nombre
            json_deporte['restriccion'] = PermissionsSales.objects.filter(
                deporte_id=deporte.id,
                grupo__isnull=True,
                modalidad__isnull=True,
                comercializadora_id=comercializadora.id
            ).exists()

            json_deporte['grupos'] = []
            for grupo in deporte.deportes_grupos_set.select_related(
                    'grupo').all():
                json_grupo = {}
                json_grupo['nombre'] = grupo.grupo.nombre
                json_grupo['restriccion'] = PermissionsSales.objects.filter(
                    deporte_id=deporte.id,
                    grupo_id=grupo.grupo.pk,
                    modalidad__isnull=True,
                    comercializadora_id=comercializadora.id
                ).exists()

                json_grupo['modalidades'] = []
                modalidades = grupo.grupo.modalidades_grupos_set.select_related(
                    'modalidad').all()
                for modalidad in modalidades.order_by("modalidad__orden"):
                    if modalidad.deporte_restriccion.filter(
                        pk=deporte.id
                    ).exists():
                        continue

                    json_modalidad = {}
                    json_modalidad['nombre'] = modalidad.modalidad.modalidad
                    json_modalidad['restriccion'] = PermissionsSales.objects.filter(
                        deporte_id=deporte.id,
                        grupo_id=grupo.grupo.pk,
                        modalidad_id=modalidad.modalidad.id,
                        comercializadora_id=comercializadora.id
                    ).exists()

                    json_grupo['modalidades'].append(json_modalidad)
                json_deporte['grupos'].append(json_grupo)
            context['deportes'].append(json_deporte)
        """
        return context


class PermissionsSalesDatatableView(MyViewBase, BaseDatatableView):
    # Orden del filtro
    order_columns = None

    def get_initial_queryset(self):
        self.opcions_url = [
            'admin_comercializacion_permisos_ventas_update$' + Icons.ok,
            'admin_comercializacion_permisos_ventas_restrictions$' + Icons.block,
            # 'admin_comercializacion_permisos_ventas_detail$' + Icons.detail,
        ]
        qs = self.get_queryset().order_by('nombre')
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            keys = {
                'pk': item.pk,
                'type': self.request.GET.get('cadena').lower()
            }
            json_data.append([
                (x + 1 + acarreo),
                item.nombre,
                self.get_urls('', 'btn btn-xs btn-ico btn-default', **keys)
            ])
        return json_data


class BloquesPermissionsSalesDatatableView(
        PermissionsSalesDatatableView, BloquesPermissionsSalesListView):
    pass


class BancasPermissionsSalesDatatableView(
        PermissionsSalesDatatableView, BancasPermissionsSalesListView):
    pass


class DistribuidoresPermissionsSalesDatatableView(
        PermissionsSalesDatatableView, DistribuidoresPermissionsSalesListView):
    pass


class AgenciasPermissionsSalesDatatableView(
        PermissionsSalesDatatableView, AgenciasPermissionsSalesListView):
    pass


class PermisosVentasAjax(View):

    def dispatch(self, request, *args, **kwargs):
        json = {}
        grupos = TipoProducto_Grupos.objects.select_related('grupo').filter(
            deporte=request.REQUEST.get('deporte')
        ).order_by('grupo__orden')

        comercializadora = Comercializadora.objects.get(pk=request.REQUEST.get('comercializadora'))

        # Aqui es optimo el len, solo porque el queryset se ejecuta completo en
        # el for de abajo
        json['i'] = len(grupos)
        json['grupos'] = []

        mayor = 0
        for grupo in grupos:
            json_grupo = {}
            json_grupo[grupo.grupo.nombre] = {}
            json_grupo[grupo.grupo.nombre]['pk'] = grupo.grupo.pk
            if comercializadora.get_permissions_sales(
                    request.REQUEST.get('deporte'), grupo.grupo.pk):
                json_grupo[grupo.grupo.nombre]['checked'] = False
                check_modalidades = False
            else:
                check_modalidades = True
                json_grupo[grupo.grupo.nombre]['checked'] = True

            json_grupo[grupo.grupo.nombre]['modalidades'] = []
            modalidades = grupo.grupo.modalidades_grupos_set.select_related('modalidad').all()
            count = 0
            for modalidad in modalidades.order_by('modalidad__orden'):
                if modalidad.deporte_restriccion.filter(
                    pk=request.REQUEST.get('deporte')
                ).exists():
                    continue
                count += 1
                json_interno = {}
                json_interno[modalidad.modalidad.modalidad] = {}
                json_interno[modalidad.modalidad.modalidad]['pk'] = modalidad.modalidad.pk
                if comercializadora.get_permissions_sales(
                        request.REQUEST.get('deporte'), grupo.grupo.pk, modalidad.modalidad.pk):
                    json_interno[modalidad.modalidad.modalidad]['checked'] = False
                else:
                    json_interno[modalidad.modalidad.modalidad]['checked'] = check_modalidades
                json_grupo[grupo.grupo.nombre]['modalidades'].append(json_interno)

            if count > mayor:
                mayor = count
            json['grupos'].append(json_grupo)
        json['j'] = count

        return HttpResponse(content=JsonDumps(json), content_type='application/json')


class PermissionsSalesRestrictionsFormView(PermissionsSalesView, FormView):
    form_class = PermissionsSalesRestrictionsForm
    template_name = 'admin_comercializacion/permisos_ventas/permisos_ventas_restrictions_form.html'

    def get_context_data(self, **kwargs):
        context = super(PermissionsSalesRestrictionsFormView, self).get_context_data(**kwargs)
        context['comercializadora'] = self.get_object().get_comercializadora()
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            self.object = self.get_object()
            comercializadora = self.object.get_comercializadora()
            deporte = self.request.POST.get('deporte')

            json = {}
            modalidades = ModalidadJuego.objects.only('pk', 'modalidad').filter(
                bet=True).order_by('orden')

            for modalidad in modalidades:
                items = sorted(map(int, list(self.request.POST.getlist(modalidad.modalidad))))
                json['{0}'.format(modalidad.id)] = items

            try:
                obj = PermissionsSalesRestrictions.objects.get(
                    comercializadora_id=comercializadora.id, deporte_id=deporte)
                obj.restrictions = json
                obj.save(update_fields=['restrictions'])
            except PermissionsSalesRestrictions.DoesNotExist:
                obj = PermissionsSalesRestrictions(
                    comercializadora_id=comercializadora.id, restrictions=json, deporte_id=deporte)
                obj.save()

            # Registrando notificacion
            cadena = comercializadora.get_object()
            notification = {
                'data': {
                    'deporte': deporte,
                    'restrictions': json
                },
                'data_origin': types_notification_cadena['permiso_venta_restriccion'][0]
            }
            notification[cadena.prefix_filter] = cadena.pk
            EventNotificationCadena.objects.create(**notification)

            # Invocando tarea asincrona que eliminara las restricciones hijas
            kwargs_async = {
                'session_id': '{0}'.format(self.object_session.pk),
                'parametros': {
                    'comercializadora': comercializadora.id,
                    'deporte': deporte,
                    'json': json,

                },
            }

            AsyncProcessInvokeMethod.func_delay(
                PermissionsSalesRestrictionsFormView.delete_permissions, kwargs_async, delay=False)

            return HttpResponseRedirect(self.get_success_url_force())
        else:
            return self.form_invalid(form)

    @staticmethod
    def delete_permissions(kwargs):
        comercializadora = Comercializadora.objects.only('id').get(
            pk=kwargs.get('comercializadora'))
        cont = 0
        childs = comercializadora.get_offspring().values_list('id', flat=True)
        for child in childs:
            permissions_comer = PermissionsSalesRestrictions.objects.only('id').filter(
                comercializadora_id=child, deporte_id=kwargs.get('deporte'))
            for permission_comer in permissions_comer:
                cont += 1
                permission_comer.audit_save = False
                permission_comer.delete()

        return ['{0} comercializadora(s) gestionada(s)'.format(cont)]


class PermissionsSalesRestrictionsAjax(View):

    def dispatch(self, request, *args, **kwargs):
        deporte = TipoProducto.objects.only('pk').get(pk=request.REQUEST.get('deporte'))
        comercializadora = Comercializadora.objects.get(pk=request.REQUEST.get('comercializadora'))

        # Buscamos las modalidades por deporte
        deportes_grupos_list = deporte.deportes_grupos_set.filter(
            deporte_id=deporte.id
        ).order_by('grupo__orden')
        array_modalidades = []
        for deporte_grupo in deportes_grupos_list:
            modalidades_grupos_list = deporte_grupo.grupo.modalidades_grupos_set.all()
            for modalidad_grupo in modalidades_grupos_list.order_by('modalidad__orden'):
                if modalidad_grupo.deporte_restriccion.filter(pk=deporte.id).exists():
                    continue
                if modalidad_grupo.modalidad not in array_modalidades:
                    array_modalidades.append(modalidad_grupo.modalidad)

        modalidades = array_modalidades
        # Buscamos las restricciones por comercializadora y deporte
        try:
            restrictions = comercializadora.get_permissions_sales_restrictions(deporte.id).restrictions
        except Exception:
            restrictions = None

        json = {}
        json['tabla'] = []

        tr = []
        td = {
            'type': 'text',
            'label': 'ModalidadJuego'
        }
        tr.append(td)

        for modalidad in modalidades:
            td = {}
            td['type'] = 'text'
            td['label'] = modalidad.modalidad
            tr.append(td)
        json['tabla'].append(tr)

        for modalidad in modalidades:
            tr = []
            td = {}
            td['type'] = 'text'
            td['label'] = modalidad.modalidad
            tr.append(td)

            restriccion_base = list(modalidad.restriction.all().values_list('modalidad', flat=True))

            for modalidad_check in modalidades:
                if modalidad_check.id == modalidad.id:
                    td = {}
                    td['type'] = 'none'
                else:
                    td = {}
                    td['type'] = 'check'
                    td['id'] = '{0}_{1}'.format(
                        modalidad.id,
                        modalidad_check.id
                    )
                    td['name'] = modalidad.modalidad
                    td['value'] = modalidad_check.id
                    if modalidad_check.modalidad in restriccion_base:
                        td['check'] = True
                        td['disabled'] = True
                    elif restrictions:
                        if restrictions.get(str(modalidad.id)):
                            if modalidad_check.id in restrictions.get(
                                    str(modalidad.id)):
                                td['check'] = True
                                td['disabled'] = False
                    else:
                        td['check'] = False

                tr.append(td)
            json['tabla'].append(tr)

        return HttpResponse(content=JsonDumps(json), content_type='application/json')
