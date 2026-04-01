import django, os, sys
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'admin_asterisco7.settings')
sys.path.insert(0, '.')
django.setup()

from django.db import connection
from admin_asterisco7.dashboard_views import _ensure_taquilla_table

_ensure_taquilla_table()
with connection.cursor() as c:
    c.execute("SELECT COUNT(*) FROM taquilla_boleto")
    print("FILAS EN taquilla_boleto:", c.fetchone()[0])
    c.execute("SELECT ticket_id, usuario, total, fecha FROM taquilla_boleto ORDER BY fecha DESC LIMIT 5")
    rows = c.fetchall()
    if rows:
        for r in rows:
            print(r)
    else:
        print("Tabla vacia - nunca se guardo un ticket")
