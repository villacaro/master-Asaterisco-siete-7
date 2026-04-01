"""
usuarios/firebase_service.py
Servicio para interactuar con Firebase Auth y Firestore usando el Admin SDK.
"""
import os
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

# ── Inicialización (lazy, una sola vez) ───────────────────────
_firebase_ready = False

def _init_firebase():
    global _firebase_ready
    if _firebase_ready:
        return True
    try:
        import firebase_admin
        from firebase_admin import credentials
        if not firebase_admin._apps:
            cred_path = settings.FIREBASE_CREDENTIALS
            if not os.path.exists(cred_path):
                logger.error(f"⚠️ No se encontró serviceAccountKey.json en: {cred_path}")
                return False
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        _firebase_ready = True
        return True
    except Exception as e:
        logger.exception("Error al inicializar Firebase Admin")
        return False


# ════════════════════════════════════════════════
# FIREBASE AUTH – Usuarios
# ════════════════════════════════════════════════

def listar_usuarios(max_resultados=100):
    """Devuelve lista de usuarios de Firebase Auth."""
    if not _init_firebase(): return []
    from firebase_admin import auth
    try:
        page  = auth.list_users()
        users = []
        count = 0
        while page and count < max_resultados:
            for u in page.users:
                users.append({
                    'uid':          u.uid,
                    'email':        u.email or '—',
                    'nombre':       u.display_name or '—',
                    'foto':         u.photo_url,
                    'verificado':   u.email_verified,
                    'deshabilitado':u.disabled,
                    'creado':       u.user_metadata.creation_timestamp,
                    'ultimo_login': u.user_metadata.last_sign_in_timestamp,
                    'proveedor':    [p.provider_id for p in u.provider_data],
                })
                count += 1
            page = page.get_next_page()
        return users
    except Exception as e:
        logger.exception("Error listando usuarios")
        return []


def crear_usuario(email, password, nombre=''):
    """Crea un nuevo usuario en Firebase Auth."""
    if not _init_firebase(): return None, "Firebase no disponible"
    from firebase_admin import auth
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=nombre or None,
            email_verified=False
        )
        return user, None
    except Exception as e:
        return None, str(e)


def deshabilitar_usuario(uid, deshabilitar=True):
    """Habilita o deshabilita un usuario."""
    if not _init_firebase(): return False, "Firebase no disponible"
    from firebase_admin import auth
    try:
        auth.update_user(uid, disabled=deshabilitar)
        return True, None
    except Exception as e:
        return False, str(e)


def eliminar_usuario(uid):
    """Elimina permanentemente un usuario de Firebase Auth."""
    if not _init_firebase(): return False, "Firebase no disponible"
    from firebase_admin import auth
    try:
        auth.delete_user(uid)
        return True, None
    except Exception as e:
        return False, str(e)


def cambiar_password(uid, nueva_password):
    """Cambia la contraseña de un usuario."""
    if not _init_firebase(): return False, "Firebase no disponible"
    from firebase_admin import auth
    try:
        auth.update_user(uid, password=nueva_password)
        return True, None
    except Exception as e:
        return False, str(e)


# ════════════════════════════════════════════════
# FIRESTORE – Datos del usuario
# ════════════════════════════════════════════════

def obtener_clientes_usuario(uid):
    """Devuelve la lista de clientes del usuario desde Firestore."""
    if not _init_firebase(): return []
    from firebase_admin import firestore
    try:
        db   = firestore.client()
        docs = db.collection('usuarios').document(uid).collection('clientes').stream()
        return [{'id': d.id, **d.to_dict()} for d in docs]
    except Exception as e:
        logger.exception(f"Error obteniendo clientes de {uid}")
        return []


def obtener_apuestas_usuario(uid, limite=20):
    """Devuelve las últimas apuestas del usuario desde Firestore."""
    if not _init_firebase(): return []
    from firebase_admin import firestore
    try:
        db   = firestore.client()
        docs = (db.collection('usuarios').document(uid)
                  .collection('apuestas')
                  .order_by('fecha', direction=firestore.Query.DESCENDING)
                  .limit(limite).stream())
        return [{'id': d.id, **d.to_dict()} for d in docs]
    except Exception as e:
        logger.exception(f"Error obteniendo apuestas de {uid}")
        return []
