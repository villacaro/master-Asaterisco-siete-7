# -*- coding: utf-8 -*-
"""
urls_local.py — URLs mínimas para desarrollo local
Solo expone el admin de Django para poder gestionar usuarios.
El sistema completo requiere PostgreSQL + Redis (producción).
"""
from django.contrib import admin
from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect

admin.autodiscover()

urlpatterns = [
    # Admin Django estándar
    path('admin/', admin.site.urls),

    # Login / logout usando vistas nativas de Django auth
    path('login/', auth_views.LoginView.as_view(
        template_name='admin/login.html',
        redirect_authenticated_user=True,
    ), name='login'),

    path('logout/', auth_views.LogoutView.as_view(next_page='/login/'), name='logout'),

    # Raíz → redirige al admin
    re_path(r'^$', lambda r: HttpResponseRedirect('/admin/')),
]
