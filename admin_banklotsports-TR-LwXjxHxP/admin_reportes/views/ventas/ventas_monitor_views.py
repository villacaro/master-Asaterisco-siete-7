# -*- coding: utf-8 -*-

import itertools
from decimal import Decimal

from admin_datamart.models import Hecho8_VentasMonitorLinea
from admin_juego.models import Deportes_Grupos, Encuentros, EncuentrosModalidades
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterCadenaComercializacionForm, FilterDeportesFechaForm
from admin_lib.util_json import JsonDumps
from admin_lib.util_reverse import new_reverse
from admin_lib.util_views import MyViewBase
from django.contrib.humanize.templatetags.humanize import intcomma
from django.db.models import Sum
from django.http import HttpResponse
from django.utils.timezone import now
from django.views.generic import ListView


class MonitorVentaView(MyViewBase, ListView):
    template_name = 'admin_reportes/ventas/ventas-monitor.html'
    model = Encuentros
    form_class = FilterDeportesFechaForm
    filter_form = None

    def get_context_data(self, **kwargs):
        context = super(MonitorVentaView, self).get_context_data(**kwargs)
        context['form_cadena'] = FilterCadenaComercializacionForm(
            self.request.GET,
            **self.get_form_kwargs()
        )
        context['form_cadena'].is_valid()
        return context

    def get_queryset(self):
        """
            get_queryset: se hace el respectivo filtro por
            los fields del formulario
        """
        if self.get_filter_form().is_valid():
            fecha = strFecha(
                self.get_filter_form().cleaned_data['fecha']).getFecha()
            deporte = self.get_filter_form().cleaned_data['deporte']

            kwargs_ventas = {}
            kwargs_ventas['tiempo__fecha'] = fecha
            if deporte is not None:
                kwargs_ventas['juegos__deporte_id'] = deporte.id
            self.ventas = Hecho8_VentasMonitorLinea.objects.filter(
                **kwargs_ventas)

            # Cadena
            cadena_list = [
                'agencia',
                'distribuidor',
                'banca',
                'bloque',
                'operadora']
            filtrado = False
            for pos in range(0, len(cadena_list)):
                if self.request.GET.get(cadena_list[pos]):
                    kwargs = {}
                    kwargs[
                        'comercializacion__' + cadena_list[pos] + '_id'
                    ] = self.request.GET.get(cadena_list[pos])
                    self.ventas = self.ventas.filter(**kwargs)
                    break

            if not filtrado:
                pertenece = self.object_comercializadora.get_object()
                if pertenece.prefix_filter == 'master':
                    self.ventas = self.ventas.filter(
                        comercializacion__operadora_id__in=list(
                            pertenece.get_offspring().values_list('pk', flat=True)),
                    )
                else:
                    kwargs = {}
                    kwargs[
                        'comercializacion__' +
                        pertenece.prefix_filter +
                        '_id'] = pertenece.pk
                    self.ventas = self.ventas.filter(
                        **kwargs
                    )

            if self.get_profile().codename == 'userprofile_master':
                encuentros = Encuentros.objects.all()
            else:
                kwargs_1 = {}
                kwargs_1['pk__in'] = list(
                    self.ventas.values_list(
                        'juegos__encuentro_id',
                        flat=True).distinct('juegos__encuentro_id'))

                encuentros = Encuentros.objects.filter(**kwargs_1)
                kwargs_2 = {}
                kwargs_2['jornada__sistema'] = self.object_sistema_juego
                kwargs_2['horajuego__range'] = (
                    fecha + hora_cero, fecha + hora_23)
                if deporte is not None:
                    kwargs_2['jornada__temporadas__torneo__deporte'] = deporte
                encuentros = encuentros.filter(**kwargs_2)

            monto_venta = self.ventas.aggregate(Sum('monto_venta'))[
                'monto_venta__sum']
            for encuentro in encuentros:
                encuentro.venta = round(self.ventas.filter(
                    juegos__encuentro_id=encuentro.pk
                ).aggregate(Sum('monto_venta'))['monto_venta__sum'], 0)
                encuentro.porcentaje = round(
                    encuentro.venta / monto_venta * 100, 2)
                if encuentro.horacierre > now():
                    encuentro.editar = True
                else:
                    encuentro.editar = None
        else:
            encuentros = Encuentros.objects.none()
        encuentros = list(encuentros)
        encuentros.sort(key=lambda x: x.venta, reverse=True)
        encuentros = sorted(encuentros, key=lambda x: x.venta, reverse=True)
        return encuentros


