# -*- coding: utf-8 -*-
from admin_juego.forms import Modalidades_GruposForm, ModalidadesForm, RestriccionesReferenciasForm
from admin_juego.models import Deportes, Modalidades, Modalidades_Grupos, RestriccionesReferencias
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView, DeleteView, DetailView, ListView, TemplateView, UpdateView, View


class ModalidadesView(MyViewBase):
    model = Modalidades
    form_class = ModalidadesForm

    def get_success_url_force(self):
        """
        Retorna un url de redireccion forzado
        """
        if self.request.POST.get("_save") == "_save":
            return reverse("admin_juego_modalidades_list")
        elif self.request.POST.get("_save") == "_continue":
            return reverse("admin_juego_modalidades_update")
        elif self.request.POST.get("_save") == "_addanother":
            return reverse("admin_juego_modalidades_create")
        elif self.request.POST.get("_save") == "_edit_deportes":
            return reverse(
                "admin_juego_modalidades_update_deportes",
                kwargs={'pk': self.object.pk}
            )
        elif self.request.POST.get("_save") == "_save_deporte_restriccion":
            return reverse("admin_juego_modalidades_list")
        elif self.request.POST.get("_save") == "_save_restriccion_referencia":
            return reverse(
                "admin_juego_modalidades_update_referencias",
                kwargs={'pk': self.object.pk}
            )
        else:
            return None


class ModalidadesCreateView(ModalidadesView, CreateView):
    pass


class ModalidadesDeleteView(ModalidadesView, DeleteView):
    """
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    """
    relate_delete = True
    relate_delete_validate = True


class ModalidadesDetailView(ModalidadesView, DetailView):
    pass


class ModalidadesListView(ModalidadesView, ListView):
    pass


class ModalidadesUpdateView(ModalidadesView, UpdateView):
    pass


class ModalidadesDeportesUpdateView(MyViewBase, TemplateView):
    model = Modalidades
    template_name = "admin_juego/modalidades/modalidades_grupos_formset.html"
    filter_form = None

    def dispatch(self, request, *args, **kwargs):
        """
        Esta clase es como el init se ejecuta de primera
        """

        try:
            self.object = Modalidades.objects.get(pk=kwargs["pk"])
        except Modalidades.DoesNotExist:
            from django.http import Http404
            raise Http404

        return super(ModalidadesDeportesUpdateView, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(ModalidadesDeportesUpdateView, self).get_context_data(**kwargs)
        context["object"] = self.object
        return context

    def get_filter_form(self):
        """
        Retorna el formulario de la instancia,
        de ya estar inicializado devuelve el que esta en memoria
        """
        if self.filter_form is None:
            form = modelformset_factory(
                Modalidades_Grupos,
                form=Modalidades_GruposForm,
                extra=1,
                max_num=Modalidades_Grupos.objects.filter(
                    modalidad=self.object
                ).count(),
            )
            self.filter_form = form(
                queryset=Modalidades_Grupos.objects.filter(
                    modalidad=self.object
                )
            )
        return self.filter_form

    def post(self, request, *args, **kwargs):
        for i in range(0, Modalidades_Grupos.objects.filter(modalidad=self.object).count()):
            pk = request.POST.get("form-{0}-id".format(i))
            restricciones = request.POST.getlist("form-{0}-deporte_restriccion".format(i))
            modalidad_grupo = Modalidades_Grupos.objects.get(
                pk=pk
            )

            for restriction in restricciones:
                try:
                    modalidad_grupo.deporte_restriccion.get(
                        pk=restriction
                    )
                except Deportes.DoesNotExist:
                    modalidad_grupo.deporte_restriccion.add(
                        restriction
                    )

            for restriction in modalidad_grupo.deporte_restriccion.all().exclude(
                pk__in=restricciones
            ):
                modalidad_grupo.deporte_restriccion.remove(
                    restriction
                )

        if self.object.etiqueta_ref:
            return HttpResponseRedirect(
                reverse(
                    "admin_juego_modalidades_update_referencias",
                    kwargs={'pk': self.object.pk}
                )
            )
        else:
            return HttpResponseRedirect(reverse("admin_juego_modalidades_list"))


class RestriccionesReferenciasModalidadView(MyViewBase, TemplateView):
    model = Modalidades
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
            self.object = Modalidades.objects.get(pk=kwargs["pk"])
        except Modalidades.DoesNotExist:
            from django.http import Http404
            raise Http404

        return super(RestriccionesReferenciasModalidadView, self).dispatch(
            request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        """
        Obtiene el context data
        """
        context = super(RestriccionesReferenciasModalidadView, self).get_context_data(**kwargs)

        context["object"] = self.object

        context["grupos"] = []
        context["titles"] = {
            "deporte": "Deporte",
            "title1": "Minima Referencia",
            "title2": "Maxima Referencia"
        }

        modalidad_grupos = Modalidades_Grupos.objects.filter(
            modalidad=self.object.pk
        )

        for mg in modalidad_grupos:
            json = {
                "grupo": mg.grupo.nombre,
                "deporte": []
            }
            for gd in mg.grupo.deportes_grupos_set.all():
                if mg.deporte_restriccion.filter(
                    pk=gd.deporte.id
                ).exists():
                    continue
                json["deporte"].append(
                    {
                        "deporte": gd.deporte.nombre,
                        "min_ref": context["form"][
                            str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_min"
                        ],
                        "max_ref": context["form"][
                            str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_max"
                        ]
                    }
                )
            context["grupos"].append(
                json
            )

        return context

    def post(self, request, *args, **kwargs):

        modalidad_grupos = Modalidades_Grupos.objects.filter(
            modalidad=self.object.pk
        )

        form = self.get_filter_form()
        if not form.is_valid():
            return super(RestriccionesReferenciasModalidadView, self).get(request, *args, **kwargs)

        for mg in modalidad_grupos:
            for gd in mg.grupo.deportes_grupos_set.all():
                if mg.deporte_restriccion.filter(
                    pk=gd.deporte.id
                ).exists():
                    continue

                valor_min = self.request.POST.get(str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_min")
                valor_max = self.request.POST.get(str(mg.grupo.id) + "_" + str(gd.deporte.id) + "_max")
                try:
                    referencia = RestriccionesReferencias.objects.get(
                        grupo=mg.grupo,
                        deporte=gd.deporte,
                        modalidad=self.object
                    )

                except RestriccionesReferencias.DoesNotExist:
                    referencia = None

                if referencia:
                    referencia.min_ref = valor_min
                    referencia.max_ref = valor_max
                    referencia.save(update_fields=["min_ref", "max_ref"])
                else:
                    obj = RestriccionesReferencias(
                        deporte=gd.deporte,
                        grupo=mg.grupo,
                        modalidad=self.object,
                        min_ref=valor_min,
                        max_ref=valor_max,
                    )
                    obj.save()

        return HttpResponseRedirect(
            reverse("admin_juego_modalidades_list")
        )


class ModalidadListbyGrupoAjax(View):

    def dispatch(self, request, *args, **kwargs):

        modalidades = Modalidades.objects.filter(
            modalidades_grupos__grupo_id=request.REQUEST['grupo'],
        ).distinct()

        modalidades_list = [{"pk": obj.pk, "nombre": obj.modalidad} for obj in modalidades]

        return HttpResponse(
            content=JsonDumps(
                modalidades_list
            ),
            content_type='application/json'
        )
