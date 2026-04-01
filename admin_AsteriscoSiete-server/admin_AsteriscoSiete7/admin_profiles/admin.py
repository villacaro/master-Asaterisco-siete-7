from admin_profiles.models import Direcciones, Estados, Municipios, Paises, Parroquias
from django.contrib import admin


@admin.register(Paises)
class PaisesAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created_at', 'updated_at')
    search_fields = ('nombre',)


@admin.register(Estados)
class EstadosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'pais', 'created_at', 'updated_at')
    list_filter = ('pais',)
    list_editable = ('pais',)
    search_fields = ('nombre', 'pais')


@admin.register(Municipios)
class MunicipiosAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'estado', 'created_at', 'updated_at')
    list_filter = ('estado',)
    list_editable = ('estado', )
    search_fields = ('nombre', 'estado__nombre',)
    raw_id_fields = ('estado',)


@admin.register(Parroquias)
class ParroquiasAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'municipio', 'created_at', 'updated_at')
    list_filter = ('municipio',)
    list_editable = ('municipio',)
    search_fields = ('nombre', 'municipio__nombre')
    raw_id_fields = ('municipio',)


@admin.register(Direcciones)
class DireccionesAdmin(admin.ModelAdmin):
    list_display = ('id', 'direccion', '__str_relate__', 'created_at', 'updated_at')
    list_display_links = ('id',)
    list_filter = ('estado', 'municipio', 'parroquia',)
    list_editable = ('direccion', )
    search_fields = ('direccion',)
