# -*- coding: utf-8 -*-

from django.core.cache import cache


def run(*args):
    """
         >> python manage.py runscript reload_menu
    """
    print('Recargando informacion del menu')
    from admin_asterisco7.urls import urlpatterns
    cache.clear()
    print('Menu actualizado con exito....'.format(urlpatterns))
