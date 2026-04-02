"""
api_rest/views.py  –  Endpoints REST para EL ARREJUNTAO

Endpoints:
    GET  /api/resultados/        → scraping de resultados del día
    POST /api/publicar/          → scraping + guardar en Firestore
    GET  /api/usuarios/          → lista usuarios Firebase Auth
    GET  /api/health/            → estado del backend y Firebase
    GET  /api/sorteos/           → estado de todos los sorteos y cupos
    POST /api/sorteos/<id>/venta/ → registrar venta en un sorteo
"""
import logging
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

import requests as http_requests
from bs4 import BeautifulSoup

from usuarios import firebase_service as fb  # reutilizamos el servicio existente

logger = logging.getLogger(__name__)

# ── Configuración de scraping ─────────────────────────────────
TARGET_URL  = "https://elarrejuntao.com"
USER_AGENT  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
TIMEOUT_SEG = 10


# ════════════════════════════════════════════════════════════════
# SCRAPING
# ════════════════════════════════════════════════════════════════

def _safe_text(soup, selector, default="---"):
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else default


def _scrape_resultados():
    """Visita elarrejuntao.com y extrae los resultados del día."""
    try:
        headers  = {"User-Agent": USER_AGENT}
        response = http_requests.get(TARGET_URL, headers=headers, timeout=TIMEOUT_SEG)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        triple_a  = _safe_text(soup, ".resultado-triple-a",  "---")
        triple_b  = _safe_text(soup, ".resultado-triple-b",  "---")
        animalito = _safe_text(soup, ".resultado-animalito",  "Sin resultado")
        pegadito  = _safe_text(soup, ".resultado-pegadito",   "----")

        return {
            "estado":    "exito",
            "fecha":     datetime.now().strftime("%Y-%m-%d"),
            "hora":      datetime.now().strftime("%H:%M"),
            "triple_a":  triple_a,
            "triple_b":  triple_b,
            "pegadito":  pegadito,
            "animalito": animalito,
            "fuente":    TARGET_URL,
        }
    except http_requests.exceptions.Timeout:
        return {"estado": "error", "mensaje": "Tiempo de espera agotado."}
    except http_requests.exceptions.ConnectionError:
        return {"estado": "error", "mensaje": "No se pudo conectar con la web."}
    except Exception as e:
        logger.exception("Error inesperado en scraper")
        return {"estado": "error", "mensaje": str(e)}


def _publicar_en_firestore(datos):
    """Escribe los resultados en Firestore usando Firebase Admin SDK."""
    if not fb._init_firebase():
        return {"guardado": False, "razon": "Firebase no configurado"}
    try:
        from firebase_admin import firestore
        db    = firestore.client()
        hoy   = datos.get("fecha", datetime.now().strftime("%Y-%m-%d"))
        errores = []

        def _set(tipo, payload):
            doc_id = f"{hoy}_{tipo}_general"
            try:
                db.collection("resultados_sorteos").document(doc_id).set({
                    "tipo":  tipo,
                    "fecha": firestore.SERVER_TIMESTAMP,
                    **payload
                })
            except Exception as e:
                logger.exception(f"Error guardando '{tipo}' en Firestore")
                errores.append(str(e))

        if datos.get("triple_a") and datos["triple_a"] != "---":
            _set("arrimao",  {"numero": datos["triple_a"]})
        if datos.get("pegadito") and datos["pegadito"] != "----":
            _set("pegadito", {"numero": datos["pegadito"]})
        if datos.get("animalito") and datos["animalito"] != "Sin resultado":
            _set("animalito", {"animalito": {"nombre": datos["animalito"], "icono": "🐾", "numero": "-"}})

        return {"guardado": len(errores) == 0, "errores": errores}
    except Exception as e:
        return {"guardado": False, "razon": str(e)}


# ════════════════════════════════════════════════════════════════
# ENDPOINTS ORIGINALES
# ════════════════════════════════════════════════════════════════

@require_http_methods(["GET"])
def resultados(request):
    """GET /api/resultados/ → resultados del día en JSON."""
    datos  = _scrape_resultados()
    status = 200 if datos.get("estado") == "exito" else 503
    return JsonResponse(datos, status=status)


