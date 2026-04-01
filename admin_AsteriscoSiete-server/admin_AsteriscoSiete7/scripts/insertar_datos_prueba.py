"""
Script: insertar_datos_prueba.py
Inserta datos de prueba directamente via SQL para la jerarquía comercial.
Evita el sistema de auditoría (Redis) usando monkey-patch.
"""
import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')
django.setup()

# ─── Monkey-patch: Deshabilitar auditoría Redis y Comercializadora auto-save ─
import admin_historic.auditoria as _aud
_aud.save_audit = lambda *a, **kw: None
print("  ✅  save_audit deshabilitado para este script")

# Mock de Redis para que no falle
class _RedisMock:
    def get(self, *a, **kw): return None
    def set(self, *a, **kw): return None
    def delete(self, *a, **kw): return None
_aud.REDIS_DB = _RedisMock()

# Deshabilitar la creación automática de Comercializadora en save()
try:
    from admin_finanzas import models as _fin_models
    _orig_com_save = _fin_models.Comercializadora.save
    def _noop_com_save(self, *a, **kw): pass
    _fin_models.Comercializadora.save = _noop_com_save
    print("  ✅  Comercializadora.save deshabilitado para este script")
except Exception as _e:
    print(f"  ℹ️   No se deshabilitó Comercializadora: {_e}")

# También parchear el BaseModelCadena.save para saltarse el sync de finanzas
try:
    from admin_comercializacion.models import BaseModelCadena
    _orig_cadena_save = BaseModelCadena.save
    def _safe_cadena_save(self, *a, **kw):
        # Llamar solo al save de Django, sin el sync de finanzas
        from django.db.models import Model
        Model.save(self, *a, **kw)
    BaseModelCadena.save = _safe_cadena_save
    print("  ✅  BaseModelCadena.save simplificado para este script")
except Exception as _e:
    print(f"  ℹ️   No se pudo parchear BaseModelCadena: {_e}")

from django.db import connection, transaction
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

SEP = "─" * 60
print(SEP)
print("  ASTERISCO *7 — Inserción de Datos de Prueba")
print(SEP)

# ─── 0. Verificar/crear Status via SQL directo ──────────────────────────────
print("\n[0] Verificando Status en base de datos...")
import sqlite3 as _sqlite3
from datetime import datetime as _dt

db_path = connection.settings_dict['NAME']
_now = _dt.now().strftime('%Y-%m-%d %H:%M:%S')
ct = ContentType.objects.first()

_conn = _sqlite3.connect(db_path)
_cur = _conn.cursor()
_cur.execute("SELECT COUNT(*) FROM admin_status_status")
cnt = _cur.fetchone()[0]
print(f"  Status existentes: {cnt}")

if cnt == 0:
    _cur.execute(
        "INSERT INTO admin_status_status (name, codename, content_type, [order], created_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        ('Activo', 'activo', ct.pk, 1, _now, _now)
    )
    _conn.commit()
    status_id = _cur.lastrowid
    print(f"  ✅  Status 'Activo' creado: id={status_id}")
else:
    _cur.execute("SELECT id, name FROM admin_status_status LIMIT 1")
    row = _cur.fetchone()
    status_id = row[0]
    print(f"  ✅  Status existente: id={status_id}, name={row[1]}")

_conn.close()


# ─── Cargar modelos ──────────────────────────────────────────────────────────
Status       = apps.get_model('admin_status', 'Status')
Direcciones  = apps.get_model('admin_profiles', 'Direcciones')
Operadoras   = apps.get_model('admin_comercializacion', 'Operadoras')
Bloques      = apps.get_model('admin_comercializacion', 'Bloques')
Bancas       = apps.get_model('admin_comercializacion', 'Bancas')
Distribuidores = apps.get_model('admin_comercializacion', 'Distribuidores')
Agencias     = apps.get_model('admin_comercializacion', 'Agencias')
Taquillas    = apps.get_model('admin_comercializacion', 'Taquillas')
UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')

status_obj = Status.objects.get(pk=status_id)

def ok(msg): print(f"  ✅  {msg}")
def info(msg): print(f"  ℹ️   {msg}")

# Helper status
def S(d):
    d['status'] = status_obj
    return d

# ─── 1. Dirección ────────────────────────────────────────────────────────────
print("\n[1/7] Dirección de prueba...")
dir_fields = [f.name for f in Direcciones._meta.concrete_fields]
dir_prueba = Direcciones.objects.first()
if dir_prueba is None:
    kwargs = {}
    if 'direccion' in dir_fields: kwargs['direccion'] = 'Av. Principal 123'
    if 'ciudad'    in dir_fields: kwargs['ciudad']    = 'Caracas'
    if 'pais'      in dir_fields: kwargs['pais']      = 'Venezuela'
    if 'estado'    in dir_fields: kwargs['estado']    = 'Distrito Capital'
    dir_prueba = Direcciones.objects.create(**kwargs)
    ok(f"Dirección creada: pk={dir_prueba.pk}")
else:
    ok(f"Dirección existente: pk={dir_prueba.pk}")

# ─── 2. Operadora ────────────────────────────────────────────────────────────
print("\n[2/7] Operadora PRUEBA...")
op, cre = Operadoras.objects.get_or_create(
    nombre='OPERADORA PRUEBA',
    defaults=S({
        'telefono': '0414-0000001', 'rif': 'J-00000001-1',
        'email': 'operadora@prueba.test', 'direccion': dir_prueba,
        'resumen_automatic': True, 'pk_clone': 0,
    })
)
ok(f"Operadora {'creada' if cre else 'ya existe'}: pk={op.pk} → {op.nombre}")

