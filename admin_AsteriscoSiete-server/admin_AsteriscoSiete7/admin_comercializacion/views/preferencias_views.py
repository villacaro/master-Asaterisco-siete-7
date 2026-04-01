# -*- coding: utf-8 -*-
from decimal import Decimal

from admin_comercializacion.forms import PreferencesForm
from admin_comercializacion.models import (
    EventNotificationCadena, GroupPreferences, Porcentajes, Preferences, TypePreferences, types_notification_cadena,
)
from admin_comercializacion.task import AsyncProcessInvokeMethod
from admin_comercializacion.views.agencias_views import AgenciasListView
from admin_comercializacion.views.bancas_views import BancasListView
from admin_comercializacion.views.bloques_views import BloquesListView
from admin_comercializacion.views.distribuidores_views import DistribuidoresListView
from admin_finanzas.models import Comercializadora
from admin_lib.util_datatable.util_datatable_view import BaseDatatableView
from admin_lib.util_fechas import Funs as funs_dates
from admin_lib.util_icons import Icons
from admin_lib.util_views import MyViewBase
from django.core.cache import cache
from django.urls import reverse
from django.views.generic.edit import FormView


class PreferenciasView(MyViewBase):
    template_name = "admin_comercializacion/preferencias/preferencias_list.html"
    """
        ADVERTENCIA: si se cambia el nombre del modelo, hay que cambiarlos en
        la verificacion del datatable de preferencias
        Esta variable de envia para verificar sobre cual link se esta ubicado
    """


class BloquesPreferenciasListView(PreferenciasView, BloquesListView):

    def get_context_data(self, **kwargs):
        context = super(BloquesPreferenciasListView,
                        self).get_context_data(**kwargs)
        context["cadena"] = "Bloques"
        context["model"] = "Bloques"
        return context


class BancasPreferenciasListView(PreferenciasView, BancasListView):

    def get_context_data(self, **kwargs):
        context = super(BancasPreferenciasListView,
                        self).get_context_data(**kwargs)
        context["cadena"] = "Bancas"
        context["model"] = "Bancas"
        return context


class DistribuidoresPreferenciasListView(PreferenciasView, DistribuidoresListView):

    def get_context_data(self, **kwargs):
        context = super(DistribuidoresPreferenciasListView,
                        self).get_context_data(**kwargs)
        context["cadena"] = "Distribuidores"
        context["model"] = "Distribuidores"
        return context


class AgenciasPreferenciasListView(PreferenciasView, AgenciasListView):

    def get_context_data(self, **kwargs):
        context = super(AgenciasPreferenciasListView,
                        self).get_context_data(**kwargs)
        context["cadena"] = "Centros de apuestas"
        context["model"] = "Agencias"
        return context


class PreferencesView(MyViewBase):
    model = Preferences

    def get_object(self):
        try:
            model = self.get_model()

            return model.objects.get(
                pk=self.kwargs.get("pk")
            )
        except Exception:
            from django.http import Http404
            raise Http404

    def get_model(self):
        try:
            from django.db.models import get_app
            return getattr(
                get_app("admin_comercializacion"),
                self.kwargs.get("type").capitalize()
            )
        except Exception:
            from django.http import Http404
            raise Http404

    def get_success_url_force(self):
        return reverse(
            "admin_comercializacion_{0}_preferencias_list".format(
                self.object.get_class_name()
            )
        )

    def get_success_url_filter_form(self):
        """
        Devuelve los filtros equivalentes
        """
        return "?{0}={1}".format(
            self.object.prefix_filter,
            self.object.pk
        )


