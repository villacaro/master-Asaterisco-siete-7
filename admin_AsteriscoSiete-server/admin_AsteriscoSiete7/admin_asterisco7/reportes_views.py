# -*- coding: utf-8 -*-
"""
reportes_views.py — Sistema Asterisco Siete (*7)
=================================================
APIs y vistas para los reportes de:
  1. Lista en Línea  — grilla numérica 000-999 con montos apostados
  2. Reporte por Producto — resumen de venta, premios y saldo por producto
  3. Riesgo de Venta  — ranking de números candidatos con nivel de alerta
"""
import json
from decimal import Decimal
from datetime import date, datetime

from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Count, Sum, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator


# ─────────────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────────────

def _parse_date(s, fallback=None):
    """Convierte string 'YYYY-MM-DD' a date; retorna fallback si falla."""
    try:
        return datetime.strptime(s, '%Y-%m-%d').date()
    except Exception:
        return fallback or date.today()


def _dec(val):
    """Serializa Decimal a float con 2 lugares para JSON."""
    if val is None:
        return 0.0
    return float(round(Decimal(str(val)), 2))


def _get_base_qs(fecha_inicio, fecha_fin, sorteo_id=None, tipo_jugada=None, producto_id=None):
    """
    Construye el QuerySet base de ApuestaDetalle con los filtros comunes.
    Solo incluye apuestas de tickets válidos (no anulados).
    """
    from admin_juego.models_arrejuntao import ApuestaDetalle
    qs = ApuestaDetalle.objects.filter(
        ticket__anulado=False,
        ticket__fecha_emision__date__gte=fecha_inicio,
        ticket__fecha_emision__date__lte=fecha_fin,
    ).exclude(estatus='A')

    if sorteo_id:
        qs = qs.filter(ticket__sorteo_id=sorteo_id)
    if tipo_jugada:
        qs = qs.filter(tipo_jugada=tipo_jugada)
    if producto_id:
        qs = qs.filter(ticket__producto_id=producto_id)
    return qs


