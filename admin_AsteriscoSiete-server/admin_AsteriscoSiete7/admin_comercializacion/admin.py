# -*- coding: utf-8 -*-
"""
admin.py — admin_comercializacion
==================================
Jerarquía de comercialización del Sistema Asterisco Siete (*7):

  Súper usuario (Django Auth)
       └── Operadoras
             └── Bloques
                   └── Bancas
                         └── Distribuidores
                               └── Agencias
                                     └── Taquillas
                                           └── UsuariosTaquilla
"""
from django.contrib import admin
from django.utils.html import format_html, mark_safe

from admin_comercializacion.models import (
    Agencias,
    Bancas,
    Bloques,
    Cupos,
    DataDefault,
    DefaultPreferences,
    Distribuidores,
    FactorRiesgo,
    GroupPreferences,
    Operadoras,
    Porcentajes,
    TaquillaDataDefault,
    Taquillas,
    TicketsDataDefault,
    TipoPorcentajes,
    TypePreferences,
    UsuariosTaquilla,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helper
# ─────────────────────────────────────────────────────────────────────────────

def status_badge(obj):
    s = getattr(obj, 'status', None)
    if s is None:
        return '—'
    nombre = str(s)
    color = 'green' if 'activ' in nombre.lower() else '#c00'
    return format_html('<b style="color:{};">{}</b>', color, nombre)


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 1: Operadoras  (raíz de la jerarquía)
# ─────────────────────────────────────────────────────────────────────────────

class BloquesEnOperadoraInline(admin.TabularInline):
    model = Bloques
    extra = 0
    fields = ('nombre', 'telefono', 'rif', 'is_sistema_juego')
    show_change_link = True




@admin.register(Operadoras)
class OperadorasAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'rif', 'telefono', 'email', 'bloques_count',
                     'tema_asignado', 'created_at')
    search_fields = ('nombre', 'rif', 'email')
    ordering      = ('nombre',)
    inlines       = [BloquesEnOperadoraInline]

    def bloques_count(self, obj):
        c = obj.bloques_set.count()
        return format_html('<b>{}</b>', c)
    bloques_count.short_description = '# Bloques'

    def tema_asignado(self, obj):
        """Muestra el tema (plantilla) asignado al SistemaJuego de esta operadora."""
        try:
            from admin_finanzas.models import Comercializadora
            comer = Comercializadora.objects.filter(operadora=obj).first()
            if comer:
                sistemas = comer.sistemas_juego_principal.select_related('theme').all()
                if sistemas.exists():
                    sj = sistemas.first()
                    if sj.theme:
                        url = f'/admin/admin_juego/sistemajuego/{sj.pk}/change/'
                        return format_html(
                            '<a href="{}" style="color:#2563eb;font-weight:bold;">🎨 {}</a>',
                            url, sj.theme.name
                        )
                    return format_html('<a href="/admin/admin_juego/sistemajuego/{}/change/">⚙️ Sin tema</a>', sj.pk)
        except Exception:
            pass
        return mark_safe('<span style="color:#aaa;">—</span>')
    tema_asignado.short_description = '🎨 Plantilla/Tema'


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 2: Bloques
# ─────────────────────────────────────────────────────────────────────────────

class BancasEnBloqueInline(admin.TabularInline):
    model = Bancas
    extra = 0
    fields = ('nombre', 'telefono', 'rif', 'is_sistema_juego')
    show_change_link = True


@admin.register(Bloques)
class BloquesAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'operadora', 'rif', 'telefono',
                     'is_sistema_juego', 'bancas_count', 'created_at')
    list_filter   = ('operadora', 'is_sistema_juego', 'is_resultados')
    search_fields = ('nombre', 'rif')
    ordering      = ('operadora', 'nombre')
    exclude       = ('is_logros',)
    inlines       = [BancasEnBloqueInline]

    def bancas_count(self, obj):
        c = obj.bancas_set.count()
        return format_html('<b>{}</b>', c)
    bancas_count.short_description = '# Bancas'


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 3: Bancas
# ─────────────────────────────────────────────────────────────────────────────