class PreferencesFormView(PreferencesView, FormView):
    form_class = PreferencesForm
    template_name = "admin_comercializacion/preferencias/preferencias_form.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        content = super(PreferencesFormView, self).get_context_data(**kwargs)
        forms = []
        kwargs_group = self.get_form_kwargs()

        groups = GroupPreferences.objects.all().order_by(
            'order').only('id', 'name', 'codename')

        for group in groups:
            kwargs_group['group'] = group
            form = PreferencesForm(**kwargs_group)
            form.name = group.name
            if len(form.fields) != 0:
                forms.append(form)

        content['object'] = self.get_object()
        content['forms'] = forms
        content['object'].distribute = form.distribute
        content['object'].heredity = form.heredity

        return content

    def form_valid(self, form):
        self.object = self.get_object()
        comercializadora = self.object.get_comercializadora()

        array_codename = []
        array_distribute = []
        array_heredity = []

        for key in form.data:
            # Buscamos la data que tenga que ver con los campos de lleno
            if '.' not in key and 'distribute' not in key and 'heredity' not in key \
                    and 'preference' in key:
                array_codename.append(key)
            if 'distribute' in key \
                    and self.object.user_type_codename == 'userprofile_distribuidor':
                args = key.split('-')
                array_distribute.append(args[1])
            if 'heredity' in key:
                args = key.split('-')
                array_heredity.append(args[1])

        dict_preferencias = {}
        array_typepreference_codename = []
        array_typepreference_codename_no_heredity = []
        for key in array_codename:
            distribute = False

            typepreference = TypePreferences.objects.get(
                codename=key
            )
            # Transformacion del tipo de dato al guardarlo
            if typepreference.comparison != TypePreferences.comparison_codenames['codename_free']:
                if typepreference.type_data == TypePreferences.comparison_type['codename_decimal']:
                    value = self.get_decode_valor(form.data.get(key))
                elif typepreference.type_data == TypePreferences.comparison_type['codename_int']:
                    value = int(Decimal(form.data.get(key)))
                else:
                    value = form.data.get(key)
            else:
                value = form.data.get(key)

            if key in array_distribute:
                distribute = True

            old_value = comercializadora.create_or_update_preference(
                typepreference,
                value,
                distribute
            )

            cache.delete('preference_{0}_{1}'.format(
                comercializadora.id,
                typepreference.codename))
            cache.delete('preference_value_{0}_{1}'.format(
                comercializadora.id,
                typepreference.codename))

            if distribute:
                childs = comercializadora.get_offspring().only('id')
                try:
                    rate = round(value / len(childs), 2)
                except Exception:
                    rate = round(value, 2)
                dict_preferencias[TypePreferences.OLD_PREFERENCES[key]] = rate
                for child in childs:
                    child.create_or_update_preference(
                        typepreference,
                        rate,
                        distribute
                    )
                    cache.delete('preference_{0}_{1}'.format(
                        child.id,
                        typepreference.codename)
                    )
                    cache.delete('preference_value_{0}_{1}'.format(
                        child.id,
                        typepreference.codename)
                    )
            else:
                try:
                    dict_preferencias[
                        TypePreferences.OLD_PREFERENCES[key]] = value
                except Exception:
                    dict_preferencias[key] = value
                if typepreference.heredity and key not in array_heredity:
                    array_typepreference_codename_no_heredity.append(
                        {
                            'codename': typepreference.codename,
                            'old_value': old_value

                        })
                else:
                    array_typepreference_codename.append(
                        typepreference.codename)

        # Fragmento de codigo, envia la notificacion de cadena de comercializacion
        ########################################################################
        if dict_preferencias:
            kwargs_notificacion = {
                "data_origin": types_notification_cadena["preferencia"][0],
                "data": dict_preferencias,
            }

            kwargs_notificacion[
                self.object.prefix_filter
            ] = self.object.pk

            EventNotificationCadena.objects.create(
                **kwargs_notificacion
            )
        ########################################################################

        # Preferencias hereditarias
        kwargs_async = {
            'session_id': '{0}'.format(self.object_session.pk),
            'parametros': {
                'comercializadora': comercializadora.id,
                'typepreferences': array_typepreference_codename,
            },
        }

        AsyncProcessInvokeMethod.func_delay(
            PreferencesFormView.delete_preferences,
            kwargs_async
        )
        ######

        # Preferencias no hereditarias
        if array_typepreference_codename_no_heredity:
            kwargs_async = {
                'session_id': '{0}'.format(self.object_session.pk),
                'parametros': {
                    'comercializadora': comercializadora.id,
                    'typepreferences': array_typepreference_codename_no_heredity,
                },
            }
            AsyncProcessInvokeMethod.func_delay(
                PreferencesFormView.preferences_no_heredity,
                kwargs_async,
            )

        ######

        return super(PreferencesFormView, self).form_valid(form)

    @staticmethod
    def delete_preferences(kwargs):
        comercializadora = Comercializadora.objects.only('id').get(
            pk=kwargs.get('comercializadora')
        )
        cont = 0

        if kwargs.get('typepreferences'):
            childs = comercializadora.get_offspring().values_list('id', flat=True)
            frecuencia_queda_origen = Preferences.objects.get(
                comercializacion_id=comercializadora.pk,
                typepreference__codename='preference_queda_frequency'
            )

            for child in childs:
                preferences_comer = Preferences.objects.only('id').filter(
                    comercializacion_id=child,
                    typepreference__codename__in=kwargs.get('typepreferences')
                )
                for preference_comer in preferences_comer.exclude(
                        typepreference__codename='preference_queda_frequency'):
                    cont += 1
                    preference_comer.delete()

                for preference_comer in preferences_comer.only('id', 'value').filter(
                        typepreference__codename='preference_queda_frequency'):
                    delete_disable = False
                    if preference_comer.value == 'frecuencia_semanal':
                        delete_disable = funs_dates.is_first_week_of_month()
                    elif preference_comer.value == 'frecuencia_quincenal':
                        if frecuencia_queda_origen.value == 'frecuencia_semanal':
                            delete_disable = funs_dates.is_first_week_of_fortnight()
                        elif frecuencia_queda_origen.value == 'frecuencia_mensual':
                            delete_disable = funs_dates.is_first_fortnight_of_month()
                    elif preference_comer.value == 'frecuencia_mensual':
                        if frecuencia_queda_origen.value == 'frecuencia_semanal':
                            delete_disable = funs_dates.is_first_week_of_month()
                        elif frecuencia_queda_origen.value == 'frecuencia_quincenal':
                            delete_disable = funs_dates.is_first_fortnight_of_month()
                    if delete_disable:
                        # Si se esta en las fechas correctas si procede a eliminar, para tomar el valor del padre
                        cont += 1
                        preference_comer.delete()

                for codename in kwargs.get('typepreferences'):
                    key = 'preference_{0}_{1}'.format(child, codename)
                    cache.delete(key)
                    key = 'preference_value_{0}_{1}'.format(child, codename)
                    cache.delete(key)

        return ['{0} comercializadora(s) gestionada(s)'.format(cont)]

    @staticmethod
    def preferences_no_heredity(kwargs):
        comercializadora = Comercializadora.objects.only('id').get(
            pk=kwargs.get('comercializadora')
        )
        cont = 0

        for dicc in kwargs.get('typepreferences'):
            childs = comercializadora.get_offspring().values_list('id', flat=True)
            typepreference = TypePreferences.objects.get(
                codename=dicc['codename']
            )
            for child in childs:
                if not Preferences.objects.only('id').filter(
                    comercializacion_id=child,
                    typepreference__codename__in=typepreference.codename
                ).exists():
                    cont += 1
                    preference = Preferences(
                        comercializacion_id=child,
                        typepreference_id=typepreference.id,
                        value=dicc['old_value'],
                    )
                    preference.save()
        return ['{0} comercializadora(s) gestionada(s)'.format(cont)]

    def check_decimal(self, valor):
        try:
            return Decimal(valor.replace(",", "%").replace(".", "").replace("%", "."))
        except Exception:
            return valor

    def check_int(self, valor):
        try:
            return int(valor)
        except Exception:
            return valor

    def get_encode_valor(self, valor):
        try:
            return '{:,}'.format(
                round(Decimal(valor), 2)
            ).replace(".", "%").replace(",", ".").replace("%", ",")
        except Exception:
            return valor

    def get_decode_valor(self, valor):
        try:
            return Decimal(valor.replace(",", "%").replace(".", "").replace("%", "."))
        except Exception:
            return valor


