from admin_comercializacion.models import (
    DataDefault, DefaultPreferences, GroupPreferences, TaquillaDataDefault, TicketsDataDefault, TipoPorcentajes,
    TypePreferences,
)
from django.contrib import admin


@admin.register(TaquillaDataDefault)
class TaquillaDataDefaultAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user_name', 'passwd', )
    list_editable = ('user_name', 'passwd', )
    search_fields = ['user_name', ]


@admin.register(TicketsDataDefault)
class TicketsDataDefaultAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'titulo1',
        'titulo2',
        'titulo3',
        'pie1',
        'pie2',
        'pie3',
    )
    list_editable = ('titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3',)
    list_filter = ('titulo1', 'pie1')
    search_fields = ['titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3', ]


@admin.register(DataDefault)
class DataDefaultAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'user_type', 'cupo', 'porcentaje_comision', 'porcentaje_regalia',
        'porcentaje_participacion', 'porcentaje_queda', 'porcentaje_maximo',
        'monto_alquiler',
    )

    list_editable = (
        'cupo', 'porcentaje_comision', 'porcentaje_regalia',
        'porcentaje_participacion', 'porcentaje_queda', 'porcentaje_maximo',
        'monto_alquiler',
    )

    list_filter = ('user_type',)

    search_fields = [
        'cupo', 'porcentaje_comision', 'porcentaje_regalia',
        'porcentaje_participacion', 'porcentaje_queda', 'porcentaje_maximo',
        'monto_alquiler',
    ]


@admin.register(TipoPorcentajes)
class TipoPorcentajesAdmin(admin.ModelAdmin):
    list_display = (
        'pk', 'nombre', 'codename', 'orden', 'bloque',
                        'banca', 'distribuidor', 'agencia',
                        'taquilla'
    )
    list_editable = (
        'orden', 'bloque',
        'banca', 'distribuidor', 'agencia',
        'taquilla'
    )
    list_filter = ('nombre', 'codename')
    search_fields = ['nombre', 'codename']


@admin.register(GroupPreferences)
class GroupPreferencesAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order', )
    search_fields = ('name', 'codename')


@admin.register(TypePreferences)
class TypePreferencesAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'comparison', 'type_data', 'edit', 'distribute', 'group', 'get_profiles')
    filter_horizontal = ('profile', )
    list_editable = ('order', )
    search_fields = ('name', 'codename',)
    list_filter = ('group', 'type_data', 'edit', 'distribute', 'comparison')


@admin.register(DefaultPreferences)
class DefaultPreferencesAdmin(admin.ModelAdmin):
    list_display = ('typepreference', 'value', 'default')
    list_editable = ('value', 'default', )
    search_fields = ('typepreference__name', 'typepreference__codename')
