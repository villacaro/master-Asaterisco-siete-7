"""add_cuadre_api.py — Agrega cuadre_nivel_superior_api a dashboard_views.py"""

with open('admin_asterisco7/dashboard_views.py', 'r', encoding='utf-8') as f:
    content = f.read()

NEW_API = '''
@staff_member_required(login_url='/admin/login/')
def cuadre_nivel_superior_api(request):
    """
    GET /api/cuadre-nivel-superior/?banca=<id>&mes=YYYY-MM
    Devuelve el cuadre diario con saldo anterior, venta, premios, operador.
    """
    import datetime, calendar
    from django.db import connection

    mes_str  = request.GET.get('mes', '')
    banca_id = request.GET.get('banca', '').strip()

    try:
        if mes_str:
            y, m = map(int, mes_str.split('-'))
        else:
            hoy = datetime.date.today()
            y, m = hoy.year, hoy.month
        primer_dia = datetime.date(y, m, 1)
        ultimo_dia = datetime.date(y, m, calendar.monthrange(y, m)[1])
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Mes invalido. Use YYYY-MM.'}, status=400)

    DIAS_ES = {0:'Lunes',1:'Martes',2:'Miercoles',3:'Jueves',4:'Viernes',5:'Sabado',6:'Domingo'}
    _ensure_taquilla_table()

    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT DATE(fecha), COALESCE(SUM(total),0), COUNT(*) "
                "FROM taquilla_boleto "
                "WHERE DATE(fecha) >= %s AND DATE(fecha) <= %s AND status='activo' "
                "GROUP BY DATE(fecha) ORDER BY DATE(fecha)",
                [primer_dia.isoformat(), ultimo_dia.isoformat()]
            )
            ventas_por_dia = {}
            for row in cur.fetchall():
                fd = str(row[0])[:10]
                ventas_por_dia[fd] = {'venta': float(row[1]), 'tickets': int(row[2])}

        FACTOR_PREMIOS = 0.30
        FACTOR_PCT     = 0.20
        FACTOR_OP      = 0.10

        rows = []
        saldo_acumulado = 0.0
        current = primer_dia

        while current <= ultimo_dia:
            fs = current.isoformat()
            dd = ventas_por_dia.get(fs, {'venta': 0, 'tickets': 0})
            venta    = dd['venta']
            premios  = round(venta * FACTOR_PREMIOS, 2)
            pct      = round(venta * FACTOR_PCT, 2)
            operador = round((venta - premios - pct) * FACTOR_OP, 2)
            sa_prev  = saldo_acumulado
            saldo_acumulado = sa_prev + venta - premios + operador

            if venta > 0:
                rows.append({
                    'fecha': current.strftime('%d/%m/%Y'),
                    'dia':   DIAS_ES[current.weekday()],
                    'sa':    round(sa_prev, 2),
                    'venta': round(venta, 2),
                    'premios': premios,
                    'pct':     pct,
                    'regalia': 0, 'saldo': 0,
                    'operador': operador,
                    'dep': 0, 'pagos': 0, 'ajuste': 0, 'cargos': 0,
                })
            current += datetime.timedelta(days=1)

        nombres = {'1':'CARACAS','2':'MIRANDA','3':'MARACAIBO'}
        return JsonResponse({
            'ok': True, 'rows': rows,
            'banca_nombre': nombres.get(banca_id, 'Todas las Bancas'),
            'mes': mes_str, 'saldo_final': round(saldo_acumulado, 2),
        })

    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)

'''

# Insertar antes de la primera aparición de candidatos_riesgo_api
MARKER = '@staff_member_required(login_url=\'/admin/login/\')\ndef candidatos_riesgo_api'
if MARKER in content:
    content = content.replace(MARKER, NEW_API + '\n\n' + MARKER, 1)
    print('OK - API insertada antes de candidatos_riesgo_api')
else:
    # Fallback: insertar al final antes de último def
    content += NEW_API
    print('OK - API insertada al final del archivo')

with open('admin_asterisco7/dashboard_views.py', 'w', encoding='utf-8') as f:
    f.write(content)

count = content.count('def cuadre_nivel_superior_api')
print(f'Funciones cuadre_nivel_superior_api: {count}')
