# -*- coding: utf-8 -*-
from admin_juego.forms import CondicionesForm, RestriccionesReferenciasForm
from admin_juego.models import Condiciones, Deportes_Grupos, Modalidades_Grupos, RestriccionesReferencias
from admin_lib.util_views import MyViewBase
from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView


class CondicionesView(MyViewBase):
    model = Condiciones
    form_class = CondicionesForm

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        if self.request.POST.get("_save") == "_save":
            return reverse("admin_juego_condiciones_list")
        elif self.request.POST.get("_save") == "_continue":
            return reverse(
                "admin_juego_condiciones_update",
                kwargs={'pk': self.object.pk}
            )
        elif self.request.POST.get("_save") == "_addanother":
            return reverse("admin_juego_condiciones_create")
        elif self.request.POST.get("_save") == "_save_restriccion_referencia":
            return reverse(
                "admin_juego_condiciones_update_referencias",
                kwargs={'pk': self.object.pk}
            )
        else:
            return None


class CondicionesCreateView(CondicionesView, CreateView):
    pass


class CondicionesDeleteView(CondicionesView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class CondicionesDetailView(CondicionesView, DetailView):
    pass


class CondicionesListView(CondicionesView, ListView):
    pass


class CondicionesUpdateView(CondicionesView, UpdateView):
    pass


class RestriccionesReferenciasCondicionView(MyViewBase, TemplateView):
    model = Condiciones
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
            self.object = Condiciones.objects.get(pk=kwargs["pk"])
        except Condiciones.DoesNotExist:
            raise Http404

        return super(RestriccionesReferenciasCondicionView, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(RestriccionesReferenciasCondicionView, self).get_context_data(**kwargs)

        context["object"] = self.object

        context["grupos"] = []
        context["titles"] = {
            "deporte": "Deporte",
            "title1": "Minima Referencia",
            "title2": "Maxima Referencia"
        }

        modalidad_grupos = Modalidades_Grupos.objects.filter(
            modalidad=self.object.modalidad.pk
        )
        for mg in modalidad_grupos:
            json = {}
            json["grupo"] = mg.grupo.nombre
            json["deporte"] = []
            grupo_deportes = Deportes_Grupos.objects.filter(
                grupo=mg.grupo
            )
            for gd in grupo_deportes:
                if mg.deporte_restriccion.filter(
                    pk=gd.deporte.id
                ).exists():
                    continue
                json_interno = {
                    "deporte": gd.deporte.nombre,
                    "min_ref": context["form"][
                        str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_min"
                    ],
                    "max_ref": context["form"][
                        str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_max"
                    ]
                }
                json["deporte"].append(json_interno)
            context["grupos"].append(
                json
            )

        return context

    def post(self, request, *args, **kwargs):

        form = self.get_filter_form()
        if not form.is_valid():
            return super(RestriccionesReferenciasCondicionView, self).get(request, *args, **kwargs)

        modalidad_grupos = Modalidades_Grupos.objects.filter(
            modalidad=self.object.modalidad
        )

        for mg in modalidad_grupos:
            grupo_deportes = Deportes_Grupos.objects.filter(
                grupo=mg.grupo
            )
            for gd in grupo_deportes:
                valor_min = request.POST.get(str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_min")
                valor_max = request.POST.get(str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_max")
                try:
                    referencia = RestriccionesReferencias.objects.get(
                        grupo=mg.grupo,
                        deporte=gd.deporte,
                        condicion=self.object
                    )
                except RestriccionesReferencias.DoesNotExist:
                    referencia = None

                if referencia:
                    referencia.min_ref = valor_min
                    referencia.max_ref = valor_max
                    referencia.save(update_fields=["min_ref", "max_ref"])
                else:
                    referencia = RestriccionesReferencias(
                        deporte=gd.deporte,
                        grupo=mg.grupo,
                        condicion=self.object,
                        min_ref=valor_min,
                        max_ref=valor_max,
                    )
                    referencia.save()

        return HttpResponseRedirect(
            reverse("admin_juego_condiciones_list")
        )
