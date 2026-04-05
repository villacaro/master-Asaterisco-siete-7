"""
Comando de gestión para:
  1. Crear el superusuario de producción (si no existe).
  2. Inicializar la cadena comercial + usuario taquilla (idempotente).
Se ejecuta en cada arranque del contenedor — todas las operaciones son seguras
de re-ejecutar gracias a get_or_create.
"""
import os
from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Crea el superusuario de prod y prepara la cadena comercial."

    def handle(self, *args, **options):

        # ── 1. Superusuario ──────────────────────────────────────────────────
        User = get_user_model()
        username = os.environ.get("SU_USERNAME", "admin")
        email    = os.environ.get("SU_EMAIL",    "admin@asterisco7.com")
        password = os.environ.get("SU_PASSWORD", "")

        if not password:
            self.stderr.write("⚠  SU_PASSWORD no definido — omitiendo superusuario.")
        elif User.objects.filter(username=username).exists():
            self.stdout.write(f"ℹ  El usuario '{username}' ya existe. Nada que hacer.")
        else:
            User.objects.create_superuser(username=username, email=email, password=password)
            self.stdout.write(self.style.SUCCESS(f"✅ Superusuario '{username}' creado."))

        # ── 2. Cadena comercial + usuario taquilla ───────────────────────────
        self.stdout.write("── Iniciando setup_taquilla_inicial ──────────────")
        try:
            call_command("setup_taquilla_inicial")
        except Exception as exc:
            self.stderr.write(f"⚠  setup_taquilla_inicial error: {exc}")
            # No re-raise: el servidor inicia aunque el setup falle
