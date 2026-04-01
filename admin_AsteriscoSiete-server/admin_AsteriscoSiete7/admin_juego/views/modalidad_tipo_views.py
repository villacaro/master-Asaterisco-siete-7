# -*- coding: utf-8 -*-
from admin_juego.forms import EquiposForm
from admin_juego.models import ModalidadJuego, ModalidadProducto, ModalidadPeriodo, GruposApuesta, Fechas
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_forms import FilterEquipoForm
from admin_lib.util_icons import Icons
from admin_lib.util_json import JsonDumps
from admin_lib.util_views import MyViewBase
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponse
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView, View


class EquiposView(MyViewBase):
    model = ModalidadJuego
    form_class = EquiposForm

    def get_success_url_filter_form(self):
        '''
        Devuelve los filtros equivalentes
        '''
        return '?deporte={0}&equipo={1}'.format(
            self.object.deporte.pk,
            self.object.pk,
        )

    def get_queryset(self):
        return ModalidadJuego.objects.all()


class EquiposCreateView(EquiposView, CreateView):

    def form_valid(self, form):
        ligas = self.request.POST.getlist('liga_deporte')
        form.instance.save()
        if len(ligas) > 0:
            for i, liga in enumerate(ligas):
                ModalidadProducto.objects.create(
                    equipo=form.instance,
                    liga=TipoProducto.objects.get(pk=liga)
                )
        if self.request.POST['_save'] == '_addanother':

            messages.success(
                self.request,
                '¡Enhorabuena! {0} {1} '
                'ha sido guardado con éxito!'.format(
                    self.model().__class__.__name__.lower(),
                    form.instance
                )
            )

            ligas = TipoProducto.objects.filter(
                deporte=form.instance.deporte
            )
            ligas_array = []
            for liga in ligas:
                liga_array = {}
                liga_array['pk'] = liga.pk
                liga_array['nombre'] = liga.nombre
                liga_array['logo'] = liga.logo
                if ModalidadProducto.objects.filter(
                    equipo=form.instance,
                    liga=liga
                ).exists():
                    liga_array['check'] = 'checked'
                ligas_array.append(liga_array)

            form.data['nombre'] = ''
            return self.render_to_response(self.get_context_data(form=form, ligas=ligas_array))
        return super(EquiposCreateView, self).form_valid(form)


class EquiposDeleteView(EquiposView, DeleteView):
    '''
    se activa la bandera relate_delete_validate que sirve de proteccion
    contra la eliminacion de los objetos
    '''
    relate_delete = True
    relate_delete_validate = True


class EquiposDetailView(EquiposView, DetailView):
    pass


class EquiposListView(EquiposView, ListView):
    filter_form = None
    form_class = FilterEquipoForm

    def get_next_url_filter_form(self):
        parameters = '?deporte={0}&torneo={1}&equipo={2}'.format(
            self.request.GET.get('deporte'),
            self.request.GET.get('torneo') if self.request.GET.get('torneo') else 0,
            self.request.GET.get('equipo') if self.request.GET.get('equipo') else 0,
        )
        return '?next=' + reverse('admin_juego_equipos_list') + parameters

    def get_queryset(self):
        equipos = ModalidadJuego.objects.select_related('deporte').all()
        deporte = self.request.GET.get('deporte')
        torneo = self.request.GET.get('torneo')
        equipo = self.request.GET.get('equipo')

        if equipo and equipo != '0':
            equipos = equipos.filter(pk=equipo)
        elif torneo and torneo != '0':
            equipos = equipos.filter(equiposligas__liga_id=torneo)
        elif deporte and deporte != '0':
            equipos = equipos.filter(deporte_id=deporte)
        else:
            equipos = equipos.none()

        return equipos.order_by('nombre', 'id').distinct()


