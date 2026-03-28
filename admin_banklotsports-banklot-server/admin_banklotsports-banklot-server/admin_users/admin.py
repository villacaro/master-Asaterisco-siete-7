from admin_users.models import UserProfile, Users
from django.contrib import admin


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'codename', 'content_type', 'created_at', 'updated_at')
    list_filter = ('nombre', 'codename', 'created_at', 'updated_at')
    search_fields = ('nombre', 'codename', 'created_at', 'updated_at')
    ordering = ('content_type',)

    list_editable = ('codename', 'content_type',)


@admin.register(Users)
class UsersAdmin(admin.ModelAdmin):
    actions_selection_counter = True
    actions_on_top = True
    list_per_page = 50

    list_display = ('profile', 'etiqueta', 'user', 'email', 'user_ref', 'superuser', 'last_login')
    list_editable = ('superuser',)
    exclude = ('last_login', 'password')
    list_filter = ('last_login', 'profile')
    search_fields = ('user', 'email')
    ordering = ('profile', 'user',)
    filter_horizontal = ('comercializadora', 'user_permissions', 'groups')
