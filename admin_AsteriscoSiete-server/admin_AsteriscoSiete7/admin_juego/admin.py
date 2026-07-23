# -*- coding: utf-8 -*-
"""
admin.py — Sistema Asterisco Siete (*7)
=======================================
Panel de Control Django Admin para la gestión completa del sistema de lotería.

Módulos registrados:
    ─ Configuración base:  SistemaJuego
    ─ Arquitectura multi-producto:
        Loteria, GrupoAnimales + AnimalFigura (inline),
        ProductoLoteria + SorteoArrejuntao (inline)
    ─ Plantillas Arrejuntao: PlantillaProducto + PlantillaJugada (inline)
    ─ Tickets y apuestas:   Ticket + ApuestaDetalle (inline), ResultadoSorteo
    ─ Liquidación:          LiquidacionSorteo
"""
from django.contrib import admin
from django.utils.html import format_html, mark_safe

from admin_juego.models import (
    SistemaJuego, TipoProducto, Fechas, RestriccionesSorteo,
    ModalidadJuego, ModalidadProducto, ModalidadPeriodo,
    OperadoraLoteria,
)
from admin_juego.models_arrejuntao import (
    # Modelos de Plantilla Arrejuntao
    AnimalFigura,
    Animalito,
    ApuestaDetalle,
    GrupoAnimales,
    LiquidacionSorteo,
    Loteria,
    PlantillaJugada,
    PlantillaProducto,
    ProductoLoteria,
    ResultadoSorteo,
    SorteoArrejuntao,
    Ticket,
)


# ─────────────────────────────────────────────────────────────────────────────
# Helpers de presentación
# ─────────────────────────────────────────────────────────────────────────────

def logo_preview(obj, campo='logo', size=40):
    """Muestra una miniatura del logo/imagen en el listado."""
    imagen = getattr(obj, campo, None)
    if imagen:
        return format_html(
            '<img src="{}" style="height:{px}px;border-radius:4px;" />',
            imagen.url, px=size
        )
    return '—'


# ─────────────────────────────────────────────────────────────────────────────
# TipoProducto  (Tipos de Producto de Lotería)
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(TipoProducto)
class TipoProductoAdmin(admin.ModelAdmin):
    list_display  = ('id', 'nombre', 'por_jornadas', 'por_grupos', 'created_at')
    list_filter   = ('por_jornadas', 'por_grupos')
    search_fields = ('nombre',)
    ordering      = ('nombre',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = [
        ('Identificación', {
            'fields': ('nombre', 'deporte'),
        }),
        ('Imágenes', {
            'fields': ('logo', 'fondoweb'),
            'classes': ('collapse',),
        }),
        ('Configuración', {
            'fields': ('por_jornadas', 'por_grupos', 'pk_clone'),
        }),
        ('Fechas (solo lectura)', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    ]


# ─────────────────────────────────────────────────────────────────────────────
# SistemaJuego (existente, mejorado)
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(SistemaJuego)
class SistemaJuegoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'logo_thumbnail', 'theme_display', 'comercializadora', 'notificacion_automatica', 'created_at')
    list_filter   = ('notificacion_automatica',)
    search_fields = ('nombre',)
    ordering      = ('nombre',)
    raw_id_fields = ('comercializadora', 'theme', 'company')
    fieldsets = [
        ('Información básica', {
            'fields': ('nombre', 'comercializadora', 'company')
        }),
        ('🎨 Plantilla / Tema', {
            'fields': ('theme',),
            'description': 'Seleccione el tema visual que usará este sistema de juego.',
        }),
        ('Imágenes', {
            'fields': ('logo', 'banner'),
            'classes': ('collapse',),
        }),
        ('Configuración', {
            'fields': ('notificacion_automatica',),
        }),
    ]

    def logo_thumbnail(self, obj):
        return logo_preview(obj, 'logo', 36)
    logo_thumbnail.short_description = 'Logo'

    def theme_display(self, obj):
        if obj.theme:
            return format_html(
                '<b style="color:#2563eb;">{}</b>',
                obj.theme.name
            )
        return mark_safe('<span style="color:#aaa;">— Sin tema —</span>')
    theme_display.short_description = '🎨 Tema'



# =============================================================================
# ARQUITECTURA MULTI-PRODUCTO
# =============================================================================

# ─────────────────────────────────────────────────────────────────────────────
# Loteria
# ─────────────────────────────────────────────────────────────────────────────

class ProductoLoteriaInline(admin.TabularInline):
    """Muestra los productos directamente en el formulario de la Lotería."""
    model  = ProductoLoteria
    extra  = 1
    fields = ('nombre_producto', 'tipo', 'digitos_requeridos', 'es_terminal',
              'requiere_signo', 'resultado_key', 'multiplicador_pago',
              'grupo_animales', 'activo', 'orden')
    show_change_link = True


@admin.register(Loteria)
class LoteriaAdmin(admin.ModelAdmin):
    list_display  = ('logo_thumbnail', 'nombre', 'activo', 'orden', 'sistema',
                     'productos_count', 'updated_at')
    list_filter   = ('activo',)
    search_fields = ('nombre',)
    ordering      = ('orden', 'nombre')
    inlines       = [ProductoLoteriaInline]
    list_editable = ('activo', 'orden')

    def logo_thumbnail(self, obj):
        return logo_preview(obj, 'logo', 36)
    logo_thumbnail.short_description = ''

    def productos_count(self, obj):
        n = obj.productos.filter(activo=True).count()
        return format_html('<b>{}</b> producto(s)', n)
    productos_count.short_description = 'Productos activos'


# ─────────────────────────────────────────────────────────────────────────────
# GrupoAnimales + AnimalFigura (inline)
# ─────────────────────────────────────────────────────────────────────────────

class AnimalFiguraInline(admin.TabularInline):
    model  = AnimalFigura
    extra  = 5
    fields = ('numero', 'nombre', 'imagen', 'activo')


@admin.register(GrupoAnimales)
class GrupoAnimalesAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'total_figuras', 'activo')
    list_filter   = ('activo',)
    search_fields = ('nombre',)
    inlines       = [AnimalFiguraInline]

    def total_figuras(self, obj):
        return obj.animales.filter(activo=True).count()
    total_figuras.short_description = 'Figuras activas'


