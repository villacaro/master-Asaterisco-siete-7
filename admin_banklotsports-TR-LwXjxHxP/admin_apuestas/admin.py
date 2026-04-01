from admin_apuestas.models import TicketsType
from django.contrib import admin


@admin.register(TicketsType)
class TicketsTypeAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codename', 'descripcion')
    list_editable = ('codename', 'descripcion',)
    search_fields = ('nombre', 'codename', 'descripcion')
    ordering = ('nombre',)
