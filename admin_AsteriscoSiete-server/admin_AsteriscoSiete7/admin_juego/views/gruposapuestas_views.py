# -*- coding: utf-8 -*-
from admin_juego.forms import GruposApuestasForm, RestriccionesReferenciasForm
from admin_juego.models import TipoProducto_Grupos, GruposApuesta
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.urls import reverse
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View


class GruposApuestasView(MyViewBase):
    model = GruposApuesta
    form_class = GruposApuestasForm

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        if self.request.POST.get("_save") == "_save":
            return reverse("admin_juego_gruposapuestas_list")
        elif self.request.POST.get("_save") == "_continue":
            return reverse(
                "admin_juego_gruposapuestas_update",
                kwargs={'pk': self.object.pk}
            )
        elif self.request.POST.get("_save") == "_addanother":
            return reverse("admin_juego_gruposapuestas_create")
        elif self.request.POST.get("_save") == "_save_restriccion_referencia":
            return reverse(
                "admin_juego_gruposapuestas_update_logros",
                kwargs={'pk': self.object.pk}
            )
        else:
            return None


class GruposApuestasCreateView(GruposApuestasView, CreateView):
    pass


class GruposApuestasDeleteView(GruposApuestasView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True

    def get_context_data(self, **kwargs):
        context = super(GruposApuestasDeleteView, self).get_context_data(**kwargs)
        context["rangos"] = []
        for gd in self.object.deportes_grupos_set.all():
            referencia = RestriccionesSorteo.objects.get(
                deporte=gd.deporte,
                grupo=self.object,
                min_ref='logro'
            )
            json = {
                "logo": referencia.deporte.logo,
                "nombre": referencia.deporte.nombre,
                "logro_favorito": referencia.max_logro_favorito,
                "logro_no_favorito": referencia.max_logro_no_favorito,
            }

            context["rangos"].append(
                json
            )
        return context


class GruposApuestasDetailView(GruposApuestasView, DetailView):

    def get_context_data(self, **kwargs):
        context = super(GruposApuestasDetailView, self).get_context_data(**kwargs)
        context["rangos"] = []
        for gd in self.object.deportes_grupos_set.all():
            referencia = RestriccionesSorteo.objects.get(
                deporte=gd.deporte,
                grupo=self.object,
                min_ref='logro'
            )
            json = {
                "logo": referencia.deporte.logo,
                "nombre": referencia.deporte.nombre,
                "logro_favorito": referencia.max_logro_favorito,
                "logro_no_favorito": referencia.max_logro_no_favorito,
            }

            context["rangos"].append(
                json
            )
        return context


class GruposApuestasListView(GruposApuestasView, ListView):
    pass


class GruposApuestasUpdateView(GruposApuestasView, UpdateView):
    pass


class RestriccionesReferenciasGrupoView(MyViewBase, TemplateView):
    model = GruposApuesta
    template_name = "admin_juego/modalidades/modalidades_referencias.html"

    form_class = RestriccionesReferenciasForm
    filter_form = None

    def get_filter_form(self):
        """
        Retorna el formulario de la instancia,
        de ya estar inicializado devuelve el que esta en memoria
        """
        if self.filter_form is None:
            if self.request.method == "POST":
                self.filter_form = self.form_class(
                    self.request.POST,
                    **self.get_form_kwargs()
                )
            else:
                self.filter_form = self.form_class(
                    **self.get_form_kwargs()
                )
        return self.filter_form

    def dispatch(self, request, *args, **kwargs):
        """
        Esta clase es como el init se ejecuta de primera
        """
        try:
            self.object = GruposApuesta.objects.get(pk=kwargs["pk"])
        except GruposApuesta.DoesNotExist:
            raise Http404

        return super(RestriccionesReferenciasGrupoView, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(RestriccionesReferenciasGrupoView, self).get_context_data(**kwargs)

        context["object"] = self.object

        context["titles"] = {
            "deporte": "deporte",
            "title1": "Logro maximo (-)",
            "title2": "Logro maximo (+)"
        }

        context["grupos"] = []
        json = {}
        json["grupo"] = self.object.nombre
        json["deporte"] = []
        grupo_deportes = TipoProducto_Grupos.objects.filter(
            grupo=self.object
        )
        for gd in grupo_deportes:
            json_interno = {
                "deporte": gd.deporte.nombre,
                "min_ref": context["form"][
                    str(self.object.id) + "_" + str(gd.deporte.id) + "_maxfavorito"
                ],
                "max_ref": context["form"][
                    str(self.object.id) + "_" + str(gd.deporte.id) + "_maxnofavorito"
                ]
            }
            json["deporte"].append(
                json_interno
            )

        context["grupos"].append(
            json
        )

        return context

    def post(self, request, *args, **kwargs):

        form = self.get_filter_form()
        if not form.is_valid():
            return super(RestriccionesReferenciasGrupoView, self).get(request, *args, **kwargs)

        grupo_deportes = TipoProducto_Grupos.objects.filter(
            grupo=self.object
        )

        for gd in grupo_deportes:
            valor_maxfav = request.POST.get(
                str(self.object.id) + "_" + str(gd.deporte.id) + "_maxfavorito"
            )
            valor_maxnofav = request.POST.get(

                str(self.object.id) + "_" + str(gd.deporte.id) + "_maxnofavorito"
            )
            try:
                referencia = RestriccionesSorteo.objects.get(
                    deporte=gd.deporte,
                    grupo=self.object,
                    min_ref='logro'
                )
            except RestriccionesSorteo.DoesNotExist:
                referencia = None

            if referencia:
                referencia.max_logro_favorito = int(valor_maxfav)
                referencia.max_logro_no_favorito = int(valor_maxnofav)
                referencia.save()
            else:
                referencia = RestriccionesSorteo(
                    deporte=gd.deporte,
                    grupo=self.object,
                    min_ref='logro',
                    max_logro_favorito=int(valor_maxfav),
                    max_logro_no_favorito=int(valor_maxnofav)

                )
                referencia.save()

        return HttpResponseRedirect(
            reverse("admin_juego_gruposapuestas_list")
        )


class GruposListbyDeporteAjax(View):

    def dispatch(self, request, *args, **kwargs):

        grupos = GruposApuesta.objects.filter(
            deportes_grupos__deporte_id=request.REQUEST['deporte'],
        ).distinct()

        return HttpResponse(
            content=JsonDumps(
                list(
                    grupos.values(
                        "pk",
                        "nombre"
                    )
                )
            ),
            content_type='application/json'
        )