class EquiposUpdateView(EquiposView, UpdateView):

    def form_valid(self, form):
        form.instance.save()
        ligas = self.request.POST.getlist('liga_deporte')
        if len(ligas) > 0:
            new_equipo_liga = []
            for i, liga in enumerate(ligas):
                equipo_liga = ModalidadProducto.objects.get_or_create(
                    equipo=form.instance,
                    liga=TipoProducto.objects.get(pk=liga)
                )[0]
                new_equipo_liga.append(equipo_liga.pk)

            for old_equipo_liga in ModalidadProducto.objects.filter(
                equipo=form.instance
            ).exclude(pk__in=new_equipo_liga):
                old_equipo_liga.delete()

        return super(EquiposUpdateView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EquiposUpdateView, self).get_context_data(**kwargs)

        ligas = TipoProducto.objects.filter(
            deporte=self.object.deporte
        )
        ligas_array = []
        for liga in ligas:
            liga_array = {}
            liga_array['pk'] = liga.pk
            liga_array['nombre'] = liga.nombre
            liga_array['logo'] = liga.logo
            if ModalidadProducto.objects.filter(
                equipo=self.object,
                liga=liga
            ).exists():
                liga_array['check'] = 'checked'
            ligas_array.append(liga_array)
        context['ligas'] = ligas_array
        return context


class EquiposListbyTemporadaAjax(View):

    def dispatch(self, request, *args, **kwargs):

        temporada = Fechas.objects.get(
            pk=request.REQUEST.get('temporada')
        )

        equipos_array = []

        if ModalidadPeriodo.objects.filter(
            temporada=temporada
        ).exists():

            equipos = ModalidadJuego.objects.filter(
                deporte_id=temporada.torneo.deporte.pk
            ).order_by('nombre')

            for equipo in equipos:
                equipo_json = {
                    'pk': equipo.pk,
                    'nombre': equipo.nombre,
                    'logo': '{0}'.format(equipo.logo)
                }
                if ModalidadPeriodo.objects.filter(
                    temporada=temporada,
                    equipo=equipo
                ).exists():
                    equipo_json['check'] = 'checked'
                equipos_array.append(equipo_json)

        return HttpResponse(
            content=JsonDumps(
                equipos_array
            ),
            content_type='application/json'
        )


class EquiposListbyTemporada2Ajax(View):

    def dispatch(self, request, *args, **kwargs):

        temporada = Fechas.objects.get(
            pk=request.REQUEST.get('temporada')
        )

        deporte = temporada.torneo.deporte

        equipos = ModalidadJuego.objects.filter(
            deporte_id=deporte.pk,
            equipostemporadas__temporada_id=temporada.pk
        ).distinct().order_by('nombre', 'id')

        indices = []
        for indice in range(0, deporte.cantidad):
            indices.append(
                {
                    'pk': (indice + 1)
                }
            )

        json = {
            'equipos': list(
                equipos.values(
                    'pk',
                    'nombre',
                    'logo'
                )
            ),
            'indices': indices
        }

        return HttpResponse(
            content=JsonDumps(
                json
            ),
            content_type='application/json'
        )


class EquiposListbyTemporada3Ajax(View):

    def dispatch(self, request, *args, **kwargs):

        if request.REQUEST.get('temporada', None) is None:
            equipos = ModalidadJuego.objects.none()
        else:
            equipos = ModalidadJuego.objects.filter(

                equipostemporadas__temporada_id=request.REQUEST.get('temporada')

            ).distinct().order_by('nombre', 'id')

        return HttpResponse(
            content=JsonDumps(
                list(
                    equipos.values(
                        'pk',
                        'nombre',
                        'logo'
                    )
                )
            ),
            content_type='application/json'
        )


