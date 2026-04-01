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
