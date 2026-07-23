"""
Script para crear el usuario administrador del sistema Asterisco Siete.
Ejecutar con:
    python manage.py shell --settings=admin_asterisco7.settings_local < crear_admin.py
"""
import os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')

import django
django.setup()

from admin_permisologia.models import Permissions
from admin_users.models import Users
from admin_status.models import Status, StatusDetail

# 1. Seed status values (from seed_status.py)
required_statuses = [
    {'name': 'Habilitado',         'codename': 'status_habilitado',        'content_type': 2, 'order': 1},
    {'name': 'Pendiente',          'codename': 'status_pendiente',         'content_type': 2, 'order': 2},
    {'name': 'Reanudado',          'codename': 'status_reanudado',         'content_type': 2, 'order': 3},
    {'name': 'Eliminado',          'codename': 'status_eliminado',         'content_type': 2, 'order': 4},
    {'name': 'Eliminado frio',     'codename': 'status_eliminado_frio',    'content_type': 2, 'order': 5},
    {'name': 'Procesandose',       'codename': 'status_procesandose',      'content_type': 2, 'order': 6},
    {'name': 'Procesado',          'codename': 'status_procesado',         'content_type': 2, 'order': 7},
    {'name': 'Activo',             'codename': 'status_activo',            'content_type': 4, 'order': 1},
    {'name': 'Activo sin venta',   'codename': 'status_activo_sin_venta',  'content_type': 4, 'order': 2},
    {'name': 'Bloqueado',          'codename': 'status_bloqueado',         'content_type': 4, 'order': 3},
    {'name': 'Procesando ganador', 'codename': 'status_procesandoganador', 'content_type': 4, 'order': 4},
    {'name': 'Perdedor',           'codename': 'status_perdedor',          'content_type': 4, 'order': 5},
    {'name': 'Nuevo',              'codename': 'status_nuevo',             'content_type': 1, 'order': 1},
]
seeded_count = 0
for s in required_statuses:
    obj, created = Status.objects.get_or_create(codename=s['codename'], defaults=s)
    if created:
        seeded_count += 1
print('[OK] Estatus creados:', seeded_count)

# 2. Perfil master
perm, creado = Permissions.objects.get_or_create(
    codename='userprofile_master',
    defaults={'nombre': 'Master', 'content_type': 1}
)
print('[OK] Perfil:', perm.codename, '(creado=%s)' % creado)

# 3. Estado activo (debe ser status_activo)
status = Status.objects.filter(codename='status_activo').first()
print('[OK] Estado activo:', status)

# 4. Crear o actualizar usuario admin (modelo personalizado Users)
USUARIO  = 'admin'
EMAIL    = 'admin@asterisco7.com'
CLAVE    = 'admin1234'

if not Users.objects.filter(user=USUARIO).exists():
    u = Users(
        user=USUARIO,
        email=EMAIL,
        profile=perm,
        superuser=True,
    )
    u.set_password(CLAVE)
    u.save()
    if status:
        StatusDetail.objects.get_or_create(user=u, status=status)
    print('[OK] Usuario CREADO exitosamente (Modelo Users)')
else:
    u = Users.objects.get(user=USUARIO)
    u.set_password(CLAVE)
    u.superuser    = True
    u.save()
    # Close any other active status details and set to status_activo
    if status:
        # deactivate previous status details
        StatusDetail.objects.filter(user=u, enddate=None).exclude(status=status).update(enddate=django.utils.timezone.now())
        StatusDetail.objects.get_or_create(user=u, status=status, enddate=None)
    print('[OK] Usuario ACTUALIZADO exitosamente (Modelo Users)')

# 5. Crear o actualizar usuario admin en el modelo incorporado de Django (django.contrib.auth.models.User)
from django.contrib.auth.models import User as DjangoUser
dj_u, created_dj = DjangoUser.objects.get_or_create(
    username=USUARIO,
    defaults={
        'email': EMAIL,
        'is_staff': True,
        'is_superuser': True,
    }
)
dj_u.set_password(CLAVE)
dj_u.is_staff = True
dj_u.is_superuser = True
dj_u.save()
print('[OK] Usuario Django %s (creado=%s) PASSWORD seteada con éxito' % (USUARIO, created_dj))

print()
print('============================================')
print('  CREDENCIALES DE ACCESO - ASTERISCO SIETE')
print('============================================')
print('  URL:      http://127.0.0.1:8000/login/')
print('  Admin URL: http://127.0.0.1:8000/admin/')
print('  Usuario:  admin')
print('  Clave:    admin1234')
print('============================================')
