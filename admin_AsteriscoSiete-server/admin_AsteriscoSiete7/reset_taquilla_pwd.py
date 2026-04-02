import os, django
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings_local'
django.setup()

from django.apps import apps
from django.contrib.auth.hashers import check_password, make_password

UT = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')

# Mostrar todos los usuarios
print("=== USUARIOS TAQUILLA (todos) ===")
for u in UT.objects.all():
    pwd_raw = str(getattr(u, 'password', ''))
    nombre  = getattr(u, 'nombre', '')
    user    = getattr(u, 'user', '')
    print(f"  id={u.pk}  user={user!r}  nombre={nombre!r}")
    print(f"    pwd_hash={pwd_raw[:80]!r}")
    # Test: contraseña = '1234'
    for test_pwd in ['1234', 'admin', 'taquilla', '12345', '123456', user]:
        ok = check_password(test_pwd, pwd_raw)
        if ok:
            print(f"    >>> CONTRASEÑA ENCONTRADA: {test_pwd!r}")
    print()

# Cambiar/crear usuario de prueba
print("=== ACTUALIZANDO usuario 'carovilla' con password '1234' ===")
u = UT.objects.filter(user='carovilla').first()
if u:
    u.password = make_password('1234')
    u.save()
    print("  OK - password actualizado a '1234'")
else:
    print("  No encontrado")

print("\n=== ACTUALIZANDO usuario 'usuario_prueba' con password 'taquilla' ===")
u2 = UT.objects.filter(user='usuario_prueba').first()
if u2:
    u2.password = make_password('taquilla')
    u2.save()
    print("  OK - password actualizado a 'taquilla'")
else:
    print("  No encontrado")

print("\nDone! Prueba con:")
print("  usuario: carovilla   / clave: 1234")
print("  usuario: usuario_prueba / clave: taquilla")
