"""
api/app.py  –  API de scraping + Firebase Admin para EL ARREJUNTAO

Instalación:
    pip install flask requests beautifulsoup4 flask-cors firebase-admin

Ejecutar:
    python api/app.py
    → http://localhost:5001/api/resultados
    → http://localhost:5001/api/publicar      (POST – publica en Firestore)
    → http://localhost:5001/api/health

Pasos previos:
1. Ve a Firebase Console → Proyecto → ⚙️ Configuración → Cuentas de servicio
2. Haz clic en "Generar nueva clave privada" → guarda el JSON
3. Pon la ruta al JSON en FIREBASE_CREDENTIALS_PATH abajo
"""

import os
import logging
from datetime import datetime

from flask import Flask, jsonify, request
from flask_cors import CORS
import requests as http_requests
from bs4 import BeautifulSoup

# ── Firebase Admin SDK ────────────────────────────────────────
import firebase_admin
from firebase_admin import credentials, firestore

# ▼▼▼ CAMBIA ESTA RUTA al archivo JSON de tu cuenta de servicio ▼▼▼
FIREBASE_CREDENTIALS_PATH = "path/to/serviceAccountKey.json"

_fs_client = None   # cliente Firestore (lazy init)

def get_firebase_client():
    """Inicializa Firebase Admin (solo una vez) y devuelve el cliente Firestore."""
    global _fs_client
    if _fs_client is None:
        if not firebase_admin._apps:
            cred_path = os.environ.get("FIREBASE_CREDENTIALS", FIREBASE_CREDENTIALS_PATH)
            if not os.path.exists(cred_path):
                logging.warning(
                    f"⚠️  Credenciales no encontradas en '{cred_path}'. "
                    "Define la variable de entorno FIREBASE_CREDENTIALS o ajusta "
                    "FIREBASE_CREDENTIALS_PATH en app.py"
                )
                return None
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        _fs_client = firestore.client()
    return _fs_client

# ── Flask ─────────────────────────────────────────────────────
app = Flask(__name__)
CORS(app)
logging.basicConfig(level=logging.INFO)

# ── Config de scraping ────────────────────────────────────────
TARGET_URL  = "https://elarrejuntao.com"
USER_AGENT  = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
TIMEOUT_SEG = 10

# ════════════════════════════════════════════════════════════════
# SCRAPING
# ════════════════════════════════════════════════════════════════
def scrape_resultados() -> dict:
    """Visita la web y extrae los resultados del día."""
    try:
        headers  = {"User-Agent": USER_AGENT}
        response = http_requests.get(TARGET_URL, headers=headers, timeout=TIMEOUT_SEG)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # ────────────────────────────────────────────────────
        # ⚠️  AJUSTA los selectores CSS según la estructura
        #     real de la página (usa F12 en el navegador)
        # ────────────────────────────────────────────────────
        triple_a   = _safe_text(soup, ".resultado-triple-a",  "---")
        triple_b   = _safe_text(soup, ".resultado-triple-b",  "---")
        animalito  = _safe_text(soup, ".resultado-animalito",  "Sin resultado")
        pegadito   = _safe_text(soup, ".resultado-pegadito",   "----")

        return {
            "estado":    "exito",
            "fecha":     datetime.now().strftime("%Y-%m-%d"),
            "hora":      datetime.now().strftime("%H:%M"),
            "triple_a":  triple_a,
            "triple_b":  triple_b,
            "pegadito":  pegadito,
            "animalito": animalito,
            "fuente":    TARGET_URL
        }

    except http_requests.exceptions.Timeout:
        return {"estado": "error", "mensaje": "Tiempo de espera agotado."}
    except http_requests.exceptions.ConnectionError:
        return {"estado": "error", "mensaje": "No se pudo conectar con la web."}
    except Exception as e:
        logging.exception("Error inesperado en scraper")
        return {"estado": "error", "mensaje": str(e)}


def _safe_text(soup: BeautifulSoup, selector: str, default: str) -> str:
    el = soup.select_one(selector)
    return el.get_text(strip=True) if el else default


