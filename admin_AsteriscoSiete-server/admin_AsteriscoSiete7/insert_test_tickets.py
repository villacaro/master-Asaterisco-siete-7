"""
Script de prueba: Inserta tickets de muestra para el reporte Cuadre.
"""
from django.db import connection

cursor = connection.cursor()

# Limpiar tickets de prueba anteriores
cursor.execute("DELETE FROM admin_juego_ticket WHERE serie LIKE 'TST%'")

hoy   = '2026-03-30 10:00:00'
ayer  = '2026-03-29 10:00:00'
antes = '2026-03-28 10:00:00'

sql = (
    "INSERT INTO admin_juego_ticket "
    "(serie, sorteo_id, fecha_emision, total, anulado, tserial_ifa, id_agencia, id_taquilla, producto_id, vendedor_id) "
    "VALUES (%s, %s, %s, %s, 0, '', %s, %s, %s, NULL)"
)

rows = [
  ('TST001', 1, hoy,    85000,  1, 1, 1),
  ('TST002', 1, hoy,   120000,  1, 1, 1),
  ('TST003', 2, hoy,    63500,  1, 2, 8),
  ('TST004', 2, hoy,    97200,  1, 2, 8),
  ('TST005', 3, hoy,    45000,  1, 3, 1),
  ('TST006', 1, ayer,  110000,  1, 1, 1),
  ('TST007', 1, ayer,   78000,  1, 2, 8),
  ('TST008', 2, ayer,   53000,  1, 3, 1),
  ('TST009', 3, ayer,   92000,  1, 1, 1),
  ('TST010', 1, antes,  67000,  1, 2, 8),
  ('TST011', 2, antes,  48500,  1, 3, 1),
  ('TST012', 3, antes, 130000,  1, 1, 1),
]

for r in rows:
    cursor.execute(sql, list(r))

connection.commit()

from admin_juego.models_arrejuntao import Ticket
from django.db.models import Sum
cnt = Ticket.objects.count()
venta = Ticket.objects.filter(fecha_emision__date='2026-03-30').aggregate(t=Sum('total'))['t']
print("Tickets en DB:", cnt)
print("Venta hoy 30/03:", venta)
print("OK - ahora prueba el reporte Cuadre (28/03 - 30/03)")
