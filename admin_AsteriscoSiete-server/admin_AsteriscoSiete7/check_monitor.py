import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings')
django.setup()

from django.apps import apps

# HechoConnectionsComer
try:
    HechoConn = apps.get_model('admin_historic', 'HechoConnectionsComer')
    print('HechoConnectionsComer OK')
    for f in HechoConn._meta.get_fields():
        print(f'  {f.name}: {type(f).__name__}')
    print(f'  Total registros: {HechoConn.objects.count()}')
except Exception as e:
    print(f'ERROR HechoConnectionsComer: {e}')

print()
TaqSessions = apps.get_model('admin_historic', 'TaquillaSessions')
print(f'TaquillaSessions registros: {TaqSessions.objects.count()}')
for f in TaqSessions._meta.get_fields():
    print(f'  {f.name}: {type(f).__name__}')

print()
from django.db import connection
with connection.cursor() as cur:
    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='admin_historic_taquillasessions'")
    row = cur.fetchone()
    if row:
        print('Schema TaquillaSessions:')
        print(row[0])

    cur.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name LIKE '%hechoconn%'")
    row = cur.fetchone()
    if row:
        print('Schema HechoConn:')
        print(row[0])
    else:
        print('Tabla HechoConnectionsComer NO existe en la BD')

    # Listar todas las tablas relevantes
    cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE '%historic%'")
    print('Tablas admin_historic:')
    for r in cur.fetchall():
        print(f'  {r[0]}')
