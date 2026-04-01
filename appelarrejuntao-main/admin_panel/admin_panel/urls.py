"""
admin_panel/urls.py
"""
from django.contrib import admin
from django.urls import path, include

admin.site.site_header  = "🎰 EL ARREJUNTAO – Panel de Administración"
admin.site.site_title   = "Arrejuntao Admin"
admin.site.index_title  = "Gestión de Usuarios y Datos"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_rest.urls')),   # API REST para la taquilla
    path('', include('usuarios.urls')),
]
