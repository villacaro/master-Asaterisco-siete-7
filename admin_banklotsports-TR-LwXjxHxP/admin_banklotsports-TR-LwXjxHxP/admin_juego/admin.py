from admin_juego.models import SistemaJuego
from django.contrib import admin


@admin.register(SistemaJuego)
class SistemaJuegoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'logo', 'comercializadora', 'created_at', 'updated_at')
    list_filter = ('nombre', )
    search_fields = ('nombre', )
    ordering = ("nombre", )
