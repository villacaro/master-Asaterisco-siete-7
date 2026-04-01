# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_asterisco7.settings import CACHES_CONF_TIME, MESSAGES_GLOBAL
from admin_comercializacion.models import Agencias
from admin_datamart.models import Hecho1_VentasCadenasJuegos, Hecho2_VentasCadenasLinea
from admin_juego.models import TipoProducto, Sorteo, apuesta, ModalidadJuego, Fechas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_views import MyViewBase, ReportsBaseView
from admin_reportes.forms import FilterFechasForm, FilterOrdenPresentacionReporteForm
from django.contrib import messages
from django.core.cache import cache
from django.db.models import Sum
from django.views.generic import TemplateView


class VentaEnLineaAgrupadaView(MyViewBase, TemplateView):
    template_name = "admin_reportes/ventas/venta-en-linea.html"

    def get_context_data(self, **kwargs):
        context = super(
            VentaEnLineaAgrupadaView,
            self).get_context_data(
            **kwargs)

        if self.request.method == "GET":
            context["form_orden"] = FilterOrdenPresentacionReporteForm()

            context["form_fecha"] = FilterFechasForm()

        return context


class VentasLineaProcessView(ReportsBaseView):
    pdf_url = 'admin_reportes_venta_en_linea_print_pdf'
    csv_url = 'admin_reportes_venta_en_linea_print_csv'
    datatable_url = 'admin_reportes_venta_en_linea_list_datatable'

    template_print = 'admin_reportes/ventas/ventas-en-linea-print.html'
    name_report = 'Venta en línea'
    codename_report = 'ventas_linea'

    valid_columns = False

    def get_hecho_venta(self):
        if self.agrupado != 'parley':
            self.ventas = Hecho2_VentasCadenasLinea.objects.filter(
                tiempo__fecha__range=(self.fecha_inicio, self.fecha_inicio)
            )
        else:
            self.ventas = Hecho1_VentasCadenasJuegos.objects.filter(
                tiempo__fecha__range=(self.fecha_inicio, self.fecha_inicio)
            )

    def execute_all_process(self):
        self.get_hecho_venta()
        if self.agrupado == 'parley':
            self.apply_filter_juego()
        else:
            self.apply_filter_cadena()
        self.execute_query()
        self.set_cache()

        cache.set(
            self.get_key_report(),
            self.cache_key,
            CACHES_CONF_TIME['reportes_csv_pdf']['listado_logros']
        )

    def get_titles_for_comercializacion(self):
        titles = []

        titles.append({'text': 'Nro.', 'width': '10%'})

        verbose_name_hijos = ''
        if self.pertenece.get_offspring():
            verbose_name_hijos = self.pertenece.get_offspring()[
                0].get_verbose_name_plural()

        titles.append({'text': verbose_name_hijos, 'width': '30%'})
        titles.append({'text': 'Venta', 'width': '15%'})
        titles.append({'text': 'Porcentaje', 'width': '15%'})

        return titles

    def apply_presentation_for_comercializacion(self):
        data = {}

        # Totalizacion de venta
        sum_venta_total = self.ventas.aggregate(Sum('monto_total'))[
            'monto_total__sum']
        sum_venta_total = round(
            Decimal(str("0.00")) if not sum_venta_total else sum_venta_total,
            2
        )

        i = 0
        data_cadena = []
        for item in self.pertenece.get_offspring():
            i += 1
            data_interna_cadena = {}
            data_interna_cadena["pertenece"] = []

            texto = ""
            if item.prefix_filter != "taquilla":
                texto = "<a href='#' class='link' onclick='{0}'>{1}</a>".format(
                    'AgrupadoPorCadena({0},"{1}")'.format(
                        item.pk,
                        item.prefix_filter
                    ),
                    item
                )

            else:
                texto = item.taquilla

            data_interna_cadena["pertenece"].append(
                self.type_html_conf(False, i, "")
            )

            data_interna_cadena["pertenece"].append(
                self.type_html_conf(True, texto, "")
            )

            venta_detalle = self.ventas.filter(
                ** item.get_kwargs_dimension_comercializadora()
            )

            sum_venta = venta_detalle.aggregate(Sum('monto_total'))[
                'monto_total__sum']

            if not sum_venta:
                data_interna_cadena["pertenece"][1]["val"] = data_interna_cadena["pertenece"][1]["val"].replace(
                    "AgrupadoPorCadena",
                    ""
                ).replace("link", "link-red").replace("<a", "<span").replace("a>", "span>")
                sum_venta = Decimal(str("0.00"))

            sum_venta = round(sum_venta, 2)
            data_interna_cadena["pertenece"].append(
                self.type_html_conf(False, sum_venta)
            )

            porcentaje = 0 if not sum_venta_total else round(((sum_venta * 100) / sum_venta_total), 2)

            data_interna_cadena["pertenece"].append(
                self.type_html_conf(
                    True,
                    '<p class="{0} no-pd" >{1}</p>'.format(
                        'text-align-right',
                        "0%" if not porcentaje else str(
                            round(porcentaje, 2)) + "%"
                    )
                )
            )
            data_cadena.append(data_interna_cadena)

        data['totales'] = [
            'Total',
            '',
            sum_venta_total,
            "0%" if not sum_venta_total else "100%",
        ]

        data["detalle"] = data_cadena
        return data

    def get_titles_for_parley(self):
        titles = []

        titles.append({"text": "Nro.", "width": "10%"})

        if self.modalidad:
            titles.append({"text": "Condicion", "width": "30%"})
        elif self.grupo_modalidad:
            titles.append({"text": "Modalidad", "width": "30%"})
        elif self.encuentro:
            titles.append({"text": "Grupo", "width": "30%"})
        elif self.temporada:
            titles.append({"text": "Sorteo", "width": "30%"})
            titles.append({"text": "Fecha", "width": "10%"})
            titles.append({"text": "Hora", "width": "10%"})
        elif self.deporte:
            titles.append({"text": "Liga", "width": "30%"})
        else:
            titles.append({"text": "Deporte", "width": "30%"})

        titles.append({"text": "Venta", "width": "15%"})
        titles.append({"text": "Porcentaje", "width": "15%"})

        return titles

    def apply_presentation_for_parley(self):
        data = {}

        data["column_extra"] = "1"

        if self.modalidad:
            tipo = 6
            encuentros_modalidades = list(SorteoModalidades.objects.filter(
                encuentro_id=self.encuentro,
                modalidad_grupo__grupo_id=self.grupo_modalidad,
                modalidad_grupo__modalidad_id=self.modalidad
            ).distinct().values_list("pk", flat=True))

            self.ventas = self.ventas.filter(
                juegos__encuentros_modalidad_id__in=encuentros_modalidades,
            )

            filtro_juego = apuesta.objects.filter(
                encuentros_modalidad__encuentro_id=self.encuentro,
                encuentros_modalidad__modalidad_grupo__grupo_id=self.grupo_modalidad,
                condicion__modalidad_id=self.modalidad,
                origen__isnull=True
            )

        elif self.grupo_modalidad:
            tipo = 5
            encuentro_modalidad_all = SorteoModalidades.objects.filter(
                encuentro_id=self.encuentro,
                modalidad_grupo__grupo_id=self.grupo_modalidad
            ).distinct("pk")

            self.ventas = self.ventas.filter(
                juegos__encuentros_modalidad_id__in=list(encuentro_modalidad_all
                                                         .values_list("pk", flat=True))
            )

            filtro_juego = ModalidadJuego.objects.filter(
                pk__in=list(encuentro_modalidad_all.values_list(
                    "modalidad_grupo__modalidad_id", flat=True))
            )

        elif self.encuentro:
            tipo = 4
            encuentro = Sorteo.objects.get(pk=self.encuentro)

            filtro_juego = encuentro.encuentrosmodalidades_set.all() \
                .distinct("modalidad_grupo__grupo_id")

        elif self.temporada:
            tipo = 3

            ini = self.fecha_inicio + hora_cero
            fin = self.fecha_inicio + hora_23

            kwargs_1 = {}
            kwargs_2 = {}
            if self.pertenece.prefix_filter != "master":
                kwargs_1["jornada__sistema"] = self.kwargs[
                    'object_sistema_juego']
                kwargs_2["jornada__sistema"] = self.kwargs[
                    'object_sistema_juego']

            kwargs_1["pk__in"] = list(
                self.ventas.filter(
                    juegos__temporada_id=self.temporada).values_list(
                    "juegos__encuentro_id",
                    flat=True).distinct("juegos__encuentro_id"))

            kwargs_2["jornada__temporadas_id"] = self.temporada
            kwargs_2["horajuego__range"] = (ini, fin)

            filtro_juego = Sorteo.objects.filter(
                **kwargs_1
            ).filter(**kwargs_2)

            data["column_extra"] = "123"

        elif self.deporte:
            tipo = 2

            kwargs = {}
            if self.pertenece.prefix_filter != "master":
                kwargs["jornadas__sistema"] = self.kwargs[
                    'object_sistema_juego']
            kwargs["pk__in"] = list(
                self.ventas.filter(
                    juegos__deporte_id=self.deporte).values_list(
                    "juegos__temporada_id",
                    flat=True).distinct("juegos__temporada_id"))

            filtro_juego = Fechas.objects.filter(
                **kwargs
            ).distinct("pk")

        else:
            tipo = 1
            filtro_juego = TipoProducto.objects.filter(
                pk__in=list(self.ventas.values_list(
                    "juegos__deporte_id",
                    flat=True
                ).distinct("juegos__deporte_id"))
            )

        # Totalizacion de venta
        sum_venta_total = self.ventas.aggregate(Sum('monto_total'))['monto_total__sum']
        sum_venta_total = round(
            Decimal(str("0.00")) if not sum_venta_total else sum_venta_total,
            2
        )

        count = 0
        data_juegos = []
        for item in filtro_juego:
            count += 1
            data_interna_juegos = {}
            data_interna_juegos["pertenece"] = []

            data_interna_juegos["pertenece"].append(
                self.type_html_conf(False, count, "")
            )

            if tipo == 1:  # por deporte
                venta_detalle = self.ventas.filter(
                    juegos__deporte_id=item.pk
                )

                texto = '<a href="#" class="link" onclick=AgrupadoPorJuego({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        item.nombre
                    )

                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto, "")
                )

            elif tipo == 2:  # por temporada
                venta_detalle = self.ventas.filter(
                    juegos__temporada_id=item.pk)

                texto = '<a href="#" class="link" onclick=AgrupadoPorJuego({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        item.torneo.nombre + " - " + item.nombre
                    )

                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto, "")
                )

            elif tipo == 3:  # por encuentros
                venta_detalle = self.ventas.filter(
                    juegos__encuentro_id=item.pk)

                campo = ""
                d_e = item.encuentrosdetail_set.all()
                equipo_len = d_e.count()
                i = 0
                for obj in d_e:
                    campo += obj.equipos_temporadas.equipo.nombre
                    i += 1
                    if (equipo_len > i):
                        campo += " Vs. "

                texto = '<a href="#" class="link" onclick=AgrupadoPorJuego({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        campo
                    )

                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto, "")
                )
                objFecha = strFecha(item.horajuego)
                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, objFecha.getFecha(), "")
                )
                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, objFecha.getHora(), "")
                )

            elif tipo == 4:  # por grupos

                encuentro_modalidad_all = SorteoModalidades.objects.filter(
                    encuentro=item.encuentro,
                    modalidad_grupo__grupo=item.modalidad_grupo.grupo
                ).distinct()

                venta_detalle = self.ventas.filter(
                    juegos__encuentros_modalidad_id__in=list(encuentro_modalidad_all
                                                             .values_list("pk", flat=True))
                )

                texto = '<a href="#" class="link" onclick=AgrupadoPorJuego({0},"{1}")>{2}</a>'\
                    .format(
                        item.modalidad_grupo.grupo_id,
                        item.modalidad_grupo.prefix_filter,
                        item.modalidad_grupo.grupo.nombre
                    )

                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto, "")
                )

            elif tipo == 5:  # por modalidades

                venta_detalle = self.ventas.filter(
                    juegos__modalidad_id=item.pk
                )

                texto = '<a href="#" class="link" onclick=AgrupadoPorJuego({0},"{1}")>{2}</a>'\
                    .format(
                        item.pk,
                        item.prefix_filter,
                        item.modalidad
                    )

                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, texto, "")
                )

            elif tipo == 6:  # por condiciones
                venta_detalle = self.ventas.filter(
                    juegos__pertenece=item.get_pertenece(),
                    juegos__condicion_id=item.condicion_id,
                    juegos__modalidad_id=item.condicion.modalidad_id,
                )

                texto = item.get_pertenece()
                data_interna_juegos["pertenece"].append(
                    self.type_html_conf(True, item.get_pertenece(), "")
                )

            sum_venta = venta_detalle.aggregate(Sum('monto_total'))[
                'monto_total__sum']
            if not sum_venta:
                sum_venta = Decimal(str("0.00"))
                data_interna_juegos["pertenece"][1]["val"] = \
                    data_interna_juegos["pertenece"][1]["val"].replace("link", "link-red") \
                    .replace("AgrupadoPorJuego", "").replace("<a", "<span").replace("a>", "span>")

            sum_venta = round(sum_venta, 2)
            data_interna_juegos["pertenece"].append(
                self.type_html_conf(False, sum_venta))

            data_juegos.append(data_interna_juegos)

        for item in data_juegos:
            if sum_venta_total:
                porcentaje = round(
                    (item["pertenece"][len(item["pertenece"]) - 1]["val"] * 100) / sum_venta_total,
                    1
                )
            else:
                porcentaje = 0

            item["pertenece"].append(
                self.type_html_conf(
                    True,
                    '<p class="{0} no-pd" >{1}</p>'.format(
                        'text-align-right',
                        "0%" if not porcentaje else str(
                            round(porcentaje, 2)) + "%"
                    )
                )
            )

        data["detalle"] = data_juegos

        data['totales'] = ['Total']
        for extra in data['column_extra']:
            data['totales'].append(
                ''
            )
        data['totales'].append(sum_venta_total)
        data['totales'].append("0%" if not sum_venta_total else "100%")

        return data

    def get_titles_for_agencia(self):
        titles = []

        titles.append({'text': 'Nro.', 'width': '10%'})
        if self.all_query:
            titles.append({'text': 'Codigo', 'width': '30%'})
        titles.append({'text': 'Centros de apuesta', 'width': '30%'})
        titles.append({'text': 'Venta', 'width': '15%'})
        titles.append({'text': 'Porcentaje', 'width': '15%'})

        return titles

    def apply_presentation_for_agencia(self):
        data = {}

        # Totalizacion de venta
        sum_venta_total = self.ventas.aggregate(Sum('monto_total'))[
            'monto_total__sum']
        sum_venta_total = round(
            Decimal(str("0.00")) if not sum_venta_total else sum_venta_total,
            2
        )

        self.start = int(self.request.REQUEST.get('iDisplayStart', 0))
        if self.all_query is False:
            kwargs_filter = {}
            if self.pertenece.prefix_filter != 'agencia':
                agencias_ids = list(self.ventas.distinct(
                    'comercializacion__agencia_id'
                ).values_list('comercializacion__agencia_id', flat=True))
                kwargs_filter['pk__in'] = agencias_ids
            else:
                kwargs_filter['pk'] = self.pertenece.pk
            agencias = Agencias.objects.filter(
                **kwargs_filter).order_by('nombre')

            # Paginacion #
            self.total_display_records = agencias.count()
            limit = min(
                int(self.request.REQUEST.get('iDisplayLength', 10)), 100)
            offset = self.start + limit
            self.pagin_process = False

            agencias = agencias[self.start:offset]
        else:
            agencias = Agencias.objects.filter(
                **self.pertenece.get_kwargs_by_agencia()
            ).order_by('codigo')
            ############################################################

        i = self.start
        data_cadena = []
        for item in agencias:
            i += 1
            data_interna_cadena = {}
            data_interna_cadena["pertenece"] = []

            data_interna_cadena["pertenece"].append(
                self.type_html_conf(False, i, "")
            )

            if self.all_query:
                codigo = item.codigo
                if item.codigo:
                    codigo = item.codigo
                else:
                    codigo = 'No aplica'

                data_interna_cadena["pertenece"].append(
                    self.type_html_conf(True, codigo, "")
                )

            data_interna_cadena["pertenece"].append(
                self.type_html_conf(True, str(item), "")
            )

            venta_detalle = self.ventas.filter(
                ** item.get_kwargs_dimension_comercializadora()
            )

            sum_venta = venta_detalle.aggregate(Sum('monto_total'))[
                'monto_total__sum']

            if not sum_venta:
                sum_venta = Decimal(str("0.00"))

            sum_venta = round(sum_venta, 2)
            data_interna_cadena["pertenece"].append(
                self.type_html_conf(False, sum_venta)
            )

            if sum_venta_total:
                porcentaje = round(((sum_venta * 100) / sum_venta_total), 2)
            else:
                porcentaje = 0

            data_interna_cadena["pertenece"].append(
                self.type_html_conf(
                    True,
                    '<p class="{0} no-pd" >{1}</p>'.format(
                        'text-align-right',
                        "0%" if not porcentaje else str(
                            round(porcentaje, 2)) + "%"
                    )
                )
            )
            data_cadena.append(data_interna_cadena)

        data['totales'] = ['Total']
        data['totales'].append('')
        if self.all_query:
            data['totales'].append('')
        data['totales'].append(sum_venta_total)
        data['totales'].append("0%" if not sum_venta_total else "100%")

        data["detalle"] = data_cadena
        return data


class VentasLineaDatatableView(VentasLineaProcessView, BaseDatatableView):
    # Orden del filtro
    order_columns = None

    def get_initial_queryset(self):
        self.get_hecho_venta()

        if self.agrupado == 'parley':
            self.apply_filter_juego()
        else:
            self.apply_filter_cadena()
        self.execute_query()

        if self.ventas.exists() and self.agrupado == 'parley':
            messages.info(
                self.request,
                MESSAGES_GLOBAL["consulta_por_juegos"]
            )

        qs = self.content
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        if qs:
            json_data = self.prepare_results_for_venta(qs)
        return json_data

    def prepare_footeresults(self, qs):
        footer = []
        if qs:
            footer = self.prepare_footer_for_venta()
        return footer