# ─── 3. Bloque (Multi Banca) ─────────────────────────────────────────────────
print("\n[3/7] Multi Banca PRUEBA...")
bl, cre = Bloques.objects.get_or_create(
    nombre='MULTI BANCA PRUEBA',
    defaults=S({
        'telefono': '0414-0000002', 'rif': 'J-00000002-2',
        'email': 'multibanca@prueba.test', 'direccion': dir_prueba,
        'resumen_automatic': True, 'pk_clone': 0, 'operadora': op,
        'is_sistema_juego': True, 'is_logros': False,
        'is_resultados': True, 'permissions_create_user': True, 'tipo': False,
    })
)
ok(f"Multi Banca {'creada' if cre else 'ya existe'}: pk={bl.pk} → {bl.nombre}")

# ─── 4. Banca ────────────────────────────────────────────────────────────────
print("\n[4/7] Banca PRUEBA...")
banca, cre = Bancas.objects.get_or_create(
    nombre='BANCA PRUEBA',
    defaults=S({
        'telefono': '0414-0000003', 'rif': 'J-00000003-3',
        'email': 'banca@prueba.test', 'direccion': dir_prueba,
        'resumen_automatic': True, 'pk_clone': 0, 'bloque': bl,
        'is_sistema_juego': True, 'is_logros': False,
        'is_resultados': True, 'permissions_create_user': True, 'modelo_negocio': 1,
    })
)
ok(f"Banca {'creada' if cre else 'ya existe'}: pk={banca.pk} → {banca.nombre}")

# ─── 5. Distribuidor ─────────────────────────────────────────────────────────
print("\n[5/7] Distribuidor DIST PRUEBA...")
dist, cre = Distribuidores.objects.get_or_create(
    nombre='DIST PRUEBA',
    defaults=S({
        'telefono': '0414-0000004', 'rif': 'J-00000004-4',
        'email': 'dist@prueba.test', 'direccion': dir_prueba,
        'resumen_automatic': True, 'pk_clone': 0, 'banca': banca,
    })
)
ok(f"Distribuidor {'creado' if cre else 'ya existe'}: pk={dist.pk} → {dist.nombre}")

# ─── 6. Agencia ──────────────────────────────────────────────────────────────
print("\n[6/7] Agencia PRUEBA...")
ag_defaults = S({
    'telefono': '0414-0000005', 'rif': 'J-00000005-5',
    'email': 'agencia@prueba.test', 'direccion': dir_prueba,
    'resumen_automatic': True, 'pk_clone': 0, 'distribuidores': dist,
    'num_taquillas': 3, 'codigo': 'AGP001',
    'montomin': 1.00, 'montomax': 10000.00,
    'montomax_ganancia': 50000.00,
    'cantidad_apuesta_max': 100, 'cantidad_apuesta_min': 1,
    'tiempoexpiracion': 30,
    'parley_machos_max': 10, 'parley_machos_min': 1,
    'parley_hembras_max': 10, 'parley_hembras_min': 1,
    'parley_empates_max': 5,
    'parley_clonados_maxima_ganancia': 50000.00,
    'monto_alquiler': 0.00, 'frecuencia_monto_alquiler': 'mensual',
    'factor_riesgo': 1, 'frecuencia_queda': 'diario',
    'ticket_titulo': 'ASTERISCO *7',
    'ticket_pie': 'Gracias por su preferencia.',
})
agencia, cre = Agencias.objects.get_or_create(nombre='AGENCIA PRUEBA', defaults=ag_defaults)
ok(f"Agencia {'creada' if cre else 'ya existe'}: pk={agencia.pk} → {agencia.nombre}")

# ─── 7. Taquillas + Usuario ──────────────────────────────────────────────────
print("\n[7/7] Taquillas y Usuario de prueba...")
for i in range(1, 4):
    serial = f'TQ-PRUEBA-{i:03d}'
    tq, cre = Taquillas.objects.get_or_create(
        serial=serial,
        defaults={
            'taquilla': f'TAQUILLA-{i:03d}', 'agencia': agencia,
            'monto_alquiler': 0.00, 'modo_alquiler': False,
            'is_taquilla_master': (i == 1), 'pk_clone': 0,
        }
    )
    ok(f"Taquilla {'creada' if cre else 'ya existe'}: {tq.taquilla} (serial={tq.serial})")

    if i == 1:
        ut, cre_ut = UsuariosTaquilla.objects.get_or_create(
            user='usuario_prueba',
            defaults=S({
                'nombre': 'Usuario de Prueba', 'taquilla': tq,
                'password': 'pbkdf2_sha256$600000$salt$hash',
                'pub_key_client': '', 'pub_key': '', 'priv_key': '', 'pk_clone': 0,
            })
        )
        ok(f"Usuario {'creado' if cre_ut else 'ya existe'}: {ut.user} → {tq.taquilla}")

# ─── Resumen ─────────────────────────────────────────────────────────────────
print()
print(SEP)
print("  RESUMEN FINAL")
print(SEP)
print(f"  Operadoras:    {Operadoras.objects.count()}")
print(f"  Multi Bancas:  {Bloques.objects.count()}")
print(f"  Bancas:        {Bancas.objects.count()}")
print(f"  Distribuidores:{Distribuidores.objects.count()}")
print(f"  Agencias:      {Agencias.objects.count()}")
print(f"  Taquillas:     {Taquillas.objects.count()}")
print(f"  Usuarios Taq:  {UsuariosTaquilla.objects.count()}")
print(SEP)
print("  Recarga el dashboard para ver los KPIs actualizados.")
print(SEP)
