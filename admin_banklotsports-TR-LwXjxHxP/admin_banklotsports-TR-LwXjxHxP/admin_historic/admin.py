from admin_historic.models import UsersProcesses
from django.contrib import admin


@admin.register(UsersProcesses)
class UsersProcessesAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type', 'created_at', 'updated_at')
    list_filter = ('content_type', 'created_at', 'updated_at')
    search_fields = ('name', 'codename', 'created_at', 'updated_at')
