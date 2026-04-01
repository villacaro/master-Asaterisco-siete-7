# -*- coding: utf-8 -*-

from admin_permisologia.models import Groups, Menu, Permissions
from django.contrib import admin


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):

    def sent_messaje(self, request, rows_updated):
        if rows_updated == 1:
            message_bit = "1 registro"
        else:
            message_bit = "%s registros" % rows_updated
        self.message_user(request, "%s modificados exitosamente." % message_bit)

    def make_is_viws(self, request, queryset):
        self.sent_messaje(request, queryset.update(is_view=True))
    make_is_viws.short_description = "Cambiar a enlaces VISIBLES"

    def make_is_not_viws(self, request, queryset):
        self.sent_messaje(request, queryset.update(is_view=False))
    make_is_not_viws.short_description = "Cambiar a enlaces INVISIBLES"

    def make_is_public(self, request, queryset):
        self.sent_messaje(request, queryset.update(is_public=True))
    make_is_public.short_description = "Cambiar a enlaces PUBLICOS"

    def make_is_not_public(self, request, queryset):
        self.sent_messaje(request, queryset.update(is_public=False))
    make_is_not_public.short_description = "Cambiar a enlaces PRIVADOS"

    actions = ['make_is_viws', 'make_is_not_viws', 'make_is_public', 'make_is_not_public']
    # actions_selection_counter = True
    actions_on_top = True
    list_display = ('name', '__str__', 'orden', 'codename', 'url',
                    'icon', 'is_view', 'is_public', 'is_global')
    ordering = ['-orden']
    list_editable = ('codename', 'url', 'icon')
    search_fields = ('name', 'codename',)
    list_filter = ('content_type', 'is_view', 'is_public', 'is_global')
    list_per_page = 50


@admin.register(Permissions)
class PermissionsAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_top = True
    list_per_page = 50

    list_display = ('content_type', 'name', 'codename', 'updated_at')
    search_fields = ('name', 'codename')
    ordering = ('content_type', 'name')
    list_filter = ('content_type',)
    filter_horizontal = ('menu', 'profiles')


@admin.register(Groups)
class GroupsAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_top = True
    list_per_page = 50

    list_display = ('name', 'codename', 'updated_at',)
    search_fields = ('name', 'codename',)
    ordering = ('name',)
    filter_horizontal = ('permissions',)
