# -*- coding: utf-8 -*-

from admin_permisologia.models import Groups, Menu, Permissions
from django.core.cache import cache

print("Malote iniciandose")


def run(*args):
    """
         >> python manage.py runscript restart_menu_001
    """
    print("Reiniciando informacion del menu y permisos")
    Menu.objects.all().delete()
    Permissions.objects.all().delete()
    Groups.objects.all().delete()
    cache.clear()
    print("Data reiniciada con exito....")