class VentaMonitorViewAjax(MonitorVentaView):

    def get_queryset_ventas(self):
        """
            repite el filter de encuentros, pero solo para obtener las ventas
        """
        if self.get_filter_form().is_valid():
            fecha = strFecha(
                self.get_filter_form().cleaned_data['fecha']).getFecha()
            deporte = self.get_filter_form().cleaned_data['deporte']

            kwargs_ventas = {}
            kwargs_ventas['tiempo__fecha'] = fecha
            if deporte is not None:
                kwargs_ventas['juegos__deporte_id'] = deporte.id
            self.ventas = Hecho8_VentasMonitorLinea.objects.filter(
                **kwargs_ventas)

            # Cadena
            cadena_list = [
                'agencia',
                'distribuidor',
                'banca',
                'bloque',
                'operadora']
            filtrado = False
            for pos in range(0, len(cadena_list)):
                if self.request.GET.get(cadena_list[pos]):
                    kwargs = {}
                    kwargs[
                        'comercializacion__' + cadena_list[pos] + '_id'
                    ] = self.request.GET.get(cadena_list[pos])
                    self.ventas = self.ventas.filter(**kwargs)
                    break

            if not filtrado:
                pertenece = self.object_comercializadora.get_object()
                if pertenece.prefix_filter == 'master':
                    self.ventas = self.ventas.filter(
                        comercializacion__operadora_id__in=list(
                            pertenece.get_offspring().values_list('pk', flat=True)),
                    )
                else:
                    kwargs = {}
                    kwargs[
                        'comercializacion__' +
                        pertenece.prefix_filter +
                        '_id'] = pertenece.pk
                    self.ventas = self.ventas.filter(
                        **kwargs
                    )
            return self.ventas
        else:
            return Hecho8_VentasMonitorLinea.objects.none()

    def dispatch(self, request, *args, **kwargs):
        super(VentaMonitorViewAjax, self).dispatch(request, *args, **kwargs)

        self.ventas = self.get_queryset_ventas()

        encuentro = Encuentros.objects.get(pk=request.GET.get('encuentro'))
        ventas_encuentro = self.ventas.filter(
            juegos__encuentro_id=encuentro.pk
        )
        monto_encuentro = ventas_encuentro.aggregate(Sum('monto_venta'))[
            'monto_venta__sum']

        data = []
        for deporte_grupo in Deportes_Grupos.objects.filter(
            deporte=encuentro.jornada.temporadas.torneo.deporte
        ).order_by('-grupo__orden'):
            json = {}
            json['pk'] = deporte_grupo.grupo.pk
            json['grupo'] = deporte_grupo.grupo.nombre
            json['modalidades'] = ['Modalidad', 'Relacion', 'Venta']
            json['condiciones'] = []
            json['footer'] = []
            modalidades_grupos_list = deporte_grupo.grupo.modalidades_grupos_set.all()
            for modalidad_grupo in modalidades_grupos_list.order_by(
                    '-modalidad__orden'):

                encuentros_modalidad = list(EncuentrosModalidades.objects.filter(
                    encuentro=encuentro,
                    deporte_grupo=deporte_grupo,
                    modalidad_grupo=modalidad_grupo
                ).values_list('pk', flat=True))

                ventas_modalidad = ventas_encuentro.filter(
                    juegos__encuentros_modalidad_id__in=encuentros_modalidad,
                )
                monto_modalidad = ventas_modalidad.aggregate(Sum('monto_venta'))[
                    'monto_venta__sum']

                if monto_modalidad:
                    condiciones_list = modalidad_grupo.modalidad.condiciones_set.all()
                    for condicion in condiciones_list.order_by('orden'):
                        condicion_array = []

                        venta_detalle = ventas_modalidad.filter(
                            juegos__condicion_id=condicion.pk,
                            juegos__modalidad_id=condicion.modalidad.pk,
                        )

                        if condicion.equipo:
                            encuentrosdetail_list = encuentro.encuentrosdetail_set.all()

                            for encuentro_detail in encuentrosdetail_list.order_by(
                                    '-indice'):

                                if condicion.tipo != 4:
                                    condicion_array = []

                                    venta_detalle = ventas_modalidad.filter(
                                        juegos__equipo_id=encuentro_detail.equipos_temporadas
                                        .equipo_id,
                                        juegos__condicion_id=condicion.pk,
                                        juegos__modalidad_id=condicion.modalidad.pk,
                                    )

                                    monto_sum = venta_detalle.aggregate(
                                        Sum('monto_venta')
                                    )['monto_venta__sum']
                                    if not monto_sum:
                                        monto_sum = Decimal(str('0.00'))

                                    monto_sum = round(monto_sum, 2)
                                    condicion_array.append(
                                        encuentros_modalidad[0])
                                    condicion_array.append(
                                        deporte_grupo.grupo.nombre + ' / ' + condicion.modalidad.modalidad
                                    )
                                    condicion_array.append(
                                        encuentro_detail.equipos_temporadas.equipo.nombre
                                    )
                                    condicion_array.append(
                                        float(monto_sum)
                                    )
                                    condicion_array.append(
                                        str(round(
                                            (float(monto_sum) / float(monto_encuentro)) * 100, 2)) + '%'
                                    )
                                    # Se envian dos tds vacios
                                    condicion_array.append('')
                                    condicion_array.append('')
                                    json['condiciones'].append(condicion_array)

                        elif condicion.nombre == '':
                            condicion_array = []
                            venta_detalle = ventas_modalidad.filter(
                                juegos__condicion_id=condicion.pk,
                                juegos__modalidad_id=condicion.modalidad.pk,
                            )

                            monto_sum = venta_detalle.aggregate(Sum('monto_venta'))[
                                'monto_venta__sum']
                            if not monto_sum:
                                monto_sum = Decimal(str('0.00'))
                            monto_sum = round(monto_sum, 2)
                            condicion_array.append(encuentros_modalidad[0])
                            condicion_array.append(
                                deporte_grupo.grupo.nombre + ' / ' + condicion.modalidad.modalidad
                            )
                            condicion_array.append(
                                condicion.modalidad.modalidad)
                            condicion_array.append(float(monto_sum))
                            condicion_array.append(
                                str(round(
                                    (float(monto_sum) / float(monto_encuentro)) * 100, 2)) + '%'
                            )
                            # Se envian dos tds vacios
                            condicion_array.append('')
                            condicion_array.append('')

                            json['condiciones'].append(condicion_array)

                        else:
                            condicion_array = []
                            split = condicion.nombre.split('/')
                            venta_detalle = ventas_modalidad.filter(
                                juegos__pertenece_id=0,
                                juegos__condicion_id=condicion.pk,
                                juegos__modalidad_id=condicion.modalidad.pk,
                            )

                            monto_sum = venta_detalle.aggregate(Sum('monto_venta'))[
                                'monto_venta__sum']
                            if not monto_sum:
                                monto_sum = Decimal(str('0.00'))
                            monto_sum = round(monto_sum, 2)
                            condicion_array.append(encuentros_modalidad[0])
                            condicion_array.append(
                                deporte_grupo.grupo.nombre + ' / ' + condicion.modalidad.modalidad
                            )
                            condicion_array.append(split[0])
                            condicion_array.append(float(monto_sum))
                            condicion_array.append(
                                str(round(
                                    (float(monto_sum) / float(monto_encuentro)) * 100, 2)) + '%'
                            )
                            # Se envian dos tds vacios
                            condicion_array.append('')
                            condicion_array.append('')
                            json['condiciones'].append(condicion_array)

                            condicion_array = []
                            venta_detalle = ventas_modalidad.filter(
                                juegos__pertenece_id=1,
                                juegos__condicion_id=condicion.pk,
                                juegos__modalidad_id=condicion.modalidad.pk,
                            )
                            monto_sum = venta_detalle.aggregate(Sum('monto_venta'))[
                                'monto_venta__sum']
                            if not monto_sum:
                                monto_sum = Decimal(str('0.00'))
                            monto_sum = round(monto_sum, 2)
                            condicion_array.append(encuentros_modalidad[0])
                            condicion_array.append(
                                deporte_grupo.grupo.nombre + ' / ' + condicion.modalidad.modalidad
                            )
                            condicion_array.append(split[1])
                            condicion_array.append(float(monto_sum))
                            condicion_array.append(
                                str(round(
                                    (float(monto_sum) / float(monto_encuentro)) * 100, 2)) + '%'
                            )
                            # Se envian dos tds vacios
                            condicion_array.append('')
                            condicion_array.append('')
                            json['condiciones'].append(condicion_array)

            data.append(json)

        return HttpResponse(
            content=JsonDumps(data),
            content_type='application/json'
        )


