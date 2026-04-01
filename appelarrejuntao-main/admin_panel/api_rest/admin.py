"""
api_rest/admin.py  –  Panel de administración de sorteos
"""
from django.contrib import admin
from django.utils.html import format_html, mark_safe
from django.utils import timezone
from .models import ControlSorteo


# ── Acciones bulk ─────────────────────────────────────────────────────────────

@admin.action(description='🟢 Abrir sorteos seleccionados')
def abrir_sorteos(modeladmin, request, queryset):
    queryset.update(abierto=True)
    modeladmin.message_user(request, f'{queryset.count()} sorteo(s) abierto(s) exitosamente.')


@admin.action(description='🔴 Cerrar sorteos seleccionados')
def cerrar_sorteos(modeladmin, request, queryset):
    queryset.update(abierto=False, fecha_cierre=timezone.now())
    modeladmin.message_user(request, f'{queryset.count()} sorteo(s) cerrado(s) exitosamente.')


@admin.action(description='🔄 Reiniciar contador de ventas hoy')
def reiniciar_ventas(modeladmin, request, queryset):
    queryset.update(ventas_hoy=0)
    modeladmin.message_user(request, f'Contador reiniciado para {queryset.count()} sorteo(s).')


# ── Constantes de la matriz ────────────────────────────────────────────────────
SORTEOS_LISTA = [
    ('Triple A',         'triple_a'),
    ('Triple B',         'triple_b'),
    ('Triple + Signo',   'triple_signo'),
    ('El Arrimao',       'el_arrimao'),
    ('El Pegadito',      'el_pegadito'),
    ('Animalito',        'animalito'),
    ('Terminal A',       'terminal_a'),
    ('Terminal B',       'terminal_b'),
    ('Triple C',         'triple_c'),
    ('Terminal C',       'terminal_c'),
    ('Terminal + Signo', 'terminal_signo'),
]
HORARIOS_LISTA = ['10:00 AM', '01:00 PM', '04:00 PM', '07:00 PM', '11:00 PM']


# ── ModelAdmin ─────────────────────────────────────────────────────────────────

@admin.register(ControlSorteo)
class ControlSorteoAdmin(admin.ModelAdmin):

    # ── Lista principal ──────────────────────────────────────────
    list_display       = ['estado_badge', 'sorteo_display', 'horario', 'cupo_venta',
                          'ventas_hoy', 'disponibilidad_bar', 'actualizado']
    list_display_links = ['sorteo_display']
    list_filter        = ['abierto', 'sorteo', 'horario']
    search_fields      = ['sorteo', 'horario', 'notas']
    list_editable      = ['cupo_venta']
    ordering           = ['sorteo', 'horario']
    actions            = [abrir_sorteos, cerrar_sorteos, reiniciar_ventas]
    readonly_fields    = ['ventas_hoy', 'actualizado', 'disponibilidad_bar']
    list_per_page      = 25

    fieldsets = (
        ('📋 Identificación', {'fields': ('sorteo', 'horario')}),
        ('🎛️ Control de Estado', {
            'fields': ('abierto', 'cupo_venta', 'ventas_hoy', 'fecha_apertura', 'fecha_cierre'),
            'description': 'Controla si el sorteo acepta apuestas y cuántas puede aceptar.',
        }),
        ('📊 Info', {'fields': ('disponibilidad_bar', 'notas', 'actualizado'), 'classes': ('collapse',)}),
    )


    # ── URL personalizada para la vista matriz ────────────────────
    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom = [
            path('matriz/', self.admin_site.admin_view(self.matriz_view), name='sorteos_matriz'),
        ]
        return custom + urls

    # ── Vista matriz ──────────────────────────────────────────────
    def matriz_view(self, request):
        from django.shortcuts import render, redirect
        from django.contrib import messages

        if request.method == 'POST':
            all_sorteos = ControlSorteo.objects.all()
            updated = 0
            for s in all_sorteos:
                key = f'sorteo_{s.id}'
                nuevo_estado = key in request.POST  # checkbox marcado = abierto
                if s.abierto != nuevo_estado:
                    s.abierto = nuevo_estado
                    if not nuevo_estado:
                        s.fecha_cierre = timezone.now()
                    s.save(update_fields=['abierto', 'fecha_cierre'])
                    updated += 1
            messages.success(request, f'✅ {updated} sorteo(s) actualizados correctamente.')
            return redirect('.')

        # Construir diccionario de la matriz: clave = "sorteo_code-horario"
        all_sorteos = ControlSorteo.objects.all()
        matrix = {f'{s.sorteo}-{s.horario}': s for s in all_sorteos}

        ctx = {
            **self.admin_site.each_context(request),
            'title': 'Control de Sorteos – Matriz',
            'sorteos': SORTEOS_LISTA,
            'horarios': HORARIOS_LISTA,
            'matrix': matrix,
            'opts': self.model._meta,
        }
        return render(request, 'admin/api_rest/sorteos_matrix.html', ctx)

    # ── Columnas personalizadas ──────────────────────────────────

    @admin.display(description='Estado', ordering='abierto')
    def estado_badge(self, obj):
        color = '#16a34a' if obj.abierto else '#dc2626'
        icon  = '🟢' if obj.abierto else '🔴'
        label = 'ABIERTO' if obj.abierto else 'CERRADO'
        return format_html(
            '<span style="background:{};color:#fff;padding:3px 10px;border-radius:999px;'
            'font-size:11px;font-weight:700;white-space:nowrap;">{} {}</span>',
            color, icon, label
        )

    @admin.display(description='Sorteo', ordering='sorteo')
    def sorteo_display(self, obj):
        return format_html('<strong style="font-size:13px;">{}</strong>', obj.get_sorteo_display())

    @admin.display(description='Disponibilidad')
    def disponibilidad_bar(self, obj):
        if obj.cupo_venta == 0:
            return mark_safe('<span style="color:#6b7280;font-size:12px;">Sin límite</span>')
        pct = min(int(obj.ventas_hoy / obj.cupo_venta * 100), 100) if obj.cupo_venta else 0
        color = '#16a34a' if pct < 70 else ('#f59e0b' if pct < 90 else '#dc2626')
        return format_html(
            '<div style="width:120px;background:#e5e7eb;border-radius:4px;height:16px;overflow:hidden;">'
            '<div style="width:{}%;background:{};height:100%;border-radius:4px;"></div></div>'
            '<span style="font-size:11px;color:#374151;">{}/{} ({}%)</span>',
            pct, color, obj.ventas_hoy, obj.cupo_venta, pct
        )


# ── Vista Matriz (Proxy Admin) ────────────────────────────────────────────────

from .models import ControlSorteoMatriz

@admin.register(ControlSorteoMatriz)
class ControlSorteoMatrizAdmin(admin.ModelAdmin):
    """Aparece en el menu del admin como 'Vista Matriz de Sorteos'.
    El changelist_view redirige directamente a la pagina de la matriz."""

    def changelist_view(self, request, extra_context=None):
        from django.shortcuts import redirect
        return redirect('/admin/api_rest/controlsorteo/matriz/')

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False