@csrf_exempt
@require_http_methods(["POST"])
def publicar(request):
    """POST /api/publicar/ → scraping + guardar en Firestore."""
    datos    = _scrape_resultados()
    guardado = _publicar_en_firestore(datos) if datos.get("estado") == "exito" else {"guardado": False}
    return JsonResponse({**datos, "firestore": guardado})


@require_http_methods(["GET"])
def usuarios(request):
    """GET /api/usuarios/ → lista de usuarios Firebase Auth."""
    lista = fb.listar_usuarios()
    return JsonResponse({"estado": "exito", "total": len(lista), "usuarios": lista})


@require_http_methods(["GET"])
def health(request):
    """GET /api/health/ → estado del backend."""
    firebase_ok = fb._init_firebase()
    return JsonResponse({
        "estado":   "ok",
        "firebase": "conectado" if firebase_ok else "no configurado (falta serviceAccountKey.json)",
        "hora":     datetime.now().isoformat(),
        "version":  "django",
    })


# ════════════════════════════════════════════════════════════════
# CONTROL DE SORTEOS
# ════════════════════════════════════════════════════════════════

@require_http_methods(["GET"])
def sorteos_estado(request):
    """
    GET /api/sorteos/
    Retorna el estado de todos los sorteos y cupos de venta.
    Usado por ambas apps frontend para validar si pueden aceptar apuestas.
    """
    from .models import ControlSorteo
    sorteos = ControlSorteo.objects.all().order_by('sorteo', 'horario')
    data = []
    for s in sorteos:
        data.append({
            "id":              s.id,
            "sorteo":          s.sorteo,
            "sorteo_nombre":   s.get_sorteo_display(),
            "horario":         s.horario,
            "abierto":         s.abierto,
            "cupo_venta":      s.cupo_venta,
            "ventas_hoy":      s.ventas_hoy,
            "cupo_disponible": s.cupo_disponible,
            "notas":           s.notas,
        })
    return JsonResponse({"estado": "ok", "sorteos": data})


@csrf_exempt
@require_http_methods(["POST"])
def sorteo_registrar_venta(request, sorteo_id):
    """
    POST /api/sorteos/<id>/venta/
    Incrementa el contador de ventas del sorteo y valida cupo.
    """
    from .models import ControlSorteo
    try:
        sorteo = ControlSorteo.objects.get(id=sorteo_id)
    except ControlSorteo.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Sorteo no encontrado"}, status=404)

    if not sorteo.abierto:
        return JsonResponse({
            "ok": False,
            "error": "Sorteo cerrado",
            "mensaje": f"El sorteo {sorteo.get_sorteo_display()} [{sorteo.horario}] está cerrado."
        }, status=400)

    if sorteo.cupo_venta > 0 and sorteo.ventas_hoy >= sorteo.cupo_venta:
        return JsonResponse({
            "ok": False,
            "error": "Cupo agotado",
            "mensaje": f"Cupo de venta agotado para {sorteo.get_sorteo_display()} [{sorteo.horario}]."
        }, status=400)

    sorteo.ventas_hoy += 1
    sorteo.save(update_fields=['ventas_hoy'])
    return JsonResponse({
        "ok":            True,
        "ventas_hoy":    sorteo.ventas_hoy,
        "cupo_restante": max(0, sorteo.cupo_venta - sorteo.ventas_hoy) if sorteo.cupo_venta > 0 else None,
    })


# ════════════════════════════════════════════════════════════════
# MÓDULO VENTAS
# ════════════════════════════════════════════════════════════════

import json

@require_http_methods(["GET"])
def ventas_lista(request):
    """
    GET /api/ventas/
    Retorna lista de transacciones de venta.
    Filtros: fecha_desde, fecha_hasta, taquillero, estado, horario
    """
    from .models import TransaccionVenta
    qs = TransaccionVenta.objects.all()

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    taquillero  = request.GET.get('taquillero')
    estado      = request.GET.get('estado')
    horario     = request.GET.get('horario')

    if fecha_desde:
        qs = qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        qs = qs.filter(fecha__lte=fecha_hasta)
    if taquillero:
        qs = qs.filter(taquillero__icontains=taquillero)
    if estado:
        qs = qs.filter(estado=estado)
    if horario:
        qs = qs.filter(horario=horario)

    data = []
    total_bs = 0
    for v in qs:
        total_bs += float(v.monto)
        data.append({
            'id':         v.id,
            'fecha':      str(v.fecha),
            'horario':    v.horario,
            'modalidad':  v.modalidad,
            'modalidad_nombre': v.get_modalidad_display(),
            'numero':     v.numero,
            'monto':      float(v.monto),
            'taquillero': v.taquillero,
            'ticket_ref': v.ticket_ref,
            'estado':     v.estado,
            'notas':      v.notas,
            'creado':     v.creado.isoformat(),
        })
    return JsonResponse({'ok': True, 'total': len(data), 'total_bs': total_bs, 'ventas': data})


