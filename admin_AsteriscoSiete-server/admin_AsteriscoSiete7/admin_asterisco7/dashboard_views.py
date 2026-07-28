# -*- coding: utf-8 -*-
"""
dashboard/views.py — Vista del Panel de Gestión Asterisco Siete (*7)
"""
import json
import os
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.clickjacking import xframe_options_sameorigin
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.db import connection as _db_connection


def _ensure_taquilla_table():
    """
    Crea la tabla taquilla_boleto compatible con SQLite y PostgreSQL.
    SQLite : INTEGER PRIMARY KEY  + CURRENT_TIMESTAMP
    Postgres: BIGSERIAL PRIMARY KEY + NOW()
    """
    from django.db import connection
    vendor = connection.vendor          # 'sqlite' | 'postgresql' | 'mysql'
    if vendor == 'sqlite':
        ddl = """
            CREATE TABLE IF NOT EXISTS taquilla_boleto (
                id          INTEGER PRIMARY KEY,
                ticket_id   TEXT,
                usuario     TEXT,
                taquilla    TEXT,
                fecha       DATETIME DEFAULT CURRENT_TIMESTAMP,
                items_json  TEXT,
                total       REAL,
                status      TEXT DEFAULT 'activo'
            )
        """
    else:
        ddl = """
            CREATE TABLE IF NOT EXISTS taquilla_boleto (
                id          BIGSERIAL PRIMARY KEY,
                ticket_id   VARCHAR(50),
                usuario     VARCHAR(100),
                taquilla    VARCHAR(100),
                fecha       TIMESTAMP DEFAULT NOW(),
                items_json  TEXT,
                total       DECIMAL(15,2),
                status      VARCHAR(20) DEFAULT 'activo'
            )
        """
    try:
        with connection.cursor() as cur:
            cur.execute(ddl)
    except Exception:
        pass



@staff_member_required(login_url='/admin/login/')
def dashboard(request):
    """Render the admin dashboard — solo personal de staff."""
    u = request.user
    initials = ''
    if u.first_name:
        initials += u.first_name[0].upper()
    if u.last_name:
        initials += u.last_name[0].upper()
    if not initials:
        initials = u.username[:2].upper()

    ctx = {
        'username':    u.username,
        'email':       u.email or '—',
        'full_name':   u.get_full_name() or u.username,
        'initials':    initials,
        'role':        'Superadmin' if u.is_superuser else ('Staff' if u.is_staff else 'Usuario'),
        'last_login':  u.last_login.strftime('%d/%m/%Y %H:%M') if u.last_login else '—',
        'date_joined': u.date_joined.strftime('%d/%m/%Y') if u.date_joined else '—',
        'user_pk':     u.pk,
    }
    return render(request, 'dashboard/index.html', ctx)


