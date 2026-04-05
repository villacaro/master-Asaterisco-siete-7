"""
reset_taquilla_user.py
======================
Comando idempotente que garantiza que exista el UsuariosTaquilla 'taquilla1'
con la contrasena correctamente hasheada.

Usa queryset.update() en lugar de save() para EVITAR los signals de auditoria
que fallan cuando no existen registros de UsersProcesses en la BD de produccion.

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
            help='Contrasena a establecer (default: Taquilla2024!)'
        )

    def handle(self, *args, **options):
        username = options['user']
        password = options['password']
        hashed = make_password(password)

        from django.apps import apps
        UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')

        self.stdout.write('\n== reset_taquilla_user ==')

        # Diagnostico: mostrar todos los usuarios existentes
        all_users = list(UsuariosTaquilla.objects.values_list('user', flat=True))
        self.stdout.write('  Usuarios en BD: {0}'.format(all_users))

        qs = UsuariosTaquilla.objects.filter(user=username)

        if qs.exists():
            # Usar .update() en lugar de .save() para EVITAR signals de auditoria
            # que fallan cuando UsersProcesses no existe en la BD
            updated = qs.update(password=hashed)
            self.stdout.write(self.style.SUCCESS(
                '  OK Password actualizado via queryset.update() (filas: {0})\n'
                '  Usuario:  {1}\n'
                '  Clave:    {2}\n'
                '  URL: https://master-asaterisco-siete-7-production.up.railway.app/taquilla/\n'.format(
                    updated, username, password
                )
            ))
        else:
            self.stdout.write(self.style.WARNING(
                '  WARN Usuario {0!r} no existe. Intentando crear...'.format(username)
            ))
            created = self._create_usuario_sin_signals(username, password, hashed)
            if created:
                self.stdout.write(self.style.SUCCESS(
                    '  OK Usuario creado:\n'
                    '  Usuario:  {0}\n'
                    '  Clave:    {1}\n'.format(username, password)
                ))
            else:
                self.stdout.write(self.style.ERROR(
                    '  ERROR No se pudo crear el usuario. Ver traza arriba.'
                ))

    def _create_usuario_sin_signals(self, username, password, hashed):
        """Crea UsuariosTaquilla via SQL directo (bypass de signals y auditoria)."""
        from django.db import connection
        from django.apps import apps

        try:
            UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')
            Taquillas = apps.get_model('admin_comercializacion', 'Taquillas')
            Status = apps.get_model('admin_status', 'Status')

            taquilla = Taquillas.objects.first()
            if not taquilla:
                self.stdout.write(self.style.ERROR(
                    '  ERROR No hay Taquillas en la BD. Ejecuta setup_taquilla_inicial primero.'
                ))
                return False

            # Verificar si ya hay usuario en esa taquilla (con distinto user)
            existing = UsuariosTaquilla.objects.filter(taquilla=taquilla).first()
            if existing:
                self.stdout.write(
                    '  INFO Taquilla pk={0} ya tiene usuario: {1!r}. '
                    'Reseteando password...'.format(taquilla.pk, existing.user)
                )
                UsuariosTaquilla.objects.filter(pk=existing.pk).update(password=hashed)
                return True

            status = (
                Status.objects.filter(codename='status_instalacion').first()
                or Status.objects.filter(codename='activo').first()
            )
            if not status:
                self.stdout.write(self.style.ERROR('  ERROR No se encontro Status valido.'))
                return False

            # Insertar via SQL directo para evitar completamente los signals
            table = UsuariosTaquilla._meta.db_table
            with connection.cursor() as cur:
                cur.execute(
                    "INSERT INTO {0} "
                    "(user, nombre, taquilla_id, status_id, password, "
                    "pub_key_client, pub_key, priv_key, pk_clone) "
                    "VALUES (%s, %s, %s, %s, %s, '', '', '', 0)".format(table),
                    [username, 'Operador Principal', taquilla.pk, status.pk, hashed]
                )
            self.stdout.write('  OK Insertado via SQL directo (sin signals).')
            return True

        except Exception as exc:
            import traceback
            self.stdout.write(self.style.ERROR(
                '  ERROR al crear: {0}\n{1}'.format(exc, traceback.format_exc())
            ))
            return False