@csrf_exempt
@require_http_methods(["POST"])
def ventas_crear(request):
    """
    POST /api/ventas/crear/
    Crea una nueva transacción de venta.
    Body JSON: fecha, horario, modalidad, numero, monto, taquillero, ticket_ref, notas
    """
    from .models import TransaccionVenta
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    required = ['horario', 'modalidad', 'numero', 'monto']
    for field in required:
        if not body.get(field):
            return JsonResponse({'ok': False, 'error': f'Campo requerido: {field}'}, status=400)

    try:
        v = TransaccionVenta.objects.create(
            fecha       = body.get('fecha', datetime.now().strftime('%Y-%m-%d')),
            horario     = body['horario'],
            modalidad   = body['modalidad'],
            numero      = body['numero'],
            monto       = body['monto'],
            taquillero  = body.get('taquillero', ''),
            ticket_ref  = body.get('ticket_ref', ''),
            estado      = body.get('estado', 'pendiente'),
            notas       = body.get('notas', ''),
        )
        return JsonResponse({'ok': True, 'id': v.id, 'mensaje': 'Venta registrada correctamente'})
    except Exception as e:
        logger.exception('Error creando venta')
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def ventas_actualizar_estado(request, venta_id):
    """
    POST /api/ventas/<id>/estado/
    Actualiza el estado de una venta (pendiente/ganador/perdedor/anulado).
    """
    from .models import TransaccionVenta
    try:
        v = TransaccionVenta.objects.get(id=venta_id)
    except TransaccionVenta.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Venta no encontrada'}, status=404)

    try:
        body   = json.loads(request.body)
        estado = body.get('estado')
        if estado not in ['pendiente', 'ganador', 'perdedor', 'anulado']:
            return JsonResponse({'ok': False, 'error': 'Estado inválido'}, status=400)
        v.estado = estado
        if body.get('notas'):
            v.notas = body['notas']
        v.save()
        return JsonResponse({'ok': True, 'id': v.id, 'estado': v.estado})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


# ════════════════════════════════════════════════════════════════
# MÓDULO PAGOS
# ════════════════════════════════════════════════════════════════

@require_http_methods(["GET"])
def pagos_lista(request):
    """
    GET /api/pagos/
    Lista pagos de taquilleros.
    Filtros: fecha_desde, fecha_hasta, taquillero, estado
    """
    from .models import Pago
    qs = Pago.objects.all()

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    taquillero  = request.GET.get('taquillero')
    estado      = request.GET.get('estado')

    if fecha_desde:
        qs = qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        qs = qs.filter(fecha__lte=fecha_hasta)
    if taquillero:
        qs = qs.filter(taquillero__icontains=taquillero)
    if estado:
        qs = qs.filter(estado=estado)

    data = []
    total_bs = 0
    for p in qs:
        total_bs += float(p.monto)
        data.append({
            'id':              p.id,
            'fecha':           str(p.fecha),
            'taquillero':      p.taquillero,
            'monto':           float(p.monto),
            'metodo':          p.metodo,
            'metodo_nombre':   p.get_metodo_display(),
            'referencia':      p.referencia,
            'estado':          p.estado,
            'estado_nombre':   p.get_estado_display(),
            'periodo_desde':   str(p.periodo_desde) if p.periodo_desde else '',
            'periodo_hasta':   str(p.periodo_hasta) if p.periodo_hasta else '',
            'confirmado_por':  p.confirmado_por,
            'notas':           p.notas,
            'creado':          p.creado.isoformat(),
        })
    return JsonResponse({'ok': True, 'total': len(data), 'total_bs': total_bs, 'pagos': data})


