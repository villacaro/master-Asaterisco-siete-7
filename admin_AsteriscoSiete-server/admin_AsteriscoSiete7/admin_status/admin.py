from admin_status.models import Status, StatusDetail, TaquillaStatusDetail
from django.contrib import admin


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name', 'codename', 'content_type', 'order', 'created_at', 'updated_at')
    list_filter = ('content_type',)
    list_editable = ('codename', 'content_type', 'order')
    search_fields = ('name',)
    ordering = ("content_type",)


@admin.register(StatusDetail)
class StatusDetailAdmin(admin.ModelAdmin):
    list_display = ('user', 'status', 'startdate', 'enddate', 'created_at')
    list_filter = ('status', 'startdate')
    search_fields = ('user__username',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'


@admin.register(TaquillaStatusDetail)
class TaquillaStatusDetailAdmin(admin.ModelAdmin):
    list_display = ('usuariotaquilla', 'status', 'startdate', 'enddate', 'created_at')
    list_filter = ('status', 'startdate')
    search_fields = ('usuariotaquilla__nombre',)
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
