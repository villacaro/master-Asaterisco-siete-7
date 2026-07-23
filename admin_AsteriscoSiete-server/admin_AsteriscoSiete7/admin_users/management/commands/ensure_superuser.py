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
        else:
            # 1. Create Django User
            dj_user, created = User.objects.get_or_create(username=username, defaults={'email': email})
            dj_user.set_password(password)
            dj_user.is_staff = True
            dj_user.is_superuser = True
            dj_user.save()

            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Superusuario '{username}' creado (Django)."))
            else:
                self.stdout.write(f"ℹ  El usuario '{username}' actualizado con SU_PASSWORD.")

            # 2. Create Custom Users object
            from admin_users.models import Users
            from admin_permisologia.models import Permissions
            from admin_status.models import Status, StatusDetail

            perm, _ = Permissions.objects.get_or_create(codename='userprofile_master', defaults={'nombre': 'Master', 'content_type': 1})
            status, _ = Status.objects.get_or_create(codename='status_activo', defaults={'name': 'Activo', 'content_type': 4, 'order': 1})

            u, u_created = Users.objects.get_or_create(
                user=username,
                defaults={'email': email, 'profile': perm, 'superuser': True}
            )
            u.set_password(password)
            u.superuser = True
            u.save()

            StatusDetail.objects.get_or_create(user=u, status=status, enddate=None)
            self.stdout.write(self.style.SUCCESS(f"✅ Perfil custom '{username}' configurado para el Dashboard."))

        # ── 2. Cadena comercial + usuario taquilla ───────────────────────────
        self.stdout.write("── Iniciando setup_taquilla_inicial ──────────────")
        try:
            call_command("setup_taquilla_inicial")
        except Exception as exc:
            self.stderr.write(f"⚠  setup_taquilla_inicial error: {exc}")
            # No re-raise: el servidor inicia aunque el setup falle