class DistribuidoresEnBancaInline(admin.TabularInline):
    model = Distribuidores
    extra = 0
    fields = ('nombre', 'telefono', 'rif')
    show_change_link = True


@admin.register(Bancas)
class BancasAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'bloque', 'rif', 'telefono',
                     'is_sistema_juego', 'distribuidores_count', 'created_at')
    list_filter   = ('is_sistema_juego',)
    search_fields = ('nombre', 'rif')
    ordering      = ('bloque', 'nombre')
    raw_id_fields = ('bloque',)
    exclude       = ('is_logros',)
    inlines       = [DistribuidoresEnBancaInline]

    def distribuidores_count(self, obj):
        c = obj.distribuidores_set.count()
        return format_html('<b>{}</b>', c)
    distribuidores_count.short_description = '# Distribuidores'


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 4: Distribuidores
# ─────────────────────────────────────────────────────────────────────────────

class AgenciasEnDistribuidorInline(admin.TabularInline):
    model = Agencias
    extra = 0
    fields = ('nombre', 'codigo', 'num_taquillas', 'telefono')
    show_change_link = True


@admin.register(Distribuidores)
class DistribuidoresAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'banca', 'rif', 'telefono',
                     'agencias_count', 'created_at')
    list_filter   = ()
    search_fields = ('nombre', 'rif')
    ordering      = ('banca', 'nombre')
    raw_id_fields = ('banca',)
    inlines       = [AgenciasEnDistribuidorInline]

    def agencias_count(self, obj):
        c = obj.agencias_set.count()
        return format_html('<b>{}</b>', c)
    agencias_count.short_description = '# Agencias'


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 5: Agencias
# ─────────────────────────────────────────────────────────────────────────────

class TaquillasEnAgenciaInline(admin.TabularInline):
    model = Taquillas
    extra = 0
    fields          = ('taquilla', 'serial', 'is_taquilla_master', 'modo_alquiler')
    readonly_fields = ('modo_alquiler',)   # editable=False en el modelo → solo lectura
    show_change_link = True


@admin.register(Agencias)
class AgenciasAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'distribuidores', 'codigo', 'num_taquillas',
                     'taquillas_count', 'montomin', 'montomax', 'created_at')
    list_filter   = ()
    search_fields = ('nombre', 'codigo', 'rif')
    raw_id_fields = ('distribuidores',)
    ordering      = ('distribuidores', 'nombre')
    inlines       = [TaquillasEnAgenciaInline]

    fieldsets = (
        ('Identificación', {
            'fields': ('nombre', 'codigo', 'rif', 'telefono', 'email',
                       'direccion', 'status'),
        }),
        ('Jerarquía', {
            'fields': ('distribuidores',),
        }),
        ('Reglas de Taquilla', {
            'fields': ('num_taquillas', 'montomin', 'montomax', 'montomax_ganancia',
                       'cantidad_apuesta_min', 'cantidad_apuesta_max',
                       'tiempoexpiracion'),
        }),
        ('Modelo Financiero', {
            'classes': ('collapse',),
            'fields': (
                       'factor_riesgo', 'frecuencia_queda',
                       'parley_clonados_maxima_ganancia'),
        }),
        ('Branding Ticket', {
            'classes': ('collapse',),
            'fields': ('ticket_titulo', 'ticket_pie'),
        }),
    )

    def taquillas_count(self, obj):
        c = obj.taquillas_set.count()
        return format_html('<b>{}</b>', c)
    taquillas_count.short_description = '# Taquillas'


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 6: Taquillas
# ─────────────────────────────────────────────────────────────────────────────

class UsuariosTaquillaInline(admin.TabularInline):
    model = UsuariosTaquilla
    extra = 0
    fields = ('user', 'nombre', 'is_taquilla_master_display')
    readonly_fields = ('is_taquilla_master_display',)
    show_change_link = True

    def is_taquilla_master_display(self, obj):
        return '⭐ Master' if obj.pk else ''
    is_taquilla_master_display.short_description = 'Tipo'


