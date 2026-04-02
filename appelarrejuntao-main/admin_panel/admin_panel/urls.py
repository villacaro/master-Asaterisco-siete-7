"""
admin_panel/urls.py
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.contrib.auth.models import User

admin.site.site_header  = "🎰 EL ARREJUNTAO – Panel de Administración"
admin.site.site_title   = "Arrejuntao Admin"
admin.site.index_title  = "Gestión de Usuarios y Datos"

@staff_member_required
def arrejuntao_dashboard(request):
    """Panel principal personalizado de El Arrejuntao."""
    return render(request, 'arrejuntao/dashboard.html')

@staff_member_required
def api_django_users(request):
    """Devuelve los usuarios Django del sistema como JSON."""
    users = User.objects.all().order_by('-date_joined')
    data = []
    for u in users:
        data.append({
            'id': u.id,
            'username': u.username,
            'email': u.email,
            'first_name': u.first_name,
            'last_name': u.last_name,
            'is_staff': u.is_staff,
            'is_superuser': u.is_superuser,
            'is_active': u.is_active,
            'date_joined': u.date_joined.strftime('%d/%m/%Y %H:%M'),
            'last_login': u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else '—',
        })
    return JsonResponse({'usuarios': data, 'total': len(data)})

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api_rest.urls')),
    path('api/django-users/', api_django_users, name='api_django_users'),
    path('arrejuntao/', arrejuntao_dashboard, name='arrejuntao_dashboard'),
    path('', include('usuarios.urls')),
]

