"""
admin_panel/settings.py  –  Configuración Django para EL ARREJUNTAO Admin Panel
Soporta desarrollo local (DEBUG=True) y producción en Railway (DEBUG=False).
"""
import os
import json
import base64
import tempfile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# ── Seguridad ─────────────────────────────────────────────────
SECRET_KEY = os.environ.get('SECRET_KEY', 'arrejuntao-django-admin-secret-dev-key-cambia-en-produccion')
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS', '')
ALLOWED_HOSTS = ['localhost', '127.0.0.1']
if ALLOWED_HOSTS_ENV:
    ALLOWED_HOSTS += [h.strip() for h in ALLOWED_HOSTS_ENV.split(',')]
# Railway añade automáticamente el dominio *.railway.app
ALLOWED_HOSTS += ['.railway.app', '.up.railway.app']

# ── Apps ──────────────────────────────────────────────────────
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'usuarios',
    'api_rest',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',       # ← estáticos en producción
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── CORS ──────────────────────────────────────────────────────
CORS_ALLOW_ALL_ORIGINS = True

# ── REST Framework ────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.AllowAny'],
    'DEFAULT_RENDERER_CLASSES':   ['rest_framework.renderers.JSONRenderer'],
}

ROOT_URLCONF = 'admin_panel.urls'
WSGI_APPLICATION = 'admin_panel.wsgi.application'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# ── Base de datos ─────────────────────────────────────────────
# En Railway usa la variable DATABASE_URL (PostgreSQL).
# Localmente usa SQLite.
DATABASE_URL = os.environ.get('DATABASE_URL', '')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {'default': dj_database_url.config(default=DATABASE_URL, conn_max_age=600)}
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ── Firebase Credentials ──────────────────────────────────────
# OPCIÓN 1: ruta a un archivo local (desarrollo)
# OPCIÓN 2: JSON en base64 como variable de entorno FIREBASE_CREDENTIALS_B64 (Railway)
_creds_b64 = os.environ.get('FIREBASE_CREDENTIALS_B64', '')
if _creds_b64:
    # Decodificar y escribir a un archivo temporal
    _creds_data = base64.b64decode(_creds_b64).decode('utf-8')
    _tmp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
    _tmp.write(_creds_data)
    _tmp.close()
    FIREBASE_CREDENTIALS = _tmp.name
else:
    FIREBASE_CREDENTIALS = os.environ.get(
        'FIREBASE_CREDENTIALS',
        str(BASE_DIR.parent / 'api' / 'serviceAccountKey.json')
    )
FIREBASE_PROJECT_ID = 'app-el-arrejuntao'

# ── Estáticos ─────────────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
LANGUAGE_CODE = 'es-ve'
TIME_ZONE     = 'America/Caracas'
USE_I18N = True
USE_TZ   = True