# ─────────────────────────────────────────────────────────────────────────────
# ProductoLoteria + SorteoArrejuntao (inline)
# ─────────────────────────────────────────────────────────────────────────────

class SorteoInline(admin.TabularInline):
    model  = SorteoArrejuntao
    extra  = 2
    fields = ('descripcion', 'hora_sorteo', 'minutos_cierre', 'activo')


@admin.register(ProductoLoteria)
class ProductoLoteriaAdmin(admin.ModelAdmin):
    list_display  = ('nombre_producto', 'loteria', 'tipo', 'digitos_requeridos',
                     'requiere_signo', 'multiplicador_pago', 'activo', 'orden')
    list_filter   = ('tipo', 'activo', 'requiere_signo')
    search_fields = ('nombre_producto', 'loteria__nombre')
    ordering      = ('loteria', 'orden')
    list_editable = ('activo', 'orden', 'multiplicador_pago')
    raw_id_fields = ('loteria', 'grupo_animales')
    inlines       = [SorteoInline]

    fieldsets = (
        ('Identificación', {
            'fields': ('loteria', 'nombre_producto', 'tipo', 'activo', 'orden'),
        }),
        ('Reglas del juego — Numérico', {
            'classes': ('collapse',),
            'fields': ('digitos_requeridos', 'es_terminal', 'requiere_signo', 'resultado_key'),
        }),
        ('Reglas del juego — Animalitos', {
            'classes': ('collapse',),
            'fields': ('grupo_animales',),
        }),
        ('Configuración de pago', {
            'fields': ('multiplicador_pago', 'cupo_por_numero'),
        }),
    )


@admin.register(SorteoArrejuntao)
class SorteoAdmin(admin.ModelAdmin):
    list_display  = ('__str__', 'hora_sorteo', 'minutos_cierre', 'activo', 'estado_apertura')
    list_filter   = ('activo',)
    search_fields = ('descripcion', 'producto__loteria__nombre')
    ordering      = ('producto', 'hora_sorteo')
    list_editable = ('activo',)
    raw_id_fields = ('producto',)

    def estado_apertura(self, obj):
        if obj.activo and obj.esta_abierto():
            return mark_safe('<span style="color:green;font-weight:700;">✓ Abierto</span>')
        return mark_safe('<span style="color:red;">✗ Cerrado</span>')
    estado_apertura.short_description = 'Estado'


# =============================================================================
# PLANTILLAS ARREJUNTAO
# =============================================================================

class PlantillaJugadaInline(admin.TabularInline):
    model  = PlantillaJugada
    extra  = 0
    fields = ('tipo_jugada', 'activa', 'factor_pago', 'cupo_por_numero', 'monto_maximo_venta')


