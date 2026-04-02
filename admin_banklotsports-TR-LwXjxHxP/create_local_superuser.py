"""
Crea la BD SQLite mínima (solo auth) y el superusuario admin/admin123
para poder ingresar al sistema Parlay Match Point localmente.
"""
import os, sys, django

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_banklotsports.settings_local'

# Patch: forzar solo las apps mínimas necesarias para crear el superusuario
from django.conf import settings as _s

# Sólo necesitamos las apps core de Django para auth
_s.INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'django.contrib.auth',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
)
_s.DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME':   os.path.join(os.path.dirname(__file__), 'db_local_matchpoint.sqlite3'),
    }
}
_s.SESSION_ENGINE   = 'django.contrib.sessions.backends.db'
_s.MIDDLEWARE        = [m for m in _s.MIDDLEWARE if 'admin_principal' not in m and 'crequest' not in m]
_s.CACHES           = {'default': {'BACKEND': 'django.core.cache.backends.locmem.LocMemCache'}}

django.setup()

from django.db import connection
print("Creando tablas de autenticación...")

# Correr sólo las migraciones de las apps core
from django.core.management import call_command
call_command('migrate', '--run-syncdb', verbosity=1)

# Crear superusuario
from django.contrib.auth.models import User

USERNAME = 'admin'
PASSWORD = 'admin123'

if User.objects.filter(username=USERNAME).exists():
    u = User.objects.get(username=USERNAME)
    u.set_password(PASSWORD)
    u.is_superuser = True
    u.is_staff     = True
    u.is_active    = True
    u.save()
    print(f"✅ Usuario existente actualizado: {USERNAME} / {PASSWORD}")
else:
    User.objects.create_superuser(
        username  = USERNAME,
        email     = 'admin@asterisco7.com',
        password  = PASSWORD,
        first_name = 'Admin',
        last_name  = 'Parlay',
    )
    print(f"✅ Superusuario creado: {USERNAME} / {PASSWORD}")

print("\n🔑 Credenciales para http://127.0.0.1:8001/login/")
print(f"   Usuario  : {USERNAME}")
print(f"   Contraseña: {PASSWORD}")
