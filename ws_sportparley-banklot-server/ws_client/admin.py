from django.contrib import admin
from django.contrib.admin import SimpleListFilter

from .forms import ClientFilesAdminForm, ClientIPAddressAdminForm, ClientVersionAdminForm
from .models import ClientFiles, ClientIPAddress, ClientStatus, ClientVersion


class ClientStatusFilter(SimpleListFilter):
    title = ('clientstatus')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        list_tuple = []
        for status in ClientStatus.objects.filter(content_type=2):
            list_tuple.append((status.id, status.status))
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id=self.value())
        else:
            return queryset


class ClientIPAddressFilter(SimpleListFilter):
    title = ('clientstatus')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        list_tuple = []
        for status in ClientStatus.objects.filter(content_type=1):
            # print category
            list_tuple.append((status.id, status.status))
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id=self.value())
        else:
            return queryset


class ClientFilesFilter(SimpleListFilter):
    title = ('systemstatus')
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        list_tuple = []
        for status in ClientStatus.objects.filter(content_type=3):
            # print category
            list_tuple.append((status.id, status.status))
        return list_tuple

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(status__id=self.value())
        else:
            return queryset


class ClientIPAddressAdmin(admin.ModelAdmin):
    list_display = ('pk', 'ip_address', 'ip_type', 'protocol', 'status')
    list_editable = ('ip_address',)
    ordering = ('status',)
    list_filter = ('ip_type', ClientIPAddressFilter,)
    form = ClientIPAddressAdminForm


class ClientVersionAdmin(admin.ModelAdmin):
    list_display = ('version', 'status',)
    list_filter = (ClientStatusFilter,)
    form = ClientVersionAdminForm


class ClientFilesAdmin(admin.ModelAdmin):
    list_display = ('pk', 'file', 'version', 'client_version', 'size', 'os', 'location', 'status')
    list_filter = ('os', ClientFilesFilter,)
    form = ClientFilesAdminForm


admin.site.register(ClientIPAddress, ClientIPAddressAdmin)
admin.site.register(ClientVersion, ClientVersionAdmin)
admin.site.register(ClientFiles, ClientFilesAdmin)


@admin.register(ClientStatus)
class ClientStatusAdmin(admin.ModelAdmin):
    list_display = ('status', 'codename', 'content_type')
