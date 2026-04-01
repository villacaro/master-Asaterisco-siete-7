"""
seed_status.py
Inserta los Status requeridos por el sistema Asterisco Siete.
Usa sqlite3 directo para evitar Redis/auditoría.

Tabla: admin_status_status
Columnas: id, name, codename, content_type, order, created_at, updated_at
  content_type choices:
    0 = Status de actualizacion
    1 = Status de usuarios
    2 = Status de encuentros
    3 = Status de taquillas
    4 = Status de jugadas
    5 = Status de encuentro resultado
    6 = Status de venta de tickets
    7 = Status de ??????
    8 = Status de tickets
"""
import os, sys, sqlite3
from pathlib import Path
from datetime import datetime

# ── Path setup ───────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')

# Setup Django solo para obtener el path de la BD
import django
django.setup()
from django.db import connection
db_path = connection.settings_dict['NAME']
print(f"  DB: {db_path}")

now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# ── Status a insertar ─────────────────────────────────────────────────────────
# (name, codename, content_type_int, order)
STATUS_LIST = [
    # Generales del sistema de cadenas (content_type=0 → actualizacion)
    ('Activo',           'activo',               0, 1),
    ('Inactivo',         'inactivo',              0, 2),
    ('Suspendido',       'suspendido',            0, 3),
    ('Eliminado',        'status_eliminado',      0, 4),
    ('En Instalación',   'status_instalacion',    0, 5),
    # Usuarios (content_type=1)
    ('Activo',           'usuario_activo',        1, 1),
    ('Inactivo',         'usuario_inactivo',      1, 2),
    ('Suspendido',       'usuario_suspendido',    1, 3),
    ('Eliminado',        'usuario_eliminado',     1, 4),
    # Taquillas (content_type=3)
    ('Conectada',        'taquilla_conectada',    3, 1),
    ('Desconectada',     'taquilla_desconectada', 3, 2),
    ('Suspendida',       'taquilla_suspendida',   3, 3),
    # Jugadas (content_type=4)
    ('Pendiente',        'jugada_pendiente',      4, 1),
    ('Procesando',       'jugada_procesando',     4, 2),
    ('Pagada',           'jugada_pagada',         4, 3),
    ('Anulada',          'jugada_anulada',        4, 4),
    # Tickets (content_type=8)
    ('Pendiente',        'ticket_pendiente',      8, 1),
    ('Pagado',           'ticket_pagado',         8, 2),
    ('Anulado',          'ticket_anulado',        8, 3),
]

conn = sqlite3.connect(db_path)
cur = conn.cursor()

print("=" * 60)
print("  Insertando Status en admin_status_status")
print("=" * 60)

# Mostrar lo que ya existe
cur.execute("SELECT id, name, codename, content_type FROM admin_status_status ORDER BY content_type, id")
existentes = cur.fetchall()
print(f"\n  Ya existen {len(existentes)} registros:")
for r in existentes:
    print(f"    id={r[0]} | ct={r[3]} | {r[2]:<30} | {r[1]}")

print()

created = 0
skipped = 0

for name, codename, content_type, order in STATUS_LIST:
    # Verificar si ya existe (por codename, que es UNIQUE)
    cur.execute("SELECT COUNT(*) FROM admin_status_status WHERE codename=?", (codename,))
    if cur.fetchone()[0] > 0:
        skipped += 1
        print(f"  ⏭  Ya existe: {codename}")
        continue

    try:
        cur.execute(
            "INSERT INTO admin_status_status (name, codename, content_type, [order], created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (name, codename, content_type, order, now_str, now_str)
        )
        created += 1
        print(f"  ✅  Creado: {codename:<30} → {name}")
    except sqlite3.IntegrityError as e:
        print(f"  ❌  Error en '{codename}': {e}")

conn.commit()
conn.close()

print()
print("=" * 60)
print(f"  Creados: {created} | Omitidos (ya existían): {skipped}")
print("=" * 60)
print("\n  ✅ Ahora recarga el admin: /admin/admin_comercializacion/operadoras/1/change/")