@csrf_exempt
@require_http_methods(["POST"])
def pagos_crear(request):
    """
    POST /api/pagos/crear/
    Registra un nuevo pago de taquillero.
    """
    from .models import Pago
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    required = ['taquillero', 'monto']
    for f in required:
        if not body.get(f):
            return JsonResponse({'ok': False, 'error': f'Campo requerido: {f}'}, status=400)

    try:
        p = Pago.objects.create(
            fecha          = body.get('fecha', datetime.now().strftime('%Y-%m-%d')),
            taquillero     = body['taquillero'],
            monto          = body['monto'],
            metodo         = body.get('metodo', 'efectivo'),
            referencia     = body.get('referencia', ''),
            estado         = body.get('estado', 'pendiente'),
            periodo_desde  = body.get('periodo_desde') or None,
            periodo_hasta  = body.get('periodo_hasta') or None,
            notas          = body.get('notas', ''),
            confirmado_por = body.get('confirmado_por', ''),
        )
        return JsonResponse({'ok': True, 'id': p.id, 'mensaje': 'Pago registrado correctamente'})
    except Exception as e:
        logger.exception('Error creando pago')
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def pagos_confirmar(request, pago_id):
    """
    POST /api/pagos/<id>/confirmar/
    Confirma o rechaza un pago. Body: {estado: 'confirmado'|'rechazado', confirmado_por: '...'}
    """
    from .models import Pago
    try:
        p = Pago.objects.get(id=pago_id)
    except Pago.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Pago no encontrado'}, status=404)

    try:
        body   = json.loads(request.body)
        estado = body.get('estado')
        if estado not in ['confirmado', 'rechazado', 'pendiente']:
            return JsonResponse({'ok': False, 'error': 'Estado inválido'}, status=400)
        p.estado         = estado
        p.confirmado_por = body.get('confirmado_por', p.confirmado_por)
        if body.get('notas'):
            p.notas = body['notas']
        p.save()
        return JsonResponse({'ok': True, 'id': p.id, 'estado': p.estado})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


# ════════════════════════════════════════════════════════════════
# MÓDULO PREMIOS
# ════════════════════════════════════════════════════════════════

@require_http_methods(["GET"])
def premios_lista(request):
    """
    GET /api/premios/
    Lista premios pagados y pendientes.
    Filtros: fecha_desde, fecha_hasta, estado, modalidad
    """
    from .models import PremioPagado
    qs = PremioPagado.objects.all()

    fecha_desde = request.GET.get('fecha_desde')
    fecha_hasta = request.GET.get('fecha_hasta')
    estado      = request.GET.get('estado')
    modalidad   = request.GET.get('modalidad')

    if fecha_desde:
        qs = qs.filter(fecha__gte=fecha_desde)
    if fecha_hasta:
        qs = qs.filter(fecha__lte=fecha_hasta)
    if estado:
        qs = qs.filter(estado=estado)
    if modalidad:
        qs = qs.filter(modalidad=modalidad)

    data = []
    total_premios = 0
    total_pendiente = 0
    for pr in qs:
        total_premios += float(pr.monto_premio)
        if pr.estado == 'pendiente':
            total_pendiente += float(pr.monto_premio)
        data.append({
            'id':             pr.id,
            'fecha':          str(pr.fecha),
            'horario':        pr.horario,
            'modalidad':      pr.modalidad,
            'modalidad_nombre': pr.get_modalidad_display(),
            'numero_ganador': pr.numero_ganador,
            'ticket_ref':     pr.ticket_ref,
            'ganador_nombre': pr.ganador_nombre,
            'ganador_id':     pr.ganador_id,
            'taquillero':     pr.taquillero,
            'monto_apuesta':  float(pr.monto_apuesta),
            'multiplicador':  float(pr.multiplicador),
            'monto_premio':   float(pr.monto_premio),
            'estado':         pr.estado,
            'estado_nombre':  pr.get_estado_display(),
            'pagado_por':     pr.pagado_por,
            'fecha_pago':     pr.fecha_pago.isoformat() if pr.fecha_pago else None,
            'notas':          pr.notas,
            'creado':         pr.creado.isoformat(),
        })
    return JsonResponse({
        'ok':              True,
        'total':           len(data),
        'total_premios':   total_premios,
        'total_pendiente': total_pendiente,
        'premios':         data,
    })