@admin.register(Taquillas)
class TaquillasAdmin(admin.ModelAdmin):
    list_display  = ('taquilla', 'serial', 'agencia', 'agencia_banca',
                     'is_taquilla_master', 'modo_alquiler', 'usuarios_count')
    list_filter   = ('is_taquilla_master', 'modo_alquiler')
    search_fields = ('taquilla', 'serial')
    raw_id_fields = ('agencia',)
    ordering      = ('agencia', 'taquilla')
    inlines       = [UsuariosTaquillaInline]

    def agencia_banca(self, obj):
        try:
            return obj.agencia.distribuidores.banca
        except Exception:
            return '—'
    agencia_banca.short_description = 'Banca'

    def usuarios_count(self, obj):
        c = obj.usuariostaquilla_set.count()
        return format_html('<b>{}</b>', c)
    usuarios_count.short_description = '# Usuarios'


# ─────────────────────────────────────────────────────────────────────────────
# NIVEL 7: UsuariosTaquilla
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(UsuariosTaquilla)
class UsuariosTaquillaAdmin(admin.ModelAdmin):
    list_display  = ('user', 'nombre', 'taquilla', 'agencia_ref',
                     'banca_ref', 'estado_usuario', 'created_at')
    list_filter   = ()
    search_fields = ('user', 'nombre')
    raw_id_fields = ('taquilla',)
    ordering      = ('taquilla', 'user')
    readonly_fields = ('last_login', 'created_at', 'updated_at',
                       'pub_key', 'priv_key', 'pub_key_client', 'keys_date')

    fieldsets = (
        ('Identificación', {
            'fields': ('user', 'nombre', 'password'),
        }),
        ('Ubicación en Jerarquía', {
            'fields': ('taquilla',),
        }),
        ('Estado y Acceso', {
            'fields': ('status', 'last_login', 'created_at', 'updated_at'),
        }),
        ('Claves de Seguridad', {
            'classes': ('collapse',),
            'fields': ('pub_key_client', 'pub_key', 'priv_key', 'keys_date'),
        }),
    )

    def agencia_ref(self, obj):
        try:
            return obj.taquilla.agencia
        except Exception:
            return '—'
    agencia_ref.short_description = 'Agencia'

    def banca_ref(self, obj):
        try:
            return obj.taquilla.agencia.distribuidores.banca
        except Exception:
            return '—'
    banca_ref.short_description = 'Banca'

    def estado_usuario(self, obj):
        s = str(obj.status) if obj.status else '?'
        color = 'green' if 'activ' in s.lower() else '#c00'
        return format_html('<b style="color:{};">{}</b>', color, s)
    estado_usuario.short_description = 'Estado'


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN BASE
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(TaquillaDataDefault)
class TaquillaDataDefaultAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'user_name', 'passwd')
    list_editable = ('user_name', 'passwd')
    search_fields = ['user_name']


@admin.register(TicketsDataDefault)
class TicketsDataDefaultAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3')
    list_editable = ('titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3')
    list_filter   = ('titulo1', 'pie1')
    search_fields = ['titulo1', 'titulo2', 'titulo3', 'pie1', 'pie2', 'pie3']


@admin.register(DataDefault)
class DataDefaultAdmin(admin.ModelAdmin):
    list_display  = (
        'pk', 'user_type', 'cupo', 'porcentaje_comision', 'porcentaje_regalia',
        'porcentaje_participacion', 'porcentaje_queda', 'porcentaje_maximo',
    )
    list_editable = (
        'cupo', 'porcentaje_comision', 'porcentaje_regalia',
        'porcentaje_participacion', 'porcentaje_queda', 'porcentaje_maximo',
    )
    list_filter   = ('user_type',)