class MonitorDatatableView(MonitorVentaView, BaseDatatableView):
    model = Encuentros
    order_columns = ['horajuego']
    # Fields de busqueda
    filter_search = ''
    query = None
    ordenar = False

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for item in qs:
            equipos = ""
            for x, equipo in enumerate(item.encuentrosdetail_set_order()):
                equipos += "<span class='tag tag-light-green'>{0}</span>".format(
                    equipo.equipos_temporadas.equipo
                )
                if x == 0:
                    equipos += "<span class='tag tag-nomargin'> vs. </span>"

            n = itertools.count(0)
            row = {}
            row[next(n)] = "<span class='tag tag-blue'>{0}</span>".format(
                item.jornada.temporadas.torneo.deporte
            )
            row[next(n)] = ""
            row[next(n)] = equipos
            row[next(n)] = "<span style='font-weight: bold;'>{0}</span>".format(
                intcomma(item.venta)
            )
            row[next(n)] = "<span style='font-weight: bold;'>{0}%</span>".format(
                item.porcentaje
            )
            row[next(n)] = "<a onclick='{0}' class='{1}'><span class='plus' id='all'>+</span></a>".format(
                'get_venta(this, {0})'.format(item.pk),
                'btn btn-mini btn-icon'
            )
            if item.editar:
                campo = "<a target='_blank' "
                campo += "onClick='window.open(this.href, this.target, 'resizable=0,width=1024,height=600');"
                campo += "return false;' class='link' href='"
                campo += new_reverse(self, 'admin_logros_ecuentros_create_update', kwargs={'pk': item.pk})
                campo += "' ><span class='btn btn-mini btn-icon'>Editar</span></a>"
            else:
                campo = ""
            row[next(n)] = campo

            row["DT_RowId"] = "encuentro_" + str(item.pk)
            json_data.append(row)

        return json_data
