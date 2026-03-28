from admin_status.models import Status
from django.contrib import admin


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type', 'order', 'created_at', 'updated_at')
    list_filter = ('content_type',)
    list_editable = ('codename', 'content_type', 'order')
    search_fields = ('name',)
    ordering = ("content_type",)
