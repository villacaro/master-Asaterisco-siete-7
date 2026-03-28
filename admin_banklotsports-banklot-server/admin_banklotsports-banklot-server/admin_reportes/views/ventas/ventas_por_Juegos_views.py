# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_banklotsports.settings import CACHES_CONF_TIME, MESSAGES_GLOBAL
from admin_datamart.models import Hecho1_VentasCadenasJuegos
from admin_juego.models import (
    Deportes, Encuentros, EncuentrosModalidades, GruposApuestas, Jugadas, Modalidades, Temporadas,
)
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_funtions import FiltersCadenaCsv
from admin_lib.util_views import MyViewBase
from admin_reportes.forms import FilterFechasForm
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.utils.timezone import now
from django.views.generic import TemplateView


class VentasPorJuegos(MyViewBase, TemplateView):
    template_name = 'admin_reportes/ventas/ventas-por-juegos.html'

    def get_context_data(self, **kwargs):
        self.context = super(VentasPorJuegos, self).get_context_data(**kwargs)

        if self.request.method == 'GET':
            self.context['form_cadena'] = FilterCadenaComercializacionForm(
                **self.get_form_kwargs()
            )
            self.context['form_fecha'] = FilterFechasForm()
        elif self.request.method == 'POST':
            self.context['form_cadena'] = FilterCadenaComercializacionForm(
                self.request.POST,
                **self.get_form_kwargs()
            )
            self.context['form_cadena'].is_valid()
            self.context['form_fecha'] = FilterFechasForm(
                self.request.POST
            )

        if self.request.REQUEST.get('fecha_inicio'):
            ini = self.request.REQUEST.get('fecha_inicio')
        else:
            ini = self.context['form_fecha'].fields['fecha_inicio'].initial
        if self.request.REQUEST.get('fecha_fin'):
            fin = self.request.REQUEST.get('fecha_fin')
        else:
            fin = self.context['form_fecha'].fields['fecha_fin'].initial

        self._object = self.object_comercializadora.get_object()

        self.ventas = Hecho1_VentasCadenasJuegos.objects.filter(
            tiempo__fecha__range=(ini, fin)
        )

        self.context['consulta'] = self.agrupado_deporte()

        if self.context['consulta']['juegos_detalle']:

            if self.context['consulta']['column_extra']:
                footer = [
                    'Total',
                    '',
                    '',
                    '',
                    '',
                    '',
                    '',
                    str(self.context['consulta']['montos']),
                    str(self.context['consulta']['premios']),
                    str(self.context['consulta']['apuestas_count']),
                    '100%'
                ]
            else:
                footer = [
                    'Total',
                    '',
                    str(self.context['consulta']['montos']),
                    str(self.context['consulta']['premios']),
                    str(self.context['consulta']['apuestas_count']),
                    '100%'
                ]

            var_cache = {
                'comercializador': self.object_comercializadora.get_object().nombre,
                'titulo': 'Reporte - Ventas por juego'.format(ini, fin),
                'fecha': '{0}/{1}'.format(ini, fin),
                'filters_cadena': FiltersCadenaCsv(self.request),
                'titles': self.context['consulta']['juegos_detalle_title'],
                'content': self.context['consulta']['juegos_detalle'],
                'footer': footer,
                'template_name': 'admin_reportes/ventas/ventas-por-juegos-print.html',
            }

            if self.object_sistema_juego is not None:
                sistema = self.object_sistema_juego.get_lower_ascci()
            else:
                sistema = 'todo'

            self.context['cache_key'] = 'generate_{0}_time_{1}_{2}_by_{3}_por_{4}_{5}_user_{6}'.format(
                var_cache['fecha'].replace('/', '_'),
                now().strftime('%Y-%m-%d-%H-%M'),
                sistema,
                self.pertenece_deporte,
                self.pertenece.prefix_filter,
                self.pertenece,
                self.object_user,
            )

            cache.set(
                self.context['cache_key'],
                var_cache,
                CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
            )

        if self.ventas.exists():
            messages.info(self.request, MESSAGES_GLOBAL['consulta_por_juegos'])

        return self.context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def agrupado_deporte(self):

        # filtros por cadena
        cadena_list = [
            'agencia',
            'distribuidor',
            'banca',
            'bloque',
            'operadora']
        filtrado = False
        for pos in range(0, len(cadena_list)):
            if self.request.POST.get(cadena_list[pos]):
                kwargs = {}
                filtrado = True
                kwargs[
                    'comercializacion__' + cadena_list[pos] + '_id'
                ] = self.request.POST.get(cadena_list[pos])
                self.ventas = self.ventas.filter(**kwargs)
                break

        self.pertenece = self.object_comercializadora.get_object()
        if not filtrado:
            if self.pertenece.prefix_filter == 'master':
                self.ventas = self.ventas.filter(
                    comercializacion__operadora_id__in=list(
                        self.pertenece.get_offspring().values_list('pk', flat=True)),
                )
            else:
                kwargs = {}
                kwargs[
                    'comercializacion__' +
                    self.pertenece.prefix_filter +
                    '_id'] = self.pertenece.pk
                self.ventas = self.ventas.filter(
                    **kwargs
                )

        data = {}

        data['juegos_detalle_title'] = []
        data['juegos_detalle_title'].append({'text': 'Nro.', 'width': '10%'})
        data['column_extra'] = ''

        modalidad = self.request.POST.get('modalidad')
        grupo_modalidad = self.request.POST.get('grupo_modalidad')
        encuentro = self.request.POST.get('encuentro')
        temporada = self.request.POST.get('temporada')
        deporte = self.request.POST.get('deporte')

        self.context['modalidad'] = self.request.POST.get('modalidad', '')
        self.context['grupo_modalidad'] = self.request.POST.get(
            'grupo_modalidad', '')
        self.context['encuentro'] = self.request.POST.get('encuentro', '')
        self.context['temporada'] = self.request.POST.get('temporada', '')
        self.context['deporte'] = self.request.POST.get('deporte', '')

        data['column_extra'] = ''

        if encuentro:
            self.ventas = self.ventas.filter(juegos__encuentro_id=encuentro)
        elif temporada:
            self.ventas = self.ventas.filter(juegos__temporada_id=temporada)
        elif deporte:
            self.ventas = self.ventas.filter(juegos__deporte_id=deporte)

        if modalidad:
            self.pertenece_deporte = 'encuentro-{0}-grupo-{1}-modalidad-{2}'.format(
                encuentro, grupo_modalidad, modalidad
            )
            encuentros_modalidades = list(EncuentrosModalidades.objects.filter(
                encuentro_id=encuentro,
                modalidad_grupo__grupo_id=grupo_modalidad,
                modalidad_grupo__modalidad_id=modalidad
            ).distinct().values_list('pk', flat=True))

            self.ventas = self.ventas.filter(
                juegos__encuentros_modalidad_id__in=encuentros_modalidades,
            )

            filtro_juego = Jugadas.objects.filter(
                encuentros_modalidad__encuentro_id=encuentro,
                encuentros_modalidad__modalidad_grupo__grupo_id=grupo_modalidad,
                condicion__modalidad_id=modalidad,
                origen__isnull=True
            )

            tipo = 6
            data['juegos_detalle_title'].append(
                {'text': 'Condicion', 'width': '40%'})

        elif grupo_modalidad:
            self.pertenece_deporte = 'encuentro-{0}-grupo-{1}'.format(encuentro, grupo_modalidad)
            grupo_modalidad = GruposApuestas.objects.get(pk=grupo_modalidad)

            encuentro_modalidad_all = EncuentrosModalidades.objects.filter(
                encuentro_id=encuentro,
                modalidad_grupo__grupo=grupo_modalidad
            ).distinct('pk')

            self.ventas = self.ventas.filter(
                juegos__encuentros_modalidad_id__in=list(
                    encuentro_modalidad_all.values_list('pk', flat=True))
            )

            filtro_juego = Modalidades.objects.filter(
                pk__in=list(
                    encuentro_modalidad_all.values_list(
                        'modalidad_grupo__modalidad_id',
                        flat=True))
            )

            tipo = 5
            data['juegos_detalle_title'].append(
                {'text': 'Modalidad', 'width': '40%'})

        elif encuentro:
            self.pertenece_deporte = 'encuentro-{0}'.format(encuentro)
            encuentro = Encuentros.objects.get(pk=encuentro)

            filtro_juego = encuentro.encuentrosmodalidades_set.all() \
                .distinct('modalidad_grupo__grupo_id')

            tipo = 4
            data['juegos_detalle_title'].append(
                {'text': 'Grupo', 'width': '40%'})

        elif temporada:
            self.pertenece_deporte = 'temporada-{0}'.format(temporada)
            temporada = Temporadas.objects.get(pk=temporada)

            ini = self.request.POST.get('fecha_inicio') + hora_cero
            fin = self.request.POST.get('fecha_inicio') + hora_23

            kwargs_1 = {}
            kwargs_2 = {}
            if self.pertenece.prefix_filter != 'master':
                kwargs_1['jornada__sistema'] = self.object_sistema_juego
                kwargs_2['jornada__sistema'] = self.object_sistema_juego

            kwargs_1['pk__in'] = list(
                self.ventas.filter(
                    juegos__temporada_id=temporada.pk).values_list(
                    'juegos__encuentro_id',
                    flat=True).distinct('juegos__encuentro_id'))

            kwargs_2['jornada__temporadas'] = temporada
            kwargs_2['horajuego__range'] = (ini, fin)

            filtro_juego = Encuentros.objects.filter(
                **kwargs_1
            ).filter(**kwargs_2)

            tipo = 3

            data['juegos_detalle_title'].append(
                {'text': 'Encuentros', 'width': '10%'})
            data['juegos_detalle_title'].append(
                {'text': 'Fecha', 'width': '10%'})
            data['juegos_detalle_title'].append(
                {'text': 'Hora', 'width': '10%'})
            data['juegos_detalle_title'].append(
                {'text': 'Jornada', 'width': '10%'})
            data['juegos_detalle_title'].append(
                {'text': 'Grupo', 'width': '10%'})
            data['juegos_detalle_title'].append(
                {'text': 'Equipos', 'width': '10%'})

            data['column_extra'] = '12345'
            # hay un ciclo en el template que lee esta plantilla y genera 5 td jejejeje
            # buscando q los totales no se desborden

        elif deporte:
            self.pertenece_deporte = 'deporte-{0}'.format(deporte)
            deporte = Deportes.objects.get(pk=deporte)

            kwargs = {}
            if self.pertenece.prefix_filter != 'master':
                kwargs['jornadas__sistema'] = self.object_sistema_juego
            kwargs['pk__in'] = list(
                self.ventas.filter(
                    juegos__deporte_id=deporte.pk).values_list(
                    'juegos__temporada_id',
                    flat=True).distinct('juegos__temporada_id'))

            filtro_juego = Temporadas.objects.filter(
                **kwargs
            ).distinct('pk')

            tipo = 2

            data['juegos_detalle_title'].append(
                {'text': 'Liga', 'width': '40%'})

        else:
            self.pertenece_deporte = 'all-deportes'
            filtro_juego = Deportes.objects.filter(
                pk__in=list(self.ventas.values_list(
                    'juegos__deporte_id',
                    flat=True
                ).distinct('juegos__deporte_id'))
            )
            tipo = 1
            data['juegos_detalle_title'].append(
                {'text': 'Deporte', 'width': '40%'})

        data['juegos_detalle_title'].append({'text': 'Ventas', 'width': '10%'})
        data['juegos_detalle_title'].append(
            {'text': 'Premios', 'width': '10%'})
        data['juegos_detalle_title'].append(
            {'text': 'Cantidad de apuestas', 'width': '10%'})
        data['juegos_detalle_title'].append(
            {'text': 'Porcentaje', 'width': '10%'})

        data['montos'] = Decimal(str('0.00'))
        data['premios'] = Decimal(str('0.00'))
        data['apuestas_count'] = 0

        data_juegos = []
        i = 0
        for item in filtro_juego:
            data_interna_juegos = {}
            data_interna_juegos['pertenece'] = []

            i += 1
            data_interna_juegos['pertenece'].append(
                self.type_html_conf(False, i, '')
            )

            if tipo == 1:  # por deporte
                venta_detalle = self.ventas.filter(juegos__deporte_id=item.pk)

                texto = "<a href='#' class='link' onclick='ConsultaEnLinea("
                texto += "" + str(tipo) + "," + str(item.pk) + ")'>"
                texto += item.nombre
                texto += "</a>"
                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto))

            elif tipo == 2:  # por temporada
                venta_detalle = self.ventas.filter(
                    juegos__temporada_id=item.pk)

                texto = "<a href='#' class='link' onclick='ConsultaEnLinea("
                texto += "" + str(tipo) + "," + str(item.pk) + ")'>"
                texto += item.torneo.nombre + " - " + item.nombre
                texto += "</a>"
                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto))

            elif tipo == 3:  # por encuentros
                venta_detalle = self.ventas.filter(
                    juegos__encuentro_id=item.pk)

                texto = "<a href='#' class='link' onclick='ConsultaEnLinea("
                texto += "" + str(tipo) + "," + str(item.pk) + ")'>"
                texto += str(item.pk)
                texto += "</a>"

                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto)
                )
                objFecha = strFecha(item.horajuego)
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(False, objFecha.getFecha()))
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(False, objFecha.getHora())
                )
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(False, item.jornada.jornada)
                )
                if item.grupo is not None:
                    data_interna_juegos['pertenece'].append(
                        self.type_html_conf(False, item.grupo.nombre)
                    )
                else:
                    data_interna_juegos['pertenece'].append(
                        self.type_html_conf(False, 'Sin grupo')
                    )
                campo = ''
                d_e = item.encuentrosdetail_set.all()
                equipo_len = d_e.count()
                i = 0
                for obj in d_e:
                    campo += obj.equipos_temporadas.equipo.nombre
                    i += 1
                    if (equipo_len > i):
                        campo += ' Vs. '
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(False, campo))
            elif tipo == 4:  # por grupos

                encuentro_modalidad_all = EncuentrosModalidades.objects.filter(
                    encuentro=item.encuentro,
                    modalidad_grupo__grupo=item.modalidad_grupo.grupo
                ).distinct()

                venta_detalle = self.ventas.filter(
                    juegos__encuentros_modalidad_id__in=list(
                        encuentro_modalidad_all.values_list('pk', flat=True))
                )

                texto = "<a href='#' class='link' onclick='ConsultaEnLinea("
                texto += "" + str(tipo) + "," + \
                    str(item.modalidad_grupo.grupo_id) + ")'>"
                texto += item.modalidad_grupo.grupo.nombre
                texto += "</a>"
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto)
                )

            elif tipo == 5:  # por modalidades
                venta_detalle = self.ventas.filter(
                    juegos__modalidad_id=item.pk
                )

                texto = "<a href='#' class='link' onclick='ConsultaEnLinea("
                texto += "" + str(tipo) + "," + str(item.pk) + ")'>"
                texto += item.modalidad
                texto += "</a>"
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, texto))

            elif tipo == 6:  # por modalidades
                venta_detalle = self.ventas.filter(
                    juegos__pertenece=item.get_pertenece(),
                    juegos__condicion_id=item.condicion.pk,
                    juegos__modalidad_id=item.condicion.modalidad.pk,
                )

                texto = item.get_pertenece()
                data_interna_juegos['pertenece'].append(
                    self.type_html_conf(True, item.get_pertenece(), '')
                )

            monto_sum = venta_detalle.aggregate(Sum('monto_total'))[
                'monto_total__sum']
            if not monto_sum:
                monto_sum = Decimal(str('0.00'))

                data_interna_juegos['pertenece'][1]['val'] = \
                    data_interna_juegos['pertenece'][1]['val'].replace("ConsultaEnLinea", "") \
                    .replace("link", "link-red").replace("<a", "<span").replace("a>", "span>")

            monto_sum = round(monto_sum, 2)

            if monto_sum:
                data['montos'] += monto_sum

            data_interna_juegos['pertenece'].append(
                self.type_html_conf(False, monto_sum)
            )

            premios_sum = venta_detalle.aggregate(Sum('monto_premios'))[
                'monto_premios__sum']
            if not premios_sum:
                premios_sum = Decimal(str('0.00'))

            premios_sum = round(premios_sum, 2)

            if premios_sum:
                data['premios'] += premios_sum

            data_interna_juegos['pertenece'].append(
                self.type_html_conf(False, premios_sum)
            )

            count_sum = venta_detalle.aggregate(
                Sum('count_apuestas'))['count_apuestas__sum']
            if not count_sum:
                count_sum = 0
            data['apuestas_count'] += count_sum

            data_interna_juegos['pertenece'].append(
                self.type_html_conf(False, count_sum)
            )

            data_juegos.append(data_interna_juegos)

        data['montos'] = Decimal(str('0.00')) if data[
            'montos'] is None else data['montos']
        data['premios'] = Decimal(str('0.00')) if data[
            'premios'] is None else data['premios']

        for item in data_juegos:
            porcentaje = 0 if data['montos'] == 0 else (
                (item['pertenece'][len(item['pertenece']) - 2]['val'] * 100) / data['montos'])

            item['pertenece'].append(
                self.type_html_conf(
                    False, round(
                        porcentaje, 2)))

        data['porcentaje'] = '0%' if data['montos'] == 0 else '100%'
        data['juegos_detalle'] = data_juegos

        return data

    def type_html_conf(self, _type, val, add_class=''):
        item = {}
        item['html'] = _type
        item['val'] = val
        return item
