"""
setup_taquilla_inicial.py
=========================
Comando de gestión para inicializar la cadena comercial completa en producción.

Qué hace:
  1. Sembrar Status necesarios
  2. Crear TaquillaDataDefault  (user_name='taquilla', passwd='Taquilla2024!')
  3. Crear cadena: Operadora → Bloque → Banca → Distribuidor → Agencia
  4. Crear 1 Taquilla + UsuariosTaquilla bajo esa Agencia

Uso:
  python manage.py setup_taquilla_inicial
  python manage.py setup_taquilla_inicial --dry-run
"""

from django.core.management.base import BaseCommand
from django.utils.timezone import now


# ──────────────────────────────────────────────────────────────────────────────
class Command(BaseCommand):
    help = 'Inicializa la cadena comercial mínima y el primer usuario de taquilla.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run', action='store_true',
            help='Muestra qué se crearía sin guardar nada.'
        )

    def handle(self, *args, **options):
        self.dry = options['dry_run']

        if self.dry:
            self.stdout.write(self.style.WARNING(
                '\n*** MODO DRY-RUN — nada será guardado ***\n'))

        try:
            self._seed_status()
            tdd = self._seed_taquilla_data_default()
            direccion = self._get_or_create_direccion()
            operadora = self._get_or_create_operadora(direccion)
            bloque = self._get_or_create_bloque(operadora, direccion)
            banca = self._get_or_create_banca(bloque, direccion)
            distribuidor = self._get_or_create_distribuidor(banca, direccion)
            agencia = self._get_or_create_agencia(distribuidor, direccion)
            self._get_or_create_taquilla_y_usuario(agencia, tdd)

            self.stdout.write(self.style.SUCCESS(
                '\n✅ Setup completo.\n'
                '  ▶ Taquilla: https://master-asaterisco-siete-7-production.up.railway.app/taquilla/\n'
                '  🔑 Usuario:  taquilla1\n'
                '  🔑 Clave:    Taquilla2024!\n'
            ))
        except Exception as exc:
            self.stdout.write(self.style.ERROR(f'\n❌ ERROR: {exc}\n'))
            raise

    # ──────────────────────────────────────────────────────────────────────────
    # 1. STATUS
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_status(self):
        from admin_status.models import Status

        STATUS_LIST = [
            # (name, codename, content_type, order)
            ('Activo',          'activo',                0, 1),
            ('Inactivo',        'inactivo',              0, 2),
            ('Suspendido',      'suspendido',            0, 3),
            ('Eliminado',       'status_eliminado',      0, 4),
            ('En Instalación',  'status_instalacion',    0, 5),
            ('Bloqueado',       'status_bloqueado',      0, 6),
            ('Reinstalación',   'status_reinstalacion',  0, 7),
            # Taquillas (content_type=3)
            ('Conectada',       'taquilla_conectada',    3, 1),
            ('Desconectada',    'taquilla_desconectada', 3, 2),
            ('Suspendida',      'taquilla_suspendida',   3, 3),
            # Usuarios (content_type=1)
            ('Activo',          'usuario_activo',        1, 1),
            ('Inactivo',        'usuario_inactivo',      1, 2),
            # Tickets (content_type=8)
            ('Pendiente',       'ticket_pendiente',      8, 1),
            ('Pagado',          'ticket_pagado',         8, 2),
            ('Anulado',         'ticket_anulado',        8, 3),
            # Jugadas (content_type=4)
            ('Pendiente',       'jugada_pendiente',      4, 1),
            ('Procesando',      'jugada_procesando',     4, 2),
            ('Pagada',          'jugada_pagada',         4, 3),
            ('Anulada',         'jugada_anulada',        4, 4),
        ]

        self.stdout.write('── 1. Status ─────────────────────────────────────')
        for name, codename, ct, order in STATUS_LIST:
            if self.dry:
                self.stdout.write(f'  [dry] crearía Status: {codename}')
            else:
                obj, created = Status.objects.get_or_create(
                    codename=codename,
                    defaults={'name': name, 'content_type': ct, 'order': order}
                )
                icon = '✅' if created else '⏭ '
                self.stdout.write(f'  {icon} {codename}')

    # ──────────────────────────────────────────────────────────────────────────
    # 2. TAQUILLA DATA DEFAULT
    # ──────────────────────────────────────────────────────────────────────────
    def _seed_taquilla_data_default(self):
        from admin_comercializacion.models import TaquillaDataDefault

        self.stdout.write('── 2. TaquillaDataDefault ────────────────────────')
        USER = 'taquilla'
        PASS = 'Taquilla2024!'

        if self.dry:
            self.stdout.write(f'  [dry] crearía TaquillaDataDefault user_name={USER}')
            return None

        qs = TaquillaDataDefault.objects.all()
        if qs.exists():
            tdd = qs.first()
            self.stdout.write(f'  ⏭  ya existe (user_name={tdd.user_name})')
        else:
            tdd = TaquillaDataDefault.objects.create(user_name=USER, passwd=PASS)
            self.stdout.write(f'  ✅ creado (user_name={USER})')

        return tdd

    # ──────────────────────────────────────────────────────────────────────────
    # 3. DIRECCIÓN
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_direccion(self):
        from admin_profiles.models import Direcciones

        self.stdout.write('── 3. Dirección ──────────────────────────────────')
        TEXTO = 'DIRECCION PRINCIPAL'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Direccion: {TEXTO}')
            return None

        obj = Direcciones.objects.filter(direccion=TEXTO).first()
        if obj:
            self.stdout.write(f'  ⏭  ya existe (pk={obj.pk})')
        else:
            obj = Direcciones.objects.create(direccion=TEXTO)
            self.stdout.write(f'  ✅ creada (pk={obj.pk})')

        return obj

    # ──────────────────────────────────────────────────────────────────────────
    # 4. OPERADORA
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_operadora(self, direccion):
        from admin_comercializacion.models import Operadoras
        from admin_status.models import Status

        self.stdout.write('── 4. Operadora ──────────────────────────────────')
        NOMBRE = 'ASTERISCO SIETE'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Operadora: {NOMBRE}')
            return None

        obj = Operadoras.objects.filter(nombre=NOMBRE).first()
        if obj:
            self.stdout.write(f'  ⏭  ya existe (pk={obj.pk})')
        else:
            s = Status.objects.get(codename='activo')
            obj = Operadoras.objects.create(
                nombre=NOMBRE, status=s, direccion=direccion)
            self.stdout.write(f'  ✅ creada (pk={obj.pk})')

        return obj

    # ──────────────────────────────────────────────────────────────────────────
    # 5. BLOQUE (Multi Banca)
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_bloque(self, operadora, direccion):
        from admin_comercializacion.models import Bloques
        from admin_status.models import Status

        self.stdout.write('── 5. Bloque (Multi Banca) ───────────────────────')
        NOMBRE = 'MULTI BANCA CENTRAL'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Bloque: {NOMBRE}')
            return None

        obj = Bloques.objects.filter(nombre=NOMBRE, operadora=operadora).first()
        if obj:
            self.stdout.write(f'  ⏭  ya existe (pk={obj.pk})')
        else:
            s = Status.objects.get(codename='activo')
            obj = Bloques.objects.create(
                nombre=NOMBRE, operadora=operadora,
                status=s, direccion=direccion)
            self.stdout.write(f'  ✅ creado (pk={obj.pk})')

        return obj

    # ──────────────────────────────────────────────────────────────────────────
    # 6. BANCA
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_banca(self, bloque, direccion):
        from admin_comercializacion.models import Bancas
        from admin_status.models import Status

        self.stdout.write('── 6. Banca ──────────────────────────────────────')
        NOMBRE = 'BANCA CENTRAL'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Banca: {NOMBRE}')
            return None

        obj = Bancas.objects.filter(nombre=NOMBRE, bloque=bloque).first()
        if obj:
            self.stdout.write(f'  ⏭  ya existe (pk={obj.pk})')
        else:
            s = Status.objects.get(codename='activo')
            obj = Bancas.objects.create(
                nombre=NOMBRE, bloque=bloque,
                status=s, direccion=direccion,
                modelo_negocio=1)   # 1 = Porcentajes
            self.stdout.write(f'  ✅ creada (pk={obj.pk})')

        return obj

    # ──────────────────────────────────────────────────────────────────────────
    # 7. DISTRIBUIDOR
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_distribuidor(self, banca, direccion):
        from admin_comercializacion.models import Distribuidores
        from admin_status.models import Status

        self.stdout.write('── 7. Distribuidor ───────────────────────────────')
        NOMBRE = 'DISTRIBUIDOR CENTRAL'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Distribuidor: {NOMBRE}')
            return None

        obj = Distribuidores.objects.filter(nombre=NOMBRE, banca=banca).first()
        if obj:
            self.stdout.write(f'  ⏭  ya existe (pk={obj.pk})')
        else:
            s = Status.objects.get(codename='activo')
            obj = Distribuidores.objects.create(
                nombre=NOMBRE, banca=banca,
                status=s, direccion=direccion)
            self.stdout.write(f'  ✅ creado (pk={obj.pk})')

        return obj

    # ──────────────────────────────────────────────────────────────────────────
    # 8. AGENCIA (Centro de Apuesta)
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_agencia(self, distribuidor, direccion):
        from admin_comercializacion.models import Agencias
        from admin_status.models import Status

        self.stdout.write('── 8. Agencia (Centro de Apuesta) ────────────────')
        NOMBRE = 'AGENCIA CENTRAL'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Agencia: {NOMBRE}')
            return None

        obj = Agencias.objects.filter(nombre=NOMBRE, distribuidores=distribuidor).first()
        if obj:
            self.stdout.write(f'  ⏭  ya existe (pk={obj.pk})')
        else:
            s = Status.objects.get(codename='activo')
            # Solo los campos sin null=True son obligatorios: nombre, distribuidores,
            # num_taquillas, status, direccion.  El resto tiene null=True.
            obj = Agencias.objects.create(
                nombre=NOMBRE,
                distribuidores=distribuidor,
                num_taquillas=1,
                status=s,
                direccion=direccion,
            )
            self.stdout.write(f'  ✅ creada (pk={obj.pk})')

        return obj

    # ──────────────────────────────────────────────────────────────────────────
    # 9. TAQUILLA + USUARIO TAQUILLA
    # ──────────────────────────────────────────────────────────────────────────
    def _get_or_create_taquilla_y_usuario(self, agencia, tdd):
        from admin_comercializacion.models import Taquillas, UsuariosTaquilla
        from admin_status.models import Status, TaquillaStatusDetail

        self.stdout.write('── 9. Taquilla + Usuario ─────────────────────────')
        TAQUILLA_NOMBRE = 'Taquilla 1'
        USER_NAME = f'{tdd.user_name}1' if tdd else 'taquilla1'
        USER_PASS = tdd.passwd if tdd else 'Taquilla2024!'

        if self.dry:
            self.stdout.write(f'  [dry] crearía Taquilla: {TAQUILLA_NOMBRE}')
            self.stdout.write(f'  [dry] crearía UsuarioTaquilla: {USER_NAME}')
            return

        # ─── Taquilla ───────────────────────────────────────────────────────
        taquilla = Taquillas.objects.filter(
            taquilla=TAQUILLA_NOMBRE, agencia=agencia
        ).first()

        if taquilla:
            self.stdout.write(f'  ⏭  Taquilla ya existe (pk={taquilla.pk})')
        else:
            taquilla = Taquillas.objects.create(
                taquilla=TAQUILLA_NOMBRE,
                agencia=agencia,
                is_taquilla_master=True,
                monto_alquiler=0,
            )
            self.stdout.write(f'  ✅ Taquilla creada (pk={taquilla.pk})')

        # ─── UsuarioTaquilla ─────────────────────────────────────────────────
        usuario = UsuariosTaquilla.objects.filter(taquilla=taquilla).first()

        if usuario:
            self.stdout.write(f'  ⏭  UsuarioTaquilla ya existe: {usuario.user}')
            return

        status_instalacion = Status.objects.get(codename='status_instalacion')

        from django.contrib.auth.hashers import make_password
        usuario = UsuariosTaquilla(
            user=USER_NAME,
            nombre='Operador Principal',
            taquilla=taquilla,
            status=status_instalacion,
        )
        usuario.password = make_password(USER_PASS)
        usuario.save()
        self.stdout.write(f'  ✅ UsuarioTaquilla creado: {USER_NAME}')

        # ─── TaquillaStatusDetail ─────────────────────────────────────────────
        TaquillaStatusDetail.objects.create(
            usuariotaquilla=usuario,
            startdate=now(),
            status=status_instalacion,
        )
        self.stdout.write(f'  ✅ TaquillaStatusDetail creado')
