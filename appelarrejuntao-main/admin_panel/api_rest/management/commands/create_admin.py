"""
management/commands/create_admin.py
Crea el superusuario de Railway desde variables de entorno.
Uso: python manage.py create_admin
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    help = 'Crea el superusuario inicial desde variables de entorno'

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email    = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@elarrejuntao.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', '')

        if not password:
            self.stderr.write('ERROR: Define DJANGO_SUPERUSER_PASSWORD en las variables de entorno')
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f'El usuario "{username}" ya existe.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Superusuario "{username}" creado correctamente.'))
