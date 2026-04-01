# -*- coding: utf-8 -*-
from django.contrib import admin
from admin_finanzas.models import (
    Banco, TipoCuenta, TipoMovimiento,
    Comercializadora, Configuracion,
)


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display  = ('nombre', 'created_at', 'updated_at')
    list_filter   = ('nombre',)
    search_fields = ('nombre',)


@admin.register(TipoCuenta)
class TipoCuentaAdmin(admin.ModelAdmin):
    list_display  = ('codigo', 'nombre', 'created_at', 'updated_at')
    list_filter   = ('codigo', 'nombre')
    search_fields = ('codigo', 'nombre')
    list_editable = ('nombre',)


@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display  = ('codename', 'nombre', 'description', 'created_at', 'updated_at')
    list_filter   = ('codename', 'nombre')
    search_fields = ('codename', 'nombre', 'description')
    list_editable = ('nombre', 'description')


@admin.register(Comercializadora)
class ComercializadoraAdmin(admin.ModelAdmin):
    # Sólo IDs simples en list_display para evitar JOINs encadenados
    list_display           = ('id', 'saldo_inicial', 'saldo_fecha', 'resumen_personalizado', 'created_at')
    list_filter            = ()
    search_fields          = ()
    readonly_fields        = ('created_at', 'updated_at')
    ordering               = ('-created_at',)
    raw_id_fields          = ('operadora', 'banca', 'taquilla',
                              'bloque', 'distribuidor', 'agencia',
                              'resumen_personalizado_comer')
    show_full_result_count = False
    # Evita el JOIN masivo por select_related automático de Django Admin
    list_select_related    = False


@admin.register(Configuracion)
class ConfiguracionAdmin(admin.ModelAdmin):
    # Omitimos 'comercializadora' del list_display para evitar el JOIN en cadena
    # que supera el límite de 64 tablas de SQLite
    list_display           = ('id', 'tipo', 'min', 'max', 'created_at')
    list_filter            = ('tipo',)
    readonly_fields        = ('created_at', 'updated_at')
    ordering               = ('tipo',)
    raw_id_fields          = ('comercializadora',)
    # Desactiva el select_related automático — causa "at most 64 tables in a join"
    list_select_related    = False
    show_full_result_count = False

