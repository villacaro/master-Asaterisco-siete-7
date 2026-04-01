"""
Script: crear_datos_prueba.py
Crea toda la jerarquía de datos de prueba para Asterisco *7:
    Operadora PRUEBA
      └── Bloque/Multi-Banca PRUEBA
              └── Banca PRUEBA
                      └── Distribuidor DIST PRUEBA
                              └── Agencia PRUEBA
                                      ├── TAQUILLA-001
                                      ├── TAQUILLA-002
                                      └── TAQUILLA-003
                                              └── usuario_prueba (UsuariosTaquilla)

Uso:
    python manage.py shell < scripts/crear_datos_prueba.py
    ó:
    $env:DJANGO_SETTINGS_MODULE="admin_asterisco7.settings_local"; python manage.py shell --no-input -c "$(Get-Content scripts\crear_datos_prueba.py -Raw)"
"""
import os, sys, django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')
django.setup()

from django.apps import apps
from django.db.models.signals import post_save, pre_save

# ─── Desconectar señales de auditoría para evitar error de Redis en local ──────
try:
    from admin_historic import auditoria as _audit
    # Desconectar señales registradas por el módulo de auditoría
    post_save.disconnect(dispatch_uid='audit_post_save')
    pre_save.disconnect(dispatch_uid='audit_pre_save')
    print("  ℹ️   Señales de auditoría desconectadas (Redis no requerido).")
except Exception as _e:
    print(f"  ℹ️   No se pudieron desconectar señales ({_e}), continuando...")

# ─── Modelos ───────────────────────────────────────────────────────────────────
Direcciones = apps.get_model('admin_profiles','Direcciones')
Operadoras  = apps.get_model('admin_comercializacion','Operadoras')
Bloques     = apps.get_model('admin_comercializacion','Bloques')
Bancas      = apps.get_model('admin_comercializacion','Bancas')
Distribuidores = apps.get_model('admin_comercializacion','Distribuidores')
Agencias    = apps.get_model('admin_comercializacion','Agencias')
Taquillas   = apps.get_model('admin_comercializacion','Taquillas')
UsuariosTaquilla = apps.get_model('admin_comercializacion','UsuariosTaquilla')

SEP = "─" * 60

def ok(msg): print(f"  ✅  {msg}")
def info(msg): print(f"  ℹ️   {msg}")

print(SEP)
print("  ASTERISCO *7 — Creación de Datos de Prueba")
print(SEP)

# ─── 1. Status ─────────────────────────────────────────────────────────────────
print("\n[1/8] Status…")
Status      = apps.get_model('admin_status',  'Status')
status_fields = [f.name for f in Status._meta.concrete_fields]
required_fields = [f.name for f in Status._meta.concrete_fields if not f.null and not f.blank and f.name != 'id' and not f.has_default()]
print(f"  Campos: {status_fields}")
print(f"  Requeridos: {required_fields}")
status_activo = Status.objects.first()
if status_activo is None:
    if 'content_type' in required_fields or 'content_type_id' in required_fields:
        # No podemos crear Status sin ContentType — usamos None
        print("  ⚠️  Status requiere content_type. Se usará None (FK opcionales).")
    else:
        create_kwargs = {}
        if 'nombre' in status_fields: create_kwargs['nombre'] = 'Activo'
        if 'name'   in status_fields: create_kwargs['name']   = 'Activo'
        if 'status' in status_fields: create_kwargs['status'] = 'Activo'
        try:
            status_activo = Status.objects.create(**create_kwargs)
            ok(f"Status creado: pk={status_activo.pk}")
        except Exception as exc:
            print(f"  ⚠️  No se pudo crear Status: {exc}. Se usará None.")
            status_activo = None
else:
    ok(f"Status existente encontrado: pk={status_activo.pk} → {status_activo}")


# ─── 2. Dirección ──────────────────────────────────────────────────────────────
print("\n[2/8] Dirección de prueba…")
dir_fields  = [f.name for f in Direcciones._meta.concrete_fields]
print(f"  Campos: {dir_fields}")
dir_prueba = Direcciones.objects.first()
if dir_prueba is None:
    create_kwargs = {}
    if 'direccion' in dir_fields: create_kwargs['direccion'] = 'Dirección de Prueba 123'
    if 'address'   in dir_fields: create_kwargs['address']   = 'Dirección de Prueba 123'
    if 'ciudad'    in dir_fields: create_kwargs['ciudad']    = 'Ciudad Prueba'
    if 'pais'      in dir_fields: create_kwargs['pais']      = 'Venezuela'
    dir_prueba = Direcciones.objects.create(**create_kwargs)
    ok(f"Dirección creada: pk={dir_prueba.pk}")
else:
    ok(f"Dirección existente: pk={dir_prueba.pk}")

# Helper para incluir status solo si existe
def add_status(d):
    if status_activo is not None:
        d['status'] = status_activo
    return d

# ─── 3. Operadora ──────────────────────────────────────────────────────────────
print("\n[3/8] Operadora PRUEBA…")
op, created = Operadoras.objects.get_or_create(
    nombre='OPERADORA PRUEBA',
    defaults=add_status({
        'telefono': '0414-0000001',
        'rif':      'J-00000001-1',
        'email':    'operadora@prueba.test',
        'direccion': dir_prueba,
        'resumen_automatic': True,
        'pk_clone': 0,
    })
)
ok(f"Operadora {'creada' if created else 'ya existe'}: pk={op.pk} → {op.nombre}")

