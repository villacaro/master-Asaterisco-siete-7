# -*- coding: utf-8 -*-
from django.contrib import admin
from admin_apuestas.models import (
    TicketsType, Tickets, TicketsDetail,
    TicketStatus, TicketsDetailStatus
)


@admin.register(TicketsType)
class TicketsTypeAdmin(admin.ModelAdmin):
    """Tipos de apuestas (Parley, Quiniela, etc.)"""
    list_display   = ('nombre', 'codename', 'descripcion')
    list_editable  = ('codename', 'descripcion')
    search_fields  = ('nombre', 'codename')
    ordering       = ('nombre',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Tickets)
class TicketsAdmin(admin.ModelAdmin):
    """
    Tickets de apuesta.
    NOTA: list_select_related = False evita el error
    'at most 64 tables in a join' de SQLite al mostrar el listado.
    Los FK se muestran como raw_id para que no generen JOINs en la lista.
    """
    list_display         = ('id', 'key', 'monto', 'monto_premio',
                            'monto_ganancia', 'fecha', 'created_at')
    list_filter          = ('fecha',)
    search_fields        = ('key', 'id')
    readonly_fields      = ('created_at', 'updated_at')
    ordering             = ('-created_at',)
    date_hierarchy       = 'fecha'
    raw_id_fields        = ('user', 'ticket_type', 'status')
    # ← clave: desactiva el select_related automático del changelist
    list_select_related  = False
    show_full_result_count = False


@admin.register(TicketsDetail)
class TicketsDetailAdmin(admin.ModelAdmin):
    """Ítems de detalle de un ticket."""
    list_display           = ('id', 'monto', 'puntaje_apostado',
                              'puntaje_calculado', 'created_at')
    search_fields          = ('id',)
    readonly_fields        = ('created_at', 'updated_at')
    ordering               = ('-created_at',)
    raw_id_fields          = ('ticket', 'jugada', 'status')
    list_select_related    = False
    show_full_result_count = False


@admin.register(TicketStatus)
class TicketStatusAdmin(admin.ModelAdmin):
    """Historial de estatus de un ticket."""
    list_display           = ('id', 'startdate', 'enddate', 'created_at')
    readonly_fields        = ('created_at', 'updated_at')
    ordering               = ('-created_at',)
    raw_id_fields          = ('ticket', 'status')
    list_select_related    = False
    show_full_result_count = False


@admin.register(TicketsDetailStatus)
class TicketsDetailStatusAdmin(admin.ModelAdmin):
    """Historial de estatus de un ítem de ticket."""
    list_display           = ('id', 'startdate', 'enddate', 'created_at')
    readonly_fields        = ('created_at', 'updated_at')
    ordering               = ('-created_at',)
    raw_id_fields          = ('detalle_ticket', 'status')
    list_select_related    = False
    show_full_result_count = False