@admin.register(PlantillaProducto)
class PlantillaProductoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'activo', 'animalito_min', 'animalito_max',
                     'usa_doble_cara', 'usa_signo', 'orden', 'updated_at')
    list_filter   = ('activo', 'usa_doble_cara', 'usa_signo')
    search_fields = ('nombre',)
    ordering      = ('orden', 'nombre')
    list_editable = ('activo', 'orden')
    inlines       = [PlantillaJugadaInline]

    actions       = ['crear_arrejuntao_action']

    def crear_arrejuntao_action(self, request, queryset):
        _, creado = PlantillaProducto.crear_arrejuntao()
        msg = 'EL ARREJUNTAO creado.' if creado else 'EL ARREJUNTAO ya existía.'
        self.message_user(request, msg)
    crear_arrejuntao_action.short_description = '⭐ Crear plantilla EL ARREJUNTAO'


# =============================================================================
# CATÁLOGO DE ANIMALITOS (modelo simple)
# =============================================================================

@admin.register(Animalito)
class AnimalitoAdmin(admin.ModelAdmin):
    list_display  = ('numero', 'nombre', 'imagen_preview', 'activo')
    list_filter   = ('activo',)
    search_fields = ('numero', 'nombre')
    ordering      = ('id',)
    list_editable = ('activo',)

    def imagen_preview(self, obj):
        return logo_preview(obj, 'imagen', 32)
    imagen_preview.short_description = 'Imagen'


# =============================================================================
# TICKETS Y APUESTAS
# =============================================================================

# NOTE: Ticket usa FK a admin_comercializacion.UsuariosTaquilla.
# Temporalmente desregistrado hasta que esa app resuelva su carga.
# class ApuestaDetalleInline(admin.TabularInline):
#     model  = ApuestaDetalle
#     extra  = 0
#     fields = ('tipo_jugada', 'numero_apostado', 'signo', 'monto_apostado',
#               'monto_premio', 'estatus')
#     readonly_fields = ('monto_premio', 'estatus')
#     show_change_link = True


# @admin.register(Ticket)
# class TicketAdmin(admin.ModelAdmin):
#     list_display  = ('serie', 'vendedor', 'sorteo_id', 'total', 'anulado',
#                      'num_apuestas', 'fecha_emision', 'id_agencia', 'id_taquilla')
#     list_filter   = ('anulado', 'vendedor', 'id_agencia')
#     search_fields = ('serie', 'vendedor__username', 'id_agencia')
#     ordering      = ('-fecha_emision',)
#     readonly_fields = ('fecha_emision', 'total')
#     date_hierarchy  = 'fecha_emision'
#     inlines         = [ApuestaDetalleInline]
#     actions = ['anular_tickets']
#     def num_apuestas(self, obj):
#         return obj.apuestas.count()
#     num_apuestas.short_description = '# Apuestas'
#     def anular_tickets(self, request, queryset):
#         for ticket in queryset.filter(anulado=False):
#             ticket.anular()
#         self.message_user(request, '{} ticket(s) anulado(s).'.format(queryset.count()))
#     anular_tickets.short_description = '🚫 Anular tickets seleccionados'


# @admin.register(ApuestaDetalle)
# class ApuestaDetalleAdmin(admin.ModelAdmin):
#     list_display  = ('ticket', 'tipo_jugada', 'numero_apostado', 'signo',
#                      'monto_apostado', 'monto_premio', 'estatus', 'liquidado_en')
#     list_filter   = ('estatus', 'tipo_jugada', 'signo')
#     search_fields = ('ticket__serie', 'numero_apostado')
#     ordering      = ('-liquidado_en',)
#     readonly_fields = ('monto_premio', 'liquidado_en', 'sistema_liquidacion')
#     date_hierarchy  = 'ticket__fecha_emision'



# =============================================================================
# RESULTADOS Y LIQUIDACIÓN
# =============================================================================

