"""
seed_sistema_juego.py
Inserta via SQL directo (sin auditoria ni Redis):
  - Theme (admin_themes_theme)
  - Comercializadora por cada taquilla (admin_finanzas_comercializadora)
  - SistemaJuego vinculado a la Operadora (admin_juego_sistemajuego)

Uso:
    python scripts/seed_sistema_juego.py
"""
import os, sys, sqlite3
from pathlib import Path
from datetime import datetime

BASE_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings_local'

import django
django.setup()

from django.db import connection
NOW = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
TODAY = datetime.now().strftime('%Y-%m-%d')
DB_PATH = connection.settings_dict['NAME']

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
conn.execute("PRAGMA foreign_keys = OFF")

SEP = "=" * 60

def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)

def ok(msg):   print(f"  [OK] {msg}")
def skip(msg): print(f"  [--] Ya existe: {msg}")
def warn(msg): print(f"  [!!] {msg}")

# ─── 1. Theme ──────────────────────────────────────────────────────────────────
section("1. Theme")

cur.execute("SELECT id, name FROM admin_themes_theme LIMIT 1")
row = cur.fetchone()
if row:
    theme_id = row[0]
    skip(f"Theme id={theme_id} '{row[1]}'")
else:
    cur.execute("""
        INSERT INTO admin_themes_theme
            (name, codename, description, template_dir, static_url, media_url, created_at, updated_at)
        VALUES (?,?,?,?,?,?,?,?)
    """, ('Tema Prueba', 'theme_default', 'Tema predeterminado',
          'templates/', '/static/', '/media/', NOW, NOW))
    conn.commit()
    theme_id = cur.lastrowid
    ok(f"Theme creado id={theme_id}")


# ─── 2. Verificar jerarquia comercial ─────────────────────────────────────────
section("2. Verificando jerarquia comercial")

cur.execute("SELECT id, nombre FROM admin_comercializacion_operadoras LIMIT 1")
r = cur.fetchone()
if not r:
    warn("No hay Operadoras -- ejecuta insertar_datos_prueba.py primero")
    conn.close(); exit(1)
op_id, op_nombre = r
ok(f"Operadora: id={op_id} '{op_nombre}'")

cur.execute("SELECT id FROM admin_comercializacion_bloques LIMIT 1")
bl_id = cur.fetchone()[0]
cur.execute("SELECT id FROM admin_comercializacion_bancas LIMIT 1")
banca_id = cur.fetchone()[0]
cur.execute("SELECT id FROM admin_comercializacion_distribuidores LIMIT 1")
dist_id = cur.fetchone()[0]
cur.execute("SELECT id FROM admin_comercializacion_agencias LIMIT 1")
ag_id = cur.fetchone()[0]
cur.execute("SELECT id, serial FROM admin_comercializacion_taquillas ORDER BY id")
taquillas = cur.fetchall()
ok(f"Taquillas: {[t[1] for t in taquillas]}")


# ─── 3. Comercializadoras por taquilla ────────────────────────────────────────
section("3. Comercializadoras (una por taquilla)")

comer_ids = []
for tq_id, tq_serial in taquillas:
    cur.execute("SELECT id FROM admin_finanzas_comercializadora WHERE taquilla_id=?", (tq_id,))
    existing = cur.fetchone()
    if existing:
        skip(f"Comercializadora para taquilla '{tq_serial}'")
        comer_ids.append(existing[0])
        continue

    # Calcular el proximo id para usarlo como self-reference desde el inicio
    cur.execute("SELECT COALESCE(MAX(id),0)+1 FROM admin_finanzas_comercializadora")
    next_id = cur.fetchone()[0]

    cur.execute("""
        INSERT INTO admin_finanzas_comercializadora
            (id, operadora_id, bloque_id, banca_id, distribuidor_id, agencia_id,
             taquilla_id, saldo_inicial, saldo_fecha, resumen_personalizado,
             resumen_personalizado_comer_id, created_at, updated_at)
        VALUES (?,?,?,?,?,?,  ?,0.00,?,0,  ?,?,?)
    """, (next_id, op_id, bl_id, banca_id, dist_id, ag_id,
          tq_id, TODAY, next_id, NOW, NOW))
    conn.commit()
    comer_ids.append(next_id)
    ok(f"Comercializadora id={next_id} creada para taquilla '{tq_serial}'")

ok(f"Total comercializadoras: {len(comer_ids)} ids={comer_ids}")


# ─── 4. SistemaJuego ──────────────────────────────────────────────────────────
section("4. SistemaJuego")

cur.execute("SELECT id, nombre FROM admin_juego_sistemajuego LIMIT 1")
row = cur.fetchone()
if row:
    sj_id = row[0]
    skip(f"SistemaJuego id={sj_id} '{row[1]}'")
else:
    # Usar la primera comercializadora como referencia para comercializadora_id y company_id
    comer_ref = comer_ids[0] if comer_ids else None
    if not comer_ref:
        warn("No hay comercializadoras para vincular al SistemaJuego")
        conn.close(); exit(1)

    cur.execute("""
        INSERT INTO admin_juego_sistemajuego
            (nombre, logo, banner, comercializadora_id, is_resultados, is_logros,
             notificacion_automatica, theme_id, company_id, created_at, updated_at)
        VALUES (?,NULL,NULL,?,1,0,
                0,?,?,?,?)
    """, ('Sistema Asterisco *7', comer_ref, theme_id, comer_ref, NOW, NOW))
    conn.commit()
    sj_id = cur.lastrowid
    ok(f"SistemaJuego creado id={sj_id}")


# ─── 5. Resumen Final ─────────────────────────────────────────────────────────
section("RESUMEN FINAL")

tablas = [
    ('admin_themes_theme',                  'Themes'),
    ('admin_finanzas_comercializadora',     'Comercializadoras'),
    ('admin_juego_sistemajuego',            'SistemasJuego'),
    ('admin_status_status',                'Status'),
    ('admin_comercializacion_operadoras',  'Operadoras'),
    ('admin_comercializacion_bloques',     'Multi Bancas'),
    ('admin_comercializacion_bancas',      'Bancas'),
    ('admin_comercializacion_distribuidores','Distribuidores'),
    ('admin_comercializacion_agencias',    'Agencias'),
    ('admin_comercializacion_taquillas',   'Taquillas'),
]

for tabla, label in tablas:
    cur.execute(f"SELECT COUNT(*) FROM {tabla}")
    cnt = cur.fetchone()[0]
    marca = "[OK]" if cnt > 0 else "[!!]"
    print(f"  {marca}  {label:<25} {cnt:>5}")

conn.close()

print()
print("  Recarga el dashboard en: http://127.0.0.1:8000/dashboard/")
print(SEP)