class PreferenciasDatatableView(PreferenciasView, BaseDatatableView):
    # Orden del filtro
    order_columns = ['nombre']
    # Patron de busqueda
    filter_search = "nombre"

    opcions_url = ["admin_comercializacion_preferencias_update$" + Icons.update]

    def get_initial_queryset(self):
        qs = self.get_queryset()
        return qs

    def prepare_results(self, qs, acarreo):
        json_data = []
        for x, item in enumerate(qs):
            json_data.append([
                (x + 1 + acarreo),
                item.nombre,
                self.get_opcions(
                    pk=item.pk, tipo=self.request.GET.get('cadena').lower())
            ])
        return json_data


class BloquesPreferenciasDatatableView(PreferenciasDatatableView, BloquesListView):
    pass


class BancasPreferenciasDatatableView(PreferenciasDatatableView, BancasListView):
    pass


class DistribuidoresPreferenciasDatatableView(PreferenciasDatatableView, DistribuidoresListView):
    pass


class AgenciasPreferenciasDatatableView(PreferenciasDatatableView, AgenciasListView):
    pass


def validate_model_bussiness(objecto, preferences):
    '''
        Validacion del modelo de negocio
    '''
    queryset_val = objecto
    while True:
        if not queryset_val:
            preferences = preferences.exclude(
                codename__in=[
                    "preference_amount_rental",
                    "preference_amount_rental_frequency"
                ]
            )
            break
        if hasattr(queryset_val, "modelo_negocio"):
            if (queryset_val.modelo_negocio_codenames["codename_negocio_alquiler"] !=
                    queryset_val.modelo_negocio):
                preferences = preferences.exclude(
                    codename__in=[
                        "preference_amount_rental",
                        "preference_amount_rental_frequency"
                    ]
                )

            else:
                preferences = preferences.exclude(
                    codename__in=[
                        "preference_queda_frequency"
                    ]
                )
            break
        else:
            queryset_val = queryset_val.get_origen()

    kwargs_porcentaje = {
        "tipo__codename": "porcentaje_queda",
        "fecha_fin": None,
    }
    kwargs_porcentaje[objecto.prefix_filter] = objecto
    try:
        porcentaje = Porcentajes.objects.only('porcentaje_ganancia').get(
            **kwargs_porcentaje
        )
    except Porcentajes.DoesNotExist:
        porcentaje = None

    if porcentaje:
        if porcentaje.porcentaje_ganancia <= 0:
            preferences = preferences.exclude(
                codename__in=[
                    "preference_queda_frequency"
                ]
            )
    return preferences


class LoadPreferences:

    def __init__(self, agencia):
        self.montomin = float(agencia.get_preference_value_by_codename(
            'preference_amount_min'
        ))
        self.montomax = float(agencia.get_preference_value_by_codename(
            'preference_amount_max'
        ))
        self.montomax_ganancia = float(agencia.get_preference_value_by_codename(
            'preference_amount_price_max'
        ))
        self.parley_clonados_maxima_ganancia = float(agencia.get_preference_value_by_codename(
            'preference_amount_price_clone_max'
        ))
        self.cantidad_apuesta_min = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_min'
        )))
        self.cantidad_apuesta_max = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_max'
        )))
        self.tiempoexpiracion = int(float(agencia.get_preference_value_by_codename(
            'preference_time_expire_max'
        )))
        self.parley_machos_min = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_male_min'
        )))
        self.parley_machos_max = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_male_max'
        )))
        self.parley_hembras_min = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_female_min'
        )))
        self.parley_hembras_max = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_female_max'
        )))
        self.parley_empates_max = int(float(agencia.get_preference_value_by_codename(
            'preference_quantity_combinations_draw_max'
        )))
        self.cancel_ticket = int(agencia.get_preference_value_by_codename(
            'preference_cancel_ticket'
        ))