@admin.register(ResultadoSorteo)
class ResultadoSorteoAdmin(admin.ModelAdmin):
    list_display  = ('sorteo_id', 'producto', 'fecha_sorteo',
                     'res_triple_a', 'res_triple_b', 'res_signo',
                     'res_animalito', 'res_cuatro_cifras', 'res_cinco_cifras',
                     'liquidado', 'liquidado_en')
    list_filter   = ('liquidado', 'producto')
    search_fields = ('sorteo_id',)
    ordering      = ('-fecha_sorteo',)
    readonly_fields = ('liquidado', 'liquidado_en', 'stats_liquidacion')
    date_hierarchy  = 'fecha_sorteo'

    fieldsets = (
        ('Identificación', {
            'fields': ('producto', 'sorteo_id', 'fecha_sorteo'),
        }),
        ('Resultados Ganadores', {
            'fields': (
                ('res_triple_a', 'res_triple_b'),
                ('res_signo', 'res_animalito'),
                ('res_cuatro_cifras', 'res_cinco_cifras'),
            ),
        }),
        ('Estado de Liquidación (solo lectura)', {
            'classes': ('collapse',),
            'fields': ('liquidado', 'liquidado_en', 'stats_liquidacion'),
        }),
    )

    actions = ['forzar_liquidacion']

    def forzar_liquidacion(self, request, queryset):
        liquidados = 0
        for resultado in queryset.filter(liquidado=False):
            resultado.liquidar_apuestas()
            liquidados += 1
        self.message_user(request, '{} sorteo(s) liquidado(s).'.format(liquidados))
    forzar_liquidacion.short_description = '⚡ Forzar liquidación de sorteos seleccionados'


from django import forms as dj_forms

class LiquidacionSorteoForm(dj_forms.ModelForm):
    """Formulario con defaults = 0 para todos los campos decimales requeridos."""

    class Meta:
        from admin_juego.models_arrejuntao import LiquidacionSorteo as _LS
        model = _LS
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pone 0 como valor inicial en todos los campos DecimalField vacíos
        _DECIMAL_DEFAULTS = [
            'nporcentaje_comision_com', 'nporcentaje_participacion_com', 'nporcentaje_regalia_com',
            'nporcentaje_comision_ban', 'nporcentaje_participacion_ban', 'nporcentaje_regalia_ban',
            'nporcentaje_comision_dis', 'nporcentaje_participacion_dis', 'nporcentaje_regalia_dis',
            'nporcentaje_comision_agc',
            'mmonto_venta', 'mmonto_venta_ganador', 'mmonto_premios',
            'mmonto_comision_com', 'mmonto_regalia_com',
            'mmonto_comision_ban', 'mmonto_regalia_ban',
            'mmonto_comision_dis', 'mmonto_regalia_dis',
            'mmonto_comision_agc',
            'msaldo_oper', 'msaldo_com', 'msaldo_ban', 'msaldo_dis',
        ]
        for fname in _DECIMAL_DEFAULTS:
            if fname in self.fields and not self.initial.get(fname):
                self.fields[fname].initial  = 0
                self.fields[fname].required = True
                if hasattr(self.fields[fname].widget, 'attrs'):
                    self.fields[fname].widget.attrs.setdefault('placeholder', '0.00')

        # Campos opcionales → no requeridos
        _OPTIONAL = ['msaldo_agc', 'msaldo_bruto_com', 'msaldo_bruto_ban', 'msaldo_bruto_dis',
                     'msaldo_oper_ban', 'msaldo_oper_dis', 'msaldo_oper_cm', 'msaldo_cm',
                     'id_perfil_pago_premios']
        for fname in _OPTIONAL:
            if fname in self.fields:
                self.fields[fname].required = False
                self.fields[fname].initial  = 0