def taquilla_view(request):
    """Sirve la app Taquilla El Arrejuntao directamente desde Django.
    Accesible en: http://127.0.0.1:8000/taquilla/
    Lee el archivo HTML directamente (sin template engine) para evitar
    conflictos con {{ }} de JavaScript.
    """
    html_path = os.path.join(settings.BASE_DIR, 'admin_asterisco7', 'templates', 'taquilla', 'index.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    response = HttpResponse(content, content_type='text/html; charset=utf-8')
    # ── Sin caché: el navegador siempre pide la versión más reciente ──
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma']        = 'no-cache'
    response['Expires']       = '0'
    return response

def taquilla_app_movil_view(request):
    """Sirve la nueva version app movil de Taquilla."""
    html_path = os.path.join(settings.BASE_DIR, 'admin_asterisco7', 'templates', 'taquilla', 'taquilla_app_movil.html')
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    response = HttpResponse(content, content_type='text/html; charset=utf-8')
    response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
    response['Pragma']        = 'no-cache'
    response['Expires']       = '0'
    return response


@csrf_exempt
def taquilla_login_api(request):
    """Autenticación de usuarios de Taquilla.
    POST { user, password } → { ok, nombre } o { error }
    Registra la sesión con IP del cliente en TaquillaSessions.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        body = json.loads(request.body)
    except Exception:
        body = request.POST

    username = (body.get('user') or '').strip()
    password = (body.get('password') or '').strip()

    if not username or not password:
        return JsonResponse({'ok': False, 'error': 'Usuario y contraseña requeridos'}, status=400)

    try:
        from django.apps import apps
        from django.contrib.auth.hashers import check_password
        from django.utils.timezone import now as tz_now
        import uuid

        UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')
        TaquillaSessions = apps.get_model('admin_historic', 'TaquillaSessions')

        usuario = UsuariosTaquilla.objects.filter(user=username).first()
        if not usuario:
            return JsonResponse({'ok': False, 'error': 'Usuario no encontrado'}, status=401)

        if not check_password(password, usuario.password):
            return JsonResponse({'ok': False, 'error': 'Contraseña incorrecta'}, status=401)

        # Obtener IP del cliente
        ip = (
            request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
            or request.META.get('REMOTE_ADDR', '127.0.0.1')
        )

        # Registrar sesión en TaquillaSessions
        try:
            from admin_historic.models import UsersProcesses
            session_id = str(uuid.uuid4())
            TaquillaSessions.objects.create(
                id=session_id,
                startdate=tz_now().date(),
                enddate=None,
                user=usuario,
                ip=ip,
            )
            # Actualizar el registro en HechoConnectionsComer para el monitor
            try:
                HechoConn = apps.get_model('admin_historic', 'HechoConnectionsComer')
                hecho, _ = HechoConn.objects.get_or_create(
                    taquilla_id=usuario.taquilla_id,
                    defaults={
                        'operadora_id': 2,
                        'bloque_id': 1,
                        'banca_id': 1,
                        'distribuidor_id': 1,
                        'agencia_id': usuario.taquilla.agencia_id if usuario.taquilla else 2,
                        'connection_at': tz_now(),
                    }
                )
                hecho.connection_at = tz_now()
                hecho.save(update_fields=['connection_at'])
            except Exception:
                pass
        except Exception:
            pass  # Si la sesión falla, igual autenticamos

        return JsonResponse({
            'ok': True,
            'nombre': usuario.nombre or username,
            'taquilla': str(usuario.taquilla) if usuario.taquilla else '',
        })

    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': f'Error interno: {e}', 'trace': traceback.format_exc()}, status=500)


@csrf_exempt
@staff_member_required(login_url='/admin/login/')
def liquidaciones_sorteo_api(request):
    """
    GET  ?sorteo=N&limit=100  → lista paginada con KPIs
    POST {campos}             → crea una nueva LiquidacionSorteo
    """
    from admin_juego.models_arrejuntao import LiquidacionSorteo

    # ── POST: crear nueva liquidación ──────────────────────────────────────────
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

        _int_fields = [
            'id_sorteo','id_lista','id_tipo_lista','id_prestador_servicio',
            'id_comercializador','id_banca','id_distribuidor','id_agencia',
            'id_taquilla','id_operador',
        ]
        _dec_fields = [
            'nporcentaje_comision_com','nporcentaje_participacion_com','nporcentaje_regalia_com',
            'nporcentaje_comision_ban','nporcentaje_participacion_ban','nporcentaje_regalia_ban',
            'nporcentaje_comision_dis','nporcentaje_participacion_dis','nporcentaje_regalia_dis',
            'nporcentaje_comision_agc',
            'mmonto_venta','mmonto_venta_ganador','mmonto_premios',
            'mmonto_comision_com','mmonto_regalia_com',
            'mmonto_comision_ban','mmonto_regalia_ban',
            'mmonto_comision_dis','mmonto_regalia_dis','mmonto_comision_agc',
            'msaldo_oper','msaldo_com','msaldo_ban','msaldo_dis','msaldo_agc',
            'msaldo_bruto_com','msaldo_bruto_ban','msaldo_bruto_dis',
            'msaldo_oper_ban','msaldo_oper_dis','msaldo_oper_cm','msaldo_cm',
        ]
        kwargs = {}
        for f in _int_fields:
            try:
                kwargs[f] = int(data.get(f, 0) or 0)
            except Exception:
                return JsonResponse({'ok': False, 'error': f'Campo inválido: {f}'}, status=400)
        for f in _dec_fields:
            try:
                kwargs[f] = float(data.get(f, 0) or 0)
            except Exception:
                kwargs[f] = 0.0

        kwargs['tserial_ifa'] = str(data.get('tserial_ifa', '') or '').strip()
        if not kwargs['tserial_ifa']:
            kwargs['tserial_ifa'] = 'SIN-IFA'

        # Auto-calcular comisiones Bs si quedan en 0
        v = kwargs['mmonto_venta']
        def _calc(pct_k, monto_k):
            if not kwargs.get(monto_k):
                kwargs[monto_k] = round(v * kwargs.get(pct_k, 0) / 100, 4)
        _calc('nporcentaje_comision_com',  'mmonto_comision_com')
        _calc('nporcentaje_regalia_com',   'mmonto_regalia_com')
        _calc('nporcentaje_comision_ban',  'mmonto_comision_ban')
        _calc('nporcentaje_regalia_ban',   'mmonto_regalia_ban')
        _calc('nporcentaje_comision_dis',  'mmonto_comision_dis')
        _calc('nporcentaje_regalia_dis',   'mmonto_regalia_dis')
        _calc('nporcentaje_comision_agc',  'mmonto_comision_agc')

        try:
            obj = LiquidacionSorteo.objects.create(**kwargs)
            return JsonResponse({'ok': True, 'pk': obj.pk,
                                 'msg': f'Liquidación #{obj.pk} creada correctamente.'})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)}, status=400)

    # ── GET: listado con KPIs ──────────────────────────────────────────────────
    sorteo_id = request.GET.get('sorteo', '')
    limit = min(int(request.GET.get('limit', 50)), 200)
    try:
        qs = LiquidacionSorteo.objects.order_by('-id_sorteo')
        if sorteo_id:
            qs = qs.filter(id_sorteo=sorteo_id)
        rows = []
        total_venta = 0
        total_premios = 0
        for obj in qs[:limit]:
            util = float(obj.get_utilidad_neta())
            v = float(obj.mmonto_venta or 0)
            p = float(obj.mmonto_premios or 0)
            total_venta   += v
            total_premios += p
            rows.append({
                'pk':              obj.pk,
                'id_sorteo':       obj.id_sorteo,
                'id_banca':        obj.id_banca,
                'id_agencia':      obj.id_agencia,
                'id_taquilla':     obj.id_taquilla,
                'mmonto_venta':    round(v, 2),
                'mmonto_premios':  round(p, 2),
                'utilidad_neta':   round(util, 2),
                'pct_premios':     round(p / v * 100, 1) if v > 0 else 0,
                'tserial_ifa':     obj.tserial_ifa or '—',
                'created_at':      obj.created_at.strftime('%d/%m/%Y %H:%M') if obj.created_at else '',
            })
        return JsonResponse({
            'ok': True,
            'count':          len(rows),
            'total_venta':    round(total_venta, 2),
            'total_premios':  round(total_premios, 2),
            'total_utilidad': round(total_venta - total_premios, 2),
            'rows':           rows,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e), 'rows': []}, status=500)


@csrf_exempt
def taquilla_venta_api(request):
    """
    Recibe un ticket confirmado desde la taquilla y lo guarda en BD (Supabase).
    POST { id, items:[{lottery,number,amount,bet_type}], total, usuario, taquillaNombre }
    La autenticación es manejada por el sistema de sesión propio de la taquilla
    (sessionStorage). No requiere Firebase Bearer token.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)

    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'error': 'JSON inválido'}, status=400)

    try:
        from django.utils.timezone import now as tz_now
        from django.db import connection, transaction
        from admin_juego.models_arrejuntao import Ticket, ApuestaDetalle, Loteria, ProductoLoteria, SorteoArrejuntao
        from admin_comercializacion.models import UsuariosTaquilla

        _ensure_taquilla_table()

        items = body.get('items', [])
        total = body.get('total', 0)
        ticket_id = str(body.get('id', ''))
        usuario = body.get('usuario', 'desconocido')
        taquilla_nombre = body.get('taquillaNombre', '')

        # 1. Guardar en taquilla_boleto como respaldo rápido (el original)
        with connection.cursor() as cursor:
            cursor.execute(
                """INSERT INTO taquilla_boleto (ticket_id, usuario, taquilla, fecha, items_json, total, status)
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                [ticket_id, usuario, taquilla_nombre, tz_now(),
                 json.dumps(items, ensure_ascii=False), float(total), 'activo']
            )

        # 2. Parsear y convertir items a los modelos reales del Dashboard para reportes
        try:
            taq_user = UsuariosTaquilla.objects.select_related('taquilla').filter(user=usuario).first()
            user_id = taq_user.id if taq_user else None
            agencia_id = taq_user.taquilla.agencia_id if (taq_user and taq_user.taquilla) else None

            # Agrupar jugadas por nombre de lotería para crear los Tickets necesarios
            groups = {}
            for item in items:
                lot_str = str(item.get('lottery', 'General'))
                if lot_str not in groups:
                    groups[lot_str] = []
                groups[lot_str].append(item)

            with transaction.atomic():
                for lot_str, lot_items in groups.items():
                    loteria, _ = Loteria.objects.get_or_create(
                        nombre=lot_str[:100], 
                        defaults={'activo': True, 'orden': 1}
                    )
                    
                    producto, _ = ProductoLoteria.objects.get_or_create(
                        loteria=loteria,
                        nombre_producto=lot_str[:100],
                        defaults={'tipo': 'NUMERICO', 'activo': True, 'orden': 1, 'multiplicador_pago': 0}
                    )
                    
                    sorteo, _ = SorteoArrejuntao.objects.get_or_create(
                        producto=producto,
                        descripcion="Sorteo Automático Taquilla",
                        defaults={'hora_sorteo': '23:59:00', 'activo': True}
                    )
                    
                    import uuid
                    short_uuid = str(uuid.uuid4())[:6].upper()
                    real_serie = f"A7-{tz_now().strftime('%Y%m%d')}-{short_uuid}"

                    t_obj = Ticket.objects.create(
                        serie=real_serie,
                        producto=producto,
                        vendedor_id=user_id,
                        sorteo_id=sorteo.id,
                        id_agencia=agencia_id,
                        total=sum(float(i.get('amount', 0)) for i in lot_items),
                        tserial_ifa=taquilla_nombre
                    )
                    
                    for i in lot_items:
                        raw_number = str(i.get('number', ''))
                        clean_number = raw_number.split(' ')[0][:5] if raw_number else '000'
                        if clean_number.upper().startswith("MÚLTI"):
                            clean_number = "MULT"

                        ApuestaDetalle.objects.create(
                            ticket=t_obj,
                            tipo_jugada='TRIPLE_A', 
                            numero_apostado=clean_number,
                            monto_apostado=float(i.get('amount', 0)),
                            estatus='P'
                        )
        except Exception as parser_ex:
            # Si el parser falla, la venta original sigue intacta
            print(f"Error parseando ticket {ticket_id} para Dashboard: {parser_ex}")

        return JsonResponse({'ok': True, 'ticket_id': ticket_id})

    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)


def taquilla_ventas_lista_api(request):
    """
    Devuelve la lista de ventas de taquilla para el dashboard.
    GET ?fecha=YYYY-MM-DD&limit=100
    """
    from django.db import connection

    try:
        _ensure_taquilla_table()
    except Exception:
        pass

    fecha_str = request.GET.get('fecha', '')
    limit = min(int(request.GET.get('limit', 100)), 500)

    try:
        with connection.cursor() as cursor:
            if fecha_str:
                cursor.execute(
                    "SELECT id,ticket_id,usuario,taquilla,fecha,items_json,total,status "
                    "FROM taquilla_boleto WHERE DATE(fecha)=%s ORDER BY fecha DESC LIMIT %s",
                    [fecha_str, limit]
                )
            else:
                cursor.execute(
                    "SELECT id,ticket_id,usuario,taquilla,fecha,items_json,total,status "
                    "FROM taquilla_boleto ORDER BY fecha DESC LIMIT %s",
                    [limit]
                )
            rows = cursor.fetchall()

        ventas = []
        for row in rows:
            pk, tid, usr, taq, fecha, items_json, total, status = row
            try:
                items = json.loads(items_json) if items_json else []
            except Exception:
                items = []
            # fecha puede llegar como datetime (Postgres) o string (SQLite)
            if hasattr(fecha, 'strftime'):
                fecha_display = fecha.strftime('%d/%m/%Y %H:%M')
            elif fecha:
                # SQLite devuelve string tipo "2026-03-31 20:10:00.000000"
                try:
                    import datetime as _dt
                    fecha_display = _dt.datetime.fromisoformat(str(fecha)[:16]).strftime('%d/%m/%Y %H:%M')
                except Exception:
                    fecha_display = str(fecha)[:16]
            else:
                fecha_display = ''
            ventas.append({
                'pk': pk, 'ticket_id': tid, 'usuario': usr, 'taquilla': taq,
                'fecha': fecha_display,
                'items': items, 'total': float(total) if total else 0, 'status': status,
            })

        # Total del día
        hoy = __import__('datetime').date.today().isoformat()
        with connection.cursor() as cursor:
            cursor.execute("SELECT COALESCE(SUM(total),0) FROM taquilla_boleto WHERE DATE(fecha)=%s AND status='activo'", [hoy])
            total_dia = float(cursor.fetchone()[0])

        return JsonResponse({'ok': True, 'ventas': ventas, 'count': len(ventas), 'total_dia': total_dia})

    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'ventas': [], 'total_dia': 0}, status=500)



# ── APIS DE REPORTES TAQUILLA (leen de Supabase) ────────────────────────────

def _parse_fecha_boleto(fecha):
    """Convierte fecha de Postgres/SQLite a dict con fecha_display, date_only, time_only."""
    if hasattr(fecha, 'strftime'):
        return {
            'fecha_display': fecha.strftime('%d/%m/%Y %H:%M'),
            'date_only': fecha.strftime('%Y-%m-%d'),
            'time_only': fecha.strftime('%H:%M'),
        }
    elif fecha:
        import datetime as _dt
        try:
            dt = _dt.datetime.fromisoformat(str(fecha)[:19])
            return {
                'fecha_display': dt.strftime('%d/%m/%Y %H:%M'),
                'date_only': dt.strftime('%Y-%m-%d'),
                'time_only': dt.strftime('%H:%M'),
            }
        except Exception:
            pass
    return {'fecha_display': str(fecha)[:16], 'date_only': str(fecha)[:10], 'time_only': str(fecha)[11:16]}


def _get_tickets_as_boletos_format(desde_str, hasta_str, taquilla_filtro=''):
    """
    Lee del ORM (Ticket y ApuestaDetalle) y genera una lista de diccionarios
    con la misma estructura JSON que la Taquilla usaba de taquilla_boleto.
    """
    from admin_juego.models_arrejuntao import Ticket
    from django.utils.timezone import localtime
    import datetime

    # parse fechas
    try:
        dt_desde = datetime.datetime.strptime(desde_str, '%Y-%m-%d').date()
        dt_hasta = datetime.datetime.strptime(hasta_str, '%Y-%m-%d').date()
    except Exception:
        dt_desde = datetime.date.today()
        dt_hasta = datetime.date.today()

    qs = Ticket.objects.filter(
        fecha_emision__date__gte=dt_desde, 
        fecha_emision__date__lte=dt_hasta
    ).order_by('-fecha_emision').select_related('vendedor', 'producto__loteria').prefetch_related('apuestas')

    if taquilla_filtro:
        qs = qs.filter(tserial_ifa=taquilla_filtro)

    boletos = []
    for t in qs:
        items = []
        premios_ticket = 0
        for d in t.apuestas.all():
            items.append({
                'lottery': t.producto.loteria.nombre if (t.producto and t.producto.loteria) else 'General',
                'number': d.numero_apostado,
                'amount': float(d.monto_apostado),
                'bet_type': d.tipo_jugada
            })
            if d.estatus in ['G', 'L']:
                premios_ticket += float(d.monto_premio or 0)

        dt = t.fecha_emision
        from django.utils.timezone import is_aware, make_aware
        if not is_aware(dt):
            dt = make_aware(dt)
        dt_local = localtime(dt)
        
        status_str = 'anulado' if t.anulado else 'activo'
        
        boletos.append({
            'pk': t.id, 
            'ticket_id': t.serie, 
            'usuario': t.vendedor.user if t.vendedor else 'desconocido', 
            'taquilla': t.tserial_ifa or 'Sin nombre',
            'fecha': dt_local.strftime('%d/%m/%Y %I:%M %p'),
            'date_only': dt_local.strftime('%d/%m/%Y'),
            'time_only': dt_local.strftime('%I:%M %p').lower(),
            'items': items,
            'total': float(t.total),
            'status': status_str,
            'prizeValue': premios_ticket,
        })
    return boletos


@csrf_exempt
def taquilla_reporte_diario(request):
    """
    GET /taquilla/reportes/analisis-diario/?fecha=YYYY-MM-DD&taquilla=T1
    Análisis diario: ventas, comisiones, premios del día desde Supabase.
    """
    from django.db import connection
    fecha = request.GET.get('fecha', '') or __import__('datetime').date.today().isoformat()
    taquilla_filtro = request.GET.get('taquilla', '')

    try:
        boletos = _get_tickets_as_boletos_format(fecha, fecha, taquilla_filtro)
        venta = sum(b['total'] for b in boletos)
        comision = venta * 0.15
        premios = sum(b['prizeValue'] for b in boletos)
        saldo = venta - comision - premios

        return JsonResponse({
            'ok': True, 'fecha': fecha,
            'total_tickets': len(boletos),
            'venta': round(venta, 2),
            'comision': round(comision, 2),
            'premios': round(premios, 2),
            'saldo': round(saldo, 2),
            'boletos': boletos,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)


@csrf_exempt
def taquilla_reporte_periodo(request):
    """
    GET /taquilla/reportes/analisis-periodo/?desde=YYYY-MM-DD&hasta=YYYY-MM-DD&taquilla=T1
    Análisis por rango de fechas desde Supabase.
    """
    from django.db import connection
    import datetime as _dt
    hoy = _dt.date.today().isoformat()
    desde = request.GET.get('desde', hoy)
    hasta = request.GET.get('hasta', hoy)
    taquilla_filtro = request.GET.get('taquilla', '')

    try:
        boletos = _get_tickets_as_boletos_format(desde, hasta, taquilla_filtro)
        venta = sum(b['total'] for b in boletos)
        comision = venta * 0.15
        premios = sum(b['prizeValue'] for b in boletos)
        saldo = venta - comision - premios

        return JsonResponse({
            'ok': True, 'desde': desde, 'hasta': hasta,
            'total_tickets': len(boletos),
            'venta': round(venta, 2),
            'comision': round(comision, 2),
            'premios': round(premios, 2),
            'saldo': round(saldo, 2),
            'boletos': boletos,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)


@csrf_exempt
def taquilla_reporte_caja(request):
    """
    GET /taquilla/reportes/cuadre-caja/?fecha=YYYY-MM-DD&taquilla=T1
    Cuadre de caja del día desde Supabase.
    """
    from django.db import connection
    fecha = request.GET.get('fecha', '') or __import__('datetime').date.today().isoformat()
    taquilla_filtro = request.GET.get('taquilla', '')

    try:
        boletos = _get_tickets_as_boletos_format(fecha, fecha, taquilla_filtro)
        venta = sum(b['total'] for b in boletos)
        comision = venta * 0.15
        premios = sum(b['prizeValue'] for b in boletos)
        saldo = venta - comision - premios

        # Resumen por taquilla
        por_taquilla = {}
        for b in boletos:
            t = b['taquilla'] or 'Sin nombre'
            if t not in por_taquilla:
                por_taquilla[t] = {'tickets': 0, 'venta': 0}
            por_taquilla[t]['tickets'] += 1
            por_taquilla[t]['venta'] += b['total']

        return JsonResponse({
            'ok': True, 'fecha': fecha,
            'total_tickets': len(boletos),
            'venta': round(venta, 2),
            'comision': round(comision, 2),
            'premios': round(premios, 2),
            'saldo': round(saldo, 2),
            'por_taquilla': {k: {'tickets': v['tickets'], 'venta': round(v['venta'], 2)} for k, v in por_taquilla.items()},
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)



@csrf_exempt
def taquilla_reporte_tickets(request):
    """
    GET /taquilla/reportes/tickets/?fecha=YYYY-MM-DD&status=activo&taquilla=T1
    Lista de tickets desde el ORM.
    """
    fecha = request.GET.get('fecha', '') or __import__('datetime').date.today().isoformat()
    status_filtro = request.GET.get('status', '')
    taquilla_filtro = request.GET.get('taquilla', '')
    limit = request.GET.get('limit', '')

    try:
        boletos = _get_tickets_as_boletos_format(fecha, fecha, taquilla_filtro)
        
        # Filtros extra manuales sobre los tickets parseados
        if limit:
            limit = int(limit)
        
        filtered = []
        for b in boletos:
            if status_filtro and b['status'] != status_filtro:
                continue
            filtered.append(b)
        
        if limit and limit > 0:
            filtered = filtered[:limit]
            
        total_venta = sum(b['total'] for b in filtered)

        return JsonResponse({
            'ok': True, 'fecha': fecha,
            'count': len(filtered),
            'total_venta': round(total_venta, 2),
            'tickets': filtered,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)


@csrf_exempt
def taquilla_reporte_ganadores(request):
    """
    GET /taquilla/reportes/ganadores/?fecha=YYYY-MM-DD&taquilla=T1
    Tickets ganadores/pagados desde el ORM.
    """
    fecha = request.GET.get('fecha', '') or __import__('datetime').date.today().isoformat()
    taquilla_filtro = request.GET.get('taquilla', '')

    try:
        boletos = _get_tickets_as_boletos_format(fecha, fecha, taquilla_filtro)
        
        # Filtrar los tickets que tienen premios
        ganadores = []
        for b in boletos:
            if b['prizeValue'] > 0:
                ganadores.append(b)

        return JsonResponse({
            'ok': True, 'fecha': fecha,
            'count': len(ganadores),
            'tickets': ganadores,
        }, json_dumps_params={'ensure_ascii': False})
    except Exception as e:
        import traceback
        return JsonResponse({'ok': False, 'error': str(e), 'trace': traceback.format_exc()}, status=500)



@csrf_exempt
def taquilla_mi_ip(request):
    """
    GET /api/taquilla/mi-ip/
    Devuelve la IP real del cliente (navegador de la taquilla).
    """
    ip = (
        request.META.get('HTTP_X_FORWARDED_FOR', '').split(',')[0].strip()
        or request.META.get('REMOTE_ADDR', '127.0.0.1')
    )

    return JsonResponse({'ip': ip})


@csrf_exempt
def taquilla_cambiar_clave_api(request):
    """
    POST /taquilla/cambiar-clave/
    Permite al operador de taquilla cambiar su propia contraseña.
    Body JSON: { username, old_password, new_password }
    """
    if request.method != 'POST':
        return JsonResponse({'success': False, 'message': 'Método no permitido'}, status=405)

    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'success': False, 'message': 'JSON inválido'}, status=400)

    username     = (body.get('username') or '').strip()
    old_password = (body.get('old_password') or '').strip()
    new_password = (body.get('new_password') or '').strip()

    if not username or not old_password or not new_password:
        return JsonResponse({'success': False, 'message': 'Todos los campos son requeridos'}, status=400)

    if len(new_password) < 8:
        return JsonResponse({'success': False, 'message': 'La nueva contraseña debe tener al menos 8 caracteres'}, status=400)

    try:
        from django.apps import apps
        from django.contrib.auth.hashers import check_password, make_password

        UsuariosTaquilla = apps.get_model('admin_comercializacion', 'UsuariosTaquilla')

        usuario = UsuariosTaquilla.objects.filter(user=username).first()
        if not usuario:
            return JsonResponse({'success': False, 'message': 'Usuario no encontrado'}, status=404)

        if not check_password(old_password, usuario.password):
            return JsonResponse({'success': False, 'message': 'La contraseña actual es incorrecta'}, status=401)

        # Actualizar con el nuevo hash
        UsuariosTaquilla.objects.filter(user=username).update(
            password=make_password(new_password)
        )

        return JsonResponse({'success': True, 'message': 'Contraseña actualizada correctamente'})

    except Exception as e:
        import traceback
        return JsonResponse({
            'success': False,
            'message': f'Error interno: {e}',
            'trace': traceback.format_exc()
        }, status=500)


@csrf_exempt
def taquilla_resultados_hoy(request):
    """
    GET /api/taquilla/resultados-hoy/
    Devuelve el resumen de ventas de hoy y los últimos tickets
    para el modal de Reportes en la taquilla.
    No requiere autenticación staff para ser accesible desde la taquilla.
    """
    import datetime
    from django.db import connection

    try:
        _ensure_taquilla_table()
    except Exception:
        pass

    fecha_str = request.GET.get('fecha', datetime.date.today().isoformat())
    limit = min(int(request.GET.get('limit', 50)), 200)

    try:
        with connection.cursor() as cursor:
            # Resumen del día
            cursor.execute(
                "SELECT COALESCE(SUM(total),0), COUNT(*) "
                "FROM taquilla_boleto WHERE DATE(fecha)=%s AND status='activo'",
                [fecha_str]
            )
            total_dia, count_dia = cursor.fetchone()
            total_dia = float(total_dia or 0)

            # Últimos tickets
            cursor.execute(
                "SELECT ticket_id, usuario, taquilla, fecha, items_json, total, status "
                "FROM taquilla_boleto WHERE DATE(fecha)=%s "
                "ORDER BY fecha DESC LIMIT %s",
                [fecha_str, limit]
            )
            rows = cursor.fetchall()

        tickets = []
        for row in rows:
            tid, usr, taq, fecha, items_json, total, status = row
            try:
                items = json.loads(items_json) if items_json else []
            except Exception:
                items = []
            if hasattr(fecha, 'strftime'):
                fecha_str_display = fecha.strftime('%H:%M')
            elif fecha:
                try:
                    import datetime as _dt
                    fecha_str_display = _dt.datetime.fromisoformat(str(fecha)[:16]).strftime('%H:%M')
                except Exception:
                    fecha_str_display = str(fecha)[:5]
            else:
                fecha_str_display = ''

            tickets.append({
                'ticket_id': tid,
                'usuario': usr,
                'taquilla': taq,
                'hora': fecha_str_display,
                'items': items,
                'total': float(total) if total else 0,
                'status': status,
                'jugadas': len(items),
            })

        return JsonResponse({
            'ok': True,
            'fecha': fecha_str,
            'total_dia': round(total_dia, 2),
            'count_dia': count_dia,
            'tickets': tickets,
        }, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        import traceback
        return JsonResponse({
            'ok': False, 'error': str(e),
            'trace': traceback.format_exc(),
            'total_dia': 0, 'count_dia': 0, 'tickets': [],
        }, status=500)


@staff_member_required(login_url='/admin/login/')
def cuadre_nivel_superior_api(request):
    """
    GET /api/cuadre-nivel-superior/?banca=<id>&mes=YYYY-MM
    Devuelve el cuadre diario con saldo anterior, venta, premios, operador.
    """
    import datetime, calendar
    mes_str  = request.GET.get('mes', '')
    banca_id = request.GET.get('banca', '').strip()

    try:
        if mes_str:
            y, m = map(int, mes_str.split('-'))
        else:
            hoy = datetime.date.today()
            y, m = hoy.year, hoy.month
            mes_str = f"{y:04d}-{m:02d}"
        
        primer_dia = datetime.date(y, m, 1)
        ultimo_dia = datetime.date(y, m, calendar.monthrange(y, m)[1])
    except Exception:
        return JsonResponse({'ok': False, 'error': 'Mes invalido. Use YYYY-MM.'}, status=400)

    DIAS_ES = {0:'Lunes',1:'Martes',2:'Miércoles',3:'Jueves',4:'Viernes',5:'Sábado',6:'Domingo'}

    try:
        # Usar la función existente para obtener todos los tickets del mes
        boletos = _get_tickets_as_boletos_format(primer_dia.isoformat(), ultimo_dia.isoformat(), banca_id)
        
        ventas_por_dia = {}
        for b in boletos:
            fecha_str = b['fecha'].split(' ')[0] if ' ' in b['fecha'] else b['fecha'].split('T')[0]
            if fecha_str not in ventas_por_dia:
                ventas_por_dia[fecha_str] = {'venta': 0.0, 'premios': 0.0}
            
            ventas_por_dia[fecha_str]['venta'] += float(b['total'])
            ventas_por_dia[fecha_str]['premios'] += float(b['prizeValue'])

        # Porcentajes de ejemplo (ajustables)
        PCT_BANCA = 0.15
        PCT_REGALIA = 0.0

        rows = []
        saldo_acumulado = 0.0
        current = primer_dia

        while current <= ultimo_dia:
            fs = current.isoformat()
            dia_semana = DIAS_ES[current.weekday()]
            
            dd = ventas_por_dia.get(fs, {'venta': 0.0, 'premios': 0.0})
            venta    = dd['venta']
            premios  = dd['premios']
            
            # Si no hay ventas ni es el día actual, podríamos saltarlo, 
            # pero el reporte de cuadre suele mostrar todos los días del mes o hasta el día actual.
            # Para no llenar de ceros el futuro:
            if venta == 0 and current > datetime.date.today():
                current += datetime.timedelta(days=1)
                continue

            pct_banca = round(venta * PCT_BANCA, 2)
            regalia   = round(venta * PCT_REGALIA, 2)
            
            # Saldo del día
            saldo_dia = venta - premios - pct_banca - regalia
            operador  = saldo_dia # Asumimos Operador = Saldo del día según ejemplo
            
            sa_prev = saldo_acumulado
            saldo_acumulado = sa_prev + saldo_dia

            rows.append({
                'fecha': fs,
                'dia': dia_semana,
                'sa': round(sa_prev, 2),
                'venta': round(venta, 2),
                'premios': round(premios, 2),
                'pct': round(pct_banca, 2),
                'regalia': round(regalia, 2),
                'saldo': round(saldo_dia, 2),
                'operador': round(operador, 2),
                'dep': 0.00,
                'pagos': 0.00,
                'ajuste': 0.00,
                'cargos': 0.00,
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



@staff_member_required(login_url='/admin/login/')
def candidatos_riesgo_api(request):
    """
    API para el panel nativo 'Selección de Candidatos' del dashboard.
    GET ?fecha=YYYY-MM-DD&sorteo=nombre&lista=TRIPLE&top=50

    Agrupa las apuestas de taquilla_boleto por número y calcula:
    - cant_ticket  : tickets distintos que apostaron ese número
    - venta_nro    : monto total apostado a ese número
    - max_jugada   : mayor apuesta individual en ese número
    - monto_prem   : venta_nro * factor_pago  (premio potencial)
    - pct_prem     : monto_prem / venta_total_general * 100
    - precaucion   : CRÍTICO >35% | ALERTA 20-35% | MODERADO 10-20%
    """
    from django.db import connection
    import datetime, collections

    fecha_str = request.GET.get('fecha', datetime.date.today().isoformat())
    sorteo_f  = request.GET.get('sorteo', '').strip().lower()
    lista_f   = request.GET.get('lista', '').strip().upper()   # TRIPLE / TERMINAL / ANIMALITO / TODOS
    top       = min(int(request.GET.get('top', 50)), 200)

    # ── factor_pago por tipo de jugada (desde BD, con fallback) ─────────────
    FACTOR_DEFAULT = {
        'triple':    700,  'terminal': 70, 'animalito': 8,
        'arrimao':   600,  'cuatro':  3000, 'reventado': 50,
    }
    factor_cache = {}
    try:
        from admin_juego.models_arrejuntao import ConfiguracionJugada
        for cfg in ConfiguracionJugada.objects.select_related('producto').filter(activa=True):
            key = cfg.tipo_jugada.lower()
            factor_cache[key] = float(cfg.factor_pago)
    except Exception:
        pass

    def _get_factor(bet_type_raw: str) -> float:
        btype = (bet_type_raw or '').lower()
        if btype in factor_cache:
            return factor_cache[btype]
        for k, v in FACTOR_DEFAULT.items():
            if k in btype:
                return float(v)
        return 70.0  # fallback conservador

    # ── Leer boletos ─────────────────────────────────────────────────────────
    try:
        _ensure_taquilla_table()
    except Exception:
        pass

    try:
        with connection.cursor() as cur:
            cur.execute(
                "SELECT ticket_id, items_json, total FROM taquilla_boleto "
                "WHERE DATE(fecha)=%s AND status='activo' ORDER BY fecha",
                [fecha_str]
            )
            boletos = cur.fetchall()
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)

    # ── Agregar por número ───────────────────────────────────────────────────
    # {numero → {tickets:set, venta:float, max:float, factor:float}}
    agg = {}
    venta_total = 0.0
    tickets_total = set()

    for tid, items_json, total in boletos:
        tickets_total.add(tid)
        try:
            items = json.loads(items_json) if items_json else []
        except Exception:
            continue

        for item in items:
            lottery  = str(item.get('lottery', '')).lower()
            number   = str(item.get('number', '')).strip()
            amount   = float(item.get('amount', 0) or 0)
            bet_type = str(item.get('bet_type', '')).lower()

            if not number:
                continue

            # Filtro por tipo de lista (sorteo)
            if lista_f and lista_f not in ('TODOS', ''):
                if lista_f.lower() not in lottery and lista_f.lower() not in bet_type:
                    continue
            if sorteo_f and sorteo_f not in lottery:
                continue

            factor = _get_factor(bet_type or lottery)
            venta_total += amount

            if number not in agg:
                agg[number] = {'tickets': set(), 'venta': 0.0, 'max_j': 0.0, 'factor': factor}
            agg[number]['tickets'].add(tid)
            agg[number]['venta'] += amount
            agg[number]['max_j']  = max(agg[number]['max_j'], amount)
            agg[number]['factor']  = factor   # último factor visto

    # ── Calcular riesgo y ordenar ─────────────────────────────────────────────
    resultados = []
    for numero, d in agg.items():
        venta_nro = d['venta']
        factor    = d['factor']
        monto_prem = round(venta_nro * factor, 2)
        pct_prem   = round(monto_prem / venta_total * 100, 1) if venta_total > 0 else 0.0

        if pct_prem >= 35:
            prec = 'CRÍTICO'
        elif pct_prem >= 20:
            prec = 'ALERTA'
        elif pct_prem >= 10:
            prec = 'MODERADO'
        else:
            prec = 'OK'

        resultados.append({
            'numero':      numero,
            'cant_ticket': len(d['tickets']),
            'venta_nro':   round(venta_nro, 2),
            'max_jugada':  round(d['max_j'], 2),
            'monto_prem':  monto_prem,
            'pct_prem':    pct_prem,
            'factor':      factor,
            'precaucion':  prec,
        })

    # Ordenar por monto premiación desc
    resultados.sort(key=lambda x: x['monto_prem'], reverse=True)
    resultados = resultados[:top]

    # KPIs
    criticos  = sum(1 for r in resultados if r['precaucion'] == 'CRÍTICO')
    alertas   = sum(1 for r in resultados if r['precaucion'] == 'ALERTA')
    moderados = sum(1 for r in resultados if r['precaucion'] == 'MODERADO')

    return JsonResponse({
        'ok':          True,
        'fecha':       fecha_str,
        'venta_total': round(venta_total, 2),
        'total_tickets': len(tickets_total),
        'criticos':    criticos,
        'alertas':     alertas,
        'moderados':   moderados,
        'rows':        resultados,
    }, json_dumps_params={'ensure_ascii': False})





@staff_member_required(login_url='/admin/login/')
def reportes_page(request):
    """
    Vista principal de Reportes de Venta.
    Accesible en: http://127.0.0.1:8000/dashboard/reportes/
    Renderiza la página completa de reportes (Lista en Línea, Por Producto,
    Riesgo de Venta) dentro del contexto autenticado del dashboard.
    Solo accesible para personal de staff.
    """
    html_path = os.path.join(
        settings.BASE_DIR,
        'admin_asterisco7', 'templates', 'reportes', 'reportes.html'
    )
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html; charset=utf-8')



@xframe_options_sameorigin
@staff_member_required(login_url='/admin/login/')
def candidatos_page(request):
    """
    Selección de Candidatos — diseño original v0.
    Accesible en: http://127.0.0.1:8000/dashboard/candidatos/
    """
    html_path = os.path.join(
        settings.BASE_DIR,
        'admin_asterisco7', 'templates', 'reportes', 'candidatos.html'
    )
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html; charset=utf-8')


@xframe_options_sameorigin
@staff_member_required(login_url='/admin/login/')
def liquidacion_page(request):
    """
    Reporte de Liquidación de Sorteo.
    Accesible en: /dashboard/liquidaciones/
    """
    html_path = os.path.join(
        settings.BASE_DIR,
        'admin_asterisco7', 'templates', 'reportes', 'liquidacion_sorteo.html'
    )
    with open(html_path, 'r', encoding='utf-8') as f:
        content = f.read()
    return HttpResponse(content, content_type='text/html; charset=utf-8')



@staff_member_required(login_url='/admin/login/')
def monitor_api(request):
    """Monitor de Conexiones en Tiempo Real — API JSON optimizada (sin N+1)."""
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

    # 1. Mapas de nombres en UNA query por tabla — evita N+1
    try:
        taq_map = dict(Taquillas.objects.values_list('id', 'taquilla'))
    except Exception:
        taq_map = {}
    try:
        ag_map = dict(Agencias.objects.values_list('id', 'nombre'))
    except Exception:
        ag_map = {}

    # 2. IP activa por taquilla_id — tomamos la sesión más reciente de cada taquilla
    #    TaquillaSessions.user → FK a UsuariosTaquilla → taquilla_id → FK a Taquillas
    ip_por_taquilla = {}
    ultima_sesion_por_taquilla = {}
    try:
        qs_ip = (TaqSessions.objects
                 .select_related('user')
                 .order_by('-created_at')
                 .values('user__taquilla_id', 'ip', 'created_at', 'enddate'))
        for s in qs_ip[:2000]:
            taq_id = s['user__taquilla_id']
            if taq_id and taq_id not in ip_por_taquilla:
                ip_por_taquilla[taq_id] = s['ip'] or '—'
                ultima_sesion_por_taquilla[taq_id] = s['created_at']
    except Exception:
        pass

    # 3. Construir filas desde HechoConnectionsComer
    rows = []
    try:
        for c in HechoConn.objects.all().order_by('-connection_at')[:500]:
            conn_at = c.connection_at
            if not conn_at:
                continue
                
            # Extraemos la hora ignorando la zona horaria para evitar crashes
            # tanto en SQLite (naive) como en PostgreSQL (aware)
            c_naive = conn_at.replace(tzinfo=None)
            l_online_naive = limite_online.replace(tzinfo=None)
            l_reciente_naive = limite_reciente.replace(tzinfo=None)
                
            if c_naive >= l_online_naive:
                estado = 'online'
            elif c_naive >= l_reciente_naive:
                estado = 'reciente'
            else:
                estado = 'offline'

            diff = ahora.replace(tzinfo=None) - c_naive
            mins = int(diff.total_seconds() // 60)
            if mins < 1:      tiempo_str = 'Ahora'
            elif mins < 60:   tiempo_str = f'{mins} min'
            elif mins < 1440: tiempo_str = f'{mins//60}h {mins%60}m'
            else:             tiempo_str = f'{mins//1440}d {(mins%1440)//60}h'

            rows.append({
                'taquilla_id':  c.taquilla_id,
                'agencia_id':   c.agencia_id,
                'taquilla':     taq_map.get(c.taquilla_id, f'Taquilla #{c.taquilla_id}'),
                'agencia':      ag_map.get(c.agencia_id,   f'Agencia #{c.agencia_id}'),
                'connection_at': conn_at.strftime('%d/%m/%Y %H:%M:%S'),
                'hace':         tiempo_str,
                'ip':           ip_por_taquilla.get(c.taquilla_id, '—'),
                'estado':       estado,
            })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

    # 4. Contadores de estado
    total_online   = sum(1 for r in rows if r['estado'] == 'online')
    total_reciente = sum(1 for r in rows if r['estado'] == 'reciente')
    total_offline  = sum(1 for r in rows if r['estado'] == 'offline')

    # 5. Agrupación por agencia para resumen
    agencias_resumen = {}
    for r in rows:
        aid = r['agencia_id']
        if aid not in agencias_resumen:
            agencias_resumen[aid] = {
                'agencia': r['agencia'],
                'online': 0, 'reciente': 0, 'offline': 0, 'total': 0
            }
        agencias_resumen[aid][r['estado']] += 1
        agencias_resumen[aid]['total'] += 1

    return JsonResponse({
        'total':         len(rows),
        'online':        total_online,
        'reciente':      total_reciente,
        'offline':       total_offline,
        'rows':          rows,
        'por_agencia':   list(agencias_resumen.values()),
    }, json_dumps_params={'ensure_ascii': False})


@staff_member_required(login_url='/admin/login/')
def dashboard_stats(request):
    """
    Endpoint JSON con conteos reales de la base de datos.
    GET /dashboard/stats/
    """
    data = {}

    # ── COMERCIALIZACIÓN ──────────────────────────────────────────
    try:
        from admin_comercializacion.models import (
            Operadoras, Bloques, Bancas, Distribuidores,
            Agencias, Taquillas, UsuariosTaquilla
        )
        data['operadoras'] = Operadoras.objects.count()
        data['bloques']    = Bloques.objects.count()
        data['bancas']     = Bancas.objects.count()
        data['distribuidores'] = Distribuidores.objects.count()
        data['agencias']   = Agencias.objects.count()
        data['taquillas']  = Taquillas.objects.count()
        data['usuarios_taquilla'] = UsuariosTaquilla.objects.count()
    except Exception as e:
        data['com_error'] = str(e)

    # ── JUEGO ──────────────────────────────────────────────────────
    try:
        from django.apps import apps
        import datetime
        Loteria          = apps.get_model('admin_juego', 'Loteria')
        TipoProducto     = apps.get_model('admin_juego', 'TipoProducto')
        SorteoArrejuntao = apps.get_model('admin_juego', 'SorteoArrejuntao')
        Animalito        = apps.get_model('admin_juego', 'Animalito')
        data['loterias']      = Loteria.objects.count()
        data['productos']     = TipoProducto.objects.count()
        data['sorteos_total'] = SorteoArrejuntao.objects.count()
        data['animalitos']    = Animalito.objects.count()
        # Productos activos para panel inferior
        try:
            prods = TipoProducto.objects.filter(activo=True)[:12]
        except Exception:
            prods = TipoProducto.objects.all()[:12]
        data['productos_activos'] = [{'nombre': str(p)} for p in prods]
        # Loterias activas
        try:
            lots = Loteria.objects.filter(activo=True)[:12]
        except Exception:
            lots = Loteria.objects.all()[:12]
        data['loterias_activas'] = [str(l) for l in lots]
    except Exception as e:
        data['juego_error'] = str(e)
        data['productos_activos'] = []
        data['loterias_activas']  = []

    # ── APUESTAS (tickets) ──────────────────────────────────────
    try:
        from admin_apuestas.models import Tickets
        import datetime
        hoy = datetime.date.today()
        data['tickets_hoy']   = Tickets.objects.filter(
            created_at__date=hoy).count()
        data['tickets_total'] = Tickets.objects.count()
    except Exception as e:
        data['apuestas_error'] = str(e)

    # ── USUARIOS ──────────────────────────────────────────
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        data['usuarios_total'] = User.objects.count()
        data['usuarios_staff'] = User.objects.filter(is_staff=True).count()
    except Exception as e:
        data['auth_error'] = str(e)

    # ── ACTIVIDAD RECIENTE ─────────────────────────────────────
    activity = []
    try:
        from admin_comercializacion.models import Taquillas as Tq2, Bancas as Ba2, Operadoras as Op2
        for obj in Tq2.objects.order_by('-updated_at')[:2]:
            activity.append({'color':'green','title':f'Taquilla {obj.taquilla}','sub':'Registro actualizado','time':_time_ago(obj.updated_at)})
        for obj in Ba2.objects.order_by('-updated_at')[:1]:
            activity.append({'color':'blue','title':f'Banca {obj.nombre}','sub':'Datos modificados','time':_time_ago(obj.updated_at)})
        for obj in Op2.objects.order_by('-updated_at')[:1]:
            activity.append({'color':'purple','title':f'Operadora {obj.nombre}','sub':'Configuracion actualizada','time':_time_ago(obj.updated_at)})
    except Exception:
        pass
    try:
        from admin_apuestas.models import Tickets as Tk2
        for tk in Tk2.objects.order_by('-created_at')[:2]:
            t = getattr(tk,'created_at',None)
            activity.append({'color':'yellow','title':f'Ticket #{getattr(tk,"key",tk.pk)}','sub':f'Monto: {getattr(tk,"monto","---")}','time':_time_ago(t)})
    except Exception:
        pass
    if not activity:
        activity = [
            {'color':'green', 'title':'Sistema iniciado',        'sub':'Servidor operativo',      'time':'Ahora'},
            {'color':'blue',  'title':'Dashboard cargado',       'sub':'Panel de gestion activo', 'time':'Ahora'},
            {'color':'purple','title':'Base de datos conectada', 'sub':'SQLite local activo',     'time':'Ahora'},
        ]
    data['actividad'] = activity[:6]

    # ── ESTADO DEL SISTEMA ──────────────────────────────────────
    import sys
    data['sistema'] = [
        {'label':'Servidor Django', 'status':'Activo',     'color':'green'},
        {'label':'Base de Datos',   'status':'Conectado',  'color':'green'},
        {'label':'Celery / Cola',   'status':'Local off',  'color':'yellow'},
        {'label':'Firebase',        'status':'Conectado',  'color':'green'},
        {'label':'Modo',            'status':'Desarrollo', 'color':'blue'},
        {'label':'Python',          'status':f'{sys.version_info.major}.{sys.version_info.minor}', 'color':'gray'},
    ]

    return JsonResponse(data, json_dumps_params={'ensure_ascii': False})


def _time_ago(dt):
    if dt is None:
        return '--'
    try:
        import django.utils.timezone as tz
        diff = tz.now() - dt
        secs = int(diff.total_seconds())
        if secs < 60:    return 'Ahora'
        if secs < 3600:  return f'{secs//60} min'
        if secs < 86400: return f'{secs//3600} h'
        return f'{secs//86400} dias'
    except Exception:
        return '--'


# ─────────────────────────────────────────────────────────────────────────────
#  GENERIC LIST API — powers the SPA in-dashboard views
# ─────────────────────────────────────────────────────────────────────────────

_MODULES = {
    # COMERCIALIZACION
    'operadoras':     ('admin_comercializacion', 'Operadoras',
                       ['id', 'nombre', 'telefono', 'rif', 'resumen_automatic'],
                       ['nombre', 'rif'],
                       ['#', 'Nombre', 'Telefono', 'RIF', 'Auto Resumen']),
    'bloques':        ('admin_comercializacion', 'Bloques',
                       ['id', 'nombre', 'telefono', 'rif'],
                       ['nombre', 'rif'],
                       ['#', 'Nombre', 'Telefono', 'RIF']),
    'bancas':         ('admin_comercializacion', 'Bancas',
                       ['id', 'nombre', 'telefono', 'rif'],
                       ['nombre', 'rif'],
                       ['#', 'Nombre', 'Telefono', 'RIF']),
    'distribuidores': ('admin_comercializacion', 'Distribuidores',
                       ['id', 'nombre', 'telefono', 'rif'],
                       ['nombre', 'rif'],
                       ['#', 'Nombre', 'Telefono', 'RIF']),
    'agencias':       ('admin_comercializacion', 'Agencias',
                       ['id', 'nombre', 'telefono', 'rif'],
                       ['nombre', 'rif'],
                       ['#', 'Nombre', 'Telefono', 'RIF']),
    'taquillas':      ('admin_comercializacion', 'Taquillas',
                       ['id', 'taquilla', 'serial', 'monto_alquiler'],
                       ['taquilla', 'serial'],
                       ['#', 'Taquilla', 'Serial', 'Monto Alquiler']),
    'usuariostaquilla': ('admin_comercializacion', 'UsuariosTaquilla',
                         ['id', 'user', 'nombre', 'taquilla_id', 'status_id'],
                         ['nombre'],
                         ['#', 'Usuario', 'Nombre', 'Taquilla', 'Status']),
    'cupos':          ('admin_comercializacion', 'Cupos',
                       ['id', 'fecha_inicio', 'fecha_fin', 'monto_diario', 'monto_premio'],
                       [],
                       ['#', 'Fecha Inicio', 'Fecha Fin', 'Monto Diario', 'Monto Premio']),
    'porcentajes':    ('admin_comercializacion', 'Porcentajes',
                       ['id', 'fecha_inicio', 'fecha_fin', 'tipo', 'porcentaje_ganancia', 'porcentaje_maximo'],
                       [],
                       ['#', 'Fecha Inicio', 'Fecha Fin', 'Tipo', '% Ganancia', '% Máximo']),
    'factorriesgo':   ('admin_comercializacion', 'FactorRiesgo',
                       ['id', 'factores', 'created_at', 'updated_at'],
                       [],
                       ['#', 'Factores', 'Creado', 'Actualizado']),
    'grouppreferences': ('admin_comercializacion', 'GroupPreferences',
                         ['id', 'name', 'codename', 'order', 'created_at'],
                         ['name', 'codename'],
                         ['#', 'Nombre', 'Codigo', 'Orden', 'Creado']),
    'typepreferences': ('admin_comercializacion', 'TypePreferences',
                        ['id', 'name', 'codename', 'comparison', 'type_data', 'order'],
                        ['name', 'codename'],
                        ['#', 'Nombre', 'Codigo', 'Comparacion', 'Tipo', 'Orden']),
    'defaultpreferences': ('admin_comercializacion', 'DefaultPreferences',
                           ['id', 'value', 'default', 'created_at'],
                           [],
                           ['#', 'Valor', 'Default', 'Creado']),
    'preferences':    ('admin_comercializacion', 'Preferences',
                       ['id', 'value', 'created_at', 'updated_at'],
                       [],
                       ['#', 'Valor', 'Creado', 'Actualizado']),
    'datadefault':    ('admin_comercializacion', 'DataDefault',
                       ['id', 'user_type', 'cupo', 'porcentaje_comision', 'porcentaje_regalia', 'porcentaje_maximo', 'monto_alquiler'],
                       [],
                       ['#', 'Tipo Usuario', 'Cupo', '% Comision', '% Regalia', '% Máximo', 'Alquiler']),
    'tipoporcentajes': ('admin_comercializacion', 'TipoPorcentajes',
                        ['id', 'nombre', 'codename', 'orden', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla'],
                        ['nombre', 'codename'],
                        ['#', 'Nombre', 'Codigo', 'Orden', 'Bloque', 'Banca', 'Distribuidor', 'Agencia', 'Taquilla']),
    # JUEGO
    'loterias':       ('admin_juego', 'Loteria',
                       ['id', 'nombre', 'activo', 'orden'],
                       ['nombre'],
                       ['#', 'Nombre', 'Activo', 'Orden']),
    'tipoproducto':   ('admin_juego', 'TipoProducto',
                       ['id', 'loteria_display', 'deporte', 'nombre'],
                       ['nombre'],
                       ['#', 'Lotería', 'Producto', 'Modalidad']),
    'sorteos':        ('admin_juego', 'SorteoArrejuntao',
                       ['id', 'producto', 'descripcion', 'hora_sorteo', 'activo'],
                       ['descripcion'],
                       ['#', 'Modalidad', 'Descripcion', 'Hora', 'Activo']),
    'plantillas':     ('admin_juego', 'PlantillaProducto',
                       ['id', 'nombre', 'descripcion', 'activo'],
                       ['nombre'],
                       ['#', 'Nombre', 'Descripcion', 'Activo']),
    'sistemajuego':   ('admin_juego', 'SistemaJuego',
                       ['id', 'nombre', 'comercializadora'],
                       ['nombre'],
                       ['#', 'Nombre', 'Comercializadora']),
    'animalitos':     ('admin_juego', 'Animalito',
                       ['id', 'numero', 'nombre', 'activo'],
                       ['nombre'],
                       ['#', 'Numero', 'Nombre', 'Activo']),
    'grupoanimales':  ('admin_juego', 'GrupoAnimales',
                       ['id', 'nombre', 'descripcion', 'activo'],
                       ['nombre'],
                       ['#', 'Nombre', 'Descripcion', 'Activo']),
    'productoloteria': ('admin_juego', 'ProductoLoteria',
                         ['id', 'loteria', 'producto', 'nombre_producto', 'tipo_label', 'multiplicador_pago', 'activo'],
                         ['nombre_producto'],
                         ['#', 'Lotería', 'Producto', 'Modalidad', 'Tipo', 'Multiplicador', 'Activo']),
    'resultados':     ('admin_juego', 'ResultadoSorteo',
                       ['id', 'producto', 'sorteo_id', 'fecha_sorteo'],
                       [],
                       ['#', 'Producto', 'Sorteo ID', 'Fecha']),
    'liquidaciones':  ('admin_juego', 'LiquidacionSorteo',
                       ['id', 'id_sorteo', 'id_lista', 'id_tipo_lista'],
                       [],
                       ['#', 'Sorteo', 'Lista', 'Tipo Lista']),
    'operadoraloteria': ('admin_juego', 'OperadoraLoteria',
                         ['id', 'nombre', 'orden', 'cantidad'],
                         ['nombre'],
                         ['#', 'Nombre', 'Orden', 'Cantidad']),
    'periodosorteo':  ('admin_juego', 'PeriodoSorteo',
                       ['id', 'nombre', 'fechaini', 'fechafin', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Fecha Ini', 'Fecha Fin', 'Creado']),
    'modalidadjuego': ('admin_juego', 'ModalidadJuego',
                       ['id', 'nombre', 'deporte', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Deporte', 'Creado']),
    'tiponumerosorteo': ('admin_juego', 'TipoNumeroSorteo',
                         ['id', 'nombre', 'codename', 'deporte'],
                         ['nombre', 'codename'],
                         ['#', 'Nombre', 'Codigo', 'Deporte']),
    'numerosorteo':   ('admin_juego', 'NumeroSorteo',
                       ['id', 'nombre', 'tipo', 'lateralidad'],
                       ['nombre'],
                       ['#', 'Nombre', 'Tipo', 'Lateralidad']),
    'fechas':         ('admin_juego', 'Fechas',
                       ['id', 'jornada', 'fechaini', 'fechafin', 'parley', 'quiniela'],
                       [],
                       ['#', 'Jornada', 'Fecha Ini', 'Fecha Fin', 'Parley', 'Quiniela']),
    'grupossorteo':   ('admin_juego', 'GruposSorteo',
                       ['id', 'nombre', 'orden', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Orden', 'Creado']),
    'sorteo':         ('admin_juego', 'Sorteo',
                       ['id', 'horajuego', 'horacierre', 'jornada', 'created_at'],
                       [],
                       ['#', 'Hora Juego', 'Hora Cierre', 'Jornada', 'Creado']),
    'sorteodetalle':  ('admin_juego', 'SorteoDetalle',
                       ['id', 'encuentro', 'indice', 'created_at'],
                       [],
                       ['#', 'Encuentro', 'Indice', 'Creado']),
    'gruposapuesta':  ('admin_juego', 'GruposApuesta',
                       ['id', 'nombre', 'codename', 'orden', 'deporte'],
                       ['nombre', 'codename'],
                       ['#', 'Nombre', 'Codigo', 'Orden', 'Deporte']),
    'modalidadapuesta': ('admin_juego', 'ModalidadApuesta',
                         ['id', 'modalidad', 'orden', 'descripcion', 'codename'],
                         ['descripcion', 'codename'],
                         ['#', 'Modalidad', 'Orden', 'Descripcion', 'Codigo']),
    'sorteomodalidades': ('admin_juego', 'SorteoModalidades',
                          ['id', 'encuentro', 'sistema', 'origen', 'created_at'],
                          [],
                          ['#', 'Encuentro', 'Sistema', 'Origen', 'Creado']),
    'condiciones':    ('admin_juego', 'Condiciones',
                       ['id', 'modalidad', 'nombre', 'tipo', 'orden'],
                       ['nombre'],
                       ['#', 'Modalidad', 'Nombre', 'Tipo', 'Orden']),
    'jugadasinformativas': ('admin_juego', 'JugadasInformativas',
                            ['id', 'ref_principal', 'sistema', 'created_at'],
                            [],
                            ['#', 'Ref Principal', 'Sistema', 'Creado']),
    'restriccionessorteo': ('admin_juego', 'RestriccionesSorteo',
                            ['id', 'deporte', 'grupo', 'modalidad', 'max_logro_favorito'],
                            [],
                            ['#', 'Deporte', 'Grupo', 'Modalidad', 'Max Logro Fav']),
    'plantillajugada': ('admin_juego', 'PlantillaJugada',
                        ['id', 'producto', 'tipo_jugada', 'activa', 'factor_pago', 'monto_maximo_venta'],
                        [],
                        ['#', 'Producto', 'Tipo Jugada', 'Activa', 'Factor Pago', 'Monto Max']),
    'limitecentro':   ('admin_juego', 'LimiteCentro',
                       ['id', 'agencia', 'max_tickets_diarios', 'monto_maximo_diario', 'activo'],
                       [],
                       ['#', 'Agencia', 'Max Tickets/Dia', 'Monto Max/Dia', 'Activo']),
    'animalfigura':   ('admin_juego', 'AnimalFigura',
                       ['id', 'grupo', 'numero', 'nombre', 'activo'],
                       ['nombre'],
                       ['#', 'Grupo', 'Numero', 'Nombre', 'Activo']),
    # APUESTAS
    'tickets':        ('admin_apuestas', 'Tickets',
                       ['id', 'key', 'monto', 'monto_premio', 'fecha', 'status'],
                       ['key'],
                       ['#', 'Clave', 'Monto', 'Premio', 'Fecha', 'Estado']),
    'ticketstype':    ('admin_apuestas', 'TicketsType',
                       ['id', 'nombre', 'codename', 'descripcion'],
                       ['nombre', 'codename'],
                       ['#', 'Nombre', 'Codigo', 'Descripcion']),
    'ticketsdetail':  ('admin_apuestas', 'TicketsDetail',
                       ['id', 'ticket', 'jugada', 'monto', 'logro_apostado', 'puntaje_calculado'],
                       [],
                       ['#', 'Ticket', 'Jugada', 'Monto', 'Logro Apostado', 'Puntaje']),
    'ticketstatus':   ('admin_apuestas', 'TicketStatus',
                       ['id', 'ticket', 'status', 'startdate', 'enddate'],
                       [],
                       ['#', 'Ticket', 'Status', 'Inicio', 'Fin']),
    'ticketsdetailstatus': ('admin_apuestas', 'TicketsDetailStatus',
                            ['id', 'detalle_ticket', 'status', 'startdate', 'enddate'],
                            [],
                            ['#', 'Detalle', 'Status', 'Inicio', 'Fin']),
    # FINANZAS
    'bancos':         ('admin_finanzas', 'Banco',
                       ['id', 'nombre', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Creado']),
    'tipocuenta':     ('admin_finanzas', 'TipoCuenta',
                       ['id', 'codigo', 'nombre', 'created_at'],
                       ['nombre', 'codigo'],
                       ['#', 'Codigo', 'Nombre', 'Creado']),
    'tipomovimiento': ('admin_finanzas', 'TipoMovimiento',
                       ['id', 'codename', 'nombre', 'description'],
                       ['nombre', 'codename'],
                       ['#', 'Codigo', 'Nombre', 'Descripcion']),
    'comercializadoras': ('admin_finanzas', 'Comercializadora',
                          ['id', 'operadora', 'banca', 'taquilla', 'saldo_inicial', 'saldo_fecha'],
                          [],
                          ['#', 'Operadora', 'Banca', 'Taquilla', 'Saldo Inicial', 'Fecha Saldo']),
    'configuracion':  ('admin_finanzas', 'Configuracion',
                       ['id', 'created_at'],
                       [],
                       ['#', 'Creado']),
    'cuentas':        ('admin_finanzas', 'Cuenta',
                       ['id', 'created_at'],
                       [],
                       ['#', 'Creado']),
    'dias':           ('admin_finanzas', 'Dia',
                       ['id', 'created_at'],
                       [],
                       ['#', 'Creado']),
    'movimientos':    ('admin_finanzas', 'Movimiento',
                       ['id', 'created_at'],
                       [],
                       ['#', 'Creado']),
    'estatocuenta':   ('admin_finanzas', 'EstatoCuenta',
                       ['id', 'dia', 'cuenta', 'saldo', 'created_at'],
                       [],
                       ['#', 'Dia', 'Cuenta', 'Saldo', 'Creado']),
    'diatrabajo':     ('admin_finanzas', 'DiaTrabajo',
                       ['id', 'comercializadora', 'dia', 'procesado', 'actual', 'created_at'],
                       [],
                       ['#', 'Comercializadora', 'Dia', 'Procesado', 'Actual', 'Creado']),
    'resumenadminfinanzas': ('admin_finanzas', 'ResumenAdministrativo',
                             ['id', 'dia', 'venta', 'premio', 'comision', 'regalia', 'queda'],
                             [],
                             ['#', 'Dia', 'Venta', 'Premio', 'Comisión', 'Regalía', 'Queda']),
    # CONFIG COMERCIAL
    'tipoporcentajes': ('admin_comercializacion', 'TipoPorcentajes',
                        ['id', 'nombre', 'codename', 'orden', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla'],
                        ['nombre', 'codename'],
                        ['#', 'Nombre', 'Codename', 'Orden', 'Bloque', 'Banca', 'Distr.', 'Agencia', 'Taquilla']),
    'cupos':            ('admin_comercializacion', 'Cupos',
                        ['id', 'fecha_inicio', 'fecha_fin', 'monto_diario', 'monto_premio'],
                        [],
                        ['#', 'Fecha Inicio', 'Fecha Fin', 'Monto Diario', 'Monto Premio']),
    'porcentajes':      ('admin_comercializacion', 'Porcentajes',
                        ['id', 'tipo', 'fecha_inicio', 'fecha_fin', 'porcentaje_ganancia', 'porcentaje_maximo'],
                        [],
                        ['#', 'Tipo', 'Desde', 'Hasta', '% Ganancia', '% Máximo']),
    'factorriesgo':     ('admin_comercializacion', 'FactorRiesgo',
                        ['id', 'factores', 'comercializadora', 'created_at'],
                        ['factores'],
                        ['#', 'Factores', 'Comercializadora', 'Creado']),
    'datadefault':      ('admin_comercializacion', 'DataDefault',
                        ['id', 'user_type', 'cupo', 'porcentaje_comision', 'porcentaje_regalia', 'factor_riesgo'],
                        [],
                        ['#', 'Tipo Usuario', 'Cupo', '% Comisión', '% Regalía', 'Factor Riesgo']),
    # STATUS
    'statuslist':     ('admin_status', 'Status',
                       ['id', 'name', 'codename', 'content_type', 'order'],
                       ['name', 'codename'],
                       ['#', 'Nombre', 'Codigo', 'Tipo', 'Orden']),
    # AUTH
    'usuarios':       ('auth', 'User',
                       ['id', 'username', 'email', 'is_staff', 'is_active', 'date_joined'],
                       ['username', 'email', 'first_name', 'last_name'],
                       ['#', 'Usuario', 'Email', 'Staff', 'Activo', 'Registrado']),
    'gruposadmin':    ('auth', 'Group',
                       ['id', 'name'],
                       ['name'],
                       ['#', 'Nombre']),
    # TEMAS / PLANTILLAS INTERNAS
    'themes':         ('admin_themes', 'Theme',
                       ['id', 'name', 'codename', 'description', 'template_dir', 'static_url', 'media_url'],
                       ['name', 'codename', 'description'],
                       ['#', 'Nombre', 'Codename', 'Descripción', 'Template Dir', 'Static URL', 'Media URL']),
    'company':        ('admin_themes', 'Company',
                       ['id', 'name', 'created_at'],
                       ['name'],
                       ['#', 'Empresa', 'Creado']),
    # TEMAS — Colores
    'colores':        ('admin_themes', 'Color',
                       ['id', 'theme', 'color', 'color_type', 'created_at'],
                       ['color'],
                       ['#', 'Tema', 'Color', 'Tipo', 'Creado']),
    # STATUS — Detalles
    'statusdetail':   ('admin_status', 'StatusDetail',
                       ['id', 'status', 'user', 'startdate', 'enddate', 'comment'],
                       [],
                       ['#', 'Status', 'Usuario', 'Inicio', 'Fin', 'Comentario']),
    'taquillastatusdetail': ('admin_status', 'TaquillaStatusDetail',
                             ['id', 'status', 'usuariotaquilla', 'startdate', 'enddate', 'comment'],
                             [],
                             ['#', 'Status', 'Usuario Taquilla', 'Inicio', 'Fin', 'Comentario']),
    # RESULTADOS
    'resultadossorteo': ('admin_resultados', 'Resultados',
                         ['id', 'encuentro', 'sistema', 'status', 'processed', 'created_at'],
                         [],
                         ['#', 'Encuentro', 'Sistema', 'Status', 'Procesado', 'Creado']),
    'resultadosrestric': ('admin_resultados', 'ResultadosRestric',
                          ['id', 'resultado', 'grupo', 'modalidad'],
                          [],
                          ['#', 'Resultado', 'Grupo', 'Modalidad']),
    'anotaciones':    ('admin_resultados', 'Anotaciones',
                       ['id', 'resultado', 'grupo', 'created_at'],
                       [],
                       ['#', 'Resultado', 'Grupo', 'Creado']),
    'anotacionesdetail': ('admin_resultados', 'AnotacionesDetail',
                          ['id', 'anotacion', 'condicion', 'puntaje', 'referencia', 'created_at'],
                          [],
                          ['#', 'Anotacion', 'Condicion', 'Puntaje', 'Referencia', 'Creado']),
    # PERMISOLOGÍA
    'menus':          ('admin_permisologia', 'Menu',
                       ['id', 'name', 'codename', 'url', 'icon', 'orden', 'is_view'],
                       ['name', 'codename'],
                       ['#', 'Nombre', 'Codigo', 'URL', 'Icono', 'Orden', 'Vista']),
    'permisos':       ('admin_permisologia', 'Permissions',
                       ['id', 'name', 'codename', 'content_type', 'created_at'],
                       ['name', 'codename'],
                       ['#', 'Nombre', 'Codigo', 'Tipo', 'Creado']),
    'grupospermisologia': ('admin_permisologia', 'Groups',
                           ['id', 'name', 'codename', 'created_at'],
                           ['name', 'codename'],
                           ['#', 'Nombre', 'Codigo', 'Creado']),
    'permisosventas': ('admin_permisologia', 'PermissionsSales',
                       ['id', 'deporte', 'grupo', 'modalidad', 'breaking', 'created_at'],
                       [],
                       ['#', 'Deporte', 'Grupo', 'Modalidad', 'Breaking', 'Creado']),
    'permisosventasrestric': ('admin_permisologia', 'PermissionsSalesRestrictions',
                              ['id', 'comercializadora', 'deporte', 'created_at'],
                              [],
                              ['#', 'Comercializadora', 'Deporte', 'Creado']),
    # PERFILES GEOGRÁFICOS
    'paises':         ('admin_profiles', 'Paises',
                       ['id', 'nombre', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Creado']),
    'estados':        ('admin_profiles', 'Estados',
                       ['id', 'nombre', 'pais', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Pais', 'Creado']),
    'municipios':     ('admin_profiles', 'Municipios',
                       ['id', 'nombre', 'capital', 'estado', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Capital', 'Estado', 'Creado']),
    'parroquias':     ('admin_profiles', 'Parroquias',
                       ['id', 'nombre', 'municipio', 'created_at'],
                       ['nombre'],
                       ['#', 'Nombre', 'Municipio', 'Creado']),
    'direcciones':    ('admin_profiles', 'Direcciones',
                       ['id', 'direccion', 'parroquia', 'municipio', 'estado', 'created_at'],
                       ['direccion'],
                       ['#', 'Dirección', 'Parroquia', 'Municipio', 'Estado', 'Creado']),
    # HISTÓRICO
    'usersprocesos':  ('admin_historic', 'UsersProcesses',
                       ['id', 'name', 'codename', 'content_type', 'created_at'],
                       ['name', 'codename'],
                       ['#', 'Nombre', 'Codigo', 'Tipo', 'Creado']),
    'sesiones':       ('admin_historic', 'Sessions',
                       ['id', 'user', 'ip', 'startdate', 'enddate', 'created_at'],
                       [],
                       ['#', 'Usuario', 'IP', 'Inicio', 'Fin', 'Creado']),
    'sesionesdetail': ('admin_historic', 'SessionsDetail',
                       ['id', 'session', 'userprocess', 'created_at'],
                       [],
                       ['#', 'Sesion', 'Proceso', 'Creado']),
    'taquillasesiones': ('admin_historic', 'TaquillaSessions',
                         ['id', 'user', 'ip', 'startdate', 'enddate', 'created_at'],
                         [],
                         ['#', 'Usuario', 'IP', 'Inicio', 'Fin', 'Creado']),
    'taquillasesionesdetail': ('admin_historic', 'TaquillaSessionsDetail',
                               ['id', 'session', 'userprocess', 'enrro', 'created_at'],
                               [],
                               ['#', 'Sesion', 'Proceso', 'Error', 'Creado']),
}


def _fmt_value(val):
    """Convierte cualquier valor a string serializable para JSON."""
    if val is None:
        return '-'
    if isinstance(val, bool):
        return 'SI' if val else 'NO'
    if hasattr(val, 'strftime'):
        try:
            return val.strftime('%d/%m/%Y %H:%M')
        except Exception:
            return val.strftime('%d/%m/%Y')
    return str(val)


@staff_member_required(login_url='/admin/login/')
def dashboard_api(request, modulo):
    """
    GET /dashboard/api/<modulo>/?page=1&search=texto
    Retorna JSON paginado con filas del modelo solicitado.
    """
    from django.apps import apps
    from django.core.paginator import Paginator
    from django.db.models import Q

    PAGE_SIZE = 25

    if modulo not in _MODULES:
        return JsonResponse(
            {'error': f'Modulo "{modulo}" no registrado.'},
            status=404
        )

    app_label, model_name, fields, search_fields, columns = _MODULES[modulo]

    try:
        Model = apps.get_model(app_label, model_name)
    except LookupError:
        return JsonResponse(
            {'error': f'Modelo {app_label}.{model_name} no encontrado'},
            status=500
        )

    try:
        qs = Model.objects.all().order_by('-pk')

        # Busqueda
        search = request.GET.get('search', '').strip()
        if search and search_fields:
            q = Q()
            for sf in search_fields:
                q |= Q(**{f'{sf}__icontains': search})
            qs = qs.filter(q)

        total = qs.count()

        # Paginacion
        page_num = max(1, int(request.GET.get('page', 1)))
        paginator = Paginator(qs, PAGE_SIZE)
        page_obj = paginator.get_page(page_num)

        # Serializar filas
        rows = []
        for obj in page_obj:
            cells = []
            for f in fields:
                try:
                    cells.append(_fmt_value(getattr(obj, f)))
                except AttributeError:
                    cells.append('-')
            rows.append({'id': obj.pk, 'cells': cells})

        admin_model_name = Model._meta.model_name
        admin_url = f'/admin/{app_label}/{admin_model_name}/'

        return JsonResponse({
            'modulo':    modulo,
            'total':     total,
            'page':      page_num,
            'pages':     paginator.num_pages,
            'columns':   columns,
            'rows':      rows,
            'admin_url': admin_url,
            'add_url':   admin_url + 'add/',
        }, json_dumps_params={'ensure_ascii': False})

    except Exception as e:
        import traceback
        return JsonResponse(
            {'error': str(e), 'trace': traceback.format_exc()},
            status=500
        )


# ─────────────────────────────────────────────────────────────────────────────
#  CRUD API — Permite crear, editar y eliminar desde el SPA del dashboard
#  Métodos: GET (schema+datos), POST (crear), PUT (editar), DELETE (borrar)
# ─────────────────────────────────────────────────────────────────────────────

_CRUD_FIELDS = {
    # ── TEMAS / PLANTILLAS ─────────────────────────────────────────────────────
    'themes': {
        'model': ('admin_themes', 'Theme'),
        'fields': ['name', 'codename', 'description', 'template_dir', 'static_url', 'media_url'],
        'labels': ['Nombre (*)', 'Codename (*)', 'Descripción (*)', 'Directorio Template (*)', 'URL Estáticos (*)', 'URL Media (*)'],
        'required': ['name', 'codename', 'description', 'template_dir', 'static_url', 'media_url'],
        'types':    ['text', 'text', 'text', 'text', 'text', 'text'],
        'fk_fields': {},
    },
    'company': {
        'model': ('admin_themes', 'Company'),
        'fields': ['name'],
        'labels': ['Nombre de la Empresa (*)'],
        'required': ['name'],
        'types': ['text'],
        'fk_fields': {},
    },
    # ── SISTEMA DE JUEGO ───────────────────────────────────────────────────────
    'sistemajuego': {
        'model': ('admin_juego', 'SistemaJuego'),
        'fields': ['nombre', 'notificacion_automatica'],
        'labels': ['Nombre (*)', 'Notificación Automática'],
        'required': ['nombre'],
        'types': ['text', 'checkbox'],
        'fk_fields': {
            'theme': {'model': ('admin_themes', 'Theme'), 'label_field': 'name'},
        },
    },
    # ── TIPOS DE PRODUCTO ──────────────────────────────────────────────────────
    'tipoproducto': {
        'model': ('admin_juego', 'TipoProducto'),
        'fields': ['nombre'],
        'labels': ['Nombre de la Modalidad (*)'],
        'required': ['nombre'],
        'types': ['text'],
        'fk_fields': {
            'deporte': {'model': ('admin_juego', 'TipoProducto'), 'label_field': 'nombre'},
        },
    },
    # ── LOTERÍAS ───────────────────────────────────────────────────────────────
    'loterias': {
        'model': ('admin_juego', 'Loteria'),
        'fields': ['nombre', 'activo', 'orden'],
        'labels': ['Nombre (*)', 'Activa', 'Orden de presentación'],
        'required': ['nombre'],
        'types': ['text', 'checkbox', 'number'],
        'fk_fields': {},
    },
    # ── PRODUCTOS LOTERÍA (Modalidades) ────────────────────────────────────────
    'productoloteria': {
        'model': ('admin_juego', 'ProductoLoteria'),
        'fields': [
            'nombre_producto', 'tipo', 'multiplicador_pago',
            'cupo_por_numero', 'digitos_requeridos', 'es_terminal',
            'requiere_signo', 'activo', 'orden',
        ],
        'labels': [
            'Nombre de la Modalidad (*)', 'Tipo (*)', 'Multiplicador de Pago (*)',
            'Cupo máximo por número', 'Dígitos requeridos', '¿Es Terminal?',
            '¿Requiere Signo Zodiacal?', 'Activo', 'Orden',
        ],
        'required': ['nombre_producto', 'tipo', 'multiplicador_pago'],
        'types': [
            'text', 'select', 'number',
            'number', 'number', 'checkbox',
            'checkbox', 'checkbox', 'number',
        ],
        'fk_fields': {
            'loteria': {'model': ('admin_juego', 'Loteria'), 'label_field': 'nombre'},
        },
        'choices': {
            'tipo': [
                ('NUMERICO',   'Numérico (Triples/Terminal/Arrimao/Pegadito)'),
                ('ANIMALITOS', 'Animalitos (por figura)'),
            ],
        },
    },
    # ── PLANTILLAS DE PRODUCTO (PlantillaProducto) ─────────────────────────────
    'plantillas': {
        'model': ('admin_juego', 'PlantillaProducto'),
        'fields': ['nombre', 'descripcion', 'activo', 'animalito_min', 'animalito_max',
                   'usa_doble_cara', 'usa_signo', 'orden'],
        'labels': ['Nombre (*)', 'Descripción', 'Activo', 'Figura mínima', 'Figura máxima',
                   'Doble cara (A/B)', 'Acepta signo', 'Orden'],
        'required': ['nombre'],
        'types': ['text', 'text', 'checkbox', 'number', 'number',
                  'checkbox', 'checkbox', 'number'],
        'fk_fields': {},
    },
    # ── ANIMALITOS ─────────────────────────────────────────────────────────────
    'animalitos': {
        'model': ('admin_juego', 'Animalito'),
        'fields': ['numero', 'nombre', 'activo'],
        'labels': ['Número/Figura (*)', 'Nombre del animal (*)', 'Activo'],
        'required': ['numero', 'nombre'],
        'types': ['text', 'text', 'checkbox'],
        'fk_fields': {},
    },
    # ── GRUPO DE ANIMALES ──────────────────────────────────────────────────────
    'grupoanimales': {
        'model': ('admin_juego', 'GrupoAnimales'),
        'fields': ['nombre', 'descripcion', 'activo'],
        'labels': ['Nombre (*)', 'Descripción', 'Activo'],
        'required': ['nombre'],
        'types': ['text', 'text', 'checkbox'],
        'fk_fields': {},
    },
    # ── SORTEOS ────────────────────────────────────────────────────────────────
    'sorteos': {
        'model': ('admin_juego', 'SorteoArrejuntao'),
        'fields': ['descripcion', 'hora_sorteo', 'minutos_cierre', 'activo'],
        'labels': ['Descripción (*)', 'Hora del Sorteo (*)', 'Minutos de cierre previo', 'Activo (Abierto/Cerrado)'],
        'required': ['descripcion', 'hora_sorteo'],
        'types': ['text', 'time', 'number', 'checkbox'],
        'fk_fields': {},
    },
    # ── OPERADORAS ── formulario completo ─────────────────────────────────────
    'operadoras': {
        'model': ('admin_comercializacion', 'Operadoras'),
        'fields': [
            'nombre', 'resumen_automatic', 'telefono', 'rif', 'email',
            'status',
        ],
        'labels': [
            'Nombre (*)', 'Cierre Administrativo Automático', 'Número Telefónico', 'RIF', 'Correo Electrónico',
            'Status',
        ],
        'required': ['nombre'],
        'types': [
            'text', 'checkbox', 'text', 'text', 'email',
            'fk',
        ],
        'fk_fields': {
            'status': {'model': ('admin_status', 'Status'), 'label_field': 'name'},
        },
    },
    # ── BANCAS ── formulario completo ─────────────────────────────────────────
    'bancas': {
        'model': ('admin_comercializacion', 'Bancas'),
        'fields': [
            'nombre', 'resumen_automatic', 'telefono', 'rif', 'email',
            'is_sistema_juego', 'is_resultados',
            'permissions_create_user',
            'virtual_username', 'virtual_password',
        ],
        'labels': [
            'Nombre (*)', 'Cierre Administrativo Automático', 'Número Telefónico', 'RIF', 'Correo Electrónico',
            '¿Administra su propio Sistema de Juego?', '¿Administra sus propios resultados?',
            '¿Tiene permiso de crear usuarios de su mismo nivel?',
            'Usuario (Opcional - Crea un usuario para esta banca)', 'Contraseña (Opcional)',
        ],
        'required': ['nombre', 'bloque'],
        'types': [
            'text', 'checkbox', 'text', 'text', 'email',
            'checkbox', 'checkbox',
            'checkbox',
            'text', 'password',
        ],
        'virtual_fields': ['virtual_username', 'virtual_password'],
        'fk_fields': {
            'status': {'model': ('admin_status', 'Status'),           'label_field': 'name'},
            'bloque': {'model': ('admin_comercializacion', 'Bloques'), 'label_field': 'nombre'},
        },
    },
    # ── CENTRO DE APUESTA (Agencias) ── formulario completo ─────────────────
    'agencias': {
        'model': ('admin_comercializacion', 'Agencias'),
        'fields': [
            'nombre', 'codigo', 'rif', 'telefono', 'email',
            'num_taquillas', 'montomin', 'montomax', 'montomax_ganancia',
            'cantidad_apuesta_min', 'cantidad_apuesta_max',
            'tiempoexpiracion',
            'monto_alquiler', 'frecuencia_monto_alquiler',
            'factor_riesgo', 'frecuencia_queda',
            'parley_clonados_maxima_ganancia',
            'ticket_titulo', 'ticket_pie',
            'resumen_automatic',
        ],
        'labels': [
            'Nombre (*)', 'Código (*)', 'RIF', 'Teléfono', 'Email',
            'Nro Taquillas', 'Monto Mín', 'Monto Máx', 'Máx Ganancia',
            'Apuesta Mín (cant)', 'Apuesta Máx (cant)',
            'Tiempo Expiración (seg)',
            'Monto Alquiler', 'Frecuencia Alquiler',
            'Factor Riesgo', 'Frecuencia Queda',
            'Máx Ganancia Clonado',
            'Título Ticket', 'Pie Ticket',
            'Resumen Automático',
        ],
        'required': ['nombre', 'codigo', 'distribuidores'],
        'types': [
            'text', 'text', 'text', 'text', 'email',
            'number', 'number', 'number', 'number',
            'number', 'number',
            'number',
            'number', 'text',
            'number', 'text',
            'number',
            'text', 'text',
            'checkbox',
        ],
        'fk_fields': {
            'distribuidores': {'model': ('admin_comercializacion', 'Distribuidores'), 'label_field': 'nombre'},
        },
    },
    'taquillas': {
        'model': ('admin_comercializacion', 'Taquillas'),
        'fields': ['taquilla', 'serial', 'agencia', 'monto_alquiler', 'is_taquilla_master'],
        'labels': ['Nombre Taquilla (*)', 'Serial (*)', 'Agencia (Centro Apuesta) (*)', 'Monto Alquiler', 'Es Master'],
        'required': ['taquilla', 'serial', 'agencia'],
        'types': ['text', 'text', 'fk', 'number', 'checkbox'],
        'fk_fields': {
            'agencia': {'model': ('admin_comercializacion', 'Agencias'), 'label_field': 'nombre'},
        },
    },
    # ── MULTI BANCA (Bloques) ── formulario completo igual al Django Admin ─────
    'bloques': {
        'model': ('admin_comercializacion', 'Bloques'),
        'fields': [
            'nombre', 'resumen_automatic', 'telefono', 'rif', 'email',
            'is_sistema_juego', 'is_resultados',
            'permissions_create_user', 'tipo',
            'virtual_username', 'virtual_password',
        ],
        'labels': [
            'Nombre (*)', 'Cierre Administrativo Automático', 'Número Telefónico', 'RIF', 'Correo Electrónico',
            '¿Administra su propio Sistema de Juego?', '¿Administra sus propios resultados?',
            '¿Tiene permiso de crear usuarios de su mismo nivel?', '¿Para venta web?',
            'Usuario (Opcional - Crea un usuario para este bloque)', 'Contraseña (Opcional)',
        ],
        'required': ['nombre', 'operadora'],
        'types': [
            'text', 'checkbox', 'text', 'text', 'email',
            'checkbox', 'checkbox',
            'checkbox', 'checkbox',
            'text', 'password',
        ],
        'virtual_fields': ['virtual_username', 'virtual_password'],
        'fk_fields': {
            'status':    {'model': ('admin_status', 'Status'),              'label_field': 'name'},
            'operadora': {'model': ('admin_comercializacion', 'Operadoras'), 'label_field': 'nombre'},
        },
    },
    # ── DISTRIBUIDORES ── formulario completo ─────────────────────────────────
    'distribuidores': {
        'model': ('admin_comercializacion', 'Distribuidores'),
        'fields': [
            'nombre', 'resumen_automatic', 'telefono', 'rif', 'email',
            'status', 'banca',
            'is_sistema_juego', 'is_resultados',
            'permissions_create_user', 'tipo',
        ],
        'labels': [
            'Nombre (*)', 'Cierre Administrativo Automático', 'Número Telefónico', 'RIF', 'Correo Electrónico',
            'Status', 'Banca (*)',
            '¿Administra su propio Sistema de Juego?', '¿Administra sus propios resultados?',
            '¿Tiene permiso de crear usuarios de su mismo nivel?', '¿Para venta web?',
        ],
        'required': ['nombre', 'banca'],
        'types': [
            'text', 'checkbox', 'text', 'text', 'email',
            'fk', 'fk',
            'checkbox', 'checkbox',
            'checkbox', 'checkbox',
        ],
        'fk_fields': {
            'status': {'model': ('admin_status', 'Status'),           'label_field': 'name'},
            'banca':  {'model': ('admin_comercializacion', 'Bancas'), 'label_field': 'nombre'},
        },
    },
    # (agencias ya definida arriba como Centro de Apuesta)
    'tipoporcentajes': {
        'model': ('admin_comercializacion', 'TipoPorcentajes'),
        'fields': ['nombre', 'codename', 'orden', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla'],
        'labels': ['Nombre (*)', 'Código (*)', 'Orden', 'Por Bloque', 'Por Banca', 'Por Distribuidor', 'Por Agencia', 'Por Taquilla'],
        'required': ['nombre', 'codename'],
        'types': ['text', 'text', 'number', 'checkbox', 'checkbox', 'checkbox', 'checkbox', 'checkbox'],
        'fk_fields': {},
    },
    'statuslist': {
        'model': ('admin_status', 'Status'),
        'fields': ['name', 'codename', 'content_type', 'order'],
        'labels': ['Nombre (*)', 'Código (*)', 'Tipo de Contenido (0-8)', 'Orden'],
        'required': ['name', 'codename'],
        'types': ['text', 'text', 'number', 'number'],
        'fk_fields': {},
    },
    # FINANZAS
    'bancos': {
        'model': ('admin_finanzas', 'Banco'),
        'fields': ['nombre'],
        'labels': ['Nombre del Banco (*)'],
        'required': ['nombre'],
        'types': ['text'],
        'fk_fields': {},
    },
    'tipocuenta': {
        'model': ('admin_finanzas', 'TipoCuenta'),
        'fields': ['codigo', 'nombre'],
        'labels': ['Código (*)', 'Nombre (*)'],
        'required': ['codigo', 'nombre'],
        'types': ['text', 'text'],
        'fk_fields': {},
    },
    'tipomovimiento': {
        'model': ('admin_finanzas', 'TipoMovimiento'),
        'fields': ['codename', 'nombre', 'description'],
        'labels': ['Código (*)', 'Nombre (*)', 'Descripción'],
        'required': ['codename', 'nombre'],
        'types': ['text', 'text', 'text'],
        'fk_fields': {},
    },
    # AUTH — Grupos
    'gruposadmin': {
        'model': ('auth', 'Group'),
        'fields': ['name'],
        'labels': ['Nombre del Grupo (*)'],
        'required': ['name'],
        'types': ['text'],
        'fk_fields': {},
    },
    # TEMAS — Empresas
    'company': {
        'model': ('admin_themes', 'Company'),
        'fields': ['name'],
        'labels': ['Nombre de la Empresa (*)'],
        'required': ['name'],
        'types': ['text'],
        'fk_fields': {},
    },
    # FINANZAS — Comercializadora (formulario completo igual al Django Admin)
    'comercializadoras': {
        'model': ('admin_finanzas', 'Comercializadora'),
        'fields': [
            'operadora', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla',
            'saldo_inicial', 'saldo_fecha',
            'resumen_personalizado',
        ],
        'labels': [
            'Operadora', 'Bloque (Multi Banca)', 'Banca', 'Distribuidor', 'Agencia', 'Taquilla',
            'Saldo inicial (*)', 'Fecha de saldo inicial (*)',
            'Resumen personalizado',
        ],
        'required': ['saldo_inicial', 'saldo_fecha'],
        'types': [
            'fk', 'fk', 'fk', 'fk', 'fk', 'fk',
            'number', 'date',
            'checkbox',
        ],
        'fk_fields': {
            'operadora':    {'model': ('admin_comercializacion', 'Operadoras'),    'label_field': 'nombre'},
            'bloque':       {'model': ('admin_comercializacion', 'Bloques'),       'label_field': 'nombre'},
            'banca':        {'model': ('admin_comercializacion', 'Bancas'),        'label_field': 'nombre'},
            'distribuidor': {'model': ('admin_comercializacion', 'Distribuidores'),'label_field': 'nombre'},
            'agencia':      {'model': ('admin_comercializacion', 'Agencias'),      'label_field': 'nombre'},
            'taquilla':     {'model': ('admin_comercializacion', 'Taquillas'),     'label_field': 'taquilla'},
        },
    },
    # ── USUARIO DE TAQUILLA ── formulario completo igual al Django Admin ──────────────
    'usuariostaquilla': {
        'model': ('admin_comercializacion', 'UsuariosTaquilla'),
        # 'new_password' es virtual: no mapea a un campo real del modelo,
        # se intercepta abajo mediante set_password()
        'fields': ['user', 'nombre', 'new_password'],
        'labels': [
            'Usuario (*)',
            'Nombre (*)',
            'Nueva Contraseña (dejar en blanco para no cambiar)',
        ],
        'required': ['user'],
        'types':  ['text', 'text', 'password'],
        # virtual_fields: campos que NO existen en el modelo y se manejan aparte
        'virtual_fields': ['new_password'],
        'fk_fields': {
            'taquilla': {'model': ('admin_comercializacion', 'Taquillas'),  'label_field': 'taquilla'},
            'status':   {'model': ('admin_status',           'Status'),     'label_field': 'name'},
        },
    },
    # ── USUARIOS GENERALES ── formulario completo ─────────────────────────────
    'usuarios': {
        'model': ('admin_users', 'Users'),
        'fields': ['user', 'email', 'etiqueta', 'new_password', 'profile'],
        'labels': [
            'Nombre de Usuario (*)',
            'Correo Electrónico',
            'Nombre o Etiqueta (Ej. Pedro Pérez)',
            'Nueva Contraseña (dejar en blanco para no cambiar)',
            'Perfil (Rol)'
        ],
        'required': ['user', 'profile'],
        'types': ['text', 'email', 'text', 'password', 'fk'],
        'virtual_fields': ['new_password'],
        'fk_fields': {
            'profile': {'model': ('admin_users', 'UserProfile'), 'label_field': 'nombre'},
        },
    },
    # ── APUESTAS / TICKETS ──────────────────────────────────────────────────────
    'tickets': {
        'model': ('admin_apuestas', 'Tickets'),
        'fields': ['key', 'monto', 'monto_premio', 'monto_ganancia', 'fecha', 'puntaje_calculado', 'pks_jugadas'],
        'labels': ['Clave (Key)', 'Monto (*)', 'Monto Premio (*)', 'Monto Ganancia (*)', 'Fecha (*)', 'Puntaje Calculado', 'Pks Jugadas'],
        'required': ['monto', 'monto_premio', 'monto_ganancia', 'fecha'],
        'types':    ['text', 'number', 'number', 'number', 'datetime-local', 'number', 'text'],
        'fk_fields': {
            'user':        {'model': ('admin_comercializacion', 'UsuariosTaquilla'), 'label_field': '__str__'},
            'ticket_type': {'model': ('admin_juego',            'apuesta'),          'label_field': '__str__'},
            'status':      {'model': ('admin_status',           'Status'),           'label_field': 'name'},
        },
    },
    'ticketstype': {
        'model': ('admin_apuestas', 'TicketsType'),
        'fields': ['nombre', 'codename', 'descripcion'],
        'labels': ['Nombre (*)', 'Codename (*)', 'Descripción (*)'],
        'required': ['nombre', 'codename', 'descripcion'],
        'types':    ['text', 'text', 'text'],
        'fk_fields': {},
    },
    'ticketsdetail': {
        'model': ('admin_apuestas', 'TicketsDetail'),
        'fields': ['monto', 'logro_apostado', 'puntaje_calculado', 'puntaje_apostado', 'modalidad_ref', 'condicion_ref'],
        'labels': ['Monto (*)', 'Logro Apostado', 'Puntaje Calculado', 'Puntaje Apostado', 'Modalidad Ref', 'Condición Ref'],
        'required': ['monto'],
        'types':    ['number', 'number', 'number', 'number', 'text', 'text'],
        'fk_fields': {
            'jugada':  {'model': ('admin_juego',    'apuesta'),   'label_field': '__str__'},
            'ticket':  {'model': ('admin_apuestas', 'Tickets'),   'label_field': '__str__'},
            'status':  {'model': ('admin_status',   'Status'),    'label_field': 'name'},
        },
    },
    'ticketstatus': {
        'model': ('admin_apuestas', 'TicketStatus'),
        'fields': ['startdate', 'enddate'],
        'labels': ['Fecha Inicio (*)', 'Fecha Fin'],
        'required': ['startdate'],
        'types':    ['datetime-local', 'datetime-local'],
        'fk_fields': {
            'ticket': {'model': ('admin_apuestas', 'Tickets'), 'label_field': '__str__'},
            'status': {'model': ('admin_status',   'Status'),  'label_field': 'name'},
        },
    },
    'ticketsdetailstatus': {
        'model': ('admin_apuestas', 'TicketsDetailStatus'),
        'fields': ['startdate', 'enddate'],
        'labels': ['Fecha Inicio (*)', 'Fecha Fin'],
        'required': ['startdate'],
        'types':    ['datetime-local', 'datetime-local'],
        'fk_fields': {
            'detalle_ticket': {'model': ('admin_apuestas', 'TicketsDetail'), 'label_field': '__str__'},
            'status':         {'model': ('admin_status',   'Status'),        'label_field': 'name'},
        },
    },
    # ── FINANZAS ─────────────────────────────────────────────────────────────
    'bancos': {
        'model': ('admin_finanzas', 'Banco'),
        'fields': ['nombre'],
        'labels': ['Nombre (*)'],
        'required': ['nombre'],
        'types': ['text'],
        'fk_fields': {},
    },
    'tipocuenta': {
        'model': ('admin_finanzas', 'TipoCuenta'),
        'fields': ['nombre', 'codigo'],
        'labels': ['Nombre (*)', 'Código (*)'],
        'required': ['nombre', 'codigo'],
        'types': ['text', 'text'],
        'fk_fields': {},
    },
    'tipomovimiento': {
        'model': ('admin_finanzas', 'TipoMovimiento'),
        'fields': ['nombre', 'codename', 'description'],
        'labels': ['Nombre (*)', 'Codename (*)', 'Descripción'],
        'required': ['nombre', 'codename'],
        'types': ['text', 'text', 'text'],
        'fk_fields': {},
    },
    'comercializadoras': {
        'model': ('admin_finanzas', 'Comercializadora'),
        'fields': ['saldo_inicial', 'saldo_fecha', 'resumen_personalizado'],
        'labels': ['Saldo Inicial', 'Fecha Saldo', 'Resumen Personalizado'],
        'required': [],
        'types': ['number', 'date', 'checkbox'],
        'fk_fields': {
            'operadora':    {'model': ('admin_comercializacion', 'Operadoras'),     'label_field': 'nombre'},
            'bloque':       {'model': ('admin_comercializacion', 'Bloques'),        'label_field': 'nombre'},
            'banca':        {'model': ('admin_comercializacion', 'Bancas'),         'label_field': 'nombre'},
            'distribuidor': {'model': ('admin_comercializacion', 'Distribuidores'), 'label_field': 'nombre'},
            'agencia':      {'model': ('admin_comercializacion', 'Agencias'),       'label_field': 'nombre'},
            'taquilla':     {'model': ('admin_comercializacion', 'Taquillas'),      'label_field': '__str__'},
        },
    },
    'cuentas': {
        'model': ('admin_finanzas', 'Cuenta'),
        'fields': ['numero', 'description'],
        'labels': ['Número de Cuenta (*)', 'Descripción'],
        'required': ['numero'],
        'types': ['text', 'text'],
        'fk_fields': {
            'comercializadora': {'model': ('admin_finanzas', 'Comercializadora'), 'label_field': '__str__'},
            'banco':            {'model': ('admin_finanzas', 'Banco'),            'label_field': 'nombre'},
            'tipocuenta':       {'model': ('admin_finanzas', 'TipoCuenta'),       'label_field': 'nombre'},
        },
    },
    'dias': {
        'model': ('admin_finanzas', 'Dia'),
        'fields': ['fecha'],
        'labels': ['Fecha (*)'],
        'required': ['fecha'],
        'types': ['date'],
        'fk_fields': {},
    },
    'estatocuenta': {
        'model': ('admin_finanzas', 'EstatoCuenta'),
        'fields': ['saldo'],
        'labels': ['Saldo (*)'],
        'required': ['saldo'],
        'types': ['number'],
        'fk_fields': {
            'dia':    {'model': ('admin_finanzas', 'Dia'),    'label_field': 'fecha'},
            'cuenta': {'model': ('admin_finanzas', 'Cuenta'), 'label_field': 'numero'},
        },
    },
    'movimientos': {
        'model': ('admin_finanzas', 'Movimiento'),
        'fields': ['numero', 'monto', 'fecha', 'observacion'],
        'labels': ['Número (*)', 'Monto (*)', 'Fecha (*)', 'Observación'],
        'required': ['numero', 'monto', 'fecha', 'comercializadora', 'cuenta', 'tipo'],
        'types': ['text', 'number', 'date', 'text'],
        'fk_fields': {
            'comercializadora': {'model': ('admin_finanzas', 'Comercializadora'), 'label_field': '__str__'},
            'cuenta':           {'model': ('admin_finanzas', 'Cuenta'),           'label_field': 'numero'},
            'tipo':             {'model': ('admin_finanzas', 'TipoMovimiento'),   'label_field': 'nombre'},
        },
    },
    'diatrabajo': {
        'model': ('admin_finanzas', 'DiaTrabajo'),
        'fields': ['procesado', 'actual'],
        'labels': ['Procesado', 'Actual'],
        'required': [],
        'types': ['checkbox', 'checkbox'],
        'fk_fields': {
            'comercializadora': {'model': ('admin_finanzas', 'Comercializadora'), 'label_field': '__str__'},
            'dia':              {'model': ('admin_finanzas', 'Dia'),              'label_field': 'fecha'},
        },
    },
    # ── CONTABILIDAD / CONFIG COMERCIAL ──────────────────────────────────────
    'resumenadminfinanzas': {
        'model': ('admin_finanzas', 'ResumenAdministrativo'),
        'fields': [
            'venta', 'premio', 'comision', 'regalia', 'queda',
            'participacion', 'saldo_bruto', 'saldo_comer', 'saldo_oper',
            'deposito', 'pago', 'ajuste', 'cargo', 'saldo_anterior', 'saldo_actual',
        ],
        'labels': [
            'Venta', 'Premio', 'Comisión', 'Regalía', 'Queda',
            'Participación', 'Saldo Bruto', 'Saldo Comer.', 'Saldo Oper.',
            'Depósito', 'Pago', 'Ajuste', 'Cargo', 'Saldo Anterior', 'Saldo Actual',
        ],
        'required': [],
        'types': [
            'number', 'number', 'number', 'number', 'number',
            'number', 'number', 'number', 'number',
            'number', 'number', 'number', 'number', 'number', 'number',
        ],
        'fk_fields': {
            'dia':             {'model': ('admin_finanzas', 'Dia'),              'label_field': 'fecha'},
            'comercializacion': {'model': ('admin_finanzas', 'Comercializadora'),'label_field': '__str__'},
        },
    },
    'tipoporcentajes': {
        'model': ('admin_comercializacion', 'TipoPorcentajes'),
        'fields': ['nombre', 'codename', 'orden', 'bloque', 'banca', 'distribuidor', 'agencia', 'taquilla'],
        'labels': ['Nombre (*)', 'Codename (*)', 'Orden (*)', 'Por Bloque', 'Por Banca', 'Por Distribuidor', 'Por Agencia', 'Por Taquilla'],
        'required': ['nombre', 'codename', 'orden'],
        'types': ['text', 'text', 'number', 'checkbox', 'checkbox', 'checkbox', 'checkbox', 'checkbox'],
        'fk_fields': {},
    },
    'cupos': {
        'model': ('admin_comercializacion', 'Cupos'),
        'fields': ['fecha_inicio', 'fecha_fin', 'monto_diario', 'monto_premio'],
        'labels': ['Fecha Inicio (*)', 'Fecha Fin', 'Monto Diario (*)', 'Monto Premio'],
        'required': ['fecha_inicio', 'monto_diario'],
        'types': ['datetime-local', 'datetime-local', 'number', 'number'],
        'fk_fields': {
            'operadora':     {'model': ('admin_comercializacion', 'Operadoras'),     'label_field': 'nombre'},
            'bloque':        {'model': ('admin_comercializacion', 'Bloques'),        'label_field': 'nombre'},
            'banca':         {'model': ('admin_comercializacion', 'Bancas'),         'label_field': 'nombre'},
            'distribuidor':  {'model': ('admin_comercializacion', 'Distribuidores'), 'label_field': 'nombre'},
            'agencia':       {'model': ('admin_comercializacion', 'Agencias'),       'label_field': 'nombre'},
        },
    },
    'porcentajes': {
        'model': ('admin_comercializacion', 'Porcentajes'),
        'fields': [
            'fecha_inicio', 'fecha_fin', 'relacion',
            'porcentaje_ganancia', 'porcentaje_maximo',
            'bloque_porc', 'banca_porc', 'distribuidor_porc', 'agencia_porc', 'taquilla_porc',
        ],
        'labels': [
            'Fecha Inicio (*)', 'Fecha Fin', '¿Relación?',
            '% Ganancia (*)', '% Máximo',
            '% Bloque', '% Banca', '% Distribuidor', '% Agencia', '% Taquilla',
        ],
        'required': ['fecha_inicio', 'porcentaje_ganancia'],
        'types': [
            'datetime-local', 'datetime-local', 'checkbox',
            'number', 'number',
            'number', 'number', 'number', 'number', 'number',
        ],
        'fk_fields': {
            'tipo':         {'model': ('admin_comercializacion', 'TipoPorcentajes'), 'label_field': 'nombre'},
            'operadora':    {'model': ('admin_comercializacion', 'Operadoras'),      'label_field': 'nombre'},
            'bloque':       {'model': ('admin_comercializacion', 'Bloques'),         'label_field': 'nombre'},
            'banca':        {'model': ('admin_comercializacion', 'Bancas'),          'label_field': 'nombre'},
            'distribuidor': {'model': ('admin_comercializacion', 'Distribuidores'),  'label_field': 'nombre'},
            'agencia':      {'model': ('admin_comercializacion', 'Agencias'),        'label_field': 'nombre'},
            'taquilla':     {'model': ('admin_comercializacion', 'Taquillas'),       'label_field': '__str__'},
        },
    },
    'factorriesgo': {
        'model': ('admin_comercializacion', 'FactorRiesgo'),
        'fields': ['factores'],
        'labels': ['Factores (JSON / texto) (*)'],
        'required': ['factores'],
        'types': ['text'],
        'fk_fields': {
            'comercializadora': {'model': ('admin_finanzas', 'Comercializadora'), 'label_field': '__str__'},
        },
    },
    'datadefault': {
        'model': ('admin_comercializacion', 'DataDefault'),
        'fields': [
            'cupo', 'porcentaje_comision', 'porcentaje_regalia',
            'porcentaje_participacion', 'porcentaje_queda', 'porcentaje_maximo',
            'monto_alquiler', 'frecuencia_monto_alquiler',
            'factor_riesgo', 'frecuencia_queda',
        ],
        'labels': [
            'Cupo', '% Comisión', '% Regalía',
            '% Participación', '% Queda', '% Máximo',
            'Monto Alquiler', 'Frecuencia Alquiler',
            'Factor Riesgo', 'Frecuencia Queda',
        ],
        'required': [],
        'types': [
            'number', 'number', 'number',
            'number', 'number', 'number',
            'number', 'text',
            'number', 'text',
        ],
        'fk_fields': {
            'user_type': {'model': ('admin_comercializacion', 'TipoPorcentajes'), 'label_field': 'nombre'},
        },
    },
    # ── PERMISOLOGÍA ─────────────────────────────────────────────────────────
    'menus': {
        'model': ('admin_permisologia', 'Menu'),
        'fields': ['name', 'codename', 'url', 'icon', 'content_type', 'orden', 'is_view', 'is_public', 'is_global'],
        'labels': [
            'Título', 'Código (*)', 'URL', 'Icono', 'Nivel',
            'Orden', 'Visible', 'Público', 'Global',
        ],
        'required': ['codename'],
        'types': ['text', 'text', 'text', 'text', 'number', 'number', 'checkbox', 'checkbox', 'checkbox'],
        'fk_fields': {
            'menu_suc': {'model': ('admin_permisologia', 'Menu'), 'label_field': '__str__'},
        },
    },
    'grupospermisologia': {
        'model': ('admin_permisologia', 'Groups'),
        'fields': ['name'],
        'labels': ['Nombre del grupo (*)'],
        'required': ['name'],
        'types': ['text'],
        'fk_fields': {},
    },
    'permisos': {
        'model': ('admin_permisologia', 'Permissions'),
        'fields': ['name', 'content_type'],
        'labels': ['Nombre (*)', 'App (*)'],
        'required': ['name', 'content_type'],
        'types': ['text', 'text'],
        'fk_fields': {},
    },
    'permisosventas': {
        'model': ('admin_permisologia', 'PermissionsSales'),
        'fields': ['deporte', 'grupo', 'modalidad', 'comercializadora', 'breaking'],
        'labels': ['Deporte (*)', 'Grupo (*)', 'Modalidad (*)', 'Comercializadora (*)', 'Breaking'],
        'required': ['deporte', 'grupo', 'modalidad', 'comercializadora'],
        'types': ['select', 'select', 'select', 'select', 'checkbox'],
        'fk_fields': {
            'deporte': {'model': ('admin_juego', 'TipoProducto'), 'label_field': 'nombre'},
            'grupo': {'model': ('admin_juego', 'GruposSorteo'), 'label_field': 'nombre'},
            'modalidad': {'model': ('admin_juego', 'ModalidadJuego'), 'label_field': 'nombre'},
            'comercializadora': {'model': ('admin_finanzas', 'Comercializadora'), 'label_field': 'nombre'},
        },
    },
    'permisosventasrestric': {
        'model': ('admin_permisologia', 'PermissionsSalesRestrictions'),
        'fields': ['comercializadora', 'deporte', 'restrictions'],
        'labels': ['Comercializadora (*)', 'Deporte (*)', 'Restricciones JSON'],
        'required': ['comercializadora', 'deporte'],
        'types': ['select', 'select', 'text'],
        'fk_fields': {
            'comercializadora': {'model': ('admin_finanzas', 'Comercializadora'), 'label_field': 'nombre'},
            'deporte': {'model': ('admin_juego', 'TipoProducto'), 'label_field': 'nombre'},
        },
    },
}



@staff_member_required(login_url='/admin/login/')
def dashboard_crud(request, modulo):
    """
    CRUD API para el SPA del dashboard (sin redirigir al Django Admin).
    GET    /dashboard/crud/<modulo>/      → schema del form
    GET    /dashboard/crud/<modulo>/?pk=X → datos del objeto X
    POST   /dashboard/crud/<modulo>/      → crear nuevo
    PUT    /dashboard/crud/<modulo>/?pk=X → actualizar
    DELETE /dashboard/crud/<modulo>/?pk=X → eliminar
    """
    from django.apps import apps

    if modulo not in _CRUD_FIELDS:
        return JsonResponse({'error': f'CRUD no disponible para "{modulo}"'}, status=404)

    cfg = _CRUD_FIELDS[modulo]
    app_label, model_name = cfg['model']
    try:
        Model = apps.get_model(app_label, model_name)
    except LookupError:
        return JsonResponse({'error': f'Modelo {model_name} no encontrado'}, status=500)

    pk = request.GET.get('pk')

    # ── GET: schema + datos del objeto ────────────────────────────────────────
    if request.method == 'GET':
        schema = {
            'fields':   cfg['fields'],
            'labels':   cfg['labels'],
            'required': cfg['required'],
            'types':    cfg['types'],
            'fk_fields': {},
            'choices':  cfg.get('choices', {}),
        }
        for fk_name, fk_cfg in cfg.get('fk_fields', {}).items():
            try:
                FkModel = apps.get_model(*fk_cfg['model'])
                label_f = fk_cfg['label_field']
                opts = []
                for obj in FkModel.objects.all().order_by('pk')[:300]:
                    label = str(obj) if label_f == '__str__' else str(getattr(obj, label_f, obj))
                    opts.append({'id': obj.pk, 'label': label})
                schema['fk_fields'][fk_name] = opts
            except Exception:
                schema['fk_fields'][fk_name] = []

        obj_data = None
        if pk:
            try:
                obj = Model.objects.get(pk=pk)
                obj_data = {}
                for f in cfg['fields']:
                    raw = getattr(obj, f, None)
                    if isinstance(raw, bool):
                        obj_data[f] = raw
                    else:
                        obj_data[f] = _fmt_value(raw)
                for fk_name in cfg.get('fk_fields', {}):
                    fk_val = getattr(obj, f'{fk_name}_id', None)
                    if fk_val:
                        obj_data[fk_name] = fk_val
            except Model.DoesNotExist:
                return JsonResponse({'error': 'No encontrado'}, status=404)
        return JsonResponse({'schema': schema, 'object': obj_data}, json_dumps_params={'ensure_ascii': False})

    # ── POST: crear ────────────────────────────────────────────────────────────
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
        except Exception:
            body = {k: v for k, v in request.POST.items()}
        kwargs = {}
        virtual = cfg.get('virtual_fields', [])
        fk_fields = set(cfg.get('fk_fields', {}).keys())
        for f in cfg['fields']:
            if f in virtual:
                continue          # Se maneja aparte (ej. new_password)
            if f in fk_fields:
                continue          # Los FK se asignan como {campo}_id en el bloque siguiente
            val = body.get(f, '')
            try:
                field_type = Model._meta.get_field(f).get_internal_type()
            except Exception:
                continue
            if field_type == 'BooleanField':
                val = val in (True, 'true', 'True', '1', 'on')
            elif field_type in ('IntegerField', 'DecimalField', 'FloatField') and val == '':
                val = None
            kwargs[f] = val
        for fk_name in cfg.get('fk_fields', {}):
            fk_val = body.get(fk_name)
            if fk_val:
                kwargs[f'{fk_name}_id'] = fk_val
        missing = []
        for f in cfg.get('required', []):
            if f in fk_fields:
                if not kwargs.get(f'{f}_id') and kwargs.get(f'{f}_id') != False:
                    missing.append(f)
            else:
                if not kwargs.get(f) and kwargs.get(f) != False:
                    missing.append(f)
        if missing:
            return JsonResponse({'error': f'Campos requeridos: {missing}'}, status=400)
        try:
            obj = Model(**kwargs)

            # ── Contraseña virtual (AbstractBaseUser) ───────────
            new_pw = body.get('new_password', '')
            if new_pw and hasattr(obj, 'set_password'):
                obj.set_password(new_pw)

            # ── Modelos de la jerarquía comercial requieren Direccion NOT NULL ──
            # Se detecta la necesidad usando el _id del campo FK (seguro en instancias no guardadas)
            if hasattr(obj, 'direccion_id') and getattr(obj, 'direccion_id', None) is None:
                from admin_profiles.models import Direcciones
                direccion_vacia = Direcciones(direccion='Sin dirección')
                direccion_vacia.audit_save = False  # Evita crash Redis en entorno local
                direccion_vacia.save()
                obj.direccion_id = direccion_vacia.pk

            # ── Igualmente, status puede ser NOT NULL en modelos de comercialización ──
            if hasattr(obj, 'status_id') and getattr(obj, 'status_id', None) is None:
                try:
                    from admin_status.models import Status
                    # Intenta primero 'activo', luego cualquier status de tipo comercial
                    st = (
                        Status.objects.filter(codename='activo').first()
                        or Status.objects.filter(codename='status_activo').first()
                        or Status.objects.filter(codename__icontains='activ').first()
                        or Status.objects.first()
                    )
                    if st:
                        obj.status_id = st.pk
                except Exception:
                    pass

            # ── Auto asignar Dia y User para Movimientos ──
            if modulo == 'movimientos':
                from admin_finanzas.models import Comercializadora, Dia
                from datetime import date
                obj.user = request.user
                if getattr(obj, 'comercializadora_id', None):
                    try:
                        com = Comercializadora.objects.get(pk=obj.comercializadora_id)
                        if com.resumen_automatic:
                            obj.dia, _ = Dia.objects.get_or_create(fecha=date.today())
                        else:
                            dt = com.get_dia_trabajo()
                            if dt:
                                obj.dia = dt.dia
                            else:
                                return JsonResponse({'error': 'Comercializadora sin fecha de trabajo'}, status=400)
                    except Exception:
                        pass

            # ── Menu.menu_suc es FK a sí mismo y no acepta NULL, se asigna un raíz ──
            if hasattr(obj, 'menu_suc_id') and getattr(obj, 'menu_suc_id', None) is None:
                try:
                    from admin_permisologia.models import Menu as MenuModel
                    raiz = MenuModel.objects.filter(menu_suc_id=None).first()
                    if raiz is None:
                        # Crear un menú raíz temporal auto-referenciado
                        raiz = MenuModel(name='Raíz', codename='__root__', url=None,
                                         orden=0, is_view=False, is_public=False, is_global=False)
                        raiz.audit_save = False
                        raiz.save()
                        raiz.menu_suc = raiz  # auto-referencia
                        raiz.save()
                    obj.menu_suc_id = raiz.pk
                except Exception:
                    pass

            obj.audit_save = False  # Evita crash Redis al guardar desde el dashboard
            obj.save()

            # ── Creación de Usuario Rápido (Bancas/Bloques) ──
            if modulo in ['bancas', 'bloques', 'operadoras'] and hasattr(obj, 'nombre'):
                vu = body.get('virtual_username')
                vp = body.get('virtual_password')
                if vu and vp:
                    from admin_users.models import Users, UserProfile
                    from admin_finanzas.models import Comercializadora
                    profile_codename = f'userprofile_{modulo[:-1]}'
                    profile, _ = UserProfile.objects.get_or_create(
                        codename=profile_codename,
                        defaults={'nombre': f'Perfil {modulo.capitalize()}'}
                    )
                    user, created = Users.objects.get_or_create(
                        user=vu.strip(),
                        defaults={
                            'profile': profile,
                            'etiqueta': obj.nombre,
                        }
                    )
                    user.set_password(vp.strip())
                    user.save()
                    com = None
                    if modulo == 'bancas':
                        com = Comercializadora.objects.filter(banca=obj).first()
                    elif modulo == 'bloques':
                        com = Comercializadora.objects.filter(bloque=obj).first()
                    elif modulo == 'operadoras':
                        com = Comercializadora.objects.filter(operadora=obj).first()
                    if com:
                        user.comercializadora.add(com)

            return JsonResponse({'ok': True, 'pk': obj.pk, 'str': str(obj)}, status=201)
        except Exception as e:
            from django.db import IntegrityError
            import traceback
            if isinstance(e, IntegrityError) and 'UNIQUE constraint failed' in str(e):
                return JsonResponse({'error': 'Ya existe un registro con estos datos. No se permiten nombres o valores duplicados.'}, status=400)
            return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

    # ── PUT: actualizar ────────────────────────────────────────────────────────
    if request.method == 'PUT':
        if not pk:
            return JsonResponse({'error': 'Se requiere ?pk=ID'}, status=400)
        try:
            body = json.loads(request.body)
        except Exception:
            return JsonResponse({'error': 'Body JSON inválido'}, status=400)
        try:
            obj = Model.objects.get(pk=pk)
        except Model.DoesNotExist:
            return JsonResponse({'error': 'No encontrado'}, status=404)
        virtual = cfg.get('virtual_fields', [])
        fk_fields = set(cfg.get('fk_fields', {}).keys())
        for f in cfg['fields']:
            if f in virtual:
                continue
            if f in fk_fields:
                continue
            if f in body:
                try:
                    field_type = Model._meta.get_field(f).get_internal_type()
                except Exception:
                    continue
                val = body[f]
                if field_type == 'BooleanField':
                    val = val in (True, 'true', 'True', '1', 'on')
                elif field_type in ('IntegerField', 'DecimalField', 'FloatField') and val == '':
                    val = None
                setattr(obj, f, val)
        # Password virtual
        new_pw = body.get('new_password', '')
        if new_pw and hasattr(obj, 'set_password'):
            obj.set_password(new_pw)
        for fk_name in cfg.get('fk_fields', {}):
            if fk_name in body:
                setattr(obj, f'{fk_name}_id', body[fk_name] or None)
        try:
            obj.save()

            # ── Actualización de Usuario Rápido (Bancas/Bloques) ──
            if modulo in ['bancas', 'bloques', 'operadoras'] and hasattr(obj, 'nombre'):
                vu = body.get('virtual_username')
                vp = body.get('virtual_password')
                if vu and vp:
                    from admin_users.models import Users, UserProfile
                    from admin_finanzas.models import Comercializadora
                    profile_codename = f'userprofile_{modulo[:-1]}'
                    profile, _ = UserProfile.objects.get_or_create(
                        codename=profile_codename,
                        defaults={'nombre': f'Perfil {modulo.capitalize()}'}
                    )
                    user, created = Users.objects.get_or_create(
                        user=vu.strip(),
                        defaults={
                            'profile': profile,
                            'etiqueta': obj.nombre,
                        }
                    )
                    user.set_password(vp.strip())
                    user.save()
                    com = None
                    if modulo == 'bancas':
                        com = Comercializadora.objects.filter(banca=obj).first()
                    elif modulo == 'bloques':
                        com = Comercializadora.objects.filter(bloque=obj).first()
                    elif modulo == 'operadoras':
                        com = Comercializadora.objects.filter(operadora=obj).first()
                    if com:
                        user.comercializadora.add(com)

            return JsonResponse({'ok': True, 'pk': obj.pk, 'str': str(obj)})
        except Exception as e:
            from django.db import IntegrityError
            if isinstance(e, IntegrityError) and 'UNIQUE constraint failed' in str(e):
                return JsonResponse({'error': 'Ya existe un registro con estos datos. No se permiten nombres o valores duplicados.'}, status=400)
            return JsonResponse({'error': str(e)}, status=500)

    # ── DELETE ────────────────────────────────────────────────────────────────
    if request.method == 'DELETE':
        if not pk:
            return JsonResponse({'error': 'Se requiere ?pk=ID'}, status=400)
        try:
            obj = Model.objects.get(pk=pk)
            obj.delete()
            return JsonResponse({'ok': True})
        except Model.DoesNotExist:
            return JsonResponse({'error': 'No encontrado'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

    return JsonResponse({'error': 'Método no permitido'}, status=405)

# Proxy para obviar el error de CORS al pedir resultados del Arrejuntao
@csrf_exempt
def taquilla_proxy_resultados(request):
    import requests
    date_str = request.GET.get('date', '')
    if not date_str:
        import datetime
        date_str = datetime.date.today().isoformat()
    
    url = f"https://backend.serviciosintegradostriple7.com/api/v1/products/el-arrejuntao/results/?date={date_str}"
    try:
        response = requests.get(url, timeout=5)
        return HttpResponse(response.content, content_type='application/json', status=response.status_code)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def taquilla_scrape_tuazar(request):
    """
    Devuelve los resultados cargados por el administrador (desde ResultadoSorteo).
    Mantiene la misma estructura JSON que esperaba la taquilla del scraper original,
    para no tener que modificar el frontend.
    """
    from admin_juego.models_arrejuntao import ResultadoSorteo
    import datetime
    
    try:
        # El frontend envía un parámetro 'date' o asume el día actual.
        # (Aunque el scraper original de tuazar no recibía fecha y siempre traía hoy,
        # vamos a soportarlo por si acaso)
        fecha_str = request.GET.get('date') or datetime.date.today().isoformat()
        
        resultados = ResultadoSorteo.objects.filter(fecha_sorteo=fecha_str).select_related('producto__loteria', 'sorteo')
        
        lotteries_dict = {}
        
        for res in resultados:
            if not res.producto or not res.producto.loteria:
                continue
                
            nombre_loteria = res.producto.loteria.nombre.upper()
            if nombre_loteria not in lotteries_dict:
                lotteries_dict[nombre_loteria] = []
                
            hora = res.sorteo.hora_sorteo.strftime('%I:%M %p') if res.sorteo else '00:00'
            vals = []
            if res.res_triple_a: vals.append(res.res_triple_a)
            if res.res_triple_b: vals.append(res.res_triple_b)
            if res.res_signo: vals.append(f"Zodiacal: {res.res_signo}")
            
            val_str = ' / '.join(vals) if vals else 'Pendiente'
            draw_text = f"{hora}: {val_str}"
            lotteries_dict[nombre_loteria].append(draw_text)
            
        lotteries = []
        for nombre, draws in lotteries_dict.items():
            lotteries.append({
                'nombre': nombre,
                'draws': draws
            })
            
        return JsonResponse({'success': True, 'lotteries': lotteries})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def taquilla_ping(request):
    if request.method == 'POST':
        try:
            body = json.loads(request.body)
            user_str = body.get('user', '')
            if user_str:
                from admin_comercializacion.models import UsuariosTaquilla
                taq_user = UsuariosTaquilla.objects.select_related('taquilla').filter(user=user_str).first()
                if taq_user and taq_user.taquilla:
                    from django.utils.timezone import now as tz_now
                    from django.apps import apps
                    HechoConn = apps.get_model('admin_historic', 'HechoConnectionsComer')
                    ip = request.META.get('REMOTE_ADDR', '127.0.0.1')
                    hecho, _ = HechoConn.objects.get_or_create(
                        taquilla_id=taq_user.taquilla.id,
                        agencia_id=taq_user.taquilla.agencia_id,
                        defaults={'ip': ip, 'connection_at': tz_now()}
                    )
                    if not _:
                        hecho.ip = ip
                        hecho.connection_at = tz_now()
                        hecho.save()
            return JsonResponse({'ok': True})
        except Exception as e:
            return JsonResponse({'ok': False, 'error': str(e)})
    return JsonResponse({'ok': False})

@csrf_exempt
def create_example_hierarchy(request):
    try:
        from admin_comercializacion.models import Operadoras, Bloques, Bancas, Agencias, Taquillas
        from admin_status.models import Status
        from admin_profiles.models import Direcciones
        
        st_activo = Status.objects.filter(codename='activo').first() or Status.objects.first()
        dir_demo, _ = Direcciones.objects.get_or_create(direccion='Dirección Demo')

        # 1. Operadora
        op, c1 = Operadoras.objects.get_or_create(nombre='OPERADORA DEMO', defaults={'resumen_automatic': True, 'status': st_activo, 'direccion': dir_demo, 'email': 'op@demo.com', 'telefono': '0000', 'rif': 'J-000'})

        # 2. Bloque
        bq, c2 = Bloques.objects.get_or_create(nombre='MULTI BANCA DEMO', operadora=op, defaults={'status': st_activo, 'direccion': dir_demo, 'email': 'bq@demo.com', 'telefono': '0000', 'rif': 'J-000'})

        # 3. Super Banca
        bc, c3 = Bancas.objects.get_or_create(nombre='SUPER BANCA DEMO', bloque=bq, defaults={'status': st_activo, 'direccion': dir_demo, 'email': 'bc@demo.com', 'telefono': '0000', 'rif': 'J-000', 'is_sistema_juego': False, 'is_resultados': False})

        return JsonResponse({
            'ok': True,
            'mensaje': 'Usuarios de prueba creados correctamente. Puedes verlos en el listado de cada módulo.',
            'usuarios': {
                '1_Operadora': op.nombre,
                '2_Multibanca': bq.nombre,
                '3_SuperBanca': bc.nombre
            }
        })
    except Exception as e:
        import traceback
        return JsonResponse({'error': str(e), 'trace': traceback.format_exc()}, status=500)

def taquilla_tuazar_view(request):
    html_path = os.path.join(settings.BASE_DIR, 'admin_asterisco7', 'templates', 'taquilla', 'taquilla_tuazar.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            return HttpResponse(f.read())
    return HttpResponse('Plantilla no encontrada: taquilla_tuazar.html', status=404)
