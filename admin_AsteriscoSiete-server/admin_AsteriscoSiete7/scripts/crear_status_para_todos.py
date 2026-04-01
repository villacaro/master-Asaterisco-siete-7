"""
crear_status_para_todos.py
Crea registros de Status para todos los ContentTypes del sistema
usando SQLite directo para evitar el trigger de Redis/auditoría.
"""
import os, sys, django, sqlite3
from pathlib import Path
from datetime import datetime

# Asegurar que el directorio raíz del proyecto esté en el path
BASE_DIR = Path(__file__).resolve().parent.parent  # .../admin_AsteriscoSiete7/
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')
django.setup()

# ── Monkey-patch Redis para evitar crash ──────────────────────────────────────
import admin_historic.auditoria as _aud
class _RedisMock:
    def get(self, *a, **kw): return None
    def set(self, *a, **kw): return None
    def delete(self, *a, **kw): return None
_aud.REDIS_DB = _RedisMock()
_aud.save_audit = lambda *a, **kw: None

from django.db import connection
from django.contrib.contenttypes.models import ContentType

db_path = connection.settings_dict['NAME']
now_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

print("=" * 60)
print("  Creando Status para todos los ContentTypes del sistema")
print("=" * 60)

# Definir los estados que queremos crear para cada grupo de apps
APPS_CONFIG = [
    # (app_label, nombre_estado, codename, orden)
    ('admin_comercializacion', 'Activo',     'activo',     1),
    ('admin_comercializacion', 'Inactivo',   'inactivo',   2),
    ('admin_comercializacion', 'Suspendido', 'suspendido', 3),
    ('admin_finanzas',         'Activo',     'activo',     1),
    ('admin_finanzas',         'Inactivo',   'inactivo',   2),
    ('admin_profiles',         'Activo',     'activo',     1),
    ('admin_profiles',         'Inactivo',   'inactivo',   2),
    ('admin_juego',            'Activo',     'activo',     1),
    ('admin_juego',            'Inactivo',   'inactivo',   2),
    ('admin_usuarios',         'Activo',     'activo',     1),
    ('admin_usuarios',         'Inactivo',   'inactivo',   2),
    ('admin_resultados',       'Activo',     'activo',     1),
    ('admin_resultados',       'Inactivo',   'inactivo',   2),
    ('admin_status',           'Activo',     'activo',     1),
]

conn = sqlite3.connect(db_path)
cur = conn.cursor()

created = 0
skipped = 0

for app_label, name, codename, order in APPS_CONFIG:
    # Obtener todos los ContentTypes de esta app
    cts = ContentType.objects.filter(app_label=app_label)
    if not cts.exists():
        print(f"  ⚠️   App '{app_label}' no tiene ContentTypes, omitiendo...")
        continue

    for ct in cts:
        # Verificar si ya existe este status para este content_type y codename
        cur.execute(
            "SELECT COUNT(*) FROM admin_status_status WHERE content_type=? AND codename=?",
            (ct.pk, codename)
        )
        if cur.fetchone()[0] > 0:
            skipped += 1
            continue

        # Crear el status
        try:
            cur.execute(
                "INSERT INTO admin_status_status (name, codename, content_type, [order], created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                (name, codename, ct.pk, order, now_str, now_str)
            )
            created += 1
            print(f"  ✅  Status '{name}' ({codename}) → {app_label}.{ct.model}")
        except sqlite3.IntegrityError as e:
            print(f"  ⚠️   Error en {app_label}.{ct.model} '{codename}': {e}")

conn.commit()
conn.close()

print()
print("=" * 60)
print(f"  Creados: {created} | Omitidos (ya existían): {skipped}")
print("=" * 60)

# Verificar cuántos status existen ahora
from admin_status.models import Status
total = Status.objects.count()
print(f"\n  Total de Status en la base de datos: {total}")

# Verificar status para Operadoras específicamente
from django.apps import apps as dj_apps
try:
    Operadoras = dj_apps.get_model('admin_comercializacion', 'Operadoras')
    ct_op = ContentType.objects.get_for_model(Operadoras)
    statuses_op = Status.objects.filter(content_type=ct_op)
    print(f"  Status disponibles para Operadoras: {statuses_op.count()}")
    for s in statuses_op:
        print(f"    → id={s.pk} name={s.name} codename={s.codename}")
except Exception as e:
    print(f"  Error verificando Operadoras: {e}")

print("\n  ✅ Recarga /admin/admin_comercializacion/operadoras/1/change/")