@admin.register(LiquidacionSorteo)
class LiquidacionSorteoAdmin(admin.ModelAdmin):
    form          = LiquidacionSorteoForm
    list_display  = ('ref_sorteo', 'id_agencia', 'id_banca',
                     'monto_venta_fmt', 'monto_premios_fmt',
                     'utilidad_neta', 'pct_premios_display',
                     'tserial_ifa', 'created_at')
    list_filter   = ('id_banca', 'id_agencia', 'id_distribuidor')
    search_fields = ('id_sorteo', 'tserial_ifa')
    ordering      = ('-id_sorteo',)
    readonly_fields = ('created_at', 'updated_at')
    date_hierarchy  = 'created_at'
    list_per_page   = 25

    fieldsets = (
        ('🔗 Identificadores de Jerarquía', {
            'description': 'Ingrese los IDs numéricos de cada actor en la cadena comercial.',
            'fields': (
                ('id_sorteo', 'id_lista', 'id_tipo_lista'),
                ('id_prestador_servicio', 'id_comercializador'),
                ('id_banca', 'id_distribuidor', 'id_agencia', 'id_taquilla', 'id_operador'),
            ),
        }),
        ('💰 Montos y Premios', {
            'description': 'Totales del sorteo en Bs.',
            'fields': (
                ('mmonto_venta', 'mmonto_venta_ganador', 'mmonto_premios'),
            ),
        }),
        ('📊 Porcentajes — Comercializador', {
            'classes': ('collapse',),
            'fields': ('nporcentaje_comision_com', 'nporcentaje_participacion_com', 'nporcentaje_regalia_com'),
        }),
        ('📊 Porcentajes — Banca', {
            'classes': ('collapse',),
            'fields': ('nporcentaje_comision_ban', 'nporcentaje_participacion_ban', 'nporcentaje_regalia_ban'),
        }),
        ('📊 Porcentajes — Distribuidor', {
            'classes': ('collapse',),
            'fields': ('nporcentaje_comision_dis', 'nporcentaje_participacion_dis', 'nporcentaje_regalia_dis'),
        }),
        ('📊 Porcentajes — Agencia', {
            'classes': ('collapse',),
            'fields': ('nporcentaje_comision_agc',),
        }),
        ('💳 Comisiones y Regalías (calculadas)', {
            'classes': ('collapse',),
            'description': 'Se calculan automáticamente si se dejan en 0.',
            'fields': (
                ('mmonto_comision_com', 'mmonto_regalia_com'),
                ('mmonto_comision_ban', 'mmonto_regalia_ban'),
                ('mmonto_comision_dis', 'mmonto_regalia_dis'),
                ('mmonto_comision_agc',),
            ),
        }),
        ('⚖️ Saldos Netos por Actor', {
            'fields': (
                ('msaldo_oper', 'msaldo_com', 'msaldo_ban'),
                ('msaldo_dis', 'msaldo_agc'),
            ),
        }),
        ('📁 Saldos Brutos y Operador', {
            'classes': ('collapse',),
            'fields': (
                ('msaldo_bruto_com', 'msaldo_bruto_ban', 'msaldo_bruto_dis'),
                ('msaldo_oper_ban', 'msaldo_oper_dis', 'msaldo_oper_cm', 'msaldo_cm'),
            ),
        }),
        ('🖨️ IFA y Perfil de Pago', {
            'fields': ('tserial_ifa', 'id_perfil_pago_premios'),
        }),
        ('🕐 Auditoría', {
            'classes': ('collapse',),
            'fields': ('created_at', 'updated_at'),
        }),
    )

    def save_model(self, request, obj, form, change):
        """Auto-calcula comisiones en Bs si quedan en 0."""
        v = float(obj.mmonto_venta or 0)
        def calc(pct, campo):
            if not getattr(obj, campo) or float(getattr(obj, campo)) == 0:
                setattr(obj, campo, round(v * float(pct or 0) / 100, 2))
        calc(obj.nporcentaje_comision_com,  'mmonto_comision_com')
        calc(obj.nporcentaje_regalia_com,   'mmonto_regalia_com')
        calc(obj.nporcentaje_comision_ban,  'mmonto_comision_ban')
        calc(obj.nporcentaje_regalia_ban,   'mmonto_regalia_ban')
        calc(obj.nporcentaje_comision_dis,  'mmonto_comision_dis')
        calc(obj.nporcentaje_regalia_dis,   'mmonto_regalia_dis')
        calc(obj.nporcentaje_comision_agc,  'mmonto_comision_agc')
        super().save_model(request, obj, form, change)

    # ── Columnas del listado ──────────────────────────────────────────────────
    @admin.display(description='Sorteo #', ordering='id_sorteo')
    def ref_sorteo(self, obj):
        return format_html('<b style="color:#1a73e8">#{}</b>', obj.id_sorteo)

    @admin.display(description='Venta Bs.', ordering='mmonto_venta')
    def monto_venta_fmt(self, obj):
        return format_html('<span style="font-weight:600">{:,.2f}</span>', obj.mmonto_venta or 0)

    @admin.display(description='Premios Bs.', ordering='mmonto_premios')
    def monto_premios_fmt(self, obj):
        v = float(obj.mmonto_premios or 0)
        color = '#dc2626' if v > 0 else '#6b7280'
        return format_html('<span style="color:{};font-weight:600">{:,.2f}</span>', color, v)

    @admin.display(description='Utilidad Neta', ordering='mmonto_venta')
    def utilidad_neta(self, obj):
        utilidad = obj.get_utilidad_neta()
        color = '#16a34a' if utilidad >= 0 else '#dc2626'
        return format_html('<b style="color:{};">{:,.2f}</b>', color, utilidad)

    @admin.display(description='% Premio')
    def pct_premios_display(self, obj):
        v = float(obj.mmonto_venta or 0)
        p = float(obj.mmonto_premios or 0)
        if v > 0:
            pct = p / v * 100
            color = '#dc2626' if pct > 80 else '#f59e0b' if pct > 60 else '#16a34a'
            return format_html('<span style="color:{};font-weight:700">{:.1f}%</span>', color, pct)
        return '—'



