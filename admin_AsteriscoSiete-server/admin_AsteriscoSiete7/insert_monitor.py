# -*- coding: utf-8 -*-
"""Insert monitor_api view into dashboard_views.py"""

fpath = 'admin_asterisco7/dashboard_views.py'
content = open(fpath, 'r', encoding='utf-8').read()

monitor_view = r'''
@staff_member_required(login_url='/admin/login/')
def monitor_api(request):
    """Monitor de Conexiones en Tiempo Real — API JSON."""
    from django.utils.timezone import now as tz_now
    from django.apps import apps
    from datetime import timedelta

    try:
        HechoConn   = apps.get_model('admin_historic', 'HechoConnectionsComer')
        TaqSessions = apps.get_model('admin_historic', 'TaquillaSessions')
        Taquillas   = apps.get_model('admin_comercializacion', 'Taquillas')
        Agencias    = apps.get_model('admin_comercializacion', 'Agencias')
    except LookupError as e:
        return JsonResponse({'error': str(e)}, status=500)

    ahora           = tz_now()
    limite_online   = ahora - timedelta(minutes=5)
    limite_reciente = ahora - timedelta(minutes=30)

    # IP activa por usuario (sesion abierta, enddate=None)
    sesiones_activas = {}
    try:
        for s in TaqSessions.objects.filter(enddate=None).order_by('-created_at')[:500]:
            if s.user_id not in sesiones_activas:
                sesiones_activas[s.user_id] = str(s.ip)
    except Exception:
        pass

    rows = []
    try:
        for c in HechoConn.objects.all().order_by('-connection_at')[:500]:
            taquilla_nombre = 'Taquilla #' + str(c.taquilla_id)
            agencia_nombre  = 'Agencia #'  + str(c.agencia_id)
            try:
                taq = Taquillas.objects.get(pk=c.taquilla_id)
                taquilla_nombre = taq.taquilla
            except Exception:
                pass
            try:
                ag = Agencias.objects.get(pk=c.agencia_id)
                agencia_nombre = ag.nombre
            except Exception:
                pass

            ip_activa = 'N/D'
            try:
                from admin_comercializacion.models import UsuariosTaquilla
                usr = UsuariosTaquilla.objects.filter(taquilla_id=c.taquilla_id).first()
                if usr:
                    ip_activa = sesiones_activas.get(usr.pk, 'N/D')
            except Exception:
                pass

            conn_at = c.connection_at
            if conn_at >= limite_online:
                estado = 'online'
            elif conn_at >= limite_reciente:
                estado = 'reciente'
            else:
                estado = 'offline'

            diff = ahora - conn_at
            mins = int(diff.total_seconds() // 60)
            if mins < 60:
                tiempo_str = str(mins) + ' min'
            elif mins < 1440:
                tiempo_str = str(mins // 60) + 'h ' + str(mins % 60) + 'm'
            else:
                tiempo_str = str(mins // 1440) + 'd'

            rows.append({
                'taquilla_id': c.taquilla_id,
                'agencia_id':  c.agencia_id,
                'taquilla':    taquilla_nombre,
                'agencia':     agencia_nombre,
                'connection_at': conn_at.strftime('%d/%m/%Y %H:%M:%S'),
                'hace':        tiempo_str,
                'ip':          ip_activa,
                'estado':      estado,
            })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

    return JsonResponse({'total': len(rows), 'rows': rows},
                        json_dumps_params={'ensure_ascii': False})


'''

# Find insertion point: after the candidatos_page function, before dashboard_stats
MARKER = "@staff_member_required(login_url='/admin/login/')\ndef dashboard_stats"

if 'def monitor_api' in content:
    print('monitor_api already present, skipping.')
elif MARKER in content:
    content = content.replace(MARKER, monitor_view + MARKER, 1)
    open(fpath, 'w', encoding='utf-8').write(content)
    print('OK — monitor_api inserted successfully.')
else:
    print('MARKER NOT FOUND. Searching for context...')
    idx = content.find('def dashboard_stats')
    print(repr(content[max(0,idx-100):idx+50]))