# ════════════════════════════════════════════════════════════════
# HELPERS FIRESTORE
# ════════════════════════════════════════════════════════════════
def publicar_en_firestore(datos: dict) -> dict:
    """
    Escribe los resultados del scraping en la colección
    `resultados_sorteos` de Firestore (con permisos de administrador).
    """
    db = get_firebase_client()
    if db is None:
        return {"guardado": False, "razon": "Firebase no configurado"}

    hoy    = datos.get("fecha", datetime.now().strftime("%Y-%m-%d"))
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
            logging.exception(f"Error guardando '{tipo}' en Firestore")
            errores.append(str(e))

    if datos.get("triple_a") and datos["triple_a"] != "---":
        _set("arrimao", {"numero": datos["triple_a"]})
    if datos.get("pegadito") and datos["pegadito"] != "----":
        _set("pegadito", {"numero": datos["pegadito"]})
    if datos.get("animalito") and datos["animalito"] != "Sin resultado":
        _set("animalito", {"animalito": {"nombre": datos["animalito"], "icono": "🐾", "numero": "-"}})

    return {
        "guardado": len(errores) == 0,
        "errores":  errores
    }


# ════════════════════════════════════════════════════════════════
# ENDPOINTS
# ════════════════════════════════════════════════════════════════
@app.route("/api/resultados", methods=["GET"])
def get_resultados():
    """GET /api/resultados → JSON con los resultados del día."""
    datos  = scrape_resultados()
    status = 200 if datos["estado"] == "exito" else 503
    return jsonify(datos), status


@app.route("/api/publicar", methods=["POST"])
def publicar():
    """
    POST /api/publicar
    Hace scraping y publica el resultado directamente en Firestore.
    Devuelve el resultado del scraping + confirmación de escritura.
    """
    datos    = scrape_resultados()
    guardado = publicar_en_firestore(datos) if datos["estado"] == "exito" else {"guardado": False}
    return jsonify({**datos, "firestore": guardado})


@app.route("/api/health", methods=["GET"])
def health():
    """GET /api/health → estado de la API y de Firebase."""
    db_ok = get_firebase_client() is not None
    return jsonify({
        "estado":   "ok",
        "firebase": "conectado" if db_ok else "no configurado",
        "hora":     datetime.now().isoformat()
    })


# ════════════════════════════════════════════════════════════════
# COLOCACIÓN DE PREMIOS
# ════════════════════════════════════════════════════════════════

def _numero_coincide(ticket_num: str, ganador: str, tipo: str) -> bool:
    """
    Verifica si el número de un item de ticket coincide con el número ganador.
    - TRIPLES: últimas 3 cifras
    - TERMINAL: últimas 2 cifras
    - 4 CIFRAS: número completo (4 dígitos)
    - PEGADITO / ARRIMAO: exacto
    """
    n = str(ticket_num).strip().split()[0]   # tomar solo dígitos, sin labels
    g = str(ganador).strip()
    t = str(tipo).upper()

    if "TERMINAL" in t:
        return n[-2:] == g[-2:] if len(n) >= 2 and len(g) >= 2 else False
    elif "4 CIFRA" in t or "4CIFRA" in t:
        return n == g
    else:
        # TRIPLES (default): últimas 3 cifras
        return n[-3:] == g[-3:] if len(n) >= 3 and len(g) >= 3 else n == g


