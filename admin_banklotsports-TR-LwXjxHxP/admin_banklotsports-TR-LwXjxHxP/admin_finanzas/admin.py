from admin_finanzas.models import Banco, TipoCuenta, TipoMovimiento
from django.contrib import admin


@admin.register(Banco)
class BancoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'created_at', 'updated_at')
    list_filter = ('nombre', 'created_at', 'updated_at')
    search_fields = ('nombre', 'created_at', 'updated_at')


@admin.register(TipoCuenta)
class TipoCuentaAdmin(admin.ModelAdmin):
    list_display = ('codigo', 'nombre', 'created_at', 'updated_at')
    list_filter = ('codigo', 'nombre', 'created_at', 'updated_at')
    search_fields = ('codigo', 'nombre', 'created_at', 'updated_at')
    list_editable = ('nombre', )


@admin.register(TipoMovimiento)
class TipoMovimientoAdmin(admin.ModelAdmin):
    list_display = ('codename', 'nombre', 'description', 'created_at', 'updated_at')
    list_filter = ('codename', 'nombre', 'description', 'created_at', 'updated_at')
    list_editable = ('nombre', 'description')
