import os, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings_local'
import django; django.setup()

from django.apps import apps

models_check = [
    ('admin_status',           'Status'),
    ('admin_profiles',         'Direcciones'),
    ('admin_comercializacion', 'Operadoras'),
    ('admin_comercializacion', 'Bloques'),
    ('admin_comercializacion', 'Bancas'),
    ('admin_comercializacion', 'Distribuidores'),
    ('admin_comercializacion', 'Agencias'),
    ('admin_comercializacion', 'Taquillas'),
    ('admin_comercializacion', 'UsuariosTaquilla'),
    ('admin_juego',            'SistemaJuego'),
    ('admin_juego',            'Sorteo'),
    ('admin_finanzas',         'Comercializadora'),
    ('admin_users',            'Users'),
]

print('=' * 55)
print(f'  {"app.MODELO":<40} {"COUNT":>8}')
print('=' * 55)
for app, model in models_check:
    try:
        M = apps.get_model(app, model)
        cnt = M.objects.count()
        flag = '  ⚠️ ' if cnt == 0 else '  ✅ '
        print(f'{flag} {app}.{model:<35} {cnt:>5}')
    except Exception as e:
        print(f'  ❌  {app}.{model:<35}   ERR: {e}')
print('=' * 55)
