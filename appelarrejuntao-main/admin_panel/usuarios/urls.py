"""
usuarios/urls.py
"""
from django.urls import path
from . import views

urlpatterns = [
    path('',                               views.lista_usuarios,  name='lista_usuarios'),
    path('usuarios/crear/',                views.crear_usuario,   name='crear_usuario'),
    path('usuarios/<str:uid>/toggle/',     views.toggle_usuario,  name='toggle_usuario'),
    path('usuarios/<str:uid>/eliminar/',   views.eliminar_usuario,name='eliminar_usuario'),
    path('usuarios/<str:uid>/password/',   views.cambiar_password,name='cambiar_password'),
    path('usuarios/<str:uid>/detalle/',    views.detalle_usuario, name='detalle_usuario'),
]