class EquiposListbyGrupoAjax(View):

    def dispatch(self, request, *args, **kwargs):

        equipos = ModalidadJuego.objects.filter(
            equiposgrupos__grupo_id=request.REQUEST.get('grupo')
        ).order_by('nombre')

        indices = []

        try:
            grupo = GruposApuesta.objects.get(
                pk=request.REQUEST.get('grupo')
            )

            for indice in range(0, grupo.temporada.torneo.deporte.cantidad):
                indices.append(
                    {
                        'pk': (indice + 1)
                    }
                )

        except GruposApuesta.DoesNotExist:
            pass

        json = {
            'equipos': list(
                equipos.values(
                    'pk',
                    'nombre',
                    'logo'
                )
            ),
            'indices': indices
        }

        return HttpResponse(
            content=JsonDumps(
                json
            ),
            content_type='application/json'
        )


class EquiposListbyDeporteAjax(View):

    def dispatch(self, request, *args, **kwargs):

        equipos = ModalidadJuego.objects.filter(
            deporte_id=request.REQUEST.get('deporte')
        ).order_by('nombre')

        equipos_array = []
        for equipo in equipos:
            equipos_array_interno = {
                'pk': equipo.pk,
                'nombre': equipo.nombre,
                'logo': '{0}'.format(equipo.logo),
                'ligas': [],
                'temporadas': [],
                'grupos': []
            }

            for equipos_liga in equipo.equiposligas_set.all():
                equipos_array_interno['ligas'].append(
                    equipos_liga.liga.nombre
                )
            for equipos_temporada in equipo.equipostemporadas_set.all():
                equipos_array_interno['temporadas'].append(
                    equipos_temporada.temporada.nombre
                )
            for equipos_grupo in equipo.equiposgrupos_set.all():
                equipos_array_interno['grupos'].append(
                    equipos_grupo.grupo.nombre
                )

            equipos_array.append(equipos_array_interno)

        return HttpResponse(
            content=JsonDumps(
                equipos_array
            ),
            content_type='application/json'
        )


class EquiposListbyDeporteAjaxSimple(View):

    def dispatch(self, request, *args, **kwargs):

        equipos = ModalidadJuego.objects.filter(
            deporte_id=request.REQUEST.get('deporte')
        ).order_by('nombre')

        return HttpResponse(
            content=JsonDumps(
                list(
                    equipos.values(
                        'pk',
                        'nombre',
                        'logo'
                    )
                )
            ),
            content_type='application/json'
        )


class EquiposListbyligaAjax(View):

    def dispatch(self, request, *args, **kwargs):

        equipos = ModalidadJuego.objects.filter(
            equiposligas__liga_id=request.REQUEST.get('liga')
        ).distinct().order_by('nombre', 'id')

        return HttpResponse(
            content=JsonDumps(
                list(
                    equipos.values(
                        'pk',
                        'nombre',
                        'logo'
                    )
                )
            ),
            content_type='application/json'
        )


class EquiposDatatableView(EquiposListView, BaseDatatableView):
    model = ModalidadJuego
    order_columns = ['nombre']
    # Fields de busqueda
    filter_search = 'nombre'

    def get_initial_queryset(self):
        self.opcions_url = [
            'admin_juego_' + self.model.prefix_filter_plural + '_detail$' + Icons.detail,
            'admin_juego_' + self.model.prefix_filter_plural + '_update$' + Icons.update +
            '$' + self.get_next_url_filter_form(),
            'admin_juego_' + self.model.prefix_filter_plural + '_delete$' + Icons.delete,
        ]
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            ligas = item.get_ligas()
            ligas_new = ''
            for liga in ligas:
                ligas_new += '<span class="tag2 %s">%s</span>' % ('tag-blue', liga)

            if item.logo:
                logo = '<img src="' + item.get_logo() + '"' + \
                       'width="50" height="50">'
            else:
                logo = 'Sin imagen'
            json_data.append([
                (x + 1 + acarreo),
                item.nombre,
                logo,
                '<span class="tag2 %s">%s</span>' % ('tag-green', item.deporte.nombre),
                ligas_new,
                self.get_opcions(item.pk)
            ])
        return json_data
