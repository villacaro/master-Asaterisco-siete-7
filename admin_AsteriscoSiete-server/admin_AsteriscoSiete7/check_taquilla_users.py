import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings_local'
django.setup()

from django.apps import apps

# 1. Ver usuarios en UsuariosTaquilla
print("=== UsuariosTaquilla ===")
try:
    UT = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')
    users = list(UT.objects.all()[:20])
    print(f"Total: {len(users)}")
    for u in users:
        pwd = str(getattr(u, 'password', ''))[:50]
        nombre = getattr(u, 'nombre', '?')
        user = getattr(u, 'user', '?')
        print(f"  user={user!r}  nombre={nombre!r}  pwd_starts={pwd!r}")
except Exception as e:
    print(f"ERROR: {e}")
    import traceback; traceback.print_exc()

# 2. Ver usuarios Django Auth
print("\n=== Django Auth Users ===")
try:
    from django.contrib.auth.models import User
    for u in User.objects.all()[:10]:
        print(f"  username={u.username!r}  is_staff={u.is_staff}  is_super={u.is_superuser}")
except Exception as e:
    print(f"ERROR: {e}")