# =============================================================================
# FECHAS / CONFIGURACIÓN DE SORTEO (LOTERÍA)
# =============================================================================

@admin.register(Fechas)
class FechasAdmin(admin.ModelAdmin):
    list_display  = ('nombre_sorteo', 'temporadas', 'sistema', 'fechaini', 'fechafin',
                     'estado_sorteo', 'permite_parley', 'permite_quiniela', 'permite_simple')
    list_filter   = ('sistema', 'status', 'apuestasimple', 'parley', 'quiniela')
    search_fields = ('jornada',)
    ordering      = ('-fechaini',)
    date_hierarchy = 'fechaini'
    # Sin raw_id_fields → dropdowns normales para bases pequeñas de lotería

    fieldsets = (
        ('📋 Datos del Sorteo', {
            'fields': ('jornada', 'sistema', 'temporadas', 'status'),
            'description': 'Identifica el sorteo o período de venta de lotería.',
        }),
        ('📅 Vigencia (Período de Ventas)', {
            'fields': (('fechaini', 'fechafin'),),
            'description': 'Rango de fechas durante el cual se aceptan apuestas.',
        }),
        ('🎯 Tipos de Apuesta Permitidos', {
            'fields': ('apuestasimple', 'parley', 'quiniela'),
            'description': (
                'Activa únicamente los tipos de apuesta que aplican para este sorteo. '
                'Para lotería estándar, activa solo "Apuesta Simple".'
            ),
        }),
        ('🏆 Opciones de Acumulado / Quiniela', {
            'classes': ('collapse',),
            'fields': ('count_encuentros', 'monto_inicial', 'valor'),
            'description': 'Solo aplica si este sorteo usa modalidad Quiniela.',
        }),
    )

    # ── Columnas personalizadas para el listado ──────────────────────────────
    @admin.display(description='Nombre del Sorteo', ordering='jornada')
    def nombre_sorteo(self, obj):
        return format_html('<b style="color:#1a73e8">{}</b>', obj.jornada)

    @admin.display(description='Estado', ordering='status')
    def estado_sorteo(self, obj):
        nombre = str(obj.status) if obj.status else '—'
        color = '#16a34a' if 'activ' in nombre.lower() or 'abierto' in nombre.lower() else '#dc2626'
        return format_html('<span style="color:{};font-weight:700">{}</span>', color, nombre)

    @admin.display(description='Simple', boolean=True)
    def permite_simple(self, obj):
        return obj.apuestasimple

    @admin.display(description='Parley', boolean=True)
    def permite_parley(self, obj):
        return obj.parley

    @admin.display(description='Quiniela', boolean=True)
    def permite_quiniela(self, obj):
        return obj.quiniela


# ─────────────────────────────────────────────────────────────────────────────
# ModalidadJuego (Equipos / Selecciones)
# ─────────────────────────────────────────────────────────────────────────────

@admin.register(ModalidadJuego)
class ModalidadJuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'deporte', 'logo_img', 'created_at', 'updated_at')
    list_filter = ('deporte',)
    search_fields = ('nombre', 'deporte__nombre')
    ordering = ('deporte', 'nombre')

    @admin.display(description='Logo')
    def logo_img(self, obj):
        return logo_preview(obj, 'logo', 32)


@admin.register(ModalidadProducto)
class ModalidadProductoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'liga', 'created_at')
    list_filter = ('liga',)
    search_fields = ('equipo__nombre', 'liga__nombre')
    ordering = ('liga', 'equipo')


@admin.register(ModalidadPeriodo)
class ModalidadPeriodoAdmin(admin.ModelAdmin):
    list_display = ('equipo', 'temporada', 'created_at')
    list_filter = ('temporada',)
    search_fields = ('equipo__nombre', 'temporada__nombre')
    ordering = ('temporada', 'equipo')

@admin.register(OperadoraLoteria)
class OperadoraLoteriaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'created_at')
    search_fields = ('nombre',)
    ordering = ('nombre',)