# ─────────────────────────────────────────────────────────────────────────────
# API 1 — Lista en Línea
# GET /dashboard/reportes/api/lista-linea/?fecha_inicio=&fecha_fin=&sorteo_id=&tipo_jugada=
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_lista_linea(request):
    """
    Devuelve para cada número (000-999) la cantidad de tickets y el monto
    total apostado en ese número en el rango de fechas/sorteo indicado.
    """
    fecha_inicio = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin    = _parse_date(request.GET.get('fecha_fin'))
    sorteo_id    = request.GET.get('sorteo_id') or None
    tipo_jugada  = request.GET.get('tipo_jugada') or None
    producto_id  = request.GET.get('producto_id') or None

    qs = _get_base_qs(fecha_inicio, fecha_fin, sorteo_id, tipo_jugada, producto_id)

    # Solo triples / terminales (números de hasta 3 dígitos)
    filas = (
        qs
        .values('numero_apostado')
        .annotate(
            cant_tickets=Count('ticket', distinct=True),
            monto_total=Sum('monto_apostado'),
            monto_premios=Sum('monto_premio'),
        )
        .order_by('numero_apostado')
    )

    # Construir mapa completo 000-999
    mapa = {str(i).zfill(3): {'numero': str(i).zfill(3), 'cant': 0, 'monto': 0.0, 'premios': 0.0}
            for i in range(1000)}

    for row in filas:
        num = row['numero_apostado'].zfill(3)[-3:]  # normalizar
        if num in mapa:
            mapa[num]['cant']    = row['cant_tickets']
            mapa[num]['monto']   = _dec(row['monto_total'])
            mapa[num]['premios'] = _dec(row['monto_premios'])

    # Metadata del sorteo
    sorteo_info = None
    if sorteo_id:
        try:
            from admin_juego.models_arrejuntao import SorteoArrejuntao
            s = SorteoArrejuntao.objects.select_related('producto__loteria').get(pk=sorteo_id)
            sorteo_info = {
                'nombre':  str(s),
                'loteria': s.producto.loteria.nombre,
                'hora':    s.hora_sorteo.strftime('%H:%M'),
            }
        except Exception:
            pass

    return JsonResponse({
        'ok':       True,
        'fecha_inicio': str(fecha_inicio),
        'fecha_fin':    str(fecha_fin),
        'sorteo':   sorteo_info,
        'tipo_jugada': tipo_jugada,
        'total_registros': sum(v['cant'] for v in mapa.values()),
        'total_monto':     _dec(sum(v['monto'] for v in mapa.values())),
        'numeros': list(mapa.values()),
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API 2 — Reporte por Producto
# GET /dashboard/reportes/api/por-producto/?fecha_inicio=&fecha_fin=
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_por_producto(request):
    """
    Resumen de venta/premios/saldo agrupado por ProductoLoteria.
    Columnas: Producto | Venta | % Venta | Premios | Saldo
    """
    fecha_inicio = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin    = _parse_date(request.GET.get('fecha_fin'))
    sorteo_id    = request.GET.get('sorteo_id') or None

    qs = _get_base_qs(fecha_inicio, fecha_fin, sorteo_id)

    rows = (
        qs
        .values(
            'ticket__producto__id',
            'ticket__producto__nombre_producto',
            'ticket__producto__loteria__nombre',
        )
        .annotate(
            venta   = Sum('monto_apostado'),
            premios = Sum('monto_premio'),
            tickets = Count('ticket', distinct=True),
        )
        .order_by('-venta')
    )

    total_venta = sum(_dec(r['venta']) for r in rows)

    resultado = []
    for r in rows:
        venta   = _dec(r['venta'])
        premios = _dec(r['premios'])
        saldo   = round(venta - premios, 2)
        pct     = round(venta / total_venta * 100, 1) if total_venta else 0
        resultado.append({
            'producto_id':   r['ticket__producto__id'],
            'producto':      r['ticket__producto__nombre_producto'],
            'loteria':       r['ticket__producto__loteria__nombre'],
            'venta':         venta,
            'pct_venta':     pct,
            'premios':       premios,
            'saldo':         saldo,
            'cant_tickets':  r['tickets'],
        })

    return JsonResponse({
        'ok':          True,
        'fecha_inicio': str(fecha_inicio),
        'fecha_fin':    str(fecha_fin),
        'total_venta':  total_venta,
        'total_premios': sum(r['premios'] for r in resultado),
        'total_saldo':   sum(r['saldo'] for r in resultado),
        'filas':        resultado,
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API 3 — Riesgo de Venta (estilo Selección de Candidatos)
# GET /dashboard/reportes/api/riesgo-venta/?fecha_inicio=&fecha_fin=&sorteo_id=&tipo_jugada=&top=50
# ─────────────────────────────────────────────────────────────────────────────

MULTIPLICADORES = {
    'TRIPLE_A':       75, 'TRIPLE_B':        75,
    'TERMINAL_A':      7, 'TERMINAL_B':        7,
    'TRIPLE_SIGNO_A': 90, 'TRIPLE_SIGNO_B':  90,
    'TERMINAL_SIGNO_A': 9, 'TERMINAL_SIGNO_B': 9,
    'ARRIMAO':        50, 'PAGADITO':        150,
    'ANIMALITO':       3,
}

def _nivel_alerta(pct_premiacion):
    """Clasifica el nivel de riesgo según el % de premiación potencial."""
    if pct_premiacion >= 80:
        return 'CRÍTICO'
    if pct_premiacion >= 50:
        return 'ALERTA'
    if pct_premiacion >= 30:
        return 'MODERADO'
    return 'NORMAL'


@staff_member_required(login_url='/admin/login/')
def api_riesgo_venta(request):
    """
    Ranking de números más jugados con cálculo de riesgo potencial.
    Ordena por monto_venta DESC y calcula cuánto pagaría si ese número sale.

    Columnas:
        No | Candidato | Cant.Ticket | Venta | Max.Apostado | Monto.Premio.Potencial |
        % Premiación | Nivel
    """
    fecha_inicio = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin    = _parse_date(request.GET.get('fecha_fin'))
    sorteo_id    = request.GET.get('sorteo_id') or None
    tipo_jugada  = request.GET.get('tipo_jugada') or None
    producto_id  = request.GET.get('producto_id') or None
    top          = min(int(request.GET.get('top', 50)), 200)

    qs = _get_base_qs(fecha_inicio, fecha_fin, sorteo_id, tipo_jugada, producto_id)

    from django.db.models import Max
    filas = (
        qs
        .values('numero_apostado', 'tipo_jugada')
        .annotate(
            cant_tickets   = Count('ticket', distinct=True),
            monto_venta    = Sum('monto_apostado'),
            max_apostado   = Max('monto_apostado'),
        )
        .order_by('-monto_venta')[:top]
    )

    # Monto total de venta para calcular el %
    total_venta = _dec(
        _get_base_qs(fecha_inicio, fecha_fin, sorteo_id, tipo_jugada, producto_id)
        .aggregate(t=Sum('monto_apostado'))['t']
    )

    resultado = []
    for idx, r in enumerate(filas, 1):
        tipo   = r['tipo_jugada']
        mult   = MULTIPLICADORES.get(tipo, 1)
        venta  = _dec(r['monto_venta'])
        # Premio potencial = monto total apostado a ese número × multiplicador
        monto_premio_potencial = round(venta * mult, 2)
        pct_premiacion = round(monto_premio_potencial / total_venta * 100, 1) if total_venta else 0
        resultado.append({
            'no':            idx,
            'candidato':     r['numero_apostado'],
            'tipo_jugada':   tipo,
            'cant_tickets':  r['cant_tickets'],
            'venta':         venta,
            'max_apostado':  _dec(r['max_apostado']),
            'monto_premio_potencial': monto_premio_potencial,
            'multiplicador': mult,
            'pct_premiacion': pct_premiacion,
            'nivel':         _nivel_alerta(pct_premiacion),
        })

    criticos  = sum(1 for r in resultado if r['nivel'] == 'CRÍTICO')
    alertas   = sum(1 for r in resultado if r['nivel'] == 'ALERTA')
    moderados = sum(1 for r in resultado if r['nivel'] == 'MODERADO')

    return JsonResponse({
        'ok':            True,
        'fecha_inicio':  str(fecha_inicio),
        'fecha_fin':     str(fecha_fin),
        'sorteo_id':     sorteo_id,
        'tipo_jugada':   tipo_jugada,
        'total_venta':   total_venta,
        'resumen_alertas': {
            'criticos':  criticos,
            'alertas':   alertas,
            'moderados': moderados,
        },
        'candidatos': resultado,
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API auxiliar — Sorteos disponibles para filtros
# GET /dashboard/reportes/api/sorteos/?fecha=YYYY-MM-DD
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_sorteos_disponibles(request):
    """Devuelve sorteos que tienen tickets en la fecha indicada."""
    from admin_juego.models_arrejuntao import SorteoArrejuntao, Ticket
    fecha = _parse_date(request.GET.get('fecha'))
    ids_con_tickets = (
        Ticket.objects.filter(
            fecha_emision__date=fecha,
            anulado=False,
        ).values_list('sorteo_id', flat=True).distinct()
    )
    sorteos = SorteoArrejuntao.objects.filter(pk__in=ids_con_tickets).select_related('producto__loteria')
    return JsonResponse({
        'ok': True,
        'fecha': str(fecha),
        'sorteos': [
            {'id': s.pk, 'nombre': str(s), 'hora': s.hora_sorteo.strftime('%H:%M')}
            for s in sorteos
        ],
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API 4 — Cuadre por Agencia / Taquilla
# GET /dashboard/reportes/api/cuadre/?fecha_inicio=&fecha_fin=&agrupar=agencia|taquilla
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_cuadre(request):
    """
    Cuadre de venta/premios/saldo agrupado por agencia o taquilla.
    Usa Ticket.total (venta) y ApuestaDetalle.monto_premio (premio pagado).
    """
    from admin_juego.models_arrejuntao import Ticket, ApuestaDetalle
    from django.apps import apps

    fecha_inicio = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin    = _parse_date(request.GET.get('fecha_fin'))
    agrupar      = request.GET.get('agrupar', 'agencia')  # 'agencia' | 'taquilla'

    campo_grupo = 'id_agencia' if agrupar == 'agencia' else 'id_taquilla'

    # QuerySet base: tickets válidos en el rango de fechas
    qs_tickets = Ticket.objects.filter(
        anulado=False,
        fecha_emision__date__gte=fecha_inicio,
        fecha_emision__date__lte=fecha_fin,
    )

    # Venta agrupada
    filas_venta = (
        qs_tickets
        .values(campo_grupo)
        .annotate(
            venta   = Sum('total'),
            tickets = Count('id'),
        )
        .order_by('-venta')
    )

    # Premios pagados desde ApuestaDetalle
    filas_premios = (
        ApuestaDetalle.objects
        .filter(
            ticket__anulado=False,
            ticket__fecha_emision__date__gte=fecha_inicio,
            ticket__fecha_emision__date__lte=fecha_fin,
        )
        .exclude(estatus='A')
        .values('ticket__' + campo_grupo)
        .annotate(premios=Sum('monto_premio'))
    )
    premios_map = {row['ticket__' + campo_grupo]: _dec(row['premios']) for row in filas_premios}

    # Mapas de nombre
    nombre_map = {}
    try:
        if agrupar == 'agencia':
            Agencias = apps.get_model('admin_comercializacion', 'Agencias')
            nombre_map = dict(Agencias.objects.values_list('id', 'nombre'))
        else:
            Taquillas = apps.get_model('admin_comercializacion', 'Taquillas')
            nombre_map = dict(Taquillas.objects.values_list('id', 'taquilla'))
    except Exception:
        pass

    resultado = []
    for row in filas_venta:
        gid     = row[campo_grupo]
        venta   = _dec(row['venta'])
        premios = premios_map.get(gid, 0.0)
        saldo   = round(venta - premios, 2)
        resultado.append({
            'id':      gid,
            'nombre':  nombre_map.get(gid, f'#{gid}'),
            'venta':   venta,
            'premios': premios,
            'saldo':   saldo,
            'tickets': row['tickets'],
        })

    total_venta   = sum(r['venta']   for r in resultado)
    total_premios = sum(r['premios'] for r in resultado)
    total_saldo   = round(total_venta - total_premios, 2)

    return JsonResponse({
        'ok':            True,
        'fecha_inicio':  str(fecha_inicio),
        'fecha_fin':     str(fecha_fin),
        'agrupar':       agrupar,
        'total_venta':   total_venta,
        'total_premios': total_premios,
        'total_saldo':   total_saldo,
        'filas':         resultado,
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API 5 — Liquidaciones de Sorteo
# GET /dashboard/reportes/api/liquidaciones/?fecha_inicio=&fecha_fin=&agencia_id=
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_liquidaciones(request):
    """
    Lista liquidaciones de sorteos en el rango de fechas indicado.
    Agrupa por (id_sorteo, id_agencia, id_taquilla) con totales financieros.
    """
    from admin_juego.models_arrejuntao import LiquidacionSorteo
    from django.apps import apps

    fecha_inicio = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin    = _parse_date(request.GET.get('fecha_fin'))
    agencia_id   = request.GET.get('agencia_id') or None

    qs = LiquidacionSorteo.objects.filter(
        created_at__date__gte=fecha_inicio,
        created_at__date__lte=fecha_fin,
    )
    if agencia_id:
        try:
            qs = qs.filter(id_agencia=int(agencia_id))
        except (ValueError, TypeError):
            pass

    qs = qs.order_by('-id_sorteo', 'id_agencia', 'id_taquilla')

    # Mapa de nombres de agencia
    nombre_agencia_map = {}
    try:
        Agencias = apps.get_model('admin_comercializacion', 'Agencias')
        nombre_agencia_map = dict(Agencias.objects.values_list('id', 'nombre'))
    except Exception:
        pass

    resultado = []
    total_venta        = 0.0
    total_premios      = 0.0
    total_comision_agc = 0.0
    total_saldo_oper   = 0.0

    for liq in qs:
        venta        = _dec(liq.mmonto_venta)
        premios      = _dec(liq.mmonto_premios)
        comision_agc = _dec(liq.mmonto_comision_agc)
        saldo_oper   = _dec(liq.msaldo_oper)
        saldo_agc    = _dec(liq.msaldo_agc) if liq.msaldo_agc is not None else 0.0

        total_venta        += venta
        total_premios      += premios
        total_comision_agc += comision_agc
        total_saldo_oper   += saldo_oper

        resultado.append({
            'id':             liq.pk,
            'id_sorteo':      liq.id_sorteo,
            'id_agencia':     liq.id_agencia,
            'id_taquilla':    liq.id_taquilla,
            'nombre_agencia': nombre_agencia_map.get(liq.id_agencia, f'Agencia #{liq.id_agencia}'),
            'venta':          venta,
            'premios':        premios,
            'comision_agc':   comision_agc,
            'saldo_oper':     saldo_oper,
            'saldo_agc':      saldo_agc,
            'pct_comision_agc': float(liq.nporcentaje_comision_agc),
            'fecha':          liq.created_at.strftime('%Y-%m-%d') if liq.created_at else None,
        })

    return JsonResponse({
        'ok':                True,
        'fecha_inicio':      str(fecha_inicio),
        'fecha_fin':         str(fecha_fin),
        'total_registros':   len(resultado),
        'total_venta':       round(total_venta, 2),
        'total_premios':     round(total_premios, 2),
        'total_comision_agc':round(total_comision_agc, 2),
        'total_saldo_oper':  round(total_saldo_oper, 2),
        'filas':             resultado,
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API 6 — Resumen Administrativo de Finanzas
# GET /dashboard/reportes/api/resumen-admin/?fecha_inicio=&fecha_fin=
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_resumen_admin(request):
    """
    Lista registros de ResumenAdministrativo (admin_finanzas) filtrados por rango de fecha.
    Calcula totales de venta, premio, comision, regalia y queda.
    """
    from django.apps import apps
    ResumenAdministrativo = apps.get_model('admin_finanzas', 'ResumenAdministrativo')

    fecha_inicio = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin    = _parse_date(request.GET.get('fecha_fin'))

    qs = ResumenAdministrativo.objects.filter(
        dia__fecha__gte=fecha_inicio,
        dia__fecha__lte=fecha_fin,
    ).select_related('dia').order_by('-dia__fecha')

    total_venta    = 0.0
    total_premio   = 0.0
    total_comision = 0.0
    total_regalia  = 0.0
    total_queda    = 0.0
    resultado      = []

    for r in qs:
        venta    = _dec(r.venta)
        premio   = _dec(r.premio)
        comision = _dec(r.comision)
        regalia  = _dec(r.regalia)
        queda    = _dec(r.queda)

        total_venta    += venta
        total_premio   += premio
        total_comision += comision
        total_regalia  += regalia
        total_queda    += queda

        resultado.append({
            'id':       r.pk,
            'dia':      str(r.dia.fecha) if r.dia else '—',
            'venta':    venta,
            'premio':   premio,
            'comision': comision,
            'regalia':  regalia,
            'queda':    queda,
        })

    return JsonResponse({
        'ok':             True,
        'fecha_inicio':   str(fecha_inicio),
        'fecha_fin':      str(fecha_fin),
        'total_registros':len(resultado),
        'total_venta':    round(total_venta, 2),
        'total_premio':   round(total_premio, 2),
        'total_comision': round(total_comision, 2),
        'total_regalia':  round(total_regalia, 2),
        'total_queda':    round(total_queda, 2),
        'filas':          resultado,
    }, json_dumps_params={'ensure_ascii': False})


# ─────────────────────────────────────────────────────────────────────────────
# API 7 — Días de Trabajo
# GET /dashboard/reportes/api/dias-trabajo/?fecha_inicio=&fecha_fin=&comercializadora_id=
# ─────────────────────────────────────────────────────────────────────────────

@staff_member_required(login_url='/admin/login/')
def api_dias_trabajo(request):
    """
    Lista registros de DiaTrabajo (admin_finanzas) filtrados por rango de fecha.
    Incluye estado procesado/actual para cada comercializadora.
    Requiere que DiaTrabajo.dia sea FK a admin_finanzas.Dia.
    """
    from django.apps import apps

    fecha_inicio        = _parse_date(request.GET.get('fecha_inicio'))
    fecha_fin           = _parse_date(request.GET.get('fecha_fin'))
    comercializadora_id = request.GET.get('comercializadora_id') or None

    try:
        DiaTrabajo      = apps.get_model('admin_finanzas', 'DiaTrabajo')
        Comercializadora = apps.get_model('admin_finanzas', 'Comercializadora')
    except LookupError as e:
        return JsonResponse({'ok': False, 'error': f'Modelo no encontrado: {e}'}, status=500)

    try:
        qs = DiaTrabajo.objects.filter(
            dia__fecha__gte=fecha_inicio,
            dia__fecha__lte=fecha_fin,
        ).select_related('dia', 'comercializadora').order_by(
            '-dia__fecha', 'comercializadora_id'
        )

        if comercializadora_id:
            try:
                qs = qs.filter(comercializadora_id=int(comercializadora_id))
            except (ValueError, TypeError):
                pass

        # Mapa id → str de comercializadora para el label
        com_map = {}
        try:
            com_map = {c.pk: str(c) for c in Comercializadora.objects.all()}
        except Exception:
            pass

        resultado = []
        for dt in qs:
            resultado.append({
                'id':                 dt.pk,
                'comercializadora_id': dt.comercializadora_id,
                'comercializadora':   com_map.get(dt.comercializadora_id,
                                                   f'#{dt.comercializadora_id}'),
                'dia':                str(dt.dia.fecha) if dt.dia else '—',
                'procesado':          dt.procesado,
                'actual':             dt.actual,
                'created_at':         dt.created_at.strftime('%Y-%m-%d %H:%M')
                                      if getattr(dt, 'created_at', None) else None,
            })

    except Exception as exc:
        return JsonResponse({
            'ok': False,
            'error': str(exc),
            'hint': 'Verifica que las tablas admin_finanzas_dia y admin_finanzas_diatrabajo existan en la BD (ejecuta makemigrations + migrate).',
        }, status=500)

    return JsonResponse({
        'ok':              True,
        'fecha_inicio':    str(fecha_inicio),
        'fecha_fin':       str(fecha_fin),
        'total_registros': len(resultado),
        'filas':           resultado,
    }, json_dumps_params={'ensure_ascii': False})



