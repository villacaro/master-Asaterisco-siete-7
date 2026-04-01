# -*- coding: utf-8 -*-

from decimal import Decimal

from admin_apuestas.models import Tickets
from admin_comercializacion.models import Agencias, Bancas, Bloques, Distribuidores, Operadoras, Taquillas
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_forms import FilterCadenaComercializacionForm
from admin_lib.util_views import MyViewBase
from admin_reportes.forms import FilterFechasForm
from django.db.models import Sum
from django.http import Http404
from django.utils.timezone import now
from django.views.generic import TemplateView


class ListadoTicketsEstatus(MyViewBase, TemplateView):
    template_name = "admin_reportes/tickets/listado-tickets-por-estatus.html"
    tipo = {
        "ganadores": {
            "codenames": (
                "status_procesandoganador",
                "status_pagado", "status_ganado_frio"
            ),
            "column": (
                "Ganadores",
            ),
        },
        "pagados": {
            "codenames": (
                "status_pagado",
                "status_ganado_frio"
            ),
            "column": (
                "Pagados",
                "Frios",
            ),
        },
        "anulados": {
            "codenames": (
                "status_anulado",
                "status_anulado_automatico"
            ),
            "column": (
                "Anulados",
            ),
        },
    }

    def get_context_data(self, **kwargs):
        self.data = super(ListadoTicketsEstatus, self).get_context_data(**kwargs)

        self.data["comercializadora"] = self.object_comercializadora
        self.tipo = self.tipo.get(self.kwargs.get("estatus"))

        if not self.tipo:
            raise Http404

        self.data["verbose_name"] = self.kwargs.get("estatus")
        if self.request.method == "POST":
            self.data["form_fecha"] = FilterFechasForm(
                self.request.POST,
                **self.get_form_kwargs()
            )
            self.data["form_cadena"] = FilterCadenaComercializacionForm(
                self.request.POST,
                **self.get_form_kwargs()
            )
            self.data["form_cadena"].is_valid()
        else:
            self.data["form_fecha"] = FilterFechasForm()
            self.data["form_cadena"] = FilterCadenaComercializacionForm(
                **self.get_form_kwargs()
            )

        self._object = self.object_comercializadora.get_object()
        self.procesar_consulta()

        return self.data

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def procesar_consulta(self):
        self.data["consulta"] = {}
        self.datos = self.request.POST

        if self.datos.get("fecha_inicio"):
            ini = self.datos.get("fecha_inicio") + hora_cero
            fin = self.datos.get("fecha_inicio") + hora_23
        else:
            objFecha = strFecha(now())
            ini = objFecha.getFecha() + hora_cero
            fin = objFecha.getFecha() + hora_23

        if self.kwargs.get("estatus") == "pagados":
            # Solo los tickets pagados se rigen por esa fecha
            tickets = Tickets.objects.filter(
                updated_at__range=(ini, fin),
                status__codename__in=self.tipo.get("codenames")
            )
        else:
            tickets = Tickets.objects.filter(
                fecha__range=(ini, fin)
            )

        self.data["consulta"]["titles"] = []
        self.data["consulta"]["titles"].append(
            {"text": "Nro.", "width": "10%"}
        )

        self.data["atras"] = ""

        if self.datos.get("taquilla"):
            pertenece = Taquillas.objects.get(pk=self.datos.get("taquilla"))
        elif self.datos.get("agencia"):
            pertenece = Agencias.objects.get(pk=self.datos.get("agencia"))
        elif self.datos.get("distribuidor"):
            pertenece = Distribuidores.objects.get(pk=self.datos.get("distribuidor"))
        elif self.datos.get("banca"):
            pertenece = Bancas.objects.get(pk=self.datos.get("banca"))
        elif self.datos.get("bloque"):
            pertenece = Bloques.objects.get(pk=self.datos.get("bloque"))
        elif self.datos.get("operadora"):
            pertenece = Operadoras.objects.get(pk=self.datos.get("operadora"))
        else:
            pertenece = self._object

        if self._object.nivel < pertenece.nivel:
            origen = pertenece.get_origen()
            self.data["atras"] = "ConsultaListadoTicketsPorEstatus({0},'{1}')".format(
                origen.pk,
                origen.prefix_filter
            )

        self.data["accion"] = "ConsultaListadoTicketsPorEstatus({0},'{1}')".format(
            pertenece.pk,
            pertenece.prefix_filter
        )

        if pertenece.prefix_filter != "taquilla":
            kwargs = {}

            if pertenece.prefix_filter != "master":
                kwargs[
                    "user__taquilla" + pertenece.get_prefix_kwargs_by_level_taquilla()
                ] = pertenece.pk
                tickets = tickets.filter(**kwargs)

            verbose_name_hijos = ""
            if pertenece.get_offspring().exists():
                verbose_name_hijos = pertenece.get_offspring()[0].get_verbose_name_plural()

            self.data["consulta"]["titles"].append(
                {
                    "text": verbose_name_hijos,
                    "width": ""
                }
            )
            for column in self.tipo.get("column"):
                self.data["consulta"]["titles"].append(
                    {"text": "Cant. " + column, "width": "15%"}
                )
            self.data["total"] = tickets.count()
            self.data["consulta"]["detalle"] = []

            for item in pertenece.get_offspring():

                json = []

                texto = "<a href='#' class='link' onclick='{0}'>{1}</a>".format(
                    'ConsultaListadoTicketsPorEstatus({0},"{1}")'.format(
                        item.pk,
                        item.prefix_filter
                    ),
                    item
                )
                # texto mas enlace
                json.append(self.type_html_Conf(True, texto))

                kwargs = {}
                kwargs[
                    "user__taquilla" + item.get_prefix_kwargs_by_level_taquilla()
                ] = item.pk

                tickets_detalle = tickets.filter(**kwargs)

                cantidad = 0
                if len(self.tipo.get("column")) == 1:
                    tickets_detalle = tickets_detalle.filter(
                        status__codename__in=self.tipo.get("codenames")
                    )
                    cantidad = tickets_detalle.count()
                    json.append(self.type_html_Conf(False, cantidad, "text-align-right"))

                else:
                    for codename in self.tipo.get("codenames"):
                        tickets_detalle_interna = tickets_detalle.filter(
                            status__codename=codename
                        )
                        cantidad_interna = tickets_detalle_interna.count()
                        cantidad += cantidad_interna
                        json.append(
                            self.type_html_Conf(False, cantidad_interna, "text-align-right")
                        )

                if cantidad == 0:
                    json[0]["val"] = json[0]["val"].replace("link", "link-red") \
                        .replace("ConsultaListadoTicketsPorEstatus", "") \
                        .replace("<a", "<span").replace("a>", "span>")

                self.data["consulta"]["detalle"].append(json)

            self.data["totales"] = []
            if len(self.tipo.get("column")) == 1:
                tickets_detalle = tickets.filter(
                    status__codename__in=self.tipo.get("codenames")
                )
                self.data["totales"].append(tickets_detalle.count())
            else:
                for codename in self.tipo.get("codenames"):
                    tickets_detalle = tickets.filter(
                        status__codename=codename
                    )
                    self.data["totales"].append(tickets_detalle.count())
        else:
            tickets = tickets.filter(
                user__taquilla=pertenece,
                status__codename__in=self.tipo.get("codenames")
            )
            self.data["consulta"]["titles"].append({"text": "Nro. Tickets", "width": ""})
            self.data["consulta"]["titles"].append({"text": "Fecha y hora", "width": "15%"})
            self.data["consulta"]["titles"].append({"text": "Apuestas", "width": ""})
            self.data["consulta"]["titles"].append({"text": "Montos", "width": ""})
            self.data["consulta"]["titles"].append({"text": "Posible ganancia", "width": ""})
            self.data["consulta"]["titles"].append({"text": "Premio", "width": ""})
            self.data["consulta"]["titles"].append({"text": "Fecha del estatus", "width": "15%"})
            self.data["consulta"]["titles"].append({"text": "Estatus", "width": ""})
            self.data["consulta"]["detalle"] = tickets
            self.data["taquilla"] = pertenece
            self.data["consulta"]["is_tickets"] = True
            self.data["totales"] = {}

            self.data["totales"]["monto"] = tickets.aggregate(Sum('monto'))["monto__sum"]
            self.data["totales"]["monto"] = 0.0 if self.data["totales"]["monto"] is None \
                else self.data["totales"]["monto"]

            self.data["totales"]["monto_premio"] = Decimal()
            for item in tickets:
                self.data["totales"]["monto_premio"] += item.get_monto_premio()

    def type_html_Conf(self, _type, val, _class=""):
        item = {}
        item["html"] = _type
        item["val"] = val
        item["class"] = _class
        return item
