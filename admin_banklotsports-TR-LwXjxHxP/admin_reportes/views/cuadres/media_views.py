# -*- coding: utf-8 -*-

from admin_banklotsports.settings import FORMAT_STR_DATE_REPORTS
from admin_datamart.models import Hecho1_VentasCadenasJuegos, Hecho2_VentasCadenasLinea
from admin_finanzas.models import Comercializadora
from admin_juego.models import (
    Deportes, Encuentros, EncuentrosModalidades, GruposApuestas, Jugadas, Modalidades, Temporadas,
)
from admin_lib.util_fechas import hora_23, hora_cero, strFecha
from admin_lib.util_views import MyViewBase
from admin_reportes.forms import FilterFechasForm, FilterOptionMediaForm, FilterOrdenPresentacionReporteMediaForm
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.template import defaultfilters
from django.utils.timezone import now
from django.views.generic import TemplateView


class Media(MyViewBase, TemplateView):
    template_name = 'admin_reportes/cuadres/media.html'

    def get_context_data(self, **kwargs):
        self.context = super(Media, self).get_context_data(**kwargs)

        if self.request.method == 'GET':
            self.context[
                'form_agrupado'] = FilterOrdenPresentacionReporteMediaForm()
            self.context['form_option_media'] = FilterOptionMediaForm()
            self.context['form_fecha'] = FilterFechasForm()
        elif self.request.method == 'POST':
            self.context['form_agrupado'] = FilterOrdenPresentacionReporteMediaForm(
                self.request.POST
            )
            self.context['form_fecha'] = FilterFechasForm(
                self.request.POST
            )
            self.context['form_option_media'] = FilterOptionMediaForm(
                self.request.POST
            )

        self.context['form_fecha'].inicializar(tipo='Periodos')

        if self.request.REQUEST.get('fecha_inicio'):
            ini = self.request.REQUEST.get('fecha_inicio')
        else:
            ini = self.context['form_fecha'].fields['fecha_inicio'].initial
        if self.request.REQUEST.get('fecha_fin'):
            fin = self.request.REQUEST.get('fecha_fin')
        else:
            fin = self.context['form_fecha'].fields['fecha_fin'].initial

        self._object = self.object_comercializadora.get_object()
        self.option = self.request.REQUEST.get('option')

        if self.request.POST.get('orden') == 'comercializacion':

            self.calcular_intervalos_de_tiempo(ini, fin)
            self.context['prefix_label'] = self.prefix_label

            ventas = Hecho2_VentasCadenasLinea.objects.filter(
                tiempo__fecha__range=(ini, fin)
            )
            self.context['consulta'] = self.process_agrupado_cadena(ventas)

        elif self.request.POST.get('orden') == 'parley':
            # Por juegos no se calculan tickets sino por numero de apuestas
            self.option = self.option.replace(
                'count_tickets', 'count_apuestas')
            self.calcular_intervalos_de_tiempo(ini, fin)
            self.context['prefix_label'] = self.prefix_label

            ventas = Hecho1_VentasCadenasJuegos.objects.filter(
                tiempo__fecha__range=(ini, fin)
            )
            self.context['consulta'] = self.agrupado_deporte(ventas)

            if ventas.exists():
                from admin_banklotsports.settings import MESSAGES_GLOBAL
                from django.contrib import messages
                messages.info(self.request,
                              MESSAGES_GLOBAL['consulta_por_juegos'])

        return self.context

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

    def calcular_intervalos_de_tiempo(self, ini, fin):
        date_ini = now().strptime(ini, FORMAT_STR_DATE_REPORTS).date()
        date_fin = now().strptime(fin, FORMAT_STR_DATE_REPORTS).date()

        self.intervalos = []

        if date_ini.year != date_fin.year:
            # Por año
            self.prefix_date = 'year'
            self.prefix_label = 'Años'
        elif date_ini.month != date_fin.month:
            # Por mes
            self.prefix_date = 'month'
            self.prefix_label = 'Meses'
        else:
            # Por dia
            self.prefix_date = 'day'
            self.prefix_label = 'Días'

        kwargs = {}
        kwargs[self.prefix_date + 's'] = 1
        set_apply_ajust = True
        while True:

            if set_apply_ajust:
                if self.prefix_date == 'year':

                    date_fin_calculate = now().strptime(
                        '{0}-12-31'.format(date_ini.year),
                        FORMAT_STR_DATE_REPORTS
                    ).date()

                elif self.prefix_date == 'month':
                    date_fin_calculate = now().strptime(
                        '{0}-{1}-1'.format(date_ini.year, date_ini.month),
                        FORMAT_STR_DATE_REPORTS
                    ).date() + relativedelta(months=1)
                    date_fin_calculate = date_fin_calculate - \
                        relativedelta(days=1)
                else:
                    date_fin_calculate = date_ini
            else:
                date_fin_calculate = date_ini

            self.intervalos.append(
                [date_ini, date_fin_calculate]
            )

            if getattr(date_ini, self.prefix_date) == getattr(
                    date_fin, self.prefix_date):
                self.intervalos[-1][1] = date_fin
                # Salgo si llegue al tope, y reconfigura la fecha fin
                break

            if set_apply_ajust:
                if self.prefix_date == 'year':
                    date_ini = now().strptime(
                        '{0}-1-1'.format(date_ini.year),
                        FORMAT_STR_DATE_REPORTS
                    ).date()
                elif self.prefix_date == 'month':
                    date_ini = now().strptime(
                        '{0}-{1}-1'.format(date_ini.year, date_ini.month),
                        FORMAT_STR_DATE_REPORTS
                    ).date()

                set_apply_ajust = False
            date_ini = date_ini + relativedelta(**kwargs)

    def process_agrupado_cadena(self, ventas):
        data = {}

        if self.request.POST.get('agencia'):
            pertenece = Comercializadora.objects.get(
                agencia_id=self.request.POST.get('agencia')).get_object()
        elif self.request.POST.get('distribuidor'):
            pertenece = Comercializadora.objects.get(
                distribuidor_id=self.request.POST.get('distribuidor')).get_object()
        elif self.request.POST.get('banca'):
            pertenece = Comercializadora.objects.get(
                banca_id=self.request.POST.get('banca')).get_object()
        elif self.request.POST.get('bloque'):
            pertenece = Comercializadora.objects.get(
                bloque_id=self.request.POST.get('bloque')).get_object()
        elif self.request.POST.get('operadora'):
            pertenece = Comercializadora.objects.get(
                operadora_id=self.request.POST.get('operadora')).get_object()
        else:
            pertenece = self._object

        ventas = ventas.filter(
            **pertenece.get_kwargs_hijos_dimension_arco_comercializadora()
        )

        items = pertenece.get_offspring_ventas(ventas)

        data['verbose_name_hijos'] = ''
        if items:
            data['verbose_name_hijos'] = items[
                0].get_object().get_verbose_name_plural()

        options_form = self.option.split(' ')
        options_form = {
            'dinero': options_form[0],
            'cantidad': options_form[1],
        }
        totales = ventas.aggregate(
            Sum(options_form['dinero']),
            Sum(options_form['cantidad']),
        )
        dinero = totales[options_form['dinero'] + '__sum']
        cantidad = totales[options_form['cantidad'] + '__sum']
        if cantidad:
            data['avg'] = float(round(
                dinero / cantidad,
                2
            ))
        else:
            data['avg'] = float(0)

        indice_label = 0
        indice_cadena = 1
        data_google = []
        # =====================================================================
        # Armando esqueleto]

        for i in range(0, len(self.intervalos) + 1):
            data_generic = []
            # Columnas
            for j in range(0, len(items) + 1):
                data_generic.append(0)
            data_google.append(data_generic)
        # =====================================================================

        # Aqui es cero xq es el primer titulo
        data_google[indice_label][0] = self.prefix_label

        data['enlaces'] = []
        # este se deja vacio ya que representa la columna de tiempo
        data['enlaces'].append('')

        for item in items:
            item = item.get_object()
            if item.prefix_filter != 'taquilla':
                texto_cod = 'cadena,{0},{1}'.format(
                    item.pk,
                    item.prefix_filter
                )
                texto_title = '{0}'.format(item.nombre)

            else:
                texto_title = item.taquilla
                texto_cod = ''
            data_google[indice_label][indice_cadena] = texto_title
            data['enlaces'].append(texto_cod)

            venta_detalle = ventas.filter(
                ** item.get_kwargs_dimension_arco_comercializadora()
            )
            indice_data = 1
            for item_date in self.intervalos:

                totales = venta_detalle.filter(
                    tiempo__fecha__range=(item_date[0], item_date[1])
                ).aggregate(
                    Sum(options_form['dinero']),
                    Sum(options_form['cantidad']),
                )
                dinero = totales[options_form['dinero'] + '__sum']
                cantidad = totales[options_form['cantidad'] + '__sum']
                if cantidad:
                    total_avg = float(round(
                        dinero / cantidad,
                        2
                    ))
                else:
                    total_avg = float(0)

                if indice_cadena == 1:
                    # Solo se inserta una vez el numero de tiempo
                    if self.prefix_date != 'month':
                        data_google[indice_data][indice_cadena - 1] = '{0}'.format(getattr(
                            item_date[0],
                            self.prefix_date
                        ))
                    else:
                        data_google[indice_data][indice_cadena - 1] = defaultfilters.date(
                            item_date[0], 'b'
                        ).capitalize()

                data_google[indice_data][indice_cadena] = total_avg
                indice_data += 1
            indice_cadena += 1
        data['google'] = data_google
        return data

    def agrupado_deporte(self, ventas):
        data = {}

        modalidad = self.request.POST.get('modalidad')
        grupo_modalidad = self.request.POST.get('grupo_modalidad')
        encuentro = self.request.POST.get('encuentro')
        temporada = self.request.POST.get('temporada')
        deporte = self.request.POST.get('deporte')

        self.context['modalidad'] = self.request.POST.get('modalidad')
        self.context['grupo_modalidad'] = self.request.POST.get(
            'grupo_modalidad')
        self.context['encuentro'] = self.request.POST.get('encuentro')
        self.context['temporada'] = self.request.POST.get('temporada')
        self.context['deporte'] = self.request.POST.get('deporte')

        pertenece = self._object
        ventas = ventas.filter(
            **pertenece.get_kwargs_hijos_dimension_arco_comercializadora()
        )

        if encuentro:
            ventas = ventas.filter(juegos__encuentro_id=encuentro)
        elif temporada:
            ventas = ventas.filter(juegos__temporada_id=temporada)
        elif deporte:
            ventas = ventas.filter(juegos__deporte_id=deporte)

        if modalidad:
            encuentros_modalidades = list(EncuentrosModalidades.objects.filter(
                encuentro_id=encuentro,
                modalidad_grupo__grupo_id=grupo_modalidad,
                modalidad_grupo__modalidad_id=modalidad
            ).distinct().values_list('pk', flat=True))

            ventas = ventas.filter(
                juegos__encuentros_modalidad_id__in=encuentros_modalidades,
            )

            filtro_juego = Jugadas.objects.filter(
                encuentros_modalidad__encuentro_id=encuentro,
                encuentros_modalidad__modalidad_grupo__grupo_id=grupo_modalidad,
                condicion__modalidad_id=modalidad,
                origen__isnull=True
            )

            tipo = 6
            data['verbose_name_hijos'] = 'Condiciones'

        elif grupo_modalidad:

            grupo_modalidad = GruposApuestas.objects.get(pk=grupo_modalidad)

            encuentro_modalidad_all = EncuentrosModalidades.objects.filter(
                encuentro_id=encuentro,
                modalidad_grupo__grupo=grupo_modalidad
            ).distinct('pk')

            ventas = ventas.filter(
                juegos__encuentros_modalidad_id__in=list(encuentro_modalidad_all.values_list(
                    'pk', flat=True
                ))
            )

            filtro_juego = Modalidades.objects.filter(
                pk__in=list(
                    encuentro_modalidad_all.values_list(
                        'modalidad_grupo__modalidad_id',
                        flat=True))
            )

            tipo = 5
            data['verbose_name_hijos'] = 'Modalidades'

        elif encuentro:
            encuentro = Encuentros.objects.get(pk=encuentro)

            filtro_juego = encuentro.encuentrosmodalidades_set.all().distinct(
                'modalidad_grupo__grupo_id'
            )

            tipo = 4
            data['verbose_name_hijos'] = 'Grupos'

        elif temporada:
            temporada = Temporadas.objects.get(pk=temporada)

            ini = self.request.POST.get('fecha_inicio') + hora_cero
            fin = self.request.POST.get('fecha_fin') + hora_23

            kwargs_1 = {}
            kwargs_2 = {}
            if pertenece.prefix_filter != 'master':
                kwargs_1['jornada__sistema'] = self.object_sistema_juego
                kwargs_2['jornada__sistema'] = self.object_sistema_juego

            kwargs_1['pk__in'] = list(ventas.filter(
                juegos__temporada_id=temporada.pk
            ).values_list(
                'juegos__encuentro_id', flat=True
            ).distinct('juegos__encuentro_id'))

            kwargs_2['jornada__temporadas'] = temporada
            kwargs_2['horajuego__range'] = (ini, fin)

            filtro_juego = Encuentros.objects.filter(
                **kwargs_1
            ).filter(**kwargs_2)

            tipo = 3
            data['verbose_name_hijos'] = 'Encuentros'

        elif deporte:
            deporte = Deportes.objects.get(pk=deporte)

            kwargs = {}
            if pertenece.prefix_filter != 'master':
                kwargs['jornadas__sistema'] = self.object_sistema_juego
            kwargs['pk__in'] = list(ventas.filter(
                juegos__deporte_id=deporte.pk
            ).values_list(
                'juegos__temporada_id', flat=True
            ).distinct('juegos__temporada_id'))

            filtro_juego = Temporadas.objects.filter(
                **kwargs
            ).distinct('pk')

            tipo = 2

            data['verbose_name_hijos'] = 'Ligas'
        else:
            filtro_juego = Deportes.objects.filter(
                pk__in=list(ventas.values_list(
                            'juegos__deporte_id',
                            flat=True
                            ).distinct('juegos__deporte_id'))
            )
            tipo = 1
            data['verbose_name_hijos'] = 'Deportes'

        if not filtro_juego.count():
            return None

        options_form = self.option.split(' ')
        options_form = {
            'dinero': options_form[0],
            'cantidad': options_form[1],
        }

        totales = ventas.aggregate(
            Sum(options_form['dinero']),
            Sum(options_form['cantidad']),
        )
        dinero = totales[options_form['dinero'] + '__sum']
        cantidad = totales[options_form['cantidad'] + '__sum']
        if cantidad:
            data['avg'] = float(round(
                dinero / cantidad,
                2
            ))
        else:
            data['avg'] = float(0)

        indice_label = 0
        indice_cadena = 1
        data_google = []
        # =====================================================================
        # Armando esqueleto]

        for i in range(0, len(self.intervalos) + 1):
            data_generic = []
            # Columnas
            for j in range(0, filtro_juego.count() + 1):
                data_generic.append(0)
            data_google.append(data_generic)
        # =====================================================================

        # Aqui es cero xq es el primer titulo
        data_google[indice_label][0] = self.prefix_label

        data['enlaces'] = []
        # este se deja vacio ya que representa la columna de tiempo
        data['enlaces'].append('')

        for item in filtro_juego:

            if tipo == 1:
                # por deporte
                venta_detalle = ventas.filter(
                    juegos__deporte_id=item.pk
                )

                texto_cod = 'juegos,{0},{1}'.format(
                    tipo,
                    item.pk
                )
                texto_title = item.nombre

            elif tipo == 2:
                # por temporada
                venta_detalle = ventas.filter(juegos__temporada_id=item.pk)

                texto_cod = 'juegos,{0},{1}'.format(
                    tipo,
                    item.pk
                )
                texto_title = item.torneo.nombre + ' - ' + item.nombre

            elif tipo == 3:
                # por encuentros
                venta_detalle = ventas.filter(juegos__encuentro_id=item.pk)

                campo = ''
                d_e = item.encuentrosdetail_set.all()
                equipo_len = d_e.count()
                i = 0
                for obj in d_e:
                    campo += obj.equipos_temporadas.equipo.nombre
                    i += 1
                    if (equipo_len > i):
                        campo += ' Vs. '

                texto_cod = 'juegos,{0},{1}'.format(
                    tipo,
                    item.pk
                )
                objFecha = strFecha(item.horajuego)
                texto_title = campo + ' - ' + objFecha.getFecha() + ' - ' + objFecha.getHora()

            elif tipo == 4:
                # por grupos

                encuentro_modalidad_all = EncuentrosModalidades.objects.filter(
                    encuentro=item.encuentro,
                    modalidad_grupo__grupo=item.modalidad_grupo.grupo
                ).distinct()

                venta_detalle = ventas.filter(
                    juegos__encuentros_modalidad_id__in=list(encuentro_modalidad_all.values_list(
                        'pk', flat=True
                    ))
                )

                texto_cod = 'juegos,{0},{1}'.format(
                    tipo,
                    item.modalidad_grupo.grupo_id
                )
                texto_title = item.modalidad_grupo.grupo.nombre

            elif tipo == 5:
                # por modalidades
                venta_detalle = ventas.filter(
                    juegos__modalidad_id=item.pk
                )

                texto_cod = 'juegos,{0},{1}'.format(
                    tipo,
                    item.pk
                )
                texto_title = item.modalidad

            elif tipo == 6:
                # por condiciones
                texto_title = getattr(item, 'get_pertenece')()
                venta_detalle = ventas.filter(
                    juegos__pertenece=texto_title,
                    juegos__condicion_id=item.condicion.pk,
                    juegos__modalidad_id=item.condicion.modalidad.pk,
                )

                texto_cod = ''

            data_google[indice_label][indice_cadena] = texto_title
            data['enlaces'].append(texto_cod)

            indice_data = 1
            for item_date in self.intervalos:

                totales = venta_detalle.filter(
                    tiempo__fecha__range=(item_date[0], item_date[1])
                ).aggregate(
                    Sum(options_form['dinero']),
                    Sum(options_form['cantidad']),
                )
                dinero = totales[options_form['dinero'] + '__sum']
                cantidad = totales[options_form['cantidad'] + '__sum']
                if cantidad:
                    total_avg = float(round(
                        dinero / cantidad,
                        2
                    ))
                else:
                    total_avg = float(0)

                if indice_cadena == 1:
                    # Solo se inserta una vez el numero de tiempo
                    if self.prefix_date != 'month':
                        data_google[indice_data][indice_cadena - 1] = '{0}'.format(getattr(
                            item_date[0],
                            self.prefix_date
                        ))
                    else:
                        data_google[indice_data][indice_cadena - 1] = defaultfilters.date(
                            item_date[0], 'b'
                        ).capitalize()

                data_google[indice_data][indice_cadena] = total_avg
                indice_data += 1
            indice_cadena += 1
        data['google'] = data_google

        return data
