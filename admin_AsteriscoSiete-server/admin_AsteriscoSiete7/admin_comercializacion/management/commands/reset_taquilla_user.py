"""
reset_taquilla_user.py
======================
Comando idempotente que garantiza que exista el UsuariosTaquilla 'taquilla1'
con la contraseña correctamente hasheada.

Qué hace:
  1. Busca el UsuariosTaquilla con user='taquilla1'
  2. Si no existe: lo crea (requiere que la cadena comercial ya exista)
  3. Si existe: resetea el password con make_password (aunque ya esté correcto)
  4. Imprime el resultado para verlo en los logs de Railway

Uso:
  python manage.py reset_taquilla_user
  python manage.py reset_taquilla_user --user taquilla1 --password Taquilla2024!
"""

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password, check_password


class Command(BaseCommand):
    help = 'Resetea o crea el usuario de taquilla con password hasheado correctamente.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--user', default='taquilla1',
            help='Nombre de usuario de taquilla (default: taquilla1)'
        )
        parser.add_argument(
            '--password', default='Taquilla2024!',
            help='Contraseña a establecer (default: Taquilla2024!)'
        )

    def handle(self, *args, **options):
        username = options['user']
        password = options['password']

        from django.apps import apps
        UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')

        self.stdout.write(f'\n── Buscando UsuariosTaquilla: {username!r} ──────────────')

        # ── Diagnóstico: mostrar todos los usuarios existentes ──────────────
        all_users = list(UsuariosTaquilla.objects.values_list('user', flat=True))
        self.stdout.write(f'  Usuarios existentes en BD: {all_users}')

        usuario = UsuariosTaquilla.objects.filter(user=username).first()

        if not usuario:
            self.stdout.write(self.style.WARNING(
                f'  ⚠  Usuario {username!r} no encontrado. Intentando crear...'
            ))
            usuario = self._create_usuario(username, password)
            if not usuario:
                return  # error ya reportado
        else:
            self.stdout.write(f'  ✅ Encontrado (pk={usuario.pk})')

        # ── Verificar estado actual del password ────────────────────────────
        pwd_raw = str(getattr(usuario, 'password', ''))
        self.stdout.write(f'  Hash actual (primeros 60 chars): {pwd_raw[:60]!r}')

        already_ok = check_password(password, pwd_raw)
        if already_ok:
            self.stdout.write(self.style.SUCCESS(
                f'  ✅ Password ya es correcto. Login debería funcionar.'
            ))
        else:
            self.stdout.write(self.style.WARNING(
                f'  ⚠  Password incorrecto o no hasheado. Reseteando...'
            ))

        # ── Siempre resetear el hash para garantizar consistencia ───────────
        usuario.password = make_password(password)
        usuario.save(update_fields=['password'])
        self.stdout.write(self.style.SUCCESS(
            f'\n✅ Password reseteado correctamente.\n'
            f'  🔑 Usuario:  {username}\n'
            f'  🔑 Clave:    {password}\n'
            f'  🌐 URL:      https://master-asaterisco-siete-7-production.up.railway.app/taquilla/\n'
        ))

    def _create_usuario(self, username, password):
        """Intenta crear el UsuariosTaquilla si la cadena comercial ya existe."""
        from django.apps import apps
        from admin_status.models import Status

        try:
            UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')
            Taquillas = apps.get_model('admin_comercializacion', 'Taquillas')

            # Buscar la primera taquilla disponible
            taquilla = Taquillas.objects.first()
            if not taquilla:
                self.stdout.write(self.style.ERROR(
                    '  ❌ No hay Taquillas en la BD. '
                    'Ejecuta primero: python manage.py setup_taquilla_inicial'
                ))
                return None

            # Verificar si ya hay un usuario en esa taquilla
            existing = UsuariosTaquilla.objects.filter(taquilla=taquilla).first()
            if existing:
                self.stdout.write(
                    f'  ℹ  La taquilla pk={taquilla.pk} ya tiene usuario: {existing.user!r}. '
                    f'Reseteando password en ese usuario...'
                )
                return existing

            status = Status.objects.filter(codename='status_instalacion').first()
            if not status:
                status = Status.objects.filter(codename='activo').first()
            if not status:
                self.stdout.write(self.style.ERROR(
                    '  ❌ No se encontró un Status válido. '
                    'Ejecuta primero: python manage.py setup_taquilla_inicial'
                ))
                return None

            from django.utils.timezone import now
            usuario = UsuariosTaquilla(
                user=username,
                nombre='Operador Principal',
                taquilla=taquilla,
                status=status,
            )
            usuario.password = make_password(password)
            usuario.save()
            self.stdout.write(self.style.SUCCESS(
                f'  ✅ UsuariosTaquilla creado: {username!r} (pk={usuario.pk})'
            ))
            return usuario

        except Exception as exc:
            import traceback
            self.stdout.write(self.style.ERROR(
                f'  ❌ Error al crear usuario: {exc}\n{traceback.format_exc()}'
            ))
            return None
