"""
Comando de gestión para crear el superusuario de producción.
Se ejecuta una sola vez. Si el usuario ya existe, no hace nada.
"""
import os
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el superusuario de producción si no existe."

    def handle(self, *args, **options):
        User = get_user_model()
        username = os.environ.get("SU_USERNAME", "admin")
        email    = os.environ.get("SU_EMAIL",    "admin@asterisco7.com")
        password = os.environ.get("SU_PASSWORD", "")

        if not password:
            self.stderr.write("⚠  SU_PASSWORD no definido. Abortando.")
            return

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"ℹ  El usuario '{username}' ya existe. Nada que hacer.")
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f"✅ Superusuario '{username}' creado correctamente."))
