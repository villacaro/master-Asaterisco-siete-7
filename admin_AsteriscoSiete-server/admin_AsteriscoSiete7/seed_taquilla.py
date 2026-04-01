"""
seed_taquilla.py  — Inserta tickets de prueba en taquilla_boleto
Ejecutar: python manage.py shell < seed_taquilla.py
"""
import json, datetime, os, sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings_local')
django.setup()

from django.db import connection
from admin_asterisco7.dashboard_views import _ensure_taquilla_table

_ensure_taquilla_table()
print("Tabla OK")

tickets = [
    {
        'ticket_id': 'TQ-20260331-001',
        'usuario': 'admin',
        'taquilla': 'Taquilla Central',
        'items': [
            {'lottery':'triple_maracaibo','number':'172','amount':15,'bet_type':'triple'},
            {'lottery':'triple_maracaibo','number':'280','amount':10,'bet_type':'triple'},
            {'lottery':'triple_maracaibo','number':'540','amount':20,'bet_type':'triple'},
        ],
        'total': 45.0,
    },
    {
        'ticket_id': 'TQ-20260331-002',
        'usuario': 'cajero01',
        'taquilla': 'Taquilla Norte',
        'items': [
            {'lottery':'triple_tachira','number':'900','amount':20,'bet_type':'triple'},
            {'lottery':'triple_tachira','number':'481','amount':10,'bet_type':'triple'},
            {'lottery':'terminal','number':'72','amount':15,'bet_type':'terminal'},
        ],
        'total': 45.0,
    },
    {
        'ticket_id': 'TQ-20260331-003',
        'usuario': 'cajero02',
        'taquilla': 'Taquilla Sur',
        'items': [
            {'lottery':'animalito','number':'06','amount':30,'bet_type':'animalito'},
            {'lottery':'animalito','number':'12','amount':25,'bet_type':'animalito'},
        ],
        'total': 55.0,
    },
    {
        'ticket_id': 'TQ-20260331-004',
        'usuario': 'cajero01',
        'taquilla': 'Taquilla Central',
        'items': [
            {'lottery':'triple_zulia','number':'172','amount':15,'bet_type':'triple'},
            {'lottery':'triple_zulia','number':'900','amount':30,'bet_type':'triple'},
            {'lottery':'terminal','number':'00','amount':10,'bet_type':'terminal'},
        ],
        'total': 55.0,
    },
    {
        'ticket_id': 'TQ-20260331-005',
        'usuario': 'admin',
        'taquilla': 'Taquilla Norte',
        'items': [
            {'lottery':'triple_maracaibo','number':'727','amount':25,'bet_type':'triple'},
            {'lottery':'triple_maracaibo','number':'687','amount':20,'bet_type':'triple'},
        ],
        'total': 45.0,
    },
    {
        'ticket_id': 'TQ-20260331-006',
        'usuario': 'cajero03',
        'taquilla': 'Taquilla Este',
        'items': [
            {'lottery':'triple_tachira','number':'172','amount':10,'bet_type':'triple'},
            {'lottery':'triple_tachira','number':'508','amount':15,'bet_type':'triple'},
            {'lottery':'arrimao','number':'35','amount':20,'bet_type':'arrimao'},
        ],
        'total': 45.0,
    },
    {
        'ticket_id': 'TQ-20260331-007',
        'usuario': 'cajero02',
        'taquilla': 'Taquilla Sur',
        'items': [
            {'lottery':'triple_maracaibo','number':'900','amount':50,'bet_type':'triple'},
            {'lottery':'triple_maracaibo','number':'172','amount':25,'bet_type':'triple'},
        ],
        'total': 75.0,
    },
    {
        'ticket_id': 'TQ-20260331-008',
        'usuario': 'admin',
        'taquilla': 'Taquilla Central',
        'items': [
            {'lottery':'terminal','number':'72','amount':20,'bet_type':'terminal'},
            {'lottery':'terminal','number':'15','amount':15,'bet_type':'terminal'},
            {'lottery':'animalito','number':'06','amount':10,'bet_type':'animalito'},
        ],
        'total': 45.0,
    },
]

hoy = datetime.datetime.now().isoformat()
vendor = connection.vendor
placeholder = '?' if vendor == 'sqlite' else '%s'
ph = f'({placeholder},{placeholder},{placeholder},{placeholder},{placeholder},{placeholder},{placeholder})'

inserted = 0
for t in tickets:
    try:
        with connection.cursor() as cur:
            cur.execute(
                f"INSERT INTO taquilla_boleto (ticket_id,usuario,taquilla,fecha,items_json,total,status) VALUES {ph}",
                [t['ticket_id'], t['usuario'], t['taquilla'], hoy,
                 json.dumps(t['items'], ensure_ascii=False), t['total'], 'activo']
            )
        inserted += 1
    except Exception as ex:
        print(f"  Skip {t['ticket_id']}: {ex}")

print(f"Insertados: {inserted}")
with connection.cursor() as cur:
    cur.execute("SELECT COUNT(*) FROM taquilla_boleto")
    print(f"Total en BD: {cur.fetchone()[0]}")
    cur.execute("SELECT COALESCE(SUM(total),0) FROM taquilla_boleto WHERE status='activo'")
    print(f"Venta total: Bs.{cur.fetchone()[0]}")
