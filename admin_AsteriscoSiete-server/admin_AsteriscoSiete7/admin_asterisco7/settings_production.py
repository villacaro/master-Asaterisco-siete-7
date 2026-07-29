# -*- coding: utf-8 -*-
"""
settings_production.py — Configuración de PRODUCCIÓN
=====================================================
Usa:
  - Base de datos: Supabase PostgreSQL (via DATABASE_URL)
  - Servidor: Railway (Gunicorn + Whitenoise para static)
  - Sin Redis/RabbitMQ/Celery en esta fase inicial

Variables de entorno requeridas en Railway:
  DATABASE_URL          — URL completa de conexión Supabase Postgres
  SECRET_KEY            — Clave secreta única para producción
  DJANGO_SETTINGS_MODULE=admin_asterisco7.settings_production
  RAILWAY_PUBLIC_DOMAIN — Seteada automáticamente por Railway
  ALLOWED_HOST_EXTRA    — (opcional) dominio adicional
"""
import os
import dj_database_url
from .settings import *

# ── Seguridad ──────────────────────────────────────────────────────────────────
DEBUG = False
TEMPLATE_DEBUG = False
DEBUG_TOOLBAR = False
ADD_MENU = False
ACTIVATE_HISTORY = True
MENU_VALID = False

SECRET_KEY = os.environ.get('SECRET_KEY', 'CAMBIA-ESTO-EN-PRODUCCION')

ALLOWED_HOSTS = [
    '*',
    '127.0.0.1',
    'localhost',
    '.railway.app',     # cubre *.railway.app automáticamente
    '.up.railway.app',
    '.back4app.run',
    '.b4a.run',
    '.back4app.com',
]
# Agrega dominio custom si lo tienes
_extra = os.environ.get('ALLOWED_HOST_EXTRA', '')
if _extra:
    ALLOWED_HOSTS.append(_extra)

# ── Rutas base ─────────────────────────────────────────────────────────────────
PROJECT_PATH = os.path.dirname(os.path.realpath(__file__))
BASE_DIR     = os.path.dirname(os.path.dirname(__file__))

# ── Base de datos: Supabase PostgreSQL ────────────────────────────────────────
DATABASE_URL = os.environ.get('SUPABASE_POOLER_URL') or os.environ.get('DATABASE_URL', '')
DATABASES = {
    'default': {
        **dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            ssl_require=True,
        ),
        'DISABLE_SERVER_SIDE_CURSORS': True,
    }
} if DATABASE_URL else {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db_local_asterisco7.sqlite3'),
    }
}

# ── Apps instaladas ────────────────────────────────────────────────────────────
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.humanize',
    'django_extensions',
    'rest_framework',
    # Apps del proyecto Asterisco Siete (*7)
    'admin_lib',
    'admin_historic',
    'admin_juego',
    'admin_apuestas',
    'admin_comercializacion',
    'admin_datamart',
    'admin_finanzas',
    'admin_logros',
    'admin_mail',
    'admin_permisologia',
    'admin_principal',
    'admin_profiles',
    'admin_reportes',
    'admin_resultados',
    'admin_soporte',
    'admin_status',
    'admin_themes',
    'admin_users',
    'api',
    # App principal del dashboard
    'admin_asterisco7',
)

# ── Middleware ────────────────────────────────────────────────────────────────
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',   # <- archivos estáticos en prod
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'admin_principal.middleware.AuthenticationAndPermissionsMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'crequest.middleware.CrequestMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ── URLs y WSGI ───────────────────────────────────────────────────────────────
ROOT_URLCONF     = 'admin_asterisco7.urls'
WSGI_APPLICATION = 'admin_asterisco7.wsgi.application'

# ── Templates ─────────────────────────────────────────────────────────────────
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'static'),
            os.path.join(PROJECT_PATH, 'templates'),
        ],
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

# ── Cache (sin Redis en fase inicial) ────────────────────────────────────────
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}

SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# ── Archivos estáticos — Whitenoise ──────────────────────────────────────────
STATIC_URL  = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(PROJECT_PATH, 'static'),)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ── Media ───────────────────────────────────────────────────────────────────
MEDIA_URL  = '/media/'
MEDIA_ROOT = os.path.join(PROJECT_PATH, 'media')

# ── REST Framework ────────────────────────────────────────────────────────────
REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
}

# ── Configuraciones del proyecto ─────────────────────────────────────────────
ADMIN_URL   = '/admin/'
ACCESO_URL  = '/login/'
LOGOUT_URL  = '/logout/'
INDEX_URL   = '/'

TIME_ZONE     = 'America/Caracas'
LANGUAGE_CODE = 'es'
SITE_ID       = 1
USE_I18N      = True
USE_L10N      = True
USE_TZ        = False

# Supabase no soporta tablespaces personalizados — sobreescribimos el valor de settings.py
DEFAULT_TABLESPACE       = ''
DEFAULT_INDEX_TABLESPACE = ''

X_FRAME_OPTIONS        = 'SAMEORIGIN'
USE_THOUSAND_SEPARATOR = False
DECIMAL_SEPARATOR      = ','

FORMAT_STR_DATE         = '%d-%m-%Y'
FORMAT_STR_DATE_2       = '%d/%m/%Y'
FORMAT_STR_DATE_REPORTS = '%Y-%m-%d'
FORMAT_STR_TIME         = '%I:%M %p'
FORMAT_STR_DATETIME     = '%d%m%y%H%M'
THEME_DEFAULT           = 'theme_default'

MESSAGES_GLOBAL = {
    'consulta_por_juegos': 'El siguiente reporte puede tener un margen de error del 0.3%'
}

# ── Seguridad HTTPS (Railway usa HTTPS automáticamente) ──────────────────────
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT     = False
SESSION_COOKIE_SECURE   = True
CSRF_COOKIE_SECURE      = True

# ── CSRF dominios confiados ───────────────────────────────────────────────────
CSRF_TRUSTED_ORIGINS = [
    'https://*.railway.app',
    'https://*.up.railway.app',
    'https://master-asaterisco-siete-7-production.up.railway.app',
    'https://*.back4app.run',
    'https://*.b4a.run',
    'https://*.back4app.com',
]

# ── Logging en producción ─────────────────────────────────────────────────────
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {'class': 'logging.StreamHandler'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
    },
}

# ── Sesiones Persistentes ────────────────────────────────────────────────
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 31536000  # 1 año