# ─── 4. Bloque (Multi Banca) ───────────────────────────────────────────────────
print("\n[4/8] Bloque/Multi-Banca PRUEBA…")
bl, created = Bloques.objects.get_or_create(
    nombre='MULTI BANCA PRUEBA',
    defaults=add_status({
        'telefono': '0414-0000002',
        'rif':      'J-00000002-2',
        'email':    'multibanca@prueba.test',
        'direccion': dir_prueba,
        'resumen_automatic': True,
        'pk_clone': 0,
        'operadora': op,
        'is_sistema_juego': True,
        'is_logros': False,
        'is_resultados': True,
        'permissions_create_user': True,
        'tipo': False,
    })
)
ok(f"Bloque {'creado' if created else 'ya existe'}: pk={bl.pk} → {bl.nombre}")

# ─── 5. Banca ──────────────────────────────────────────────────────────────────
print("\n[5/8] Banca PRUEBA…")
banca, created = Bancas.objects.get_or_create(
    nombre='BANCA PRUEBA',
    defaults=add_status({
        'telefono': '0414-0000003',
        'rif':      'J-00000003-3',
        'email':    'banca@prueba.test',
        'direccion': dir_prueba,
        'resumen_automatic': True,
        'pk_clone': 0,
        'bloque': bl,
        'is_sistema_juego': True,
        'is_logros': False,
        'is_resultados': True,
        'permissions_create_user': True,
        'modelo_negocio': 1,
    })
)
ok(f"Banca {'creada' if created else 'ya existe'}: pk={banca.pk} → {banca.nombre}")

# ─── 6. Distribuidor ────────────────────────────────────────────────────────────
print("\n[6/8] Distribuidor DIST PRUEBA…")
dist, created = Distribuidores.objects.get_or_create(
    nombre='DIST PRUEBA',
    defaults=add_status({
        'telefono': '0414-0000004',
        'rif':      'J-00000004-4',
        'email':    'dist@prueba.test',
        'direccion': dir_prueba,
        'resumen_automatic': True,
        'pk_clone': 0,
        'banca': banca,
    })
)
ok(f"Distribuidor {'creado' if created else 'ya existe'}: pk={dist.pk} → {dist.nombre}")

# ─── 7. Agencia (Centro de Apuesta) ───────────────────────────────────────────
print("\n[7/8] Agencia/Centro de Apuesta PRUEBA…")
agencia, created = Agencias.objects.get_or_create(
    nombre='AGENCIA PRUEBA',
    defaults=add_status({
        'telefono': '0414-0000005',
        'rif':      'J-00000005-5',
        'email':    'agencia@prueba.test',
        'direccion': dir_prueba,
        'resumen_automatic': True,
        'pk_clone': 0,
        'distribuidores': dist,
        'num_taquillas': 3,
        'codigo': 'AGP001',
        'montomin': 1.00,
        'montomax': 10000.00,
        'montomax_ganancia': 50000.00,
        'cantidad_apuesta_max': 100,
        'cantidad_apuesta_min': 1,
        'tiempoexpiracion': 30,
        'parley_machos_max': 10,
        'parley_machos_min': 1,
        'parley_hembras_max': 10,
        'parley_hembras_min': 1,
        'parley_empates_max': 5,
        'parley_clonados_maxima_ganancia': 50000.00,
        'monto_alquiler': 0.00,
        'frecuencia_monto_alquiler': 'mensual',
        'factor_riesgo': 1,
        'frecuencia_queda': 'diario',
        'ticket_titulo': 'ASTERISCO *7',
        'ticket_pie': 'Gracias por su preferencia.',
    })
)
ok(f"Agencia {'creada' if created else 'ya existe'}: pk={agencia.pk} → {agencia.nombre}")

# ─── 8. Taquillas + Usuario ────────────────────────────────────────────────────
print("\n[8/8] Taquillas y Usuario de prueba…")
for i in range(1, 4):
    serial = f'TQ-PRUEBA-{i:03d}'
    taquilla_nombre = f'TAQUILLA-{i:03d}'
    tq, created = Taquillas.objects.get_or_create(
        serial=serial,
        defaults={
            'taquilla': taquilla_nombre,
            'agencia': agencia,
            'monto_alquiler': 0.00,
            'modo_alquiler': False,
            'is_taquilla_master': (i == 1),
            'pk_clone': 0,
        }
    )
    ok(f"Taquilla {'creada' if created else 'ya existe'}: {tq.taquilla} (serial={tq.serial})")

    # UsuariosTaquilla para la primera taquilla
    if i == 1:
        uq_fields = [f.name for f in UsuariosTaquilla._meta.concrete_fields]
        ut, created_ut = UsuariosTaquilla.objects.get_or_create(
            user='usuario_prueba',
            defaults=add_status({
                'nombre': 'Usuario de Prueba',
                'taquilla': tq,
                'password': 'pbkdf2_sha256$600000$salt$hash',  # placeholder
                'pub_key_client': '',
                'pub_key': '',
                'priv_key': '',
                'pk_clone': 0,
            })
        )
        ok(f"UsuarioTaquilla {'creado' if created_ut else 'ya existe'}: {ut.user} → taquilla={tq.taquilla}")

print()
print(SEP)
print("  RESUMEN FINAL")
print(SEP)
print(f"  Operadoras:   {Operadoras.objects.count()}")
print(f"  Bloques:      {Bloques.objects.count()}")
print(f"  Bancas:       {Bancas.objects.count()}")
print(f"  Distribuidores: {Distribuidores.objects.count()}")
print(f"  Agencias:     {Agencias.objects.count()}")
print(f"  Taquillas:    {Taquillas.objects.count()}")
print(f"  Usuarios Taq: {UsuariosTaquilla.objects.count()}")
print(SEP)
print("  ¡Datos de prueba listos! Recarga el dashboard para ver los KPIs.")
print(SEP)
