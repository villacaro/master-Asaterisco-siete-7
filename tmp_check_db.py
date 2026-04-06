import sys, os, django

sys.path.insert(0, r'c:\Users\villa\OneDrive\Documentos\sistema Parley\proyecto master Asterisco Siete (7)\admin_AsteriscoSiete-server\admin_AsteriscoSiete7')
os.environ['DJANGO_SETTINGS_MODULE'] = 'admin_asterisco7.settings_local'
django.setup()

from django.db import connection
print('DB vendor:', connection.vendor)
print('DB name:', connection.settings_dict.get('NAME', 'N/A'))

try:
    with connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM taquilla_boleto")
        row = cur.fetchone()
        print('taquilla_boleto row count:', row[0])

        cur.execute("SELECT ticket_id, usuario, taquilla, DATE(fecha)::text, total FROM taquilla_boleto ORDER BY fecha DESC LIMIT 5")
        rows = cur.fetchall()
        print('Last 5 tickets:')
        for r in rows:
            print(' ', r)
except Exception as e:
    print('Error:', e)
    # Try creating the table
    from admin_asterisco7.dashboard_views import _ensure_taquilla_table
    _ensure_taquilla_table()
    print('Table ensured. Checking again...')
    with connection.cursor() as cur:
        cur.execute("SELECT COUNT(*) FROM taquilla_boleto")
        print('Count:', cur.fetchone()[0])