@app.route("/api/premios/colocar", methods=["POST"])
def colocar_premio():
    """
    POST /api/premios/colocar
    Body JSON:
    {
      "fecha":         "2026-03-26",
      "sorteo":        "Táchira",
      "tipo":          "TRIPLES",
      "lista":         "LISTA A",
      "numero_ganador": "845",
      "signo":         "ESCORPIO",        // opcional
      "tickets": [ ...allTransactions... ] // array del localStorage
    }
    Retorna los tickets ganadores.
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"estado": "error", "mensaje": "JSON inválido"}), 400

    sorteo_sel  = str(data.get("sorteo",  "")).strip().lower()
    lista_sel   = str(data.get("lista",   "")).strip().upper()
    tipo_sel    = str(data.get("tipo",    "TRIPLES")).strip().upper()
    ganador     = str(data.get("numero_ganador", "")).strip()
    signo_sel   = str(data.get("signo",   "")).strip().upper()
    tickets     = data.get("tickets", [])
    fecha       = data.get("fecha", datetime.now().strftime("%Y-%m-%d"))

    if not ganador:
        return jsonify({"estado": "error", "mensaje": "numero_ganador es requerido"}), 400

    resultados = []
    num_sorteo  = 1000  # contador base para No. Sorteo

    for tx in tickets:
        tx_id    = tx.get("id", "")
        tx_items = tx.get("items", [])
        tx_status = tx.get("status", "Pendiente")

        for item in tx_items:
            lottery_raw = str(item.get("lottery", "")).lower()
            number_raw  = str(item.get("number", ""))

            # Filtrar por sorteo (nombre parcial)
            if sorteo_sel and sorteo_sel not in lottery_raw:
                continue

            # Filtrar por lista (A, B, C en el nombre de la lotería)
            if lista_sel:
                lista_letra = lista_sel.replace("LISTA ", "").strip()  # "A", "B", "C"
                if f"[{lista_letra}]" not in lottery_raw.upper() and \
                   f"lista {lista_letra.lower()}" not in lottery_raw:
                    continue

            # Verificar si el número coincide
            if _numero_coincide(number_raw, ganador, tipo_sel):
                estatus = "PROCESADO" if tx_status in ("Ganador", "Pagado") else "VALIDADO"
                ganador_entry = ganador
                if signo_sel:
                    ganador_entry += f" {signo_sel}"
                resultados.append({
                    "no":         len(resultados) + 1,
                    "no_sorteo":  num_sorteo + len(resultados),
                    "ticket_id":  tx_id,
                    "sorteo":     item.get("lottery", ""),
                    "lista":      lista_sel or "LISTA A",
                    "tipo_lista": tipo_sel,
                    "validacion": "VALIDADO",
                    "no_ganador": ganador_entry,
                    "estatus":    estatus,
                    "monto":      item.get("amount", 0),
                    "premio":     (item.get("amount", 0)) * 75
                })

    return jsonify({
        "estado":     "exito",
        "fecha":      fecha,
        "sorteo":     data.get("sorteo", ""),
        "lista":      lista_sel,
        "tipo":       tipo_sel,
        "ganador":    ganador,
        "signo":      signo_sel,
        "total":      len(resultados),
        "ganadores":  resultados,
        "hora":       datetime.now().strftime("%H:%M:%S")
    })


@app.route("/api/premios/guardar", methods=["POST"])
def guardar_premio():
    """
    POST /api/premios/guardar
    Guarda el resultado del sorteo ganador en Firestore.
    """
    try:
        data = request.get_json(force=True)
    except Exception:
        return jsonify({"estado": "error", "mensaje": "JSON inválido"}), 400

    db = get_firebase_client()
    if db is None:
        return jsonify({
            "estado":  "ok_local",
            "mensaje": "Firebase no configurado — resultado no guardado en la nube.",
            "data":    data
        })

    fecha   = data.get("fecha", datetime.now().strftime("%Y-%m-%d"))
    sorteo  = data.get("sorteo", "desconocido").lower().replace(" ", "_")
    doc_id  = f"{fecha}_{sorteo}_{data.get('lista','A').lower()}"

    try:
        db.collection("premios_sorteos").document(doc_id).set({
            "fecha":          fecha,
            "sorteo":         data.get("sorteo"),
            "tipo":           data.get("tipo"),
            "lista":          data.get("lista"),
            "numero_ganador": data.get("numero_ganador"),
            "signo":          data.get("signo", ""),
            "total_ganadores":data.get("total_ganadores", 0),
            "registrado_en":  firestore.SERVER_TIMESTAMP
        })
        return jsonify({"estado": "exito", "doc_id": doc_id})
    except Exception as e:
        logging.exception("Error guardando premio en Firestore")
        return jsonify({"estado": "error", "mensaje": str(e)}), 500


# ════════════════════════════════════════════════════════════════
# INICIO
# ════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    print("=" * 60)
    print("  API EL ARREJUNTAO  –  Scraping + Firebase Admin")
    print("  → GET  http://localhost:5001/api/resultados")
    print("  → POST http://localhost:5001/api/publicar")
    print("  → GET  http://localhost:5001/api/health")
    print("  → POST http://localhost:5001/api/premios/colocar")
    print("  → POST http://localhost:5001/api/premios/guardar")
    print("=" * 60)
    app.run(debug=True, port=5001)