@csrf_exempt
@require_http_methods(["POST"])
def premios_crear(request):
    """
    POST /api/premios/crear/
    Registra un nuevo ganador / premio pendiente.
    Body JSON: fecha, horario, modalidad, numero_ganador, ganador_nombre, monto_apuesta, [multiplicador]
    """
    from .models import PremioPagado
    try:
        body = json.loads(request.body)
    except Exception:
        return JsonResponse({'ok': False, 'error': 'JSON inválido'}, status=400)

    required = ['horario', 'modalidad', 'numero_ganador', 'ganador_nombre', 'monto_apuesta']
    for f in required:
        if not body.get(f):
            return JsonResponse({'ok': False, 'error': f'Campo requerido: {f}'}, status=400)

    try:
        monto_apuesta  = float(body['monto_apuesta'])
        multiplicador  = float(body.get('multiplicador', 70))
        monto_premio   = float(body.get('monto_premio', monto_apuesta * multiplicador))

        pr = PremioPagado.objects.create(
            fecha          = body.get('fecha', datetime.now().strftime('%Y-%m-%d')),
            horario        = body['horario'],
            modalidad      = body['modalidad'],
            numero_ganador = body['numero_ganador'],
            ticket_ref     = body.get('ticket_ref', ''),
            ganador_nombre = body['ganador_nombre'],
            ganador_id     = body.get('ganador_id', ''),
            taquillero     = body.get('taquillero', ''),
            monto_apuesta  = monto_apuesta,
            multiplicador  = multiplicador,
            monto_premio   = monto_premio,
            estado         = body.get('estado', 'pendiente'),
            pagado_por     = body.get('pagado_por', ''),
            notas          = body.get('notas', ''),
        )
        return JsonResponse({'ok': True, 'id': pr.id, 'monto_premio': monto_premio, 'mensaje': 'Premio registrado correctamente'})
    except Exception as e:
        logger.exception('Error creando premio')
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def premios_pagar(request, premio_id):
    """
    POST /api/premios/<id>/pagar/
    Marca un premio como pagado.
    Body: {pagado_por: '...', notas: '...'}
    """
    from .models import PremioPagado
    try:
        pr = PremioPagado.objects.get(id=premio_id)
    except PremioPagado.DoesNotExist:
        return JsonResponse({'ok': False, 'error': 'Premio no encontrado'}, status=404)

    try:
        body   = json.loads(request.body)
        estado = body.get('estado', 'pagado')
        if estado not in ['pagado', 'rechazado', 'en_proceso', 'pendiente']:
            return JsonResponse({'ok': False, 'error': 'Estado inválido'}, status=400)
        pr.estado    = estado
        pr.pagado_por = body.get('pagado_por', pr.pagado_por)
        if body.get('notas'):
            pr.notas = body['notas']
        pr.save()
        return JsonResponse({'ok': True, 'id': pr.id, 'estado': pr.estado, 'monto_premio': float(pr.monto_premio)})
    except Exception as e:
        return JsonResponse({'ok': False, 'error': str(e)}, status=500)


@require_http_methods(["GET"])
def resumen_financiero(request):
    """
    GET /api/resumen/
    Resumen financiero del día: ventas vs premios vs pagos recibidos.
    """
    from .models import TransaccionVenta, Pago, PremioPagado
    from django.db.models import Sum

    hoy = datetime.now().strftime('%Y-%m-%d')

    ventas_hoy  = TransaccionVenta.objects.filter(fecha=hoy).aggregate(total=Sum('monto'))['total'] or 0
    pagos_hoy   = Pago.objects.filter(fecha=hoy, estado='confirmado').aggregate(total=Sum('monto'))['total'] or 0
    premios_hoy = PremioPagado.objects.filter(fecha=hoy, estado='pagado').aggregate(total=Sum('monto_premio'))['total'] or 0
    premios_pendientes = PremioPagado.objects.filter(estado='pendiente').aggregate(total=Sum('monto_premio'))['total'] or 0

    saldo_neto = float(ventas_hoy) - float(premios_hoy)

    return JsonResponse({
        'ok':                 True,
        'fecha':              hoy,
        'ventas_hoy':         float(ventas_hoy),
        'pagos_confirmados':  float(pagos_hoy),
        'premios_pagados':    float(premios_hoy),
        'premios_pendientes': float(premios_pendientes),
        'saldo_neto':         saldo_neto,
    })