@admin.register(TipoPorcentajes)
class TipoPorcentajesAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'nombre', 'codename', 'orden', 'bloque',
                     'banca', 'distribuidor', 'agencia', 'taquilla')
    list_editable = ('orden', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla')
    list_filter   = ('nombre', 'codename')
    search_fields = ['nombre', 'codename']


@admin.register(GroupPreferences)
class GroupPreferencesAdmin(admin.ModelAdmin):
    list_display  = ('name', 'order')
    list_editable = ('order',)
    search_fields = ('name', 'codename')


@admin.register(TypePreferences)
class TypePreferencesAdmin(admin.ModelAdmin):
    list_display    = ('name', 'order', 'comparison', 'type_data', 'edit',
                       'distribute', 'group', 'get_profiles')
    filter_horizontal = ('profile',)
    list_editable   = ('order',)
    search_fields   = ('name', 'codename')
    list_filter     = ('group', 'type_data', 'edit', 'distribute', 'comparison')


@admin.register(DefaultPreferences)
class DefaultPreferencesAdmin(admin.ModelAdmin):
    list_display  = ('typepreference', 'value', 'default')
    list_editable = ('value', 'default')
    search_fields = ('typepreference__name', 'typepreference__codename')


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN COMERCIAL — FactorRiesgo, Cupos, Porcentajes
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(FactorRiesgo)
class FactorRiesgoAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'comercializadora', 'created_at', 'updated_at')
    list_filter   = ('comercializadora',)
    search_fields = ('comercializadora__operadora__nombre',)
    raw_id_fields = ('comercializadora',)
    ordering      = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Cupos)
class CuposAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'monto_diario', 'monto_premio', 'fecha_inicio', 'fecha_fin')
    ordering      = ('-fecha_inicio',)
    readonly_fields = ('fecha_inicio', 'created_at', 'updated_at')

    fieldsets = (
        ('Montos', {
            'fields': ('monto_diario', 'monto_premio', 'fecha_fin'),
        }),
        ('Jerarquía (seleccione SOLO uno)', {
            'fields': ('operadora', 'bloque', 'banca', 'distribuidor', 'agencia'),
        }),
        ('Registro', {
            'classes': ('collapse',),
            'fields': ('fecha_inicio', 'created_at', 'updated_at'),
        }),
    )


@admin.register(Porcentajes)
class PorcentajesAdmin(admin.ModelAdmin):
    list_display  = ('pk', 'tipo', 'porcentaje_ganancia', 'porcentaje_maximo', 'fecha_inicio', 'fecha_fin')
    list_filter   = ('tipo', 'relacion')
    ordering      = ('-fecha_inicio',)
    readonly_fields = ('fecha_inicio', 'created_at', 'updated_at')

    fieldsets = (
        ('Tipo y Vigencia', {
            'fields': ('tipo', 'relacion', 'fecha_fin'),
        }),
        ('Porcentajes', {
            'fields': ('porcentaje_ganancia', 'porcentaje_maximo',
                       'bloque_porc', 'banca_porc', 'distribuidor_porc',
                       'agencia_porc', 'taquilla_porc'),
        }),
        ('Jerarquía (seleccione SOLO uno)', {
            'fields': ('operadora', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla'),
        }),
        ('Registro', {
            'classes': ('collapse',),
            'fields': ('fecha_inicio', 'created_at', 'updated_at'),
        }),
    )


# ─────────────────────────────────────────────────────────────────────────────
# ORDENAMIENTO JERÁRQUICO EN EL SIDEBAR DEL ADMIN
# Django ordena modelos por verbose_name_plural alfabéticamente.
# Prefijos numéricos fuerzan el orden correcto de la jerarquía.
# ─────────────────────────────────────────────────────────────────────────────
Operadoras._meta.verbose_name        = 'Operadora'
Operadoras._meta.verbose_name_plural = '1 ─ Operadoras'

Bloques._meta.verbose_name           = 'Multi Banca'
Bloques._meta.verbose_name_plural    = '2 ─ Multi Bancas'

Bancas._meta.verbose_name            = 'Banca'
Bancas._meta.verbose_name_plural     = '3 ─ Bancas'

Distribuidores._meta.verbose_name        = 'Distribuidor'
Distribuidores._meta.verbose_name_plural = '4 ─ Distribuidores'

Agencias._meta.verbose_name          = 'Centro de apuesta'
Agencias._meta.verbose_name_plural   = '5 ─ Centros de apuesta'

Taquillas._meta.verbose_name         = 'Taquilla'
Taquillas._meta.verbose_name_plural  = '6 ─ Taquillas'

UsuariosTaquilla._meta.verbose_name         = 'Usuario de taquilla'
UsuariosTaquilla._meta.verbose_name_plural  = '7 ─ Usuarios de taquillas'
